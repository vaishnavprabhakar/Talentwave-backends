from django.contrib import admin
from .models import User, Profile


class CustomBaseUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_admin", "is_active", "account_type")
    list_display_links = (
        "username",
        "email",
    )
    search_fields = (
        "username",
        "email",
        "account_type",
    )
    ordering = ("id",)
    exclude = ("first_name", "last_name")
    readonly_fields = ("password",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_active", "account_type")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password",
                    "is_admin",
                    "is_active",
                    "account_type",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        # If the user is an admin, exclude the 'account_type' field from the fieldset
        if obj and obj.is_admin:
            return super().get_fieldsets(request, obj)[:-1] + (
                ("Permissions", {"fields": ("is_admin", "is_active")}),
            )
        return super().get_fieldsets(request, obj)


admin.site.register(User, CustomBaseUserAdmin)

admin.site.register(Profile)
