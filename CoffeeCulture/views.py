from django.shortcuts import render,HttpResponse,redirect
from .models import signupMaster,notes
from .forms import signupform, notesform
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
import random
import requests
import json



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
                # mention url
                url = "https://www.fast2sms.com/dev/bulk"


                # create a dictionary
                my_data = {
                    # Your default Sender ID
                    'sender_id': 'FSTSMS',
                    
                    # Put your message here!
                    'message': 'your OTP is {otp}',
                    
                    'language': 'english',
                    'route': 'p',
                    
                    # You can send sms to multiple numbers
                    # separated by comma.
                    'numbers': '6356633872,7016210249,'	
                }

                # create a dictionary
                headers = {
                    'authorization': 'CeO7nS0PXIzsUgKT51yduojJ8QF3aEmGW4frwL9AhBbZV2HNRq8Wg1XshciEb3NqAFO2Qy4YJrflDBCV',
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache"
                }

                # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
                #load json data from source
                returned_msg = json.loads(response.text)

                # print the send message
                print(returned_msg['message'])

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
