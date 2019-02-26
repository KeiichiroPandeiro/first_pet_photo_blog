from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('blog/<int:user_id>/', views.mypage, name='mypage'),
    path('blog/index/<int:photo_id>/', views.detail, name='detail'),
    path('<int:photo_id>/good/', views.good, name='good'),
    path('create_pet/', views.create_pet, name='create_pet'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('blog/mypage/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('blog/<int:pet_id>/edit/', views.pet_edit, name='pet_edit'),

]
"""
URLS.py
    path('products/<int:product_id>/edit/', catalogue.views.product_edit,
         name='product_edit'),

VIEWS.py
def product_edit(request, product_id):
    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_detail',
                                               args=(product.id,)))
    else:
        form= ProductEditForm(instance=product)
    return TemplateResponse(request, 'catalogue/product_edit.html',
                   {'form':form,'product':product})

"""
