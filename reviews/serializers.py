from rest_framework import serializers
from .models import Review,Movie,Rating,Watch,Like,WatchList
from users.serializers import UserProfileSerializer, UserSerializer
from users.models import User


class MovieSerializer(serializers.ModelSerializer):
    # movie_id = serializers.CharField(max_length=20)
    
    class Meta:
        model=Movie
        fields = ["movie_id"]
        
    # def get_ra    
    
class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","user_name"]
        


class ReviewSerializer(serializers.ModelSerializer):
    # user = UserReviewSerializer(read_only=True)
    # user = UserSerializer(read_only=True)
    # movie = serializers.CharField(max_length=20)
    # movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    movie= serializers.SlugRelatedField(
    slug_field='movie_id',
    queryset=Movie.objects.all(),
    required=False
)   
    # rating = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Review
        fields = ["id","movie","created_at","content"]
        
    
    def create(self,validated_data):
        instance = Review.objects.create(**validated_data)
        print("serializer instance = ",instance)
        return instance
    
    
    def update(self,instance,validated_data):
        instance.content = validated_data.get("content",instance.content)
        instance.save()
        return instance
    
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
    user = UserSerializer(read_only=True)


    class Meta:
        model = Like
        fields = ["id","movie","user"]
        
    