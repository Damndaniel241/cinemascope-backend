from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User,UserProfile,Follow
from users.tokens import RefreshTokenStore,PasswordResetToken

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id","email", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email","user_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_verified","is_blacklisted","groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    

@admin.register(RefreshTokenStore)
class RefreshTokenStoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at','expires_at', 'revoked')
    readonly_fields = ('created_at',)

admin.site.register(PasswordResetToken)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Follow)



