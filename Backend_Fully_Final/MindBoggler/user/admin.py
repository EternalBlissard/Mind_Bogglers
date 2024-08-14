from django.contrib import admin
from user.models import UserManager,Book
from user.models import Rating
# Register your models here.
admin.site.register(UserManager)
admin.site.register(Book)
admin.site.register(Rating)