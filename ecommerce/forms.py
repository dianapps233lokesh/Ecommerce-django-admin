from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Brand

class CustomUserCreationForm(UserCreationForm):
    brand = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'brand', 'is_staff', 'is_superuser')

    def clean_brand(self):
        brand_name = self.cleaned_data.get('brand')
        if brand_name:
            brand, _ = Brand.objects.get_or_create(name=brand_name.strip())
            return brand  
        return None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.brand = self.cleaned_data.get('brand')  
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    brand = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'brand', 'is_staff', 'is_superuser')

    def clean_brand(self):
        brand_input = self.cleaned_data.get('brand')
        if brand_input:
          
            try:
                brand = Brand.objects.get(pk=int(brand_input))
            except (ValueError, Brand.DoesNotExist):
                brand, _ = Brand.objects.get_or_create(name=brand_input.strip())
            return brand
        return None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.brand = self.cleaned_data.get('brand')  
        user.save()
        return user
