from django.shortcuts import render
from django.views.generic import ListView
from product_app.models import Product

# Create your views here.
class SearchProductListView(ListView):
    template_name = "search/searchResult.html"

    def get_queryset(self,*args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            instance = Product.objects.search(query) #if same product is added twice, so distinct
            if instance is not None:
                return instance
        return Product.objects.all()
