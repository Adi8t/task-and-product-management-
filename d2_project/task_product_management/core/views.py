from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category ,Task ,Product
from .serializer import CategorySerializer  ,ProductSerializer ,TaskSerializer
from rest_framework.permissions import IsAuthenticated
# List all categories (nested structure for subcategories)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent_category=None)  
        serializer = CategorySerializer(categories, many=True) 
        return Response(serializer.data) 

# Create a new category or subcategory
class CategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve details of a specific category
class CategoryDetailView(APIView):
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

# Update an existing category
class CategoryUpdateView(APIView):
    def put(self, request, id):
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

# Delete a category
class CategoryDeleteView(APIView):
    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)


# List all products with filters for category and active status
class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()

        # Filtering based on category and active status
        category_id = request.query_params.get('category')
        is_active = request.query_params.get('is_active')

        if category_id:
            products = products.filter(category__id=category_id)  
        if is_active:
            products = products.filter(is_active=is_active.lower() == 'true') 

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# Create a new product
class ProductCreateView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve details of a specific product
class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

# Update an existing product
class ProductUpdateView(APIView):
    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

# Delete a product
class ProductDeleteView(APIView):
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)




class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_user=request.user)
        
        # Filtering by status and product
        status_filter = request.query_params.get('status')
        product_filter = request.query_params.get('product')
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        if product_filter:
            tasks = tasks.filter(product_id=product_filter)
        
        # Sorting by due_date
        tasks = tasks.order_by('due_date')

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
           
    # POST method for creating new tasks
    def post(self, request):
        data = request.data
        
        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the task using the updated serializer
        serializer = TaskSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Task
from .serializer import TaskSerializer

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer