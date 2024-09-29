from django.urls import  path
from . import views

urlpatterns = [
          path("", views.home, name="home"),
          path("sports/<slug:slug>/",views.facility_list, name="facility"),
          path('facility/<slug:slug>/',views.facility_detail, name="details"),
          path('profile/',views.profile, name="profile"),
          path('manager/',views.manager, name="manager"),
          path('register_facility/', views.register_facility, name='register_facility'),
          path('login/', views.login_view, name='login'),
          path('logout/', views.logout_view, name='logout'),
          path('register_user/', views.register_user, name='register'),
          path('delete_facility/<slug:slug>/', views.delete_facility, name='delete'),
          path('update_facility/<slug:slug>/', views.update_facility, name='update'),
          path ('update_booking/<int:booking_id>/', views.update_booking, name='update_booking'),
          path ('sport_list/', views.sport_list, name='sport'),
          path("booking/",views.booking,name="book"),
          path("cancle/<int:booking_id>/",views.cancle,name="cancle")
]