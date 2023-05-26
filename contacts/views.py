from .models import Contact, SpamContact
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import ContactsSerializer, ContactsDetailsSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ContactsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["potential_name","phone","linked_contacts__contact_name"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context
    

class ContactDetails(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactsDetailsSerializer

    def get(self,request,contact_id):
        contact = Contact.objects.filter(id=contact_id).first()
        context = dict()
        context.update({"user": request.user})
        contact_data = self.serializer_class(contact,context=context).data
        return Response(contact_data)
    


class SpamContactAPIView(APIView):
    """
    View for marking contact as spam.
    """
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data=request.data
        contact = Contact.objects.filter(phone=data.get("phone")).first()
        # TODO: don't create duplicate entries in spam table for same contact & user
        if contact:
            SpamContact.objects.create(user=request.user,contact=contact)
            contact.marked_as_spam = True
            contact.spam_count+=1
            contact.save()
        else:
            contact = Contact.objects.create(phone=data.get("phone"),potential_name="Spam Contact",spam_count=1,marked_as_spam=True)
            SpamContact.objects.create(user=request.user,contact=contact)
        return Response("Number marked as spam",status=status.HTTP_201_CREATED)