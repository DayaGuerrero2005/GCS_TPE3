from django import forms

from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Nueva tarea"}),
            "descripcion": forms.Textarea(attrs={"rows": 2, "placeholder": "Descripción (opcional)"}),
        }
