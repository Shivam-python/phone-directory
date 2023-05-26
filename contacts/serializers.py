from rest_framework import serializers
from .models import Contact
from authentication.models import User


class ContactsSerializer(serializers.ModelSerializer):
    """
    Contact data serializer which returns only the required fields.
    """
    class Meta:
        model = Contact
        fields = ["id","phone","potential_name"]

    def to_representation(self, instance):
        context = self.context
        response = super().to_representation(instance)
        user = context.get("user")
        # if it's in user's contact, updating name and displaying name stored in user's contact book
        if instance.linked_contacts.filter(user=user).exists():
            response["potential_name"] = instance.linked_contacts.filter(user=user).first().contact_name
        return response
    

class ContactsDetailsSerializer(serializers.ModelSerializer):
    """
    Contact details serializer which returns complete info about the contact.
    """
    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        """
        Overriding representation to check certain conditions and add/remove relevant/irrelevant data.
        """
        context = self.context
        response = super().to_representation(instance)
        user = context.get("user")
        if instance.linked_contacts.filter(user=user).exists():
            response["potential_name"] = instance.linked_contacts.filter(user=user).first().contact_name
        if instance.is_user_registered:
            searched_contact_user = User.objects.filter(phone=instance.phone).first()
            if not searched_contact_user.contacts.filter(contact__phone=user.phone).exists():
                response.pop("email")
        else:
            response.pop("email")
        
        return response