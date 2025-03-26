from rest_framework import serializers
from apps.accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owner', 'balance', 'currency', 'created_at']
        read_only_fields = ['id', 'owner', 'balance', 'created_at']
