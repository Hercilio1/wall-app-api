from rest_framework import serializers
from .models import Entry
from ..users.serializers import UserSerializer


class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Entry
        fields = '__all__'
