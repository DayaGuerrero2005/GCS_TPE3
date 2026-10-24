from django.test import TestCase
from django.urls import reverse

from .models import Tarea


class TareaModelTests(TestCase):
    def test_tarea_nueva_inicia_pendiente(self):
        tarea = Tarea.objects.create(titulo="Configurar CI")
        self.assertFalse(tarea.completada)
        self.assertEqual(str(tarea), "Configurar CI")

    def test_orden_pendientes_primero(self):
        Tarea.objects.create(titulo="Hecha", completada=True)
        Tarea.objects.create(titulo="Pendiente")
        self.assertEqual(Tarea.objects.first().titulo, "Pendiente")


class TareaViewTests(TestCase):
    def test_lista_responde_200(self):
        respuesta = self.client.get(reverse("lista_tareas"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Gestor de tareas")

    def test_crear_tarea_por_formulario(self):
        respuesta = self.client.post(reverse("lista_tareas"), {"titulo": "Crear Dockerfile"})
        self.assertRedirects(respuesta, reverse("lista_tareas"))
        self.assertTrue(Tarea.objects.filter(titulo="Crear Dockerfile").exists())

    def test_titulo_vacio_no_se_guarda(self):
        self.client.post(reverse("lista_tareas"), {"titulo": ""})
        self.assertEqual(Tarea.objects.count(), 0)

    def test_alternar_estado(self):
        tarea = Tarea.objects.create(titulo="Desplegar")
        self.client.post(reverse("alternar_tarea", args=[tarea.pk]))
        tarea.refresh_from_db()
        self.assertTrue(tarea.completada)

    def test_alternar_solo_acepta_post(self):
        tarea = Tarea.objects.create(titulo="Desplegar")
        respuesta = self.client.get(reverse("alternar_tarea", args=[tarea.pk]))
        self.assertEqual(respuesta.status_code, 405)

    def test_health_reporta_estado(self):
        respuesta = self.client.get(reverse("health"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["estado"], "ok")
