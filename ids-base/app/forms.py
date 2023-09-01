from django import forms
from app.models import Data

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = [
            "ip_source",
            "ip_destination",
            "port",
            "agent",
            "datasource",
            "created_at",
            "updated_at",
        ]
        widgets = {
            "ip_source": forms.TextInput(attrs={"class": "form-control"}),
            "ip_destination": forms.TextInput(attrs={"class": "form-control"}),
            "port": forms.TextInput(attrs={"class": "form-control"}),
            "agent": forms.TextInput(attrs={"class": "form-control"}),
            "datasource": forms.TextInput(attrs={"class": "form-control"}),
            "created_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "updated_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
