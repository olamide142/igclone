from django import forms

class ImageUploadForm(forms.Form):

    category_choice = [('PI','Profile Image'), ('RI','Regular Image')]
    type_of_extension_choice = [('jpeg','JPEG'),('png','PNG'),('jpg','JPG')]

    username = forms.CharField(max_length=15)
    category = forms.CharField(max_length=2, choices=category_choice, null=False)
    extension = forms.CharField(max_length=3, choices=type_of_extension_choice, null=False)
    file = forms.FileField()
