import os
from io import BytesIO

from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose
from PIL import Image, ImageChops

from .utils import save_products_image, save_collections_image, only_int

User = get_user_model()


# ABSTRACT CLASSES

class CommonInfo(models.Model):
    name = models.CharField('Название', max_length=150)
    description = RichTextField('Описание')
    price = models.PositiveIntegerField('Цена')
    instruction = models.FileField('Инструкция по установке', blank=True, null=True)
    material = models.CharField('Материал', max_length=50, blank=True, null=True)
    color = models.CharField('Цвет', max_length=50, blank=True, null=True)
    patina = models.CharField('Патина', max_length=50, blank=True, null=True)
    made_in = models.CharField('Производство', max_length=50, blank=True, null=True)
    slug = models.SlugField('URL', max_length=100, unique=True)
    is_published = models.BooleanField('Опубликован', default=True)

    class Meta:
        abstract = True


class SpecificationsBase(models.Model):
    custom_specification = models.ForeignKey(
        'CustomSpecification', on_delete=models.CASCADE, verbose_name='Характеристика'
    )
    value = models.CharField('Значение', max_length=50)

    class Meta:
        abstract = True


# MODELS

class WebsiteInfo(models.Model):
    name = models.CharField('Название сайта', max_length=150)
    logo = models.ImageField('Логотип', default='images/logo.png')
    address = models.CharField('Адрес', max_length=200)
    phone_number = models.CharField('Телефон', max_length=15, validators=[only_int])
    email = models.EmailField('Email', max_length=32)
    vk = models.URLField('Ссылка на ВК', null=True, blank=True)
    telegram = models.URLField('Ссылка на Telegram', null=True, blank=True)
    youtube = models.URLField('Ссылка на YouTube', null=True, blank=True)

    def __str__(self):
        return 'Данные сайта'

    class Meta:
        verbose_name = 'данные сайта'
        verbose_name_plural = 'Данные сайта'


@receiver(post_save, sender=User)
def create_initial_website_info(sender, instance, created, **kwargs):
    if created:
        if instance.id == 1:
            WebsiteInfo.objects.create(
                name='Lovely Baby',
                address='г. Махачкала, пр. Шамиля 31г',
                phone_number='88002000600',
                email='support@lovelybaby.ru',
            )


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.FileField('Картинка (svg)', validators=[FileExtensionValidator(['svg'])], blank=True, null=True)
    slug = models.SlugField('URL', max_length=100, unique=True)
    is_published = models.BooleanField('Опубликован', default=True)

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['custom_order']


class Collection(CommonInfo):
    image = models.ImageField('Картинка', upload_to=save_collections_image)
    image_2 = models.ImageField('Картинка для главной', upload_to=save_collections_image)
    bed_size = models.CharField(
        'Кровать (ДxШxВ)', max_length=50, blank=True, null=True, help_text='Пример формата: 60x140x34 см.'
    )
    drawer_size = models.CharField(
        'Комод (ДxШxВ)', max_length=50, blank=True, null=True, help_text='Пример формата: 60x140x34 см.'
    )
    wardrobe_size = models.CharField(
        'Шкаф (ДxШxВ)', max_length=50, blank=True, null=True, help_text='Пример формата: 60x140x34 см.'
    )

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('collection_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        template = Image.open(f'{os.path.dirname(__file__)}/collection_templates/template.png').convert('RGBA')
        mask = Image.open(f'{os.path.dirname(__file__)}/collection_templates/mask.png').convert('RGBA')

        image_to_insert = Image.open(self.image)
        width, height = image_to_insert.size
        mask = mask.resize((width, height))

        insert_image = ImageChops.multiply(mask, image_to_insert)
        insert_image = insert_image.resize((660, 594))

        template.paste(insert_image, (13, 0), insert_image)

        image_io = BytesIO()
        template.save(image_io, 'PNG')

        split_image_name = self.image.name.rsplit('.')

        image_name = split_image_name[0]
        image_extension = split_image_name[-1]

        new_image = File(image_io, name=f'{image_name}_main_screen.{image_extension}')
        self.image_2 = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'комплект'
        verbose_name_plural = 'Комплекты'
        ordering = ['custom_order']


class Product(CommonInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name='Комплект')
    size = models.CharField(
        'Размеры ДxШxВ', max_length=50, blank=True, null=True, help_text='Пример формата: 60x140x34 см.'
    )

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ['-custom_order']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField('Картинка', upload_to=save_products_image, null=False)
    thumbnail = ImageSpecField(
        source='image',
        processors=[
            Transpose(),
            ResizeToFill(64, 40),
        ],
        format='PNG',
        options={'quality': 60},
    )

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def __str__(self):
        return str(self.product.name)

    class Meta:
        verbose_name = 'картинка'
        verbose_name_plural = 'Картинки'
        ordering = ['custom_order']


class CustomSpecification(models.Model):
    name = models.CharField('Название', max_length=100)

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'кастомная характеристика'
        verbose_name_plural = 'Кастомные характеристики'
        ordering = ['custom_order']


class AdditionalSpecificationCollection(SpecificationsBase):
    parent = models.ForeignKey(
        Collection, on_delete=models.CASCADE, verbose_name='Комплект', related_name='additional_specifications_collection'
    )

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def __str__(self):
        return str(self.custom_specification.name)

    class Meta:
        verbose_name = 'дополнительные характеристики'
        verbose_name_plural = 'Дополнительные характеристики'
        ordering = ['custom_order']


class AdditionalSpecificationProduct(SpecificationsBase):
    parent = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='additional_specifications_product'
    )

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def __str__(self):
        return str(self.custom_specification.name)

    class Meta:
        verbose_name = 'дополнительные характеристики'
        verbose_name_plural = 'Дополнительные характеристики'
        ordering = ['custom_order']


class Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    is_published = models.BooleanField('Опубликован', default=True)

    custom_order = models.PositiveIntegerField('Кастомный порядок', default=0, blank=False, null=False)

    def __str__(self):
        return str(self.product.name)

    class Meta:
        verbose_name = 'слайдер'
        verbose_name_plural = 'Слайдер'
        ordering = ['custom_order']
