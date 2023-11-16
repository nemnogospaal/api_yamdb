from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from content.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category



class GenreSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Title.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Genre