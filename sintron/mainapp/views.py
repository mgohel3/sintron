from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .forms import SoftwareForm, UserManualForm, PDFSettingsForm
from .models import Software, UserManual, PDFSettings
from PIL import Image
import qrcode
import tempfile
import os


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'mainapp/home.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))  # Redirect to the dashboard page
    else:
        form = AuthenticationForm()

    return render(request, 'mainapp/home.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_software_links = Software.objects.count()  # Count the total software links
    total_user_manual_links = UserManual.objects.count()

    context = {
        'total_software_links': total_software_links,
        'total_user_manual_links': total_user_manual_links,
    }
    return render(request, 'mainapp/dashboard.html', context)

@login_required
def software(request):
    return render(request, 'mainapp/software.html')

@login_required
def software_list(request):
    base_url = 'http://127.0.0.1:8000/'
    softwares = Software.objects.all()
    for software in softwares:
        software.full_url = f"{base_url}{software.product_extension}/download"
    return render(request, 'mainapp/software.html', {'softwares': softwares})

@login_required
def software_create(request):
    if request.method == 'POST':
        form = SoftwareForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('software')
    else:
        form = SoftwareForm()
    return render(request, 'mainapp/software.html', {'form': form})

@login_required
def software_edit(request, pk):
    software = get_object_or_404(Software, pk=pk)
    if request.method == 'POST':
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            form.save()
            return redirect('software_list')  # Make sure this redirects to the software list
    else:
        form = SoftwareForm(instance=software)
    return render(request, 'mainapp/software.html', {'form': form})

@login_required
def software_delete(request, pk):
    if request.method == 'POST':
        software = get_object_or_404(Software, pk=pk)
        software.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def protected_redirect(request, product_extension):
    software = get_object_or_404(Software, product_extension=product_extension)
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == software.password:
            return redirect(software.download_url)
        else:
            return HttpResponseForbidden("Incorrect password")
    return render(request, 'mainapp/password_prompt.html', {'software': software})

@login_required
def usermanual(request):
    if request.method == 'POST':
        form = UserManualForm(request.POST)
        if form.is_valid():
            instance = form.save()
            # Generate link based on product name
            product_name = instance.product_name
            generated_link = f"https://m.sintronindia.com/{product_name.replace(' ', '_').upper()}"
            instance.manual_url = generated_link
            instance.save()
            return redirect('usermanual')
    else:
        form = UserManualForm()

    manuals = UserManual.objects.all()  # Ensure you fetch all user manuals
    return render(request, 'mainapp/usermanual.html', {'form': form, 'manuals': manuals})

@login_required
def usermanual_create(request):
    if request.method == 'POST':
        form = UserManualForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usermanual')
    else:
        form = UserManualForm()
    return render(request, 'mainapp/usermanual.html', {'form': form})

@login_required
def usermanual_delete(request, pk):
    if request.method == 'POST':
        usermanual = get_object_or_404(UserManual, pk=pk)
        usermanual.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def pdf_settings(request):
    settings, created = PDFSettings.objects.get_or_create(pk=1)  # Use a single instance
    if request.method == 'POST':
        form = PDFSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('pdf_settings')
    else:
        form = PDFSettingsForm(instance=settings)
    return render(request, 'mainapp/pdf_settings.html', {'form': form})

@login_required
def generate_pdf(request, pk):
    usermanual = get_object_or_404(UserManual, pk=pk)
    settings = PDFSettings.objects.get(pk=1)  # Retrieve the settings

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(400, 200))  # Adjusted to a business card size
    width, height = 400, 200  # Width and height of the business card-like PDF

    # Top Section
    qr_size_percentage = 0.15  # Adjusted QR code size to 15% of width
    qr_width = width * qr_size_percentage

    # Instructions
    p.setFont("Helvetica", 10)
    instructions_y = height - 30
    p.drawString(10, instructions_y, "Scan QR code or go to link to Download the User Manual")

    # QR Code
    qr_code_url = f"https://m.sintronindia.com/{usermanual.product_name.replace(' ', '_').lower()}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_code_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')

    # Use tempfile to create a temporary file for QR code
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_qr_file:
        qr_img.save(temp_qr_file)
        temp_qr_path = temp_qr_file.name

    # Draw QR Code on PDF
    qr_x_position = width - qr_width - 10
    qr_y_position = height - qr_width - 10
    p.drawImage(temp_qr_path, qr_x_position, qr_y_position, width=qr_width, height=qr_width)

    # Middle Section
    middle_section_height = 60
    p.setFillColorRGB(0.8, 0.8, 0.8)  # Grey background
    p.rect(0, height / 2 - middle_section_height / 2, width, middle_section_height, fill=1, stroke=1)
    p.setFillColorRGB(0, 0, 0)  # Black font color
    p.setFont("Helvetica", 12)
    text_width = p.stringWidth(qr_code_url, "Helvetica", 12)
    p.drawString((width - text_width) / 2, height / 2 - 10, qr_code_url)

    # Bottom Section
    bottom_section_height = 40
    logo_width = 40
    logo_height = 40

    # Calculate vertical center position for logos
    logos_center_y = 30 + (bottom_section_height - logo_height) / 2

    # Draw First Brand Logo
    if settings.logo1:
        try:
            with Image.open(settings.logo1.path) as img:
                logo_ratio = img.width / img.height
                if logo_width / logo_height > logo_ratio:
                    logo_width = logo_height * logo_ratio
                else:
                    logo_height = logo_width / logo_ratio
            p.drawImage(settings.logo1.path, 10, logos_center_y, width=logo_width, height=logo_height)
        except Exception as e:
            p.drawString(10, bottom_section_height / 2, f"Logo1 Error: {str(e)}")

    # Draw Second Brand Logo
    if settings.logo2:
        try:
            with Image.open(settings.logo2.path) as img:
                logo_ratio = img.width / img.height
                if logo_width / logo_height > logo_ratio:
                    logo_width = logo_height * logo_ratio
                else:
                    logo_height = logo_width / logo_ratio
            p.drawImage(settings.logo2.path, width - logo_width - 10, logos_center_y, width=logo_width, height=logo_height)
        except Exception as e:
            p.drawString(width - logo_width - 10, bottom_section_height / 2, f"Logo2 Error: {str(e)}")

    # Save PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    # Filename based on product extension
    filename = f'{usermanual.product_name.replace(" ", "_")}.pdf'
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response

# Example of a simple view with HttpResponse
def hello_world(request):
    return HttpResponse("Hello, World!")
