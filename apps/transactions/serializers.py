from rest_framework import serializers
from apps.transactions.models import Transfer
from apps.accounts.models import Account
from utils.validators import validate_currency

class TransferSerializer(serializers.ModelSerializer):
    from_account_id = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    to_account_id = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    currency = serializers.CharField(validators=[validate_currency], write_only=True)

    class Meta:
        model = Transfer
        fields = ['id', 'from_account_id', 'to_account_id', 'amount', 'currency', 'created_at']
        read_only_fields = ['id', 'created_at']
