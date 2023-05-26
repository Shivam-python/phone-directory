from django.urls import path
from .views import ContactsAPI, ContactDetails, SpamContactAPIView
urlpatterns = [
    path('', ContactsAPI.as_view()),
    path('spam/', SpamContactAPIView.as_view()),
    path('details/<int:contact_id>', ContactDetails.as_view())
 ]