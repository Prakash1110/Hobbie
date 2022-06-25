from django import forms
from shop.models import Product


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    # for field in self.fields:
    #     field.attrs['class']