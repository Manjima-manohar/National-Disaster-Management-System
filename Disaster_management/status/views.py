from django.shortcuts import render,get_object_or_404,redirect
from management.models import Person_missing,Public,Camp,volunteer_camp_allocation,Vehicle_management,Fund_request,Police_station,Rescue,Insurance
from . models import Make_alert
from Admin_management.models import Government
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def status_person_missing(request):
    user = request.user  # Fetch the current logged-in user
    person_missing = Person_missing.objects.filter(created_by=user)  # Filter data based on the user
    for person in person_missing:
        # Check if a matching camp_allocation record exists
        camp_allocation_record = Public.objects.filter(
            first_name=person.firstname,
            last_name=person.last_name,
            address=person.address,
            blood_group=person.blood_group,
            gender=person.gender,
            occupation=person.occupation,
            father_name=person.father_name,
            mother_name=person.mother_name,
        ).first()
        if camp_allocation_record:
            # Update the status to the camp name if a match is found
            person.camp_name = camp_allocation_record.camp_name.camp_name
            person.status = Person_missing.FOUNDED
            person.save()
    context = {'person_missing': person_missing}
    return render(request,'public/status-person-missing.html',context)

@login_required(login_url='login')
def camp_members(request,camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    allocations = Public.objects.filter(camp_name=camp)
    context = {
        'allocations': allocations,
        'camp': camp,
    }
    return render(request,'camp/camp-members.html',context)

@login_required(login_url='login')
def update_status_camp_members(request, person_id):
        person = get_object_or_404(Public, id=person_id)
        if request.method == 'POST':
            if person.status == 'present':  # Check if current status is 'present'
                person.status = 'Vacated'  # Update to 'vacated'
                person.save()
            camp_id = person.camp_name.id if person.camp_name else 0
            return redirect('camp-members', camp_id=camp_id)
        
@login_required(login_url='login')
def camp_person_missing_status(request,camp_name):
    camp = get_object_or_404(Camp,camp_name=camp_name)
    persons = Person_missing.objects.filter(camp_name=camp_name)
    context = {
        'persons': persons,
        'camp': camp,
    }
    return render(request,'camp/camp_personmissing_status.html',context)

@login_required(login_url='login')
def police_person_missing_status(request):
    home_page_url = ''
    try:
        police_station = Police_station.objects.get(user=request.user)
        home_page_url = 'policestation-dashboard'
        state = police_station.state 
    except Police_station.DoesNotExist:
        try:
            rescue_team = Rescue.objects.get(user=request.user)
            home_page_url = 'rescue-dashboard'
            state = rescue_team.state 
        except Rescue.DoesNotExist:
            home_page_url = 'index'  # Change to whatever default homepage URL you use

    persons = Person_missing.objects.filter(camp_name__isnull=True,state=state)
    context = {
        'persons': persons,
        'home_page_url': home_page_url
    }
    return render(request,'police/police-person-missing.html',context)

@login_required(login_url='login')
def update_status(request, person_id):
    person = get_object_or_404(Person_missing, id=person_id)
    if request.method == 'POST':
        # Update the status to 'FOUNDED'
        person.status = Person_missing.FOUNDED
        person.save()
        return redirect("police-person-missing-status")

@login_required(login_url='login')
def camp_volunteer_list(request,camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    volunteer_campallocation = volunteer_camp_allocation.objects.filter(camp_name=camp)
    context = {
        'allocations': volunteer_campallocation,
        'camp': camp,
    }
    return render(request,'camp/camp-volunteer-list.html',context)

@login_required(login_url='login')
def team_allocation(request,allocation_id):
    allocation = get_object_or_404(volunteer_camp_allocation, id=allocation_id)
    if request.method == 'POST':
        team = request.POST.get('team')
        
        if 'accept' in request.POST:
            allocation.team = team
        elif 'reject' in request.POST:
            allocation.team = 'Rejected'
        
        allocation.save()
        return redirect("camp-volunteer-list",camp_id=allocation.camp_name.id)
    
@login_required(login_url='login')
def status_camp_allocation(request):
    user=request.user
    volunteer_campallocation = volunteer_camp_allocation.objects.filter(user=user)
    context = {
        'allocations': volunteer_campallocation,
    }
    return render(request,'volunteer/status-camp-allocation.html',context)

@login_required(login_url='login')
def status_vehicle_missing(request):
    police_station = Police_station.objects.get(user=request.user)
    vehicles_missing = Vehicle_management.objects.filter(issue="missing",state=police_station.state)
    context={'vehicles_missing': vehicles_missing}
    return render(request,'police/police-vehicle-mngt.html',context)

@login_required(login_url='login')
def update_status_vehicle(request, vehicle_id):
    police_station = Police_station.objects.get(user=request.user)
    vehicles_missing = get_object_or_404(Vehicle_management, id=vehicle_id)
    if request.method == 'POST':
        # Update the status to 'FOUNDED'
        vehicles_missing.status = Vehicle_management.FOUNDED
        vehicles_missing.save()
        return redirect("status-vehicle-missing")

@login_required(login_url='login')
def status_vehicle_damage(request):
    # insurance = Insurance.objects.get(user=request.user)
    user=request.user
    insurance = Insurance.objects.get(user=user)
    vehicles_damage = Vehicle_management.objects.filter(issue="damage",company_name=insurance.id)
    context={'vehicles_damage': vehicles_damage}
    return render(request,'insurance/insurance-vehicle-mngt.html',context)

@login_required(login_url='login')
def update_status_vehicledamage(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle_management, id=vehicle_id)
    if 'status_action' in request.POST:
        action = request.POST['status_action']
        if action == 'approve':
            vehicle.status = Vehicle_management.APPROVED
        elif action == 'reject':
            vehicle.status = Vehicle_management.REJECTED
        vehicle.save()
        return redirect("status-vehicle-damage")

@login_required(login_url='login')
def public_status_vehicle_missing(request):
    user = request.user
    vehicles_missing = Vehicle_management.objects.filter(created_by=user,issue="missing")
    context={'vehicles_missing': vehicles_missing}
    return render(request,'public/status-vehicle-missing.html',context)

@login_required(login_url='login')
def public_status_vehicle_damage(request):
    user = request.user
    vehicles_damage = Vehicle_management.objects.filter(created_by=user,issue="damage")
    context={'vehicles_damage': vehicles_damage}
    return render(request,'public/status-vehicle-damage.html',context)

@login_required(login_url='login')
def camp_relief_fund_status(request):
    gov = Government.objects.get(user=request.user)
    fund_requests_with_camp = Fund_request.objects.filter(person__camp_name__isnull=False,person__state=gov.state_name)
    context = {
        'fund_requests_with_camp': fund_requests_with_camp
    }
    return render(request,'government/relief-fund-request-camp.html',context)

@login_required(login_url='login')
def update_status_fund_request(request, fund_request_id):
    fund_request = get_object_or_404(Fund_request, id=fund_request_id)
    if 'status_action' in request.POST:
        action = request.POST['status_action']
        if action == 'approve':
            fund_request.status = Fund_request.APPROVED
        elif action == 'reject':
            fund_request.status = Fund_request.REJECTED
        fund_request.save()
        if fund_request.person and fund_request.person.camp_name:
            return redirect("camp-relief-fund-status")
        else:
            return redirect("withoutcamp-relief-fund-status")
        
@login_required(login_url='login') 
def withoutcamp_relief_fund_status(request):
    gov = Government.objects.get(user=request.user)
    fund_requests_without_camp = Fund_request.objects.filter(person__camp_name__isnull=True,person__state=gov.state_name)
    context = {
        'fund_requests_without_camp': fund_requests_without_camp
    }
    return render(request,'government/relief-fund-request-withoutcamp.html',context)

@login_required(login_url='login')
def make_alert(request):
    if request.method == 'POST':
        issue = request.POST.get('issue')
        message = request.POST.get('message')
        created_by = request.user  
        print(issue)
        Make_alert.objects.create(
            issue=issue,
            message=message,
            created_by=created_by
        )

        return redirect('policestation-dashboard')   
    return render(request,'police/make-alert.html')

@login_required(login_url='login')
def public_relief_fund_status(request):
    user = request.user
    fund_request = Fund_request.objects.filter(created_by=user)
    context={'fund_request': fund_request}
    return render(request,'public/public-relief-fund-status.html',context)

@login_required(login_url='login')
def public_deatail_view(request):
    gov = Government.objects.get(user=request.user)
    publics = Public.objects.filter(camp_name__isnull=True,state=gov.state_name)
    context={"publics":publics}
    return render(request,'government/public-details.html',context)
@login_required(login_url='login')
def camp_members_view(request):
    gov = Government.objects.get(user=request.user)
    publics = Public.objects.filter(camp_name__isnull=False,state=gov.state_name)
    context={"publics":publics}
    return render(request,'government/camp-members-view.html',context)

@login_required(login_url='login')
def person_missing_view(request):
    gov = Government.objects.get(user=request.user)
    person_missing = Person_missing.objects.filter(state=gov.state_name)
    context = {'person_missing': person_missing}
    return render(request,'government/person-missing-view.html',context)

@login_required(login_url='login')
def vehicle_missing_view(request):
    gov = Government.objects.get(user=request.user)
    vehicles_missing = Vehicle_management.objects.filter(issue="missing",state=gov.state_name)
    context={'vehicles_missing': vehicles_missing}
    return render(request,'government/vehicle-missing-view.html',context)

@login_required(login_url='login')
def vehicle_damage_view(request):
    gov = Government.objects.get(user=request.user)
    vehicles_damage = Vehicle_management.objects.filter(issue="damage",state=gov.state_name)
    context={'vehicles_damage': vehicles_damage}
    return render(request,'government/vehicle-damage-view.html',context)

@login_required(login_url='login')
def notification(request):
    # Fetch the state of the logged-in user from the Public or Camp model
    user_state = None
    try:
        public_user = Public.objects.get(user=request.user)
        user_state = public_user.state
    except Public.DoesNotExist:
        try:
            camp_user = Camp.objects.get(user=request.user)
            user_state = camp_user.state
        except Camp.DoesNotExist:
            user_state = None  # Handle case where user state is not available

    # Fetch alerts created by users from the same state as the logged-in user
    if user_state:
        make_alerts = Make_alert.objects.filter( created_by__policestation_profile__state=user_state)
    else:
        make_alerts = Make_alert.objects.none()  # No alerts if user state is not found

    # Calculate the count of notifications
    notification_count = make_alerts.count()

    # Determine the home page URL
    home_page_url = ''
    if user_state:
        home_page_url = 'public-dashboard' if Public.objects.filter(user=request.user).exists() else 'camp-dashborad'

    context = {
        'make_alerts': make_alerts,
        'home_page_url': home_page_url,
        'notification_count': notification_count,
    }
    return render(request, 'notification.html', context)

@login_required(login_url='login')
def update_police_profile(request,police_id):
    police_instance = get_object_or_404(Police_station, id=police_id)
    if request.method == 'POST':
        police_instance.policestation_name=request.POST.get('policestation_name')
        police_instance.email=request.POST.get('email')
        police_instance.location=request.POST.get('location')
        police_instance.phone=request.POST.get('phone')
        police_instance.district=request.POST.get('district')
        police_instance.state=request.POST.get('state')
        police_instance.save()
        return redirect('police-profile')
    context = {
        'police': police_instance  # Provide camps for the dropdown
    }
    return render(request,'police/edit-police-profile.html',context)

@login_required(login_url='login')
def update_rescue_profile(request,rescue_id):
    rescue_instance = get_object_or_404(Rescue,id=rescue_id)
    if request.method == 'POST':
        rescue_instance.rescue_team_name=request.POST.get('rescue_team_name')
        rescue_instance.email=request.POST.get('email')
        rescue_instance.location=request.POST.get('location')
        rescue_instance.phone=request.POST.get('phone')
        rescue_instance.district=request.POST.get('district')
        rescue_instance.state=request.POST.get('state')
        rescue_instance.save()
        return redirect('rescue-profile')
    context = {
        'rescue': rescue_instance  # Provide camps for the dropdown
    }
    return render(request,'rescue/edit-rescue-profile.html',context)

@login_required(login_url='login')
def police_station_view(request):
    gov = Government.objects.get(user=request.user)
    police_station = Police_station.objects.filter(state=gov.state_name)
    context = {'police_station': police_station}
    return render(request,'government/police-station-view.html',context)
@login_required(login_url='login')
def camp_view(request):
    gov = Government.objects.get(user=request.user)
    camp = Camp.objects.filter(state=gov.state_name)
    context = {'camp': camp}
    return render(request,'government/camp-view.html',context)
@login_required(login_url='login')
def rescue_view(request):
    gov = Government.objects.get(user=request.user)
    rescue = Rescue.objects.filter(state=gov.state_name)
    context = {'rescue': rescue}
    return render(request,'government/rescue-view.html',context)
@login_required(login_url='login')
def insurance_view(request):
    gov = Government.objects.get(user=request.user)
    insurance = Insurance.objects.filter(state=gov.state_name)
    context = {'insurance': insurance}
    return render(request,'government/insurance-view.html',context)
@login_required(login_url='login')
def volunteer_view(request):
    gov = Government.objects.get(user=request.user)
    volunteer = volunteer_camp_allocation.objects.filter(state=gov.state_name)
    context = {'volunteer': volunteer}
    return render(request,'government/volunteer-view.html',context)

@login_required(login_url='login')
def update_camp_profile(request,camp_id):
    camp_instance = get_object_or_404(Camp, id=camp_id)
    if request.method == 'POST':
        camp_instance.camp_name=request.POST.get('camp_name')
        camp_instance.email=request.POST.get('email')
        camp_instance.place=request.POST.get('place')
        camp_instance.camp_head=request.POST.get('camp_head')
        camp_instance.phone=request.POST.get('phone')
        camp_instance.state=request.POST.get('state')
        camp_instance.district=request.POST.get('district')
        camp_instance.save()
        return redirect('camp-profile')
    context = {
        'camp': camp_instance # Provide camps for the dropdown
    }
    return render(request,'camp/edit-camp-profile.html',context)

@login_required(login_url='login')
def update_insurance_profile(request,insurance_id):
    insurance_instance = get_object_or_404(Insurance, id=insurance_id)
    if request.method == 'POST':
        insurance_instance.campany_name=request.POST.get('company_name')
        insurance_instance.email=request.POST.get('email')
        insurance_instance.phone=request.POST.get('phone')
        insurance_instance.district=request.POST.get('district')
        insurance_instance.state=request.POST.get('state')
        insurance_instance.save()
        return redirect('insurance-profile')
    context = {
        'insurance': insurance_instance  # Provide camps for the dropdown
    }
    return render(request,'insurance/edit-insurance-profile.html',context)