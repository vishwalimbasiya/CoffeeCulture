from django.shortcuts import render,HttpResponse,redirect
from .models import signupMaster,notes
from .forms import signupform, notesform
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
import random
from twilio.rest import Client

# Create your views here.

def index(request):
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            signupfrm=signupform(request.POST)
            if signupfrm.is_valid():
                signupfrm.save()
                print("Signup Successfully!")

                otp=random.randint(1111, 9999)
                #send mail
                sub="Success"
                msg=f"Hello user,\n your account has been created Successfully,\n your one time password is{otp},\From CoffeeCulture,\n+91 6356633872 | vishwalimbasiya18@gmail.com"
                email_from = settings.EMAIL_HOST_USER
                to_email=['krutidhinoja@gmail.com','patelvishva2001@gmail.com']
                send_mail(sub,msg,email_from,to_email)

                #send message
                client = Client('ACf33c61cd4639b66c052f41ffaf57be62', '1838ed7510903a8617ea0597ad84d7ac')

                message = client.messages \
                .create(
                     body=f"Hello user,\n your account has been created Successfully,\n your one time password is{otp},\From CoffeeCulture",
                     from_='+18317049051',
                     to='+916356633872'
                 )

                print(message.sid)
                
                return redirect('notes')
            else:
                print(signupfrm.errors)
        
        elif request.POST.get('login')=='login':
            unm=request.POST['email']
            pas=request.POST['password']
            userid=signupMaster.objects.get(password=pas)
            print("Userid:", userid.id)
            user=signupMaster.objects.filter(email=unm,password=pas)
            if user:
                print('Login Successfully!')
                request.session['user']=unm
                request.session['userid']=userid.id
                return redirect('notes')
            else:
                print("Error...Login Fail!")
    return render(request,'index.html')

def profile (request):
    user=request.session.get('user')
    userid=request.session.get('userid')
    id=signupMaster.objects.get(id=userid)
    if request.method=="POST":
        signupfrm=signupform(request.POST)
        if signupfrm.is_valid():
            signupfrm=signupform(request.POST,instance=id)
            signupfrm.save()
            print("your profile has been updated!")
            return redirect('notes')
        else:
            print(signupfrm.errors)
    return render(request, 'profile.html',{'user':user, 'userid':signupMaster.objects.get(id=userid)})
    

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def menu(request):
    return render(request, 'menu.html')

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        notesfrm=notesform(request.POST, request.FILES)
        if notesfrm.is_valid():
            notesfrm.save()
            print("File Uploaded Successfully")
            return redirect('notes')
        else:
            print(notesfrm.errors)
    else:
        notesfrm=notesform()
    return render(request, 'notes.html', {'user':user})

def userlogout(request):
    logout(request)
    return render(request, 'index.html')
