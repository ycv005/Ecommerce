from django.urls import path
from .views import ProductListView,ProductDetailSlugView, ProductFeaturedDetailView,ProductFeaturedListView,product_detailview

urlpatterns = [
    path('list/', ProductListView.as_view(),name='list'),
    path('<int:pk>/', product_detailview),
    path('<slug:slug>', ProductDetailSlugView.as_view(), name='urldetail'),
    path('featured-list/', ProductFeaturedListView.as_view()),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]