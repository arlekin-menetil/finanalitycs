from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from accounts.models import BankAccount
from transactions.models import Transaction, LedgerEntry


class InsufficientFunds(Exception):
    pass


class InvalidAccount(Exception):
    pass


def get_account_balance(account: BankAccount) -> Decimal:
    credits = account.ledger_entries.filter(
        entry_type="credit"
    ).aggregate(Sum("amount"))["amount__sum"] or Decimal("0")

    debits = account.ledger_entries.filter(
        entry_type="debit"
    ).aggregate(Sum("amount"))["amount__sum"] or Decimal("0")

    return credits - debits


@transaction.atomic
def transfer_funds(from_account_id, to_account_id, amount: Decimal):

    if amount <= 0:
        raise ValueError("Amount must be positive")

    # 🔒 Блокируем строки (защита от race condition)
    accounts = BankAccount.objects.select_for_update().filter(
        id__in=[from_account_id, to_account_id],
        is_active=True
    )

    if accounts.count() != 2:
        raise InvalidAccount("One of the accounts is invalid or inactive")

    from_account = next(acc for acc in accounts if acc.id == from_account_id)
    to_account = next(acc for acc in accounts if acc.id == to_account_id)

    # 💰 Проверка баланса
    current_balance = get_account_balance(from_account)

    if current_balance < amount:
        raise InsufficientFunds("Not enough balance")

    # 🧾 Создаём транзакцию
    tx = Transaction.objects.create(
        from_account=from_account,
        to_account=to_account,
        amount=amount,
        status="pending"
    )

    # 📉 Debit
    LedgerEntry.objects.create(
        account=from_account,
        transaction=tx,
        entry_type="debit",
        amount=amount
    )

    # 📈 Credit
    LedgerEntry.objects.create(
        account=to_account,
        transaction=tx,
        entry_type="credit",
        amount=amount
    )

    tx.status = "completed"
    tx.save()

    return tx