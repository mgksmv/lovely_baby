import random

from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.list import MultipleObjectMixin

from .models import Slider, Collection, Category, Product
from forms.forms import CommercialProposalRequestForm
from .mixins import CustomFormMixin


class HomeTemplateView(TemplateView, CustomFormMixin):
    template_name = 'home.html'
    form_class = CommercialProposalRequestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collections = list(Collection.objects
                           .filter(is_published=True)
                           .prefetch_related('product_set', 'product_set__productimage_set')
                           )
        random.shuffle(collections)

        context['sliders'] = Slider.objects \
            .filter(is_published=True) \
            .select_related('product', 'product__collection') \
            .prefetch_related('product__productimage_set')
        context['collections'] = collections[:3]
        context['categories'] = Category.objects \
            .filter(is_published=True) \
            .prefetch_related(
                'product_set',
                'product_set__productimage_set',
                'product_set__collection__additional_specifications_collection'
            )

        return context


class AboutTemplateView(CustomFormMixin, FormView):
    form_class = CommercialProposalRequestForm
    template_name = 'about.html'


class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'


class CatalogListView(ListView):
    model = Category
    template_name = 'catalog.html'

    def get_queryset(self):
        return Category.objects \
            .filter(is_published=True) \
            .prefetch_related(
                'product_set',
                'product_set__productimage_set',
                'product_set__collection__additional_specifications_collection'
            )


class CollectionsListView(ListView):
    model = Collection
    paginate_by = 12
    template_name = 'collections.html'

    def get_queryset(self):
        return Collection.objects.filter(is_published=True)


class CollectionDetailView(DetailView, CustomFormMixin):
    model = Collection
    form_class = CommercialProposalRequestForm
    template_name = 'collection_detail.html'

    def get_queryset(self):
        return Collection.objects \
            .filter(is_published=True) \
            .prefetch_related('product_set', 'product_set__productimage_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collections = list(self.get_queryset())
        random.shuffle(collections)

        context['random_collections'] = collections[:3]

        return context


class ProductDetailView(DetailView, CustomFormMixin):
    model = Product
    form_class = CommercialProposalRequestForm
    template_name = 'product_detail.html'

    def get_queryset(self):
        return Product.objects \
            .filter(is_published=True) \
            .select_related('category', 'collection') \
            .prefetch_related(
                'collection__product_set__productimage_set',
                'category__product_set__productimage_set',
                'additional_specifications_product__custom_specification',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_image_set'] = self.object.productimage_set.all()
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            context['before_prev_path'] = referer.split('/')[-3]
            context['prev_path'] = referer.split('/')[-2]
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    paginate_by = 9
    template_name = 'category_detail.html'

    def get_queryset(self):
        return Category.objects \
            .filter(is_published=True) \
            .prefetch_related('product_set')

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.get_object()) \
            .filter(is_published=True) \
            .prefetch_related('productimage_set', 'collection')
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context
