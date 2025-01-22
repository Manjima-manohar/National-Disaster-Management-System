from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Camp,Person_missing,Vehicle_management,Police_station,volunteer_camp_allocation,Insurance,Public,Fund_request,Rescue
from status.models import Make_alert
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from datetime import datetime
# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def user_login(request):
    return render(request,'login.html')

@login_required(login_url='login')
def public_vehicle_management(request):
    insurance=Insurance.objects.all()
    return render(request,'public/public-vehicle-mngt.html',{"insurance":insurance})

@login_required(login_url='login')
def public_dashboard(request):
     # Get the username of the logged-in user
    username = request.user.username
    
    try:
        # Get the Public instance for the logged-in user
        public_user = Public.objects.get(user=request.user)
        user_state = public_user.state
        
        # Count Make_alert entries where the created_by user's state matches the user's state
        notification_count = Make_alert.objects.filter(
            created_by__policestation_profile__state=user_state
        ).count()
        
    except Public.DoesNotExist:
        # Handle cases where Public profile does not exist
        notification_count = 0

    context = {
        'username': username,
        'notification_count': notification_count,
    }
    return render(request,'public/public-dashboard.html',context)

def public_register(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirmpassword')
        try:
            if password==confirm_password:
                #create user accounts
                user=User.objects.create_user(username=username,password=password)
                # success_message="Registration Completed"
                # messages.success(request,success_message)
                return redirect('public-login')
            else:
                error_message="Invalid Password"
                messages.error(request,error_message)
        except Exception as e:
            print(e)
            error_message="Duplicate username or invalid data"
            messages.error(request,error_message)
    return render(request, 'Registration/public-register.html')


def public_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('public-dashboard')  
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
            # Add more redirects for other user types
    return render(request,'signin/public-login.html')



def camp_details(request):
    if request.method == 'POST':
        camp_name = request.POST.get('name')
        email= request.POST.get('email')
        place = request.POST.get('place')
        district = request.POST.get('district')
        phone = request.POST.get('phone')
        camp_head = request.POST.get('camp_head')

        # Create a new Camp instance
        camp = Camp.objects.create(
            camp_name=camp_name,
            place=place,
            district=district,
            phone=phone,
            camp_head=camp_head,
            user=request.user,
            email=email
        )
        camp.save()
        return redirect('index')  # Redirect to the appropriate URL after saving
    
    # For GET requests or if form submission fails
     # Get the email of the logged-in user
    return render(request, 'camp_details.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def public_registration(request):
    if request.method == "POST":
        state = request.POST.get('state')
        dob = request.POST.get('dob')
        try:
            public_user = Public.objects.get(user=request.user)
        except Public.DoesNotExist:
            # If the Public instance doesn't exist, create a new one
            public_user = Public(user=request.user)

        # Update the Public instance with form data
        public_user.first_name = request.POST.get('firstname', public_user.first_name)
        public_user.last_name = request.POST.get('lastname', public_user.last_name)
        #public_user.dob = request.POST.get('dob', public_user.dob)
        public_user.address = request.POST.get('address', public_user.address)
        public_user.blood_group = request.POST.get('blood_group', public_user.blood_group)
        public_user.email = request.POST.get('email', public_user.email)
        public_user.phone = request.POST.get('phone', public_user.phone)
        public_user.gender = request.POST.get('gender', public_user.gender)
        public_user.occupation = request.POST.get('occupation', public_user.occupation)
        public_user.father_name = request.POST.get('father_name', public_user.father_name)
        public_user.mother_name = request.POST.get('mother_name', public_user.mother_name)
        public_user.state = state
        public_user.district = request.POST.get('district', public_user.district)
        public_user.photo = request.FILES.get('photo', public_user.photo)
        if dob:
            try:
                public_user.dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format
                return render(request, 'public/public-camp-allocation.html', {
                    'public': public_user,
                    'camps': Camp.objects.filter(state=state) if state else None,
                    'error': 'Date of birth must be in YYYY-MM-DD format.'
                })
        else:
            public_user.dob = None  # or handle as needed
        public_user.save()

        # After saving the state, check if the camp name is being selected
        camp_name = request.POST.get('camp_name')
        if camp_name:
            camp = Camp.objects.get(id=camp_name)
            public_user.camp_name = camp
            public_user.save()
            return redirect('public-dashboard')

        # If no camp is selected yet, filter camps based on the state
        camps = Camp.objects.filter(state=state) if state else None

        return render(request, 'public/public-camp-allocation.html', {
            'public': public_user,
            'camps': camps,
        })

    # If the request is not POST, just render the form
    try:
        public_user = Public.objects.get(user=request.user)
    except Public.DoesNotExist:
        public_user = None  # Handle the case where the user hasn't registered yet

    return render(request, 'public/public-camp-allocation.html', {'public': public_user})


    
@login_required(login_url='login')
def public_profile(request):
    user = request.user  # Fetch the current logged-in user
    public = Public.objects.filter(user=user)  # Filter data based on the user  
    if not public.exists():
         context = {'no_public_data': True,'user':user}
    else:
        context = {'campallocations': public,'user':user}
    return render(request, 'public/public-profile.html',context)


@login_required(login_url='login')
def person_missing(request):
    if request.method == 'POST' and request.FILES['photo']:
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        address = request.POST.get('address', 'Unknown') 
        dob = request.POST.get('dob')
        blood_group = request.POST.get('blood_group')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        state = request.POST.get('state')
        district = request.POST.get('district')
        photo=request.FILES['photo']
        # Create a new Camp instance
        personmissing = Person_missing(
            firstname=first_name,
            last_name=last_name,
            address=address,
            dob=dob,
            blood_group=blood_group,
            gender=gender,
            occupation=occupation,
            father_name=father_name,
            mother_name=mother_name,          
            photo=photo,
            district=district,
            state=state,
            created_by=request.user,
            status=Person_missing.SEARCHING
        )
        personmissing.save()
        return render(request, 'public/public-dashboard.html')
    return render(request, 'public/public-person-missing.html')



@login_required(login_url='login')
def public_vehicle_damage(request):
     if request.method == 'POST':
        reg_no=request.POST.get('reg_no')
        ower_name=request.POST.get('ower_name')
        license_no = request.POST.get('license_no')
        vehicle_model = request.POST.get('vehicle_model')
        fuel_type = request.POST.get('fuel_type')
        district = request.POST.get('district')
        state = request.POST.get('state')
        company_id = request.POST.get('company_name')
        rc_photo = request.POST.get('rc_photo')
        licence_photo = request.POST.get('licence_photo')
        vehicle_photo = request.POST.get('vehicle_photo')
        issue = request.POST.get('issue')
        ins=Insurance.objects.get(id=company_id)
        # Create a new Camp instance
        vehicledamage =Vehicle_management.objects.create(
            reg_no=reg_no,
            owner_name=ower_name,
            license_no=license_no,
            make_model=vehicle_model,
            fuel_type=fuel_type,
            district=district,
            state=state,
            company_name=ins,
            rc_book=rc_photo,
            license_image=licence_photo,          
            vehicle_image=vehicle_photo,
            created_by=request.user,
            issue=issue,
            status=Vehicle_management.PENDING

        )
        vehicledamage.save()
        return redirect("public-dashboard")
     


@login_required(login_url='public-login')
def public_vehicle_missing(request):
     if request.method == 'POST':
        reg_no=request.POST.get('reg_no')
        ower_name=request.POST.get('ower_name')
        license_no = request.POST.get('license_no')
        vehicle_model = request.POST.get('vehicle_model')
        fuel_type = request.POST.get('fuel_type')
        district = request.POST.get('district')
        state = request.POST.get('state')
        rc_photo = request.POST.get('rc_photo')
        licence_photo = request.POST.get('licence_photo')
        vehicle_photo = request.POST.get('vehicle_photo')
        issue = request.POST.get('issue')
        
        # Create a new Camp instance
        vehiclemissing =Vehicle_management.objects.create(
            reg_no=reg_no,
            owner_name=ower_name,
            license_no=license_no,
            make_model=vehicle_model,
            fuel_type=fuel_type,
            district=district,
            state=state,
            rc_book=rc_photo,
            license_image=licence_photo,          
            vehicle_image=vehicle_photo,
            created_by=request.user,
            issue=issue,
            status=Vehicle_management.SEARCHING
        )
        vehiclemissing.save()
        return redirect("public-dashboard")


def camp_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        campname = request.POST.get('campname')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        state = request.POST.get('state')
        camp_head = request.POST.get('camp_head')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password!=confirm_password:
            error_message="Password do NOT match"
            messages.error(request,error_message)
        else:
            try:
                # Create the user account
                user = User.objects.create_user(username=username, password=password)
                 # Create a customer account
                camp_obj =user= Camp.objects.create(camp_name=campname,email=email,user=user,place=place,phone=phone,district= district,camp_head=camp_head,state=state)
                camp_obj.save()
                return redirect('camp-login')
            except Exception as e:
                print(e)
                error_message="Duplicate username or invalid inputs"
                messages.error(request,error_message)
    return render(request,'registration/camp-register.html')


def camp_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('camp-dashborad')
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
            # Add more redirects for other user types
    return render(request,'signin/camp-login.html')

@login_required(login_url='login')
def camp_dashborad(request):
    camp = get_object_or_404(Camp, user=request.user)
     # Get the username of the logged-in user
    username = request.user.username
    
    try:
        # Get the Public instance for the logged-in user
        camp_user = Camp.objects.get(user=request.user)
        user_state = camp_user.state
        
        # Count Make_alert entries where the created_by user's state matches the user's state
        notification_count = Make_alert.objects.filter(
            created_by__policestation_profile__state=user_state
        ).count()
        
    except Public.DoesNotExist:
        # Handle cases where Public profile does not exist
        notification_count = 0

    context = {
        'username': username,
        'notification_count': notification_count,
        'camp':camp
    }
    
    return render(request,'camp/camp-dashboard.html',context)

def policestation_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        policestation_name = request.POST.get('policestation_name')
        location = request.POST.get('location')
        district = request.POST.get('district')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password!=confirm_password:
            error_message="Password do NOT match"
            messages.error(request,error_message)
        else:
            try:
                # Create the user account
                user = User.objects.create_user(username=username, password=password)
                 # Create a customer account
                pstation_obj=user= Police_station.objects.create(policestation_name=policestation_name,email=email,user=user,location=location,district=district,phone=phone,state=state)
                pstation_obj.save()
                return redirect('policestation-login')
            except Exception as e:
                print(e)
                error_message="Duplicate username or invalid inputs"
                messages.error(request,error_message)
    return render(request,'registration/police-register.html')


def policestation_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('policestation-dashboard')
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
            # Add more redirects for other user types
    return render(request,'signin/police-login.html')

@login_required(login_url='login')
def policestation_dashboard(request):
    return render(request,'police/police-dashboard.html')

def volunteer_register(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        try:
            if password==confirm_password:
                #create user accounts
                user=User.objects.create_user(username=username,password=password)
                # success_message="Registration Completed"
                # messages.success(request,success_message)
                return redirect('volunteer-login')
            else:
                error_message="Invalid Password"
                messages.error(request,error_message)
        except Exception as e:
            print(e)
            error_message="Duplicate username or invalid data"
            messages.error(request,error_message)
    return render(request,'registration/volunteer-register.html')

def volunteer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('volunteer-dashboard')
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
            # Add more redirects for other user types
    return render(request,'signin/volunteer-login.html')

@login_required(login_url='login')
def volunteer_dashboard(request):
    username = request.user.username
    return render(request,'volunteer/volunteers-dashboard.html',{'username':username})

@login_required(login_url='login')
def volunteer_camp_allocations(request):
    if request.method == "POST":
        state = request.POST.get('state')
        print(state)
        try:
            volunteer= volunteer_camp_allocation.objects.get(user=request.user)
        except volunteer_camp_allocation.DoesNotExist:
            # If the Public instance doesn't exist, create a new one
            volunteer= volunteer_camp_allocation(user=request.user)

        # Update the Public instance with form data
        volunteer.first_name = request.POST.get('firstname', volunteer.first_name)
        volunteer.last_name = request.POST.get('lastname', volunteer.last_name)
        age = request.POST.get('age')
        if age and age.isdigit():  # Check if age is provided and is a valid integer
            volunteer.age = int(age)
        else:
            volunteer.age = None 
        volunteer.address = request.POST.get('address', volunteer.address)
        volunteer.blood_group = request.POST.get('blood_group', volunteer.blood_group)
        volunteer.email = request.POST.get('email', volunteer.email)
        volunteer.phone = request.POST.get('phone', volunteer.phone)
        volunteer.gender = request.POST.get('gender', volunteer.gender)
        volunteer.state = state
        volunteer.district = request.POST.get('district', volunteer.district)
        volunteer.photo = request.FILES.get('photo', volunteer.photo)
        if volunteer.age is not None and volunteer.age >= 18:
            volunteer.save()
        elif volunteer.age is None:
            volunteer.save()
            # return render(request, 'volunteer/volunteers-camp-allocation.html', {
            #     'volunteer': volunteer,
            # })
        else:
            messages.error(request, "No one under 18 is permitted.")
            return render(request, 'volunteer/volunteers-camp-allocation.html', {
                'volunteer': volunteer,
                })
    
        # After saving the state, check if the camp name is being selected
        camp_name = request.POST.get('camp_name')
        print("camp",camp_name)
        if camp_name:
            camp = Camp.objects.get(id=camp_name)
            volunteer.camp_name = camp
            volunteer.save()
            return redirect('volunteer-dashboard')

        # If no camp is selected yet, filter camps based on the state
        camps = Camp.objects.filter(state=state) if state else None
        for camp in camps:
            print("Camp Name:", camp.camp_name)
        return render(request, 'volunteer/volunteers-camp-allocation.html', {
            'volunteer': volunteer,
            'camps': camps,
        })

    # If the request is not POST, just render the form
    try:
        volunteer = volunteer_camp_allocation.objects.get(user=request.user)
    except volunteer_camp_allocation.DoesNotExist:
        volunteer = None  # Handle the case where the user hasn't registered yet
    return render(request,'volunteer/volunteers-camp-allocation.html',{'volunteer':volunteer})

  
def insurance_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')      
        campany_name = request.POST.get('campany_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        state = request.POST.get('state')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password!=confirm_password:
            error_message="Password do NOT match"
            messages.error(request,error_message)
        else:
            try:
                # Create the user account
                user = User.objects.create_user(username=username, password=password)
                 # Create a customer account
                insurance_obj=user= Insurance.objects.create(company_name=campany_name,email=email,user=user,phone=phone,district=district,state=state)
                insurance_obj.save()
                return redirect('insurance-login')
            except Exception as e:
                print(e)
                error_message="Duplicate username or invalid inputs"
                messages.error(request,error_message)
    return render(request,'registration/insurance-register.html')

def insurance_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('insurance-dashboard')
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
    return render(request,'signin/insurance-login.html')

@login_required(login_url='login')
def insurance_dashboard(request):
    insurance = get_object_or_404(Insurance, user=request.user)
    return render(request,'insurance/insurance-dashboard.html',{'insurance':insurance})

@login_required(login_url='login')
def relief_fund_request(request):
    user = request.user  # Fetch the current logged-in user
    public = Public.objects.filter(user=user)  # Filter data based on the user
    if not public.exists():
        context = {'no_public_data': True}
    else:
        context = {'publics': public, 'user': user}
    return render(request,'public/relief-fund-request.html',context)

@login_required(login_url='login')
def fund_request(request,public_id):
    public = Public.objects.get(id=public_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        Fund_request.objects.create(
                person=public,
                reason=reason,
                created_by=request.user,
                status = Fund_request.PENDING 
            )
    return redirect("public-dashboard")



def gov_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('gov-dashboard')
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
            # Add more redirects for other user types
    return render(request,'signin/government-login.html')

@login_required(login_url='login')
def gov_dashboard(request):
    user=request.user
    return render(request,'government/government-dashboard.html',{user:user})

@login_required(login_url='login')
def police_profile(request):
    user = request.user  # Fetch the current logged-in user
    print(user)
    police_station = get_object_or_404(Police_station,user=user)  # Filter data based on the user  
    context = {'policestation':  police_station}
    return render(request,'police/police-profile.html',context)


def rescue_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        Rescue_team_name = request.POST.get('Rescue_team_name')
        location = request.POST.get('location')
        district = request.POST.get('district')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password!=confirm_password:
            error_message="Password do NOT match"
            messages.error(request,error_message)
        else:
            try:
                # Create the user account
                user = User.objects.create_user(username=username, password=password)
                 # Create a customer account
                Rescue_obj=user= Rescue.objects.create(Rescue_team_name=Rescue_team_name,email=email,user=user,location=location,district=district,phone=phone,state=state)
                Rescue_obj.save()
                return redirect('rescue-login')
            except Exception as e:
                print(e)
                error_message="Duplicate username or invalid inputs"
                messages.error(request,error_message)
    return render(request,'registration/rescue-register.html')

def rescue_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('rescue-dashboard')
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
    return render(request,'signin/rescue-login.html')

@login_required(login_url='login')
def rescue_dashboard(request):
    user=request.user
    return render(request,'rescue/rescue-dashboard.html',{user:user})

@login_required(login_url='login')
def rescue_profile(request):
    user = request.user  # Fetch the current logged-in user
    print(user)
    rescueprofile = get_object_or_404(Rescue,user=user)  # Filter data based on the user  
    context = {'rescue_profile':  rescueprofile}
    return render(request,'rescue/rescue-profile.html',context)

@login_required(login_url='login')
def volunteer_profile(request):
    user=request.user
    volunteer = volunteer_camp_allocation.objects.filter(user=user)  # Filter data based on the user  
    if not volunteer.exists():
         context = {'no_public_data': True,'user':user}
    else:
        context = {'campallocations': volunteer,'user':user}
    return render(request,'volunteer/volunteers-profile.html',context)

@login_required(login_url='login')
def update_public_profile(request,public_id):
    public_instance = get_object_or_404(Public, id=public_id)
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        public_instance.first_name=request.POST.get('firstname')
        public_instance.last_name=request.POST.get('lastname')
        public_instance.address = request.POST.get('address', 'Unknown') 
        public_instance.dob = request.POST.get('dob')
        public_instance.blood_group = request.POST.get('blood_group')
        public_instance.gender = request.POST.get('gender')
        public_instance.occupation = request.POST.get('occupation')
        public_instance.father_name = request.POST.get('father_name')
        public_instance.mother_name = request.POST.get('mother_name')
        public_instance.state = request.POST.get('state')
        public_instance.district = request.POST.get('district')
        public_instance.phone = request.POST.get('phone')
         # Update the photo if provided
        if photo:
            public_instance.photo = photo

        public_instance.save()
        return redirect('public-profile')
    context = {
        'public': public_instance,
        'camps': Camp.objects.all(),  # Provide camps for the dropdown
    }
    return render(request, 'public/public-camp-allocation.html',context)

@login_required(login_url='login')
def camp_profile(request):
    user = request.user  # Fetch the current logged-in user
    print(user)
    camp = get_object_or_404(Camp,user=user)  # Filter data based on the user  
    context = {'camp':  camp}
    return render(request,'camp/camp-profile.html',context)

@login_required(login_url='login')
def update_volunteer_profile(request,volunteer_id):
    volunteer_instance = get_object_or_404(volunteer_camp_allocation, id=volunteer_id)
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        volunteer_instance.first_name=request.POST.get('firstname')
        volunteer_instance.last_name=request.POST.get('lastname')
        volunteer_instance.address = request.POST.get('address', 'Unknown') 
        volunteer_instance.age = request.POST.get('age')
        volunteer_instance.blood_group = request.POST.get('blood_group')
        volunteer_instance.gender = request.POST.get('gender')
        volunteer_instance.district = request.POST.get('district')
        volunteer_instance.state = request.POST.get('state')
        volunteer_instance.phone = request.POST.get('phone')
         # Update the photo if provided
        if photo:
            volunteer_instance.photo = photo

        volunteer_instance.save()
        return redirect('volunteer-profile')
    context = {
        'volunteer': volunteer_instance,
        'camps': Camp.objects.all(),  # Provide camps for the dropdown
    }
    return render(request, 'volunteer/volunteers-camp-allocation.html',context)

@login_required(login_url='login')
def insurance_profile(request):
    user = request.user  # Fetch the current logged-in user
    print(user)
    insurance = get_object_or_404(Insurance,user=user)  # Filter data based on the user  
    context = {'insurance':  insurance}
    return render(request,'insurance/insurance-profile.html',context)

