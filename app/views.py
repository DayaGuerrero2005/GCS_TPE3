from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TareaForm
from .models import Tarea


def lista_tareas(request):
    form = TareaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lista_tareas")
    tareas = Tarea.objects.all()
    contexto = {
        "form": form,
        "tareas": tareas,
        "pendientes": tareas.filter(completada=False).count(),
    }
    return render(request, "app/lista.html", contexto)


@require_POST
def alternar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completada = not tarea.completada
    tarea.save(update_fields=["completada"])
    return redirect("lista_tareas")


def health(request):
    """Endpoint que usa el pipeline para validar el despliegue."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({
        "estado": "ok",
        "version": settings.APP_VERSION,
        "base_de_datos": connection.vendor,
    })
