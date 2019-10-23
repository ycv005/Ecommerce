from django.urls import path
from search_app.views import SearchProductListView

urlpatterns = [
    path('', SearchProductListView.as_view(),name='query'),
]