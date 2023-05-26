from django.contrib import admin
from .models import Contact, UserContact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ['potential_name', 'phone','is_user_registered','marked_as_spam','email']
    search_fields = ["potential_name","phone","email"]
    

class UserContactAdmin(admin.ModelAdmin):
    list_display = ["id","user","contact_name","contact"]
    autocomplete_fields = ["contact"]

admin.site.register(Contact, ContactAdmin)
admin.site.register(UserContact, UserContactAdmin)