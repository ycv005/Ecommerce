from django.urls import path
from .views import ProductListView,product_detailview

urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('<int:pk>/', product_detailview),
]