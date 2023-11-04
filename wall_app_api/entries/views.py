from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Entry
from .serializers import EntrySerializer, EntryListSerializer
from ..common.permissions import IsOwnerOrReadOnly


class EntryListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Entry.objects.all().order_by('-created_at')
    serializer_class = EntryListSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EntryCreateView(generics.CreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntryDetailViewSet(viewsets.GenericViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
