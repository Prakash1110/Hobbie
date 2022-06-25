from django import forms
from .models import Address


class ChangeCart(forms.Form):
    itemid = forms.CharField(widget=forms.HiddenInput)


class PlaceOrderForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    product_slug = forms.SlugField(widget=forms.HiddenInput(), required=False)
    # total = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def __init__(self, *args, **kwargs):
        user = None
        if 'user' in kwargs:
            user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            queryset = user.address_set.all()
            self.fields['address'].queryset = queryset


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Address'
                }
            )
        }


