from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from users.models import User, Address, Phone


class UserAddressInline(admin.TabularInline):
    model = Address


class UserPhoneInline(admin.TabularInline):
    model = Phone


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'password']
    list_filter = ['is_superuser']
    inlines = [UserAddressInline, UserPhoneInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_superuser', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city']


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'number']
