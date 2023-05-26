from django.db import models
from authentication.models import User

# Create your models here.
class Contact(models.Model):
    """
    Global contacts table.
    """
    phone = models.CharField(max_length=10)
    potential_name= models.CharField(max_length=255,null=True,blank=True) # globaal user name.
    email = models.EmailField(max_length=255,null=True,blank=True)
    marked_as_spam = models.BooleanField(default=False)
    spam_count = models.IntegerField(default=0)
    is_user_registered = models.BooleanField(default=False)
    country_code = models.CharField(max_length=4,default="+91")

    def __str__(self) -> str:
        return f"{self.potential_name} - {self.phone}"


class UserContact(models.Model):
    """
    Linking contact & user. Also storing contact name in user's phone
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="contacts")
    contact_name = models.CharField(max_length=255) # the name user has saved in his phone.
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE,related_name="linked_contacts")


class SpamContact(models.Model):
    """
    Table to store spam contact data(Who has marked which contact as spam.)
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        contact = self.contact
        contact.marked_as_spam=True
        contact.spam_count+=1
        contact.save()