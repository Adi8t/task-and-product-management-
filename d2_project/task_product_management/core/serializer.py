from rest_framework import serializers
from .models import Category, Product ,Task

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'is_active', 'category']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField() 

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'product', 'assigned_user']
    
    # Overriding the create method to assign the current logged-in user automatically
    def create(self, validated_data):
        user = self.context['request'].user  # Get the current logged-in user
        validated_data['assigned_user'] = user  # Automatically assign the logged-in user
        return super().create(validated_data)
