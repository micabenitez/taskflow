from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Board, Column, Card
from .serializers import BoardSerializer, ColumnSerializer, CardSerializer

class SoftDeleteViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class BoardViewSet(SoftDeleteViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ColumnViewSet(SoftDeleteViewSet):
    queryset = Column.objects.all() 
    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

class CardViewSet(SoftDeleteViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]