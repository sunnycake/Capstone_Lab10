from django import forms
from .models import Place 

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place 
        fields = ('name', 'visited')

# create django's built in date input
class DateInput(forms.DateInput):
    input_type = 'date'  # Override the default input type, which is 'text'


class TripReviewForm(forms.ModelForm):
    class Meta: # describing info about the object
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput() # date customization for user friendly
        }