from django.urls import path
from .views import ProductListView,product_detailview, ProductFeaturedDetailView,ProductFeaturedListView

urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('<int:pk>/', product_detailview),
    path('featured-list/', ProductFeaturedListView.as_view()),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]