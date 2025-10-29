from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contact/<int:contact_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('contact/<int:contact_id>/edit/', views.edit_contact, name='edit_contact'),
    path('contact/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)