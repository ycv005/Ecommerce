from django.contrib import admin
# Register your models here.
from .models import GuestModel, User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff', 'active')
    # fieldsets are basically how you want to see the admin, when you open or viewing it.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    # fieldsets (for fields to be used in editing users) and to add_fieldsets (for fields to be used when creating a user

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email', 'password1', 'password2','admin','staff')}
        ),
    )
    search_fields = ('email','name')
    ordering = ('email',)
    filter_horizontal = ()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

admin.site.register(GuestModel)
admin.site.register(User, UserAdmin)