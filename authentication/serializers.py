from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.contrib.auth.hashers import make_password
from contacts.models import Contact


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration 
    """
    password = serializers.CharField(write_only=True)

    def validate_password(self, password):
        password = make_password(password)
        return password
    
    def create(self, validated_data):
        user =  super().create(validated_data)
        # updating potential name in global contacts database
        if Contact.objects.filter(phone=user.phone).exists():
            global_contact = Contact.objects.filter(phone=user.phone).first()
            global_contact.potential_name = user.name
            global_contact.is_user_registered = True
            global_contact.save()
        else:
            # if contact not present in global Db, add new entry.
            Contact.objects.create(potential_name=user.name,
                                   phone=user.phone,
                                   email=user.email,
                                   is_user_registered=True
                                   )
        return user

    class Meta:
        model = User
        fields = ['phone', 'name', 'email', 'password']


class UserLoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login & generating jwt token 
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = user.phone

        return token