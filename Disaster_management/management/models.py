from django.db import models
from django.contrib.auth.models import User

# # Create your models here.
class Camp(models.Model):
    camp_name = models.CharField(max_length=100)
    email = models.EmailField()
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Not Specified")
    camp_head = models.CharField(max_length=30, default="")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile',default=1)
    def __str__(self):
        return self.camp_name
    
class Public(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob=models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100)
    blood_group=models.CharField(max_length=30)
    email = models.EmailField()
    phone=models.CharField(max_length=30)
    gender=models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    father_name=models.CharField(max_length=30)
    mother_name=models.CharField(max_length=30)
    state = models.CharField(max_length=100, default="Not Specified")
    district = models.CharField(max_length=100)
    camp_name=models.ForeignKey(Camp,on_delete=models.CASCADE,blank=True, null=True)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    status=models.CharField(max_length=100,blank=True, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='public_profile')
    def __str__(self):
        return self.user.username
   
class Person_missing(models.Model):
    STAGE=0
    SEARCHING="Searching"
    FOUNDED="founded"
    STATUS_CHOICE=((SEARCHING,"SEARCHING"),
                   (FOUNDED,"FOUNDED"),
                   )
    firstname = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address=models.TextField(default='Unknown')
    dob=models.DateField()
    blood_group=models.CharField(max_length=30)
    gender=models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    father_name=models.CharField(max_length=30)
    mother_name=models.CharField(max_length=30)
    photo = models.ImageField(upload_to='media/',blank=True, null=True)
    state = models.CharField(max_length=100, default="Not Specified")
    district = models.CharField(max_length=100,default="Unknown")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_missing_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default=SEARCHING)
    camp_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.created_by.username

class Insurance(models.Model):
    company_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    state = models.CharField(max_length=100, default="Not Specified")
    district = models.CharField(max_length=100,default="Unknown")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='insurance_profile',default=1)
    def __str__(self):
        return self.company_name

class Vehicle_management(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    STAGE=0
    PENDING="Pending"
    SEARCHING="Searching"
    FOUNDED="Founded"
    APPROVED="Approved"
    REJECTED="Rejected"
    STATUS_CHOICE=((PENDING,"PENDING"),
                   (SEARCHING,"SEARCHING"),
                   (APPROVED,"APPROVED"),
                   (REJECTED,"REJECTED"),
                   (FOUNDED,"FOUNDED")
                   )
    reg_no =models.IntegerField()
    owner_name = models.CharField(max_length=30)
    license_no =models.IntegerField()
    make_model=models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Not Specified")
    district = models.CharField(max_length=100,default="Unknown")
    rc_book=models.ImageField(upload_to='media/')
    license_image=models.ImageField(upload_to='media/')
    vehicle_image=models.ImageField(upload_to='media/')
    issue = models.CharField(max_length=255, blank=True, null=True)
    company_name=models.ForeignKey(Insurance,on_delete=models.CASCADE,blank=True, null=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICE,default=STAGE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_management')
    created_at = models.DateTimeField(auto_now_add=True)
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)


class Police_station(models.Model):
    policestation_name = models.CharField(max_length=30)
    email = models.EmailField()
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default="Not Specified")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='policestation_profile',default=1)
    def __str__(self):
        return self.policestation_name
    

class volunteer_camp_allocation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.CharField(null=True, blank=True,max_length=30) 
    address = models.CharField(max_length=100)
    blood_group=models.CharField(max_length=30)
    email = models.EmailField()
    phone=models.CharField(max_length=30)
    gender=models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default="Not Specified")
    camp_name=models.ForeignKey(Camp,on_delete=models.CASCADE,null=True, blank=True)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='volunteer_profile')
    team=models.CharField(max_length=30, blank=True, null=True)


class Fund_request(models.Model):
    STAGE=None
    PENDING="Pending"
    APPROVED="Approved"
    REJECTED="Rejected"
    STATUS_CHOICE=((PENDING,"PENDING"),
                   (APPROVED,"APPROVED"),
                   (REJECTED,"REJECTED"),
                   )
    person=models.ForeignKey(Public,on_delete=models.CASCADE,blank=True, null=True)
    reason=models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fund_request')
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICE,default=STAGE)
    def __str__(self):
        return self.created_by.username
    

class Rescue(models.Model):
    Rescue_team_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default="Not Specified")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='rescue_profile',default=1)
    def __str__(self):
        return self.Rescue_team_name