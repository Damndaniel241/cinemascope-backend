from django.contrib import admin



# Register your models here.
from .models import Review,Movie,Rating,Watch,Like,WatchList
from reviews.review_comment import ReviewComment
from reviews.review_like import ReviewLike

class CustomReviewAdmin(admin.ModelAdmin):
    list_display = ("id","__str__")
    
class CustomMovieAdmin(admin.ModelAdmin):
    list_display = ("__str__","id")
   

admin.site.register(Review,CustomReviewAdmin)
admin.site.register(Movie, CustomReviewAdmin)
admin.site.register(Rating)
admin.site.register(Watch)
admin.site.register(Like)
admin.site.register(WatchList)
admin.site.register(ReviewComment)
admin.site.register(ReviewLike)