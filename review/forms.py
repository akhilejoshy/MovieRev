from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'form-control border-0 border-bottom bg-transparent text-white rounded-0  w-75',
                'placeholder': 'Add a comment…',
                'required': True
            }),
            
        }
