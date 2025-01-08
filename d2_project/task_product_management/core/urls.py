#CRUD operations for categories and subcategories.
from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView
from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView
# from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView
from .views import TaskListCreateView ,TaskDetailView
urlpatterns = [
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('api/categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/categories/<int:id>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('api/categories/<int:id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/products/<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('api/products/<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]

