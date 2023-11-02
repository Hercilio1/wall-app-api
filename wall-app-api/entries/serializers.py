from rest_framework import serializers
from .models import Entry
from ..users.serializers import UserSerializer


class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'user', 'content', 'created_at']

    def to_representation(self, instance):
        data = super(EntrySerializer, self).to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data


class EntryListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Entry
        fields = '__all__'
