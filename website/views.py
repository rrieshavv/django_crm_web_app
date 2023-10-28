from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Record

def home(request):

    records = Record.objects.all()

    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in!")
            return redirect('home')
        else:
            messages.success(
                request, "There was an error logging in. Try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out ...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        username =  request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email_address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # validation check: exisiting user name
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'register.html')
        # validation check: password do not match
        if password1 != password2:
            messages.error(request,  "Passwords do not match.")
            return render(request, 'register.html')
        #validation check: length of password
        if len(password1)<8:
            messages.error(request,"Password must contain atleast 8 letters.")
            return render(request,'register.html')
        
        #if all validation checks pass
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        #logging user in after registration
        user = authenticate(username=username, password=password1)
        login(request, user)
        messages.success(request,"You have succesfully registered.")
        return redirect('home')
    
    return render(request, 'register.html')

        

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html',{'customer_record':customer_record})
    else:
        messages.error(request,"You must be logged in to view this page.")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('home')
    else:
        messages.error(request,"You must be logged in to delete a record.")
        return redirect('home')
    
def add_record(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email =  request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            city = request.POST['city']
            state=  request.POST['state']
            zipcode = request.POST['zipcode']

            if not (firstname and lastname and email and phone and address and city and state and zipcode):
                messages.error(request, "Empty fields found! Try again.")
                return render(request, 'add_record.html')
            
            new_record = Record(
                first_name=firstname,
                last_name = lastname,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode
            )

            new_record.save()
            messages.success(request, 'New record has been added!')
            return redirect('home')

        return render(request, 'add_record.html',{})
    else:
        messages.success(request, "Log in to add a record!")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        if request.method == "POST":
            #retrieving values
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email =  request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            city = request.POST['city']
            state=  request.POST['state']
            zipcode = request.POST['zipcode']

            #validation checks
            if not(firstname and lastname and email and phone and address and city and state and zipcode):
                messages.error(request,"Can't update the record with the info you submitted. Try again!")
                return render(request, 'update_record.html', {'record':record})
            #updating values
            record.first_name = firstname
            record.last_name = lastname
            record.email = email
            record.phone = phone
            record.address = address
            record.city=city
            record.state=state
            record.zipcode=zipcode
            record.save()

            messages.success(request, "Record updated!")
            return redirect('home')
                
        else:
            return render(request, 'update_record.html', {'record':record})
    else:
        messages.error(request, "You must be logged in to update a record.")
        return redirect('home')