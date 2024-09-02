from django.contrib import admin
from .models import Software, UserManual, PDFSettings

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('product_extension', 'download_url', 'password')
    search_fields = ('product_extension',)
    list_filter = ('password',)  # Filters by password presence

@admin.register(UserManual)
class UserManualAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manual_url')
    search_fields = ('product_name',)
    list_filter = ('product_name',)  # Filters by product name

@admin.register(PDFSettings)
class PDFSettingsAdmin(admin.ModelAdmin):
    list_display = ('logo1', 'logo2', 'logo1_x', 'logo1_y', 'logo2_x', 'logo2_y', 'qr_code_x', 'qr_code_y', 'instructions')
    search_fields = ('instructions',)  # Optionally, search by instructions
