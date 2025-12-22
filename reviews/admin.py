from django.contrib import admin



# Register your models here.
from .models import Review,Movie,Rating


class CustomReviewAdmin(admin.ModelAdmin):
    list_display = ("id","__str__")
    
class CustomMovieAdmin(admin.ModelAdmin):
    list_display = ("__str__","id")
   

admin.site.register(Review,CustomReviewAdmin)
admin.site.register(Movie, CustomReviewAdmin)
admin.site.register(Rating)