from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Sport, Turf, Booking

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom App Fields', {'fields': ('member_id', 'identity_card_number', 'strike_count', 'is_banned')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom App Fields', {
            'fields': ('identity_card_number', 'strike_count', 'is_banned'),
        }),
    )

    list_display = ['username', 'email', 'member_id', 'strike_count', 'is_banned', 'is_staff']

    list_editable = ['strike_count', 'is_banned']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Sport)
admin.site.register(Turf)
admin.site.register(Booking)
