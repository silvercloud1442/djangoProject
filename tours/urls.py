from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('base/', base, name='base'),
    path('tour_details/<slug:tour_slug>', TourView.as_view(), name='tour_details'),
    path('hotel_details/<slug:hotel_slug>', HotelView.as_view(), name='hotel_details'),
    path('tours/<str:ordering>', ToursView.as_view(), name='tours'),
    path('register/', register, name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('booking/<slug:tour_slug>', BookingView.as_view(), name='booking'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='profile')
]