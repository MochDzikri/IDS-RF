from django.shortcuts import render, redirect
from app.forms import DataForm
from app.models import Data
import csv
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import requests
from django.core.files.storage import FileSystemStorage
from sklearn.preprocessing import LabelEncoder

# Create your views here.

def index(request):
    return render(request, "app/index.html")

def data(request):
    datas = Data.objects.all()
    return render(request, "app/data.html", {"datas":datas})

def addnew(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('data')
            except:
                pass
    else:
        form = DataForm()
    return render(request, "app/tambahdata.html", {"form":form})

def edit(request, id):
    data = Data.objects.get(id=id)
    return render(request, "app/edit.html", {"data":data})

def update(request, id):
    data = Data.objects.get(id=id)
    form = DataForm(request.POST, instance = data)
    if form.is_valid():
        form.save()
        return redirect("data")
    return render(request, "app/edit.html", {"data":data})

def destroy(request, id):
    data = Data.objects.get(id=id)
    data.delete()
    return redirect("data")


def process_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        csv_data = csv.reader(csv_file.read().decode("utf-8").splitlines())
        header = next(csv_data)
        
        for row in csv_data:
            source_ip = row[0]
            destination_ip = row[1]
            source_port = int(row[2])
            destination_port = int(row[3])
            protocol = int(row[4])
            packet_length = int(row[5])
            timestamp = datetime.fromtimestamp(float(row[6]))
            flag_packet = row[7]
            data_payload = row[8]
            label = row[9]
            
            Data.objects.create(
                source_ip=source_ip,
                destination_ip=destination_ip,
                source_port=source_port,
                destination_port=destination_port,
                protocol=protocol,
                packet_length=packet_length,
                timestamp=timestamp,
                flag_packet=flag_packet,
                data_payload=data_payload,
                label=label,
            )
        
        return redirect("data")
    
    return redirect("upload_csv")

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # Redirect to desired page after successful login
    else:
        form = AuthenticationForm()
    return render(request, "app/signin.html", {"form": form})
    
def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'app/signup.html', {"form":form})
    else:
        form = UserCreationForm()
        return render(request, 'app/signup.html', {'form':form})
    
def signout(request):
    logout(request)
    return redirect("signin")