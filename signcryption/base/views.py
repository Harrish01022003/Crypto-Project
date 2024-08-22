from django.shortcuts import render, redirect
from .models import User, Transaction, TwoFactorAuth
from django.contrib.auth import authenticate, login, logout
from PIL import Image
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.decorators import login_required
import imagehash
from django.http import HttpResponse

def home(request):
    print(request.user)
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        vein = request.FILES['file']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        tfa = TwoFactorAuth.objects.create(user=user, vein_pattern=vein)
        tfa.save()
        return redirect('home')
    return render(request, 'user_register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tfa')
        else:
            return render(request, 'user_login.html', {'error': 'Invalid username or password'})
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def tfa(request):
    curr_user = request.user
    if request.method == 'POST' and request.FILES:
        user_uploaded_vein = request.FILES['file']
        # file : UploadedFile = user_uploaded_vein
        image = Image.open(user_uploaded_vein)
        tfa_ins = TwoFactorAuth.objects.get(user=curr_user)
        tfa_image = tfa_ins.vein_pattern.name
        tfa_image = tfa_image.split('/')[-1]
        tfa_image = f'media\\vein\\{tfa_image}'
        print(tfa_image)
        tfa_image = Image.open(tfa_image)
        hash0 = imagehash.average_hash(image)
        hash1 = imagehash.average_hash(tfa_image)
        if (hash0 - hash1) < 5:
            print(hash0, hash1)
            return redirect('home')
        else:
            logout(request)
            return HttpResponse('<strong>vein pattern didnt match</strong>')
    return render(request, 'tfa.html')

@login_required
def make_transaction(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        reciever = request.POST['reciever']
        curr_user = request.user
        transaction = Transaction.objects.create(user=curr_user, amount=amount, reciever = reciever, status='Succeed')
        transaction.save()
        return redirect('home')
    return render(request,'make_transaction.html')

@login_required
def list_transactions(request):
    curr_user = request.user
    transactions = Transaction.objects.filter(user=curr_user)
    return render(request, 'list_transaction.html', {'transactions': transactions})