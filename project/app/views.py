from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse, HttpResponse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from django.contrib.auth.decorators import login_required
from .models import User, EncryptedData,register,DencryptedData

def home(request):
    return render(request,'home.html')

def clientsignup(request):
    if request.method == 'POST':
        getusername = request.POST['username']
        getemail = request.POST['email']
        getpassword = request.POST['password']
        users = register()
        users.Username = getusername
        users.Email = getemail
        users.Password = getpassword
        users.save()
    return render(request,'clientsignup.html')

def clientsignin(request):
    if request.method == 'POST':
        getusername = request.POST['username']
        getpassword = request.POST['password']
        try:
            register.objects.get(Username=getusername,Password=getpassword)
            return redirect('/client')
        except:
            return HttpResponse('Invalid user')
    return render(request,'clientsignin.html')

def client(request):
    return render(request,'client.html')

def adminlogin(request):
    if request.method == 'POST':
        getusername = request.POST['username']
        getpassword = request.POST['password']
        if getusername == 'admin' and getpassword == 'admin':
            return redirect('/manage_keys')
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'adminlogin.html')
    
# Generate a DES key (must be 8 bytes)
def generate_des_key():
    return get_random_bytes(8)

# DES encryption function
def encrypt_with_des(plaintext, key):
    iv = get_random_bytes(8)  # Initialization Vector (8 bytes for DES)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode(), DES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return iv + encrypted_data  # Return IV + encrypted data

# DES decryption function
def decrypt_with_des(encrypted_data, key):
    iv = encrypted_data[:8]  # Extract IV
    encrypted_content = encrypted_data[8:]  # Extract encrypted content
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_padded_data = unpad(cipher.decrypt(encrypted_content), DES.block_size)
    return decrypted_padded_data.decode()

# Encrypt view
def encrypt_view(request):
    if request.method == "POST":
        plaintext = request.POST.get("plaintext")
        if not plaintext:
            return JsonResponse({"error": "No plaintext provided"}, status=400)

        key = generate_des_key()
        encrypted_data = encrypt_with_des(plaintext, key)

        # Save the encrypted data and key in the database
        data_entry = EncryptedData.objects.create(data=encrypted_data, key=key)
        return JsonResponse({
            "message": "Data encrypted successfully",
            "id": data_entry.id,
            "key": key.hex()  # Convert key to hexadecimal for readability
        })

    # Handle GET request to show encryption form
    if request.method == "GET":
        return render(request, "encrypt.html")

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)

# Decrypt view
# Decrypt view
def decrypt_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        data_id = request.POST.get("data_id")

        if not user_id or not data_id:
            return JsonResponse({"error": "Missing user_id or data_id"}, status=400)

        # Verify user
        user = User.objects.filter(user_id=user_id, is_authorized=True).first()
        if not user:
            return JsonResponse({"error": "Unauthorized user"}, status=403)

        # Retrieve and decrypt data
        data_entry = EncryptedData.objects.filter(id=data_id).first()
        if not data_entry:
            return JsonResponse({"error": "Data not found"}, status=404)

        decrypted_data = decrypt_with_des(data_entry.data, data_entry.key)

        # Save decrypted data as a string
        dencrypted_entry = DencryptedData.objects.create(data=decrypted_data.encode('utf-8'), encrypted_data=data_entry)

        return JsonResponse({
            "message": "Data decrypted successfully",
            "data": decrypted_data  # This should be a string now
        })

    # Handle GET request to show decryption form
    if request.method == "GET":
        return render(request, "decrypt.html")

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def manage_keys(request):
    keys = EncryptedData.objects.all()
    dataa = DencryptedData.objects.all()
    details = register.objects.all()
    return render(request,'manage_keys.html',{'keys': keys,'dataa':dataa,'details':details})