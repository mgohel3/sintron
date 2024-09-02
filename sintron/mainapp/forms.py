from django import forms
from .models import Software, UserManual, PDFSettings

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['product_extension', 'download_url', 'password']
        widgets = {
            'product_extension': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Extension'}),
            'download_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.softwaredownloadlink.com'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter URL Access Password'}),
        }

class UserManualForm(forms.ModelForm):
    class Meta:
        model = UserManual
        fields = ['product_name', 'manual_url']


class PDFSettingsForm(forms.ModelForm):
    logo1_x = forms.IntegerField(label='Logo 1 X Position')
    logo1_y = forms.IntegerField(label='Logo 1 Y Position')
    logo2_x = forms.IntegerField(label='Logo 2 X Position')
    logo2_y = forms.IntegerField(label='Logo 2 Y Position')
    qr_code_x = forms.IntegerField(label='QR Code X Position')
    qr_code_y = forms.IntegerField(label='QR Code Y Position')
    instructions = forms.CharField(widget=forms.Textarea, label='Instructions')

    class Meta:
        model = PDFSettings
        fields = ['logo1', 'logo2', 'logo1_x', 'logo1_y', 'logo2_x', 'logo2_y', 'qr_code_x', 'qr_code_y', 'instructions']
