from django.contrib import admin
from .models import Rating,Review,Movie,Comment,Like
# Register your models here.

admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Like)