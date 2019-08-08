from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Avg
from django.db.models.functions import math
from sorl.thumbnail import ImageField

# Create your models here.
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField


class Menu(models.Model):
    title = models.CharField(max_length=30)
    link = models.CharField(max_length=250)
    Weight = models.IntegerField(default=0)  # jasko weight dherai huncha tyo agadi aucha

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', unique=True)
    details = RichTextField()
    image = ImageField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'


class Banner(models.Model):
    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=50)
    image = ImageField()
    button = models.CharField(max_length=50)
    text = models.CharField(max_length=80)
    link = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.IntegerField()
    strike_price = models.IntegerField()
    availability = models.BooleanField()
    brand = models.CharField(max_length=50)
    short_intro = RichTextField()
    sizes = models.CharField(max_length=50)
    colors = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # foreign key rakheko
    details = RichTextField()
    deal_of_day = models.BooleanField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image(self):
        return self.producthasimage_set.first().image  # first le producthasimageko object dinch hamilai image chaiyeko

    def list_of_size(self):
        return self.sizes.split(',')
    def list_of_color(self):
        return self.colors.split(',')

    def rating(self):
        op = self.producthasreview_set.aggregate(Avg('rating'))

        if 'rating__avg' in op and op['rating__avg']: #key hunu paryodictionary hunu bhaya pachadi ko value null hunubhyena
            return int(math.ceil(op['rating__avg']))
            return op['rating__avg']
        else:
            return 0

        def rating_range(self):
            return range(self.rating)

        def empty_rating_range(self):
            return range(5 - self.rating)


class ProductHasImage(models.Model):
    image = ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductHasReview(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def rating_range(self):

        if not self.rating:
            return[]
        return range(self.rating)

    def empty_rating_range(self):

        if not self.rating:
            return range(5)
        return range(5-self.rating)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.IntegerField()
