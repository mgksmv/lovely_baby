from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('contacts/', views.ContactsTemplateView.as_view(), name='contacts'),
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    path('collections/', views.CollectionsListView.as_view(), name='collections'),
    path('collections/<slug:slug>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
