from django.contrib import admin
from .models import Todo, User

admin.site.register(User)
admin.site.register(Todo)
