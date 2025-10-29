from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Transaction
from .forms import ContactForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q



@login_required
def dashboard(request):
    query = request.GET.get('q', '')  # search query from input
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query),
            owner=request.user
        )
    else:
        contacts = Contact.objects.filter(owner=request.user)

    total_get = sum([c.balance for c in contacts if c.balance > 0])
    total_give = abs(sum([c.balance for c in contacts if c.balance < 0]))

    return render(request, 'core/dashboard.html', {
        'contacts': contacts,
        'total_get': total_get,
        'total_give': total_give,
        'query': query
    })




@login_required
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)  # request.FILES zaruri hai
        if form.is_valid():
            contact = form.save(commit=False)  # don't save yet
            contact.owner = request.user       # set the owner
            contact.save()                     # now save
            return redirect('dashboard')       # or any success page
    else:
        form = ContactForm()
    return render(request, 'core/add_contact.html', {'form': form})




@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    transactions = contact.transactions.all().order_by('-date')
    return render(request, 'core/contact_detail.html', {'contact': contact, 'transactions': transactions})



@login_required
def add_transaction(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.contact = contact
            transaction.save()
            return redirect('contact_detail', contact_id=contact.id)
    else:
        form = TransactionForm(initial={'date': timezone.now()})

    return render(request, 'core/add_transaction.html', {
        'form': form,
        'contact': contact
    })


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_detail', contact_id=contact.id)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'core/edit_contact.html', {'form': form, 'contact': contact})


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        contact.delete()
        return redirect('dashboard')
    return render(request, 'core/delete_contact.html', {'contact': contact})






from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
