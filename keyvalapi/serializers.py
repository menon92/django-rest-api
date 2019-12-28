from rest_framework import serializers
from .models import KeyValStore


class KeyValStoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KeyValStore
        fields = ['id', 'url', 'key', 'value', 'ttl']