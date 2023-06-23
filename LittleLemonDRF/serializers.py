from rest_framework import serializers
from .models import * # temporary, change at end
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(**category_data)
        return MenuItem.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        if category_data is not None:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.category = category

        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.featured = validated_data.get('featured', instance.featured)
        instance.save()

        return instance
    
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    class Meta:
        model = Cart
        fields = ['id','user', 'menuitem', 'quantity', 'unit_price', 'price']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']