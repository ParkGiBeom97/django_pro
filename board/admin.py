from django.contrib import admin
from .models import Board, Reply
from .models import User

# Register your models here.
admin.site.register(User)
admin.site.register(Board)
admin.site.register(Reply)
