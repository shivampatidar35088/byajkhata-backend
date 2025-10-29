from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='contacts/', blank=True, null=True)
    
    @property
    def balance(self):
        credits = self.transactions.filter(type='credit').aggregate(models.Sum('amount'))['amount__sum'] or 0
        debits = self.transactions.filter(type='debit').aggregate(models.Sum('amount'))['amount__sum'] or 0
        return credits - debits

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('credit', 'credit'),
        ('debit', 'debit'),
    )
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    # Interest fields
    interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    interest_enabled = models.BooleanField(default=False)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    compound_months = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto calculate compound interest if enabled
        if self.interest_enabled and self.interest_rate and self.compound_months:
            P = float(self.amount)
            r = float(self.interest_rate)
            t = float(self.compound_months)
            self.interest = round(P * ((1 + (r/100))**t - 1), 2)
        else:
            self.interest = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contact.name} - {self.type} - {self.amount}"
