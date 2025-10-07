from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from .models import Movie, Show, Booking
from .serializers import SignupSerializer, MovieSerializer, ShowSerializer, BookingSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.AllowAny,)

class MovieShowsView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        shows = movie.shows.all()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)

class BookSeatView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, pk):
        user = request.user
        show = get_object_or_404(Show, pk=pk)
        seat_number = request.data.get('seat_number')
        try:
            seat_number = int(seat_number)
        except Exception:
            return Response({'detail':'seat_number must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if seat_number < 1 or seat_number > show.total_seats:
            return Response({'detail':'seat_number out of range'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # lock bookings for this show to reduce race conditions
            existing_count = Booking.objects.select_for_update().filter(show=show, status='booked').count()
            if existing_count >= show.total_seats:
                return Response({'detail':'Show fully booked'}, status=status.HTTP_400_BAD_REQUEST)
            # check seat already booked
            if Booking.objects.select_for_update().filter(show=show, seat_number=seat_number, status='booked').exists():
                return Response({'detail':'Seat already booked'}, status=status.HTTP_400_BAD_REQUEST)
            booking = Booking.objects.create(user=user, show=show, seat_number=seat_number)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CancelBookingView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if booking.user != request.user:
            return Response({'detail':'Cannot cancel others\' bookings'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == 'cancelled':
            return Response({'detail':'Booking already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({'detail':'Booking cancelled'})

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')
