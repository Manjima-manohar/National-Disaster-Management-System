from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from management.models import Person_missing,Public,Camp,volunteer_camp_allocation,Vehicle_management,Fund_request,Police_station,Rescue,Insurance
from . models import Government
# Create your views here.

def admin_interface(request):
    user=request.user
    return render(request,'admin/admin-dashboard.html',{user:user})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard or homepage based on user type
            return redirect('admin-interface')  
        else:
            error_message="Invalid Username & Password"
            messages.error(request,error_message)
            # Add more redirects for other user types
    return render(request,'admin/signin.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
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
                gov_obj=user= Government.objects.create(email=email,user=user,phone=phone,state_name=state)
                gov_obj.save()
                success_message="Registered successfully"
                messages.success(request,success_message)
            except Exception as e:
                print(e)
                error_message="Duplicate username or invalid inputs"
                messages.error(request,error_message)
    return render(request,'admin/state-registration.html')

@login_required(login_url='Admin')
def public_deatails_view(request):
    publics = Public.objects.filter(camp_name__isnull=True)
    context={"publics":publics}
    return render(request,'admin/public-details.html',context)

@login_required(login_url='Admin')
def person_missing_all_view(request):
    person_missing = Person_missing.objects.all()
    context = {'person_missing': person_missing}
    return render(request,'admin/person-missing-all-view.html',context)

@login_required(login_url='Admin')
def camp_members_all_view(request):
    publics = Public.objects.filter(camp_name__isnull=False)
    context={"publics":publics}
    return render(request,'admin/camp-members-all-view.html',context)

@login_required(login_url='Admin')
def camp_relief_fund_all_status(request):
    fund_requests_with_camp = Fund_request.objects.filter(person__camp_name__isnull=False)
    context = {
        'fund_requests_with_camp': fund_requests_with_camp
    }
    return render(request,'admin/fund_request_all_view.html',context)

@login_required(login_url='Admin')
def withoutcamp_fund_status(request):
    fund_requests_without_camp = Fund_request.objects.filter(person__camp_name__isnull=True)
    context = {
        'fund_requests_without_camp': fund_requests_without_camp
    }
    return render(request,'admin/fund_request_view_withoutcamp.html',context)

@login_required(login_url='Admin')
def vehicle_missing_all_view(request):
    vehicles_missing = Vehicle_management.objects.filter(issue="missing")
    context={'vehicles_missing': vehicles_missing}
    return render(request,'admin/vehicle_missing_all_view.html',context)

@login_required(login_url='Admin')
def vehicle_damage_all_view(request):
    vehicles_damage = Vehicle_management.objects.filter(issue="damage")
    context={'vehicles_damage': vehicles_damage}
    return render(request,'admin/vehicle_damage_all_view.html',context)

@login_required(login_url='Admin')
def police_station_all_view(request):
    police_station = Police_station.objects.all()
    context = {'police_station': police_station}
    return render(request,'admin/police_station_all_view.html',context)

@login_required(login_url='Admin')
def camp_all_view(request):
    camp = Camp.objects.all()
    context = {'camp': camp}
    return render(request,'admin/camp_all_view.html',context)

@login_required(login_url='Admin')
def rescue_all_view(request):
    rescue = Rescue.objects.all()
    context = {'rescue': rescue}
    return render(request,'admin/rescue_all_view.html',context)

@login_required(login_url='Admin')
def insurance_all_view(request):
    insurance = Insurance.objects.all()
    context = {'insurance': insurance}
    return render(request,'admin/insurance_all_view.html',context)

@login_required(login_url='Admin')
def volunteer_all_view(request):
    volunteer = volunteer_camp_allocation.objects.all()
    context = {'volunteer': volunteer}
    return render(request,'admin/volunteer_all_view.html',context)


@login_required(login_url='Admin')
def states_view(request):
    gov = Government.objects.all()
    context = {'government': gov}
    return render(request,'admin/states.html',context)
