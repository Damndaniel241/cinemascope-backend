from lists.models import List,ListComment,ListLike
from users.models import User,UserProfile
from users.serializers import UserProfileSerializer,UserSerializer
from reviews.serializers import TagSerializer,MovieSerializer
from reviews.models import Tag,Movie
from rest_framework import serializers

class ListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True,read_only=True)
    movie = MovieSerializer(many=True,read_only=True)
    tags= serializers.ListField(child=serializers.CharField(max_length=20),write_only=True,allow_empty=True)
    movies= serializers.ListField(child=serializers.CharField(max_length=20),write_only=True,required=True)
    user = UserSerializer(read_only=True)




    def create(self, validated_data):
        tags = validated_data.pop("tags",[])
        movies = validated_data.pop("movies",[])
        created_tags,created_movies = [],[]
        
        # print("movies = ",movies)
        for tag in tags:
            stored_tag,created = Tag.objects.get_or_create(tag=tag)
            created_tags.append(stored_tag)

        for movie in movies:
            stored_movie,created = Movie.objects.get_or_create(movie_id=movie)
            created_movies.append(stored_movie)

        # print("nkki 1")
        created_list = List.objects.create(**validated_data)
        # print("nkki 2")
        created_list.movie.set(created_movies)
        # print("nkki 3")
        created_list.tag.set(created_tags)
        # print("nkki 4")
        created_list.save()

        return created_list


    
    class Meta:
        model = List
        fields= ["id","user","title","description","tag","movie","tags","movies"]



class ListLikeSerializer(serializers.ModelSerializer):
    # movie = serializers.SlugRelatedField(
    #     slug_field="movie_id", queryset=Movie.objects.all(), required=True
    # )
    # user = UserSerializer(read_only=True)
    list = ListSerializer()

    class Meta:
        model = ListLike
        fields = ["id", "list"]



class ListCommentSerializer(serializers.ModelSerializer):
    # review = serializers.SlugRelatedField(
    #     slug_field="id", queryset=Review.objects.all(), required=True
    # )
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request.user.pk != instance.user.pk:
            raise serializers.ValidationError(
                "You do not have permission to edit this comment."
            )
        instance.save()
        return instance

    class Meta:
        model = ListComment
        fields = ["id", "user", "review", "created_at", "content"]