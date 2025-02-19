from wsgiref.validate import validator
from django import forms


class ExcelStaffForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=None,
        label='Импортировать данные из файла',
    )
    file_fields = forms.FileField(
        allow_empty_file=None,
    )
    