from django.urls import path
from . import views

urlpatterns = [
    path('Admin',views.admin_login,name="Admin"),
    path('admin-interface',views.admin_interface,name="admin-interface"),
    path('registration',views.registration,name="registration"),
    path('public-deatails-view',views.public_deatails_view,name="public-deatails-view"),
    path('person-missing-all-view',views.person_missing_all_view,name="person-missing-all-view"),
    path('camp-members-all-view',views.camp_members_all_view,name="camp-members-all-view"),
    path('camp-relief-fund-all-status',views.camp_relief_fund_all_status,name="camp-relief-fund-all-status"),
    path('withoutcamp-fund-status',views.withoutcamp_fund_status,name="withoutcamp-fund-status"),
    path('vehicle-missing-all-view',views.vehicle_missing_all_view,name="vehicle-missing-all_view"),
    path('vehicle-damage-all-view',views.vehicle_damage_all_view,name="vehicle-damage-all-view"),
    path('police-station-all-view',views.police_station_all_view,name="police-station-all-view"),
    path('camp-all-view',views.camp_all_view,name="camp-all-view"),
    path('rescue-all-view',views.rescue_all_view,name="rescue-all-view"),
    path('insurance-all-view',views.insurance_all_view,name="insurance-all-view"),
    path('volunteer-all-view',views.volunteer_all_view,name="volunteer-all-view"),
    path('states-view',views.states_view,name="states-view"),
]