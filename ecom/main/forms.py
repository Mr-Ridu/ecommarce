from django import forms
from .models import PurchesDetails,ProductDetails



class PurchesDetailsForms(forms.ModelForm):
    class Meta:
        model = PurchesDetails
        fields = '__all__'


class ProductDetailsforms(forms.ModelForm):
    class Meta:
        model = ProductDetails
        fields= '__all__'