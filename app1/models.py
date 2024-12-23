from django.db import models
# Create your models here.
class account(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=20)
    username=models.CharField(max_length=30)
    account_balance=models.IntegerField()
    email=models.CharField(max_length=40)

class transaction(models.Model):
    transaction_type=models.CharField(max_length=50)
    main_user_name=models.CharField(max_length=20)
    sender_user_name=models.CharField(max_length=30)
    amount_deducted=models.IntegerField()
    time_of_transaction=models.DateTimeField(auto_now_add=True)
    reciever_name=models.CharField(max_length=30)
    amount_recieved=models.IntegerField()
    balance=models.IntegerField()
    
