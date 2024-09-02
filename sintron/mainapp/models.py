from django.db import models

class Software(models.Model):
    product_extension = models.CharField(max_length=255, unique=True)
    download_url = models.URLField(max_length=500)
    password = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.product_extension


class UserManual(models.Model):
    product_name = models.CharField(max_length=255)
    manual_url = models.URLField()

    def __str__(self):
        return self.product_name

class PDFSettings(models.Model):
    logo1 = models.ImageField(upload_to='logos/', blank=True, null=True)
    logo2 = models.ImageField(upload_to='logos/', blank=True, null=True)
    logo1_x = models.IntegerField(default=10)  # X position for logo1
    logo1_y = models.IntegerField(default=30)  # Y position for logo1
    logo2_x = models.IntegerField(default=300)  # X position for logo2
    logo2_y = models.IntegerField(default=30)  # Y position for logo2
    qr_code_x = models.IntegerField(default=280)  # X position for QR code
    qr_code_y = models.IntegerField(default=100)  # Y position for QR code
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return "PDF Settings"


