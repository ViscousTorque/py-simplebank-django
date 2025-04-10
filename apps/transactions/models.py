from django.db import models
from apps.accounts.models import Account


class Entry(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="entries"
    )
    amount = models.BigIntegerField(help_text="Can be negative or positive")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry {self.id} - {self.amount}"


class Transfer(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_account_id = models.ForeignKey(
        Account,
        to_field="id",
        db_column="from_account_id",
        on_delete=models.CASCADE,
        related_name="outgoing_transfers",
    )
    to_account_id = models.ForeignKey(
        Account,
        to_field="id",
        db_column="to_account_id",
        on_delete=models.CASCADE,
        related_name="incoming_transfers",
    )
    amount = models.BigIntegerField(help_text="Must be positive")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer {self.id}: {self.from_account_id} -> {self.to_account_id} : {self.amount}"
