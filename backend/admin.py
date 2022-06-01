from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from backend.models import User, Post


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'email', 'is_staff', 'is_active', 'username')
    list_filter = ('id', 'email', 'is_staff', 'is_active', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Post.likes.through)
