from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Board, Column

class KanbanTests(APITestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='micaela', password='password123')
        self.user2 = User.objects.create_user(username='hacker', password='password123')
        self.board_url = '/api/boards/'

    # --- TESTS UNITARIOS ---

    def test_crear_tablero(self):
        board = Board.objects.create(owner=self.user1, name="Proyecto")
        self.assertEqual(str(board), "Proyecto")

    # --- TESTS DE INTEGRACIÓN (API) ---

    def test_crear_tablero_sin_autenticacion_falla(self):
        data = {'name': 'Tablero Secreto'}
        response = self.client.post(self.board_url, data)
      
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # verificamos que no se guardó nada en la base de datos
        self.assertEqual(Board.objects.count(), 0)


    def test_crear_tablero_autenticado_asigna_owner(self):
        """
        Verifica que al mandar un POST válido, se crea el tablero y se le asigna 
        automáticamente el usuario logueado como dueño
        """
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'name': 'Mi Primer Tablero',
            'description': 'Probando testing en Django'
        }
        response = self.client.post(self.board_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
      
        nuevo_tablero = Board.objects.get()
        self.assertEqual(nuevo_tablero.owner, self.user1)

    def test_aislamiento_de_datos_get_boards(self):
        """
        Un usuario solo debe recibir SUS tableros, nunca los de otro usuario
        """
        Board.objects.create(owner=self.user1, name="Tablero de Micaela")
        Board.objects.create(owner=self.user2, name="Tablero de Hacker")

        self.client.force_authenticate(user=self.user1)    
        response = self.client.get(self.board_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Tablero de Micaela")