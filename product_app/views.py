from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.http import Http404
from cart_app.models import Cart
# Create your views here.
from .models import Product

def product_detailview(request,pk):
    object = Product.objects.get_by_id(pk)
    # Product is the model and objects is the model manager here. It help us to do things on the model.
    # So, Model manager could be created on own.
    print("inst-",object)
    if object is None:
        raise Http404("No such product exists")
    return render(request,"product_app/product_detail.html",context={"object":object})

#class based view
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "product_app/product_list.html"
    #by default, the context is provided, where object_list contatins all the published obj
    #anyway to get context
    def get_context_data(self, **kwargs):
        context = super(ProductListView,self).get_context_data(**kwargs)
        cart,new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart
        return context

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "product_app/product_detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug)
        return instance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart,new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart
        return context

class ProductFeaturedDetailView(DetailView):   
    template_name = "product_app/featured_product_detail.html" 

    def get_queryset(self,*args, **kwargs):
        pk = self.kwargs.get('pk')
        instance  = Product.objects.get_featured().filter(id=pk)
        # print(instance)
        if instance is None:
            raise Http404("No Products in Featured List")
        return instance       

    def get_context_data(self, **kwargs):
        context = super(ProductFeaturedDetailView,self).get_context_data(**kwargs)
        print(context)
        return context

class ProductFeaturedListView(ListView):
    template_name = "product_app/product_list.html"

    def get_queryset(self):
        instance  = Product.objects.get_featured()
        if instance is None:
            raise Http404("No Products in Featured List")
        return instance