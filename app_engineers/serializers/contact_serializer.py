from rest_framework import serializers
from app_engineers.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'is_active',
            'person',
            'cellphone',
            'email',
            'address',
            'is_main',
            'use'
        ]
        read_only_fields = ['id', 'is_active']
