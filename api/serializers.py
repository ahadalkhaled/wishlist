from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class FavBySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = FavoriteItem
        fields = ['user']

class NumOfFavsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ['query']

class ItemListSerializer(serializers.ModelSerializer):
    numb_of_favs = serializers.SerializerMethodField()

    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "item_id",
        )

    added_by = UserSerializer()

    class Meta:
        model = Item
        fields = ['image', 'name', 'description', 'detail', 'added_by', 'numb_of_favs']

    def get_numb_of_favs(self, obj):
        numb_of_favs = FavoriteItem.objects.filter(item=obj).count()
        return numb_of_favs
        
        

class ItemDetailSerializer(serializers.ModelSerializer):
    favorited_by = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['image', 'name', 'description', 'favorited_by']
    
    def get_favorited_by(self, obj):
        favorited_by = FavoriteItem.objects.filter(item=obj)
        user_list = FavBySerializer(favorited_by, many=True).data
        return user_list
