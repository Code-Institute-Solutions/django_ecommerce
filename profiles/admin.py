from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    """Inline for editing profile within User model in admin"""

    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    """Add the inline profile to the default UserAdmin"""

    inlines = (UserProfileInline,)


class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile editing outside base UserAdmin"""

    list_display = (
        'user',
        'first_name',
        'last_name',
        'default_phone_number',
        'default_country',
        'default_postcode',
        'default_town_or_city',
        'default_street_address1',
        'default_street_address2',
        'default_county',
    )

    def first_name(self, instance):
        """Get the user's first name from the User model"""

        return instance.user.first_name


    def last_name(self, instance):
        """Get the user's last name from the User model"""
        
        return instance.user.last_name


# Unregister the default UserAdmin and register our custom ones
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
