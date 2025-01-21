from django import forms
from django.core.validators import ValidationError

from article.models import Message


class ContactUsForm(forms.Form):
    BIRTH_YEAR_CHOICES = ["1980", "1981", "1982"]
    FAVORITE_COLORS_CHOICES = {
        "blue": "Blue",
        "green": "Green",
        "black": "Black",
    }

    name = forms.CharField(max_length=10, label='your name')
    text = forms.CharField(max_length=10, label='your message')
    birth_year = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs={'class': 'col-md-4 col-sm-8'}))

    # colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=FAVORITE_COLORS_CHOICES)
    # colors = forms.ChoiceField(widget=forms.RadioSelect,choices=FAVORITE_COLORS_CHOICES)
    # colors = forms.ChoiceField(widget=forms.RadioSelect, choices=FAVORITE_COLORS_CHOICES)

    def clean(self):
        name = self.cleaned_data.get('name')
        text = self.cleaned_data.get('text')
        print(name)
        # if '*' in name:
        #     self.add_error('name', '* can not be in name')
        if name == text:
            raise ValidationError('name and text are same', code='name_text_same')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if '*' in name:
            raise ValidationError('* can not be in name', code='*_in_name')
        return name


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        # fields = ('title', 'text', 'email')
        exclude = ('date',)
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Enter your title',
                "style": "max-width: 600px;"
            }),
            "user": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Enter your title',
                "style": "max-width: 600px;"
            }),
            "email": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": 'Enter your email',
                "style": "max-width: 600px;"
            }),
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": 'Enter your message',
            })
        }
        title = forms.CharField(required=True)
