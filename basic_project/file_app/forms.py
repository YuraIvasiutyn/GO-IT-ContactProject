from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()
    category = forms.ChoiceField(choices=[
        ('image', 'Зображення'),
        ('document', 'Документ'),
        ('video', 'Відео'),
        ('other', 'Інше'),
    ])
