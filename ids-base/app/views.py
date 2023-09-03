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
    return render(request, "app/editdata.html", {"data":data})

def update(request, id):
    data = Data.objects.get(id=id)
    form = DataForm(request.POST, instance = data)
    if form.is_valid():
        form.save()
        return redirect("data")
    return render(request, "app/editdata.html", {"data":data})

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
            timestamp = float(row[6])
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

def prepare_data(data):
    # Pilih fitur-fitur yang akan digunakan sebagai input model
    features = data[["source_port", "destination_port", "protocol", "packet_length", "timestamp", "flag_packet", "data_payload"]].values

    # Pilih kolom "label" sebagai label
    labels = data["label"]

    # Kodekan label menjadi nilai numerik menggunakan LabelEncoder
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    return features, labels_encoded

def save_results(predictions):
    # Simpan hasil prediksi ke dalam database atau tampilkan pada halaman index.html
    # Anda dapat menggunakan Data.objects.create() atau metode lain yang sesuai
    pass

def get_training_data(request):
    # Implementasikan untuk mengambil data training dari model yang ada pada halaman data.html
    # Lakukan permintaan HTTP ke endpoint yang menyediakan data training
    response = requests.get("URL_ENDPOINT")  # Ganti dengan URL yang sesuai
    return response

def perform_detection(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        csv_data = csv.reader(csv_file.read().decode("utf-8").splitlines())
        header = next(csv_data)

        # Ambil data dari tabel tbldata
        data_objects = Data.objects.all()

        # Konversi data dari model menjadi DataFrame Pandas
        data_df = pd.DataFrame(list(data_objects.values()))

        # Persiapkan data dan label untuk training
        X_train, y_train = prepare_data(data_df)

        # Buat dan latih model Random Forest
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Proses data uji dari file CSV menjadi fitur numerik
        test_data = []
        for row in csv_data:
            source_ip_test = row[0]
            destination_ip_test = row[1]
            source_port_test = int(row[2])
            destination_port_test = int(row[3])
            protocol_test = row[4]
            packet_length_test = int(row[5])

            # Konversi kolom timestamp ke dalam float
            timestamp_test = float(row[6].replace(",", "."))

            flag_packet_test = row[7]
            data_payload_test = row[8]

            test_data.append([source_ip_test, destination_ip_test, source_port_test, destination_port_test, protocol_test, packet_length_test, timestamp_test, flag_packet_test, data_payload_test])

        test_data = np.array(test_data)

        # Lakukan label encoding pada atribut yang memerlukan
        source_ip_encoder = LabelEncoder()
        destination_ip_encoder = LabelEncoder()
        protocol_encoder = LabelEncoder()
        flag_packet_encoder = LabelEncoder()
        data_payload_encoder = LabelEncoder()
        port_encoder = LabelEncoder()  # Tambahkan encoder untuk port

        source_ip_test_encoded = source_ip_encoder.transform(test_data[:, 0])
        destination_ip_test_encoded = destination_ip_encoder.transform(test_data[:, 1])
        protocol_test_encoded = protocol_encoder.transform(test_data[:, 4])
        flag_packet_test_encoded = flag_packet_encoder.transform(test_data[:, 7])
        data_payload_test_encoded = data_payload_encoder.transform(test_data[:, 8])
        port_test_encoded = port_encoder.transform(test_data[:, 2])  # Encoding untuk source_port

        # Gabungkan atribut yang telah di-encode dengan atribut numerik lainnya
        test_data_encoded = np.column_stack((source_ip_test_encoded, destination_ip_test_encoded, port_test_encoded, test_data[:, 3], protocol_test_encoded, test_data[:, 5], test_data[:, 6], flag_packet_test_encoded, data_payload_test_encoded))

        # Pastikan data uji memiliki bentuk 2D yang sesuai dengan data latih
        test_data_encoded = test_data_encoded.reshape(-1, test_data_encoded.shape[1])

        # Lakukan prediksi pada data uji
        predictions = model.predict(test_data_encoded)

        # Simpan hasil prediksi ke dalam database atau tampilkan pada halaman index.html
        save_results(predictions)

        result = {"message": "Deteksi selesai", "predictions": predictions.tolist()}
        return JsonResponse(result)
    else:
        datas = Data.objects.all()
        return render(request, "app/index.html", {"datas": datas})