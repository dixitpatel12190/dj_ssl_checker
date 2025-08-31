
from django.http import HttpResponse
from django.shortcuts import render
import ssl
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'index.html')
    
def cert(request):
    analysed = ""
    if request.method == "POST":
        cert_file = request.FILES.get('cert_file')
        key_file = request.FILES.get('key_file')
        key_password = request.POST.get('key_password', '')
        if cert_file and key_file:
            try:
                cert_data = cert_file.read()
                key_data = key_file.read()
                from cryptography.hazmat.primitives import serialization
                from cryptography.x509 import load_pem_x509_certificate
                from cryptography.hazmat.backends import default_backend
       
                cert = load_pem_x509_certificate(cert_data, default_backend())
                password = key_password.encode() if key_password else None
                key = serialization.load_pem_private_key(key_data, password=password, backend=default_backend())
                if cert.public_key().public_numbers() == key.public_key().public_numbers():
                    analysed = "Certificate and Key match!"
                else:
                    analysed = "Certificate and Key do NOT match."
            except Exception as e:
                analysed = f"Error processing files: {e}"
        else:
            analysed = "Please upload both certificate and key files."
    params = {'purpose': 'Certificate & Key Comparison', 'analysed_text1': analysed}
    return render(request, 'cert.html', params)