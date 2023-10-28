from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Entry
from .serializers import EntrySerializer
from ..common.permissions import IsOwnerOrReadOnly


class EntryListCreateViewSet(viewsets.GenericViewSet, generics.ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsOwnerOrReadOnly]


class EntryDetailViewSet(viewsets.GenericViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]
