from rest_framework import serializers
from .models import Review,Movie,Rating,Watch,Like,WatchList
from users.serializers import UserProfileSerializer, UserSerializer
from users.models import User
from .review_comment import ReviewComment
from .review_like import ReviewLike

        
    # def get_ra    
    
class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","user_name"]
        



    
    # def get_rating(self,obj):
    #     user_instance = obj.movie_ratings.all()
    #     serializer = RatingSerializer(context=self.context,instance=user_instance)
    #     return serializer.data
    
    
class RatingSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(
    slug_field='movie_id',
    queryset=Movie.objects.all(),
    required=True
)   
    # user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ["id","movie","stars"]
        
        
class WatchSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(
    slug_field='movie_id',
    queryset=Movie.objects.all(),
    required=True
)
    # user = UserSerializer(read_only=True)
    
    class Meta:
        model = Watch
        fields = ["id","movie","date_watched"]
        

        
class WatchListSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(
    slug_field='movie_id',
    queryset=Movie.objects.all(),
    required=True
)
    # user = UserSerializer(read_only=True)
    # added = serializers.BooleanField(required=True)
    class Meta:
        model = WatchList
        fields = ["id","movie"]
    
    
    
class LikeSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(
    slug_field='movie_id',
    queryset=Movie.objects.all(),
    required=True
)   
    # user = UserSerializer(read_only=True)


    class Meta:
        model = Like
        fields = ["id","movie"]
        
    
# class PlatformMovieDataSerializer(serializers.Serializer):
#     reviews = ReviewSerializer()
#     # watches = WatchSerializer()
    
    
    
#     class Meta:
#         fields = ["reviews"]
#     # "reviews":review_obj_serializer.data,
#                                 # "rating":rating_obj_serializer.data,
#                                 # "watched":watch_obj_serializer.data,
#                                 # "added_to_watchlist":watch_list_obj_serializer.data
                                
                                
                                
class ReviewLikeSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field="id",queryset=Review.objects.all(),required=True)
    user = UserSerializer(read_only=True)
    # review_liked = serializers.SerializerMethodField()
    
    # def get_review_liked(self,obj):
    #     review_like = ReviewLike.objects.filter(user=obj.user, review=obj.review).first()
    #     return ReviewLikeSerializer(review_like).data if review_like else None 
    class Meta:
        model = ReviewLike
        fields = ["id","user","review"] 
                                    
class ReviewCommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field="id",queryset=Review.objects.all(),required=True)
    user = UserSerializer(read_only=True)
    
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request.user.pk != instance.user.pk:
            raise serializers.ValidationError("You do not have permission to edit this profile.")
        instance.save()
        return instance
        
    
    class Meta:
        model = ReviewComment
        fields = ["id","user","review","created_at","content"] 
    


class ReviewSerializer(serializers.ModelSerializer):
    
    movie= serializers.SlugRelatedField(
    slug_field='movie_id',
    queryset=Movie.objects.all(),
    required=False
)   
    
    # watched = WatchSerializer(read_only=True)
    # watched = serializers.SerializerMethodField("get_watch_status")
    user = UserSerializer(read_only=True)
    
    comments = ReviewCommentSerializer(many=True,read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    # review_liked = ReviewLikeSerializer(read_only=True)
    # review_liked = serializers.SerializerMethodField()
 
    
    rating = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    watched = serializers.SerializerMethodField()
    watchlisted = serializers.SerializerMethodField()
    
    
    def get_comments_count(self,obj):
        return obj.comments.all().count()
    
    def get_likes_count(self,obj):
        return obj.review_likes.all().count()
    
    
    def get_rating(self, obj):
        rating = Rating.objects.filter(user=obj.user, movie=obj.movie).first()
        return RatingSerializer(rating).data if rating else None

    def get_liked(self, obj):
        like = Like.objects.filter(user=obj.user, movie=obj.movie).first()
        return LikeSerializer(like).data if like else None
    
    # def get_review_liked(self, obj):
    #     queryset = obj.review_likes.all()
    #     user = ReviewLike.objects.filter(user=obj.user, review=obj.movie).first()
    #     print("userxoxo = ",user)
    #     return ReviewLikeSerializer(user)
        # if user:
        #     for i in queryset:
        #         return ReviewLikeSerializer(user) if user and i.user.id == user.user.id else None
            
        
        # like = ReviewLike.objects.filter(user=obj.user, review=obj.review).first()
        # return ReviewLikeSerializer(like).data if like else None

    def get_watched(self, obj):
        watch = Watch.objects.filter(user=obj.user, movie=obj.movie).first()
        return WatchSerializer(watch).data if watch else None

    def get_watchlisted(self, obj):
        watchlist = WatchList.objects.filter(user=obj.user, movie=obj.movie).first()
        return WatchListSerializer(watchlist).data if watchlist else None

    class Meta:
        model = Review
        fields = ["id","user","movie","created_at","content","comments","comments_count", "rating", "liked","watched","watchlisted","likes_count"]
        
    
    def create(self,validated_data):
        instance = Review.objects.create(**validated_data)
        print("serializer instance = ",instance)
        return instance
    
    
    def update(self,instance,validated_data):
        request = self.context.get('request')
        if request.user.pk != instance.user.pk:
            raise serializers.ValidationError("You do not have permission to edit this review.")
        instance.content = validated_data.get("content",instance.content)
        instance.save()
        return instance

class UserMovieDataSerializer(serializers.Serializer):
    review = serializers.SerializerMethodField()
    # watched = serializers.SerializerMethodField()
    # liked = serializers.SerializerMethodField()
    # watchlisted = serializers.SerializerMethodField()
    # rating = serializers.SerializerMethodField()
    
    def get_review(self,obj):
        return ReviewSerializer(obj.reviews)
    
    

class MovieSerializer(serializers.ModelSerializer):

    
    reviews = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model=Movie
        fields = ["movie_id","reviews"]