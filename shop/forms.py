from django.forms import ModelForm

from shop.models import ProductHasReview


class ReviewForm(ModelForm):
    class Meta:
        model = ProductHasReview
        fields = ('comment','rating')
