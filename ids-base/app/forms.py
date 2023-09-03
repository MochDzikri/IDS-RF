from django import forms
from .models import Data

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = [
            "source_ip",
            "destination_ip",
            "source_port",
            "destination_port",
            "protocol",
            "packet_length",
            "timestamp",  # Memungkinkan input timestamp dalam format float
            "flag_packet",
            "data_payload",
            "label",
        ]
        widgets = {
            "source_ip": forms.TextInput(attrs={"class": "form-control"}),
            "destination_ip": forms.TextInput(attrs={"class": "form-control"}),
            "source_port": forms.TextInput(attrs={"class": "form-control"}),
            "destination_port": forms.TextInput(attrs={"class": "form-control"}),
            "protocol": forms.TextInput(attrs={"class": "form-control"}),
            "packet_length": forms.TextInput(attrs={"class": "form-control"}),
            "timestamp": forms.TextInput(attrs={"class": "form-control"}),  # Tetap menggunakan TextInput
            "flag_packet": forms.TextInput(attrs={"class": "form-control"}),
            "data_payload": forms.Textarea(attrs={"class": "form-control"}),
            "label": forms.TextInput(attrs={"class": "form-control"}),
        }
