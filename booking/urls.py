from django.urls import path
from .views import SignupView, MovieListView, MovieShowsView, BookSeatView, CancelBookingView, MyBookingsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/shows/', MovieShowsView.as_view(), name='movie-shows'),
    path('shows/<int:pk>/book/', BookSeatView.as_view(), name='show-book'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking-cancel'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
]
