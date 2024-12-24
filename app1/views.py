from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
# Create your views here.
def register(request):
    if(request.method=='POST'):
        firstname=request.POST['Firstname']
        lastname=request.POST['Lastname']
        username=request.POST['Username']
        password=request.POST['Password']
        email=request.POST['Email']
        confirmpassword=request.POST['Confirm_password']
        error={}
        if User.objects.filter(username=username).exists():
            error['username']='username already exists'
        if (password!=confirmpassword):
            error['password']='Enter correct password'
        if error:
            return render(request,'register.html',{'error':error})
        user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,password=password,email=email)
        user.save()
        acc=account(username=username,first_name=firstname,last_name=lastname,email=email,account_balance=0)
        acc.save()
        with open('template/account_creation_success.html','r')as file:
            html_content=file.read()
            html_content=html_content.replace("[User's Email]",email)
            html_content=html_content.replace('{username}',username)
        subject='Account Created Succcessfully'
        from_email=settings.EMAIL_HOST_USER
        recipitent_list=[email]
        email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipitent_list)
        email_account_creation.attach_alternative(html_content,"text/html")
        email_account_creation.send()

        return redirect('/registersuccess/')
    return render(request,'register.html')

def loginpage(request):
    if(request.method=='POST'):
        username=request.POST['Username']
        password=request.POST['Password']
        user=auth.authenticate(username=username,password=password)
        error={}
        if(user is None):
            error['username']='Username does not exist'
            return render(request,'loginpage.html',{'error':error})
        auth.login(request,user)
        return redirect('/loginsuccess/')
    return render(request,'loginpage.html')
    
def homepage(request):
    return render(request,'homepage.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def lobby(request):
    if request.user.is_authenticated:
        return render(request,'lobby.html')
    return redirect('/loginpage/')


def deposite(request):
    Account=account.objects.get(username=request.user.username)
    if request.method =='POST':
        amount=request.POST['amount']
        Account.account_balance+=int(amount)
        Account.save()
        trans=transaction(transaction_type='deposite',main_user_name=request.user.username,sender_user_name='system',amount_deducted=amount,amount_recieved=amount,reciever_name=request.user.username,balance=Account.account_balance)
        trans.save()
        with open('template/account_deposit_success.html','r')as file:
            html_content=file.read()
            html_content=html_content.replace('{username}',request.user.username)
            html_content=html_content.replace('{amount}',amount)
        subject='Amount Deposited Succcessfully'
        from_email=settings.EMAIL_HOST_USER
        recipitent_list=[Account.email]
        email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipitent_list)
        email_account_creation.attach_alternative(html_content,"text/html")
        email_account_creation.send()
        return redirect('/depositesuccess/')
    return render(request,'deposite.html')

def withdraw(request):
    Account=account.objects.get(username=request.user.username)
    if request.method =='POST':
        amount=request.POST['amount']
        Account.account_balance-=int(amount)
        Account.save()
        trans=transaction(transaction_type='withdraw',main_user_name=request.user.username,sender_user_name=request.user.username,amount_deducted=amount,amount_recieved=amount,reciever_name='system',balance=Account.account_balance)
        trans.save()
        with open('template/account_withdraw_success.html','r')as file:
            html_content=file.read()
            html_content=html_content.replace('{username}',request.user.username)
            html_content=html_content.replace('{amount}',amount)
        subject='Amount Withdrawn Succcessfully'
        from_email=settings.EMAIL_HOST_USER
        recipitent_list=[Account.email]
        email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipitent_list)
        email_account_creation.attach_alternative(html_content,"text/html")
        email_account_creation.send()
        return redirect('/withdrawsuccess/')

    
    return render(request,'withdraw.html')  

def sendmoney(request):
    non_staff_users=User.objects.filter(is_staff=False).exclude(username=request.user.username)
    if request.method=='POST':
        recipient_username=request.POST['recipient']
        amount=request.POST['amount']
        sender=account.objects.get(username=request.user.username)
        recipient=account.objects.get(username=recipient_username)
        if int(amount)<=sender.account_balance:
            sender.account_balance-=int(amount)
            sender.save()
            recipient.account_balance+=int(amount)
            recipient.save()
            trans=transaction(transaction_type='Send Money',main_user_name=sender.username,sender_user_name=sender.username,amount_deducted=amount,amount_recieved=amount,reciever_name=recipient.username,balance=sender.account_balance)
            trans.save()
            with open('template/account_sender_success.html','r')as file:
                html_content=file.read()
                html_content=html_content.replace('{sender_user_name}',sender.username)
                html_content=html_content.replace('{receiver_name}',recipient.username)
                html_content=html_content.replace('{amount}',amount)
                html_content=html_content.replace('{receiver_email}',recipient.email)
            subject='Account Sended Succcessfully'
            from_email=settings.EMAIL_HOST_USER
            recipitent_list=[sender.email]
            email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipitent_list)
            email_account_creation.attach_alternative(html_content,"text/html")
            email_account_creation.send()
            
            trans=transaction(transaction_type='Send Money',main_user_name=recipient.username,sender_user_name=sender.username,amount_deducted=amount,amount_recieved=amount,reciever_name=recipient.username,balance=recipient.account_balance)
            trans.save()
            with open('template/account_receiver_success.html','r')as file:
                html_content=file.read()
                html_content=html_content.replace('{sender_user_name}',sender.username)
                html_content=html_content.replace('{receiver_name}',recipient.username)
                html_content=html_content.replace('{amount}',amount)
                html_content=html_content.replace('{sender_email}',sender.email)
            subject='Account Recevide Succcessfully'
            from_email=settings.EMAIL_HOST_USER
            recipitent_list=[recipient.email]
            email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipitent_list)
            email_account_creation.attach_alternative(html_content,"text/html")
            email_account_creation.send()
            return redirect('/sendmoneysuccess/')
        else:
            error={}
            error['error']='In Sufficent Balance'
            return render(request,'sendmoney.html',{'error':error})

        
    return render(request,'sendmoney.html',{'non_staff_users':non_staff_users})

def transcation(request):
    trans=transaction.objects.filter(main_user_name=request.user.username)
    return render(request,'transcation.html',{'trans':trans})

def registersuccess(request):
    return render(request,'registersuccess.html')

def loginsuccess(request):
    return render(request,'loginsuccess.html')

def depositesuccess(request):
    return render(request,'depositesuccess.html')

def withdrawsuccess(request):
    return render(request,'withdrawsuccess.html')

def sendmoneysuccess(request):
    return render(request,'sendmoneysuccess.html')
