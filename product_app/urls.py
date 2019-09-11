from django.urls import path
from .views import ProductListView,ProductDetailView, ProductFeaturedDetailView,ProductFeaturedListView,product_detailview

urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('<int:pk>/', product_detailview),
    path('<slug:slug>/', ProductDetailView.as_view()),
    path('featured-list/', ProductFeaturedListView.as_view()),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]