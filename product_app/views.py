from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView

# Create your views here.
from .models import Product

#class based view
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "product_app/product_list.html"
    #by default, the context is provided, where object_list contatins all the published obj
    #anyway to get context
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView,self).get_context_data(**kwargs)
    #     print(context)
    #     return context


def product_detailview(request,pk):
    instance = get_object_or_404(Product,pk=pk)
    return render(request,"product_app/product_detail.html",context={"object_list":instance})