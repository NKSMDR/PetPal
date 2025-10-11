from django import forms
from .models import Pet, Breed

class PetSubmissionForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'breed', 'age', 'gender', 'price', 'description',
            'image', 'image2', 'image3', 'weight', 'color',
            'vaccination_status', 'health_certificate', 'city', 'state',
            'address', 'latitude', 'longitude'
        ]
        widgets = {
            'breed': forms.Select(attrs={
                'class': 'form-control'
            }),
            'age': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2 months, 1 year'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price in USD',
                'step': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your pet in detail...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'weight': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 5 kg, 15 lbs'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pet color/markings'
            }),
            'vaccination_status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'health_certificate': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City where pet is located'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full address'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make breed queryset more user-friendly
        self.fields['breed'].queryset = Breed.objects.all().order_by('name')
        self.fields['breed'].empty_label = "Select a breed"
        
        # Set required fields
        required_fields = ['breed', 'age', 'gender', 'price', 'description', 'image', 'city', 'state', 'address']
        for field_name in required_fields:
            self.fields[field_name].required = True
