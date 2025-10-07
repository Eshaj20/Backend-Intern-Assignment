# Movie Ticket Booking API (Backend Intern Assignment)

A Django REST Framework-based backend system for managing movies, shows, and seat bookings, with JWT authentication and Swagger documentation.

---

## Deliverables

### 1. GitHub Repository containing:
- Full Django project code (`movieticket/`, `booking/`)
- `requirements.txt`
- Well-documented `README.md` (this file)

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps to Run the Project

**Clone the repository**
```bash
git clone https://github.com/<your-username>/movie-booking-backend.git
cd movie-booking-backend

## Create a virtual environment

python -m venv venv
# Activate it
venv\Scripts\activate    # Windows
# or
source venv/bin/activate # macOS/Linux

# Install dependencies

pip install -r requirements.txt

# Run migrations

python manage.py makemigrations
python manage.py migrate

# Create a superuser

python manage.py createsuperuser

# Run the server

python manage.py runserver

Now your backend will be live at:
 http://127.0.0.1:8000/

# JWT Authentication Guide

The project uses JWT (JSON Web Tokens) for secure authentication, powered by SimpleJWT
.

1. Signup (Create a new user)

Endpoint:

POST /api/signup/


Body:

{
  "username": "esha",
  "password": "password123",
  "email": "esha@example.com"
}

2️. Login (Get access and refresh tokens)

Endpoint:

POST /api/token/


Body:

{
  "username": "esha",
  "password": "password123"
}


Response:

{
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}


Use the access token in headers for authorized requests:

Authorization: Bearer <ACCESS_TOKEN>

# Core API Endpoints
Endpoint	Method	Auth	Description
/api/signup/	POST	❌	Register new user
/api/token/	POST	❌	Obtain JWT tokens
/api/token/refresh/	POST	❌	Refresh access token
/api/movies/	GET	❌	List all movies
/api/movies/<movie_id>/shows/	GET	❌	List all shows for a movie
/api/shows/<show_id>/book/	POST	✅	Book a seat for a show
/api/my-bookings/	GET	✅	View your bookings
/api/bookings/<booking_id>/cancel/	POST	✅	Cancel an existing booking

# Swagger API Documentation

Swagger UI is available at:
  -   http://127.0.0.1:8000/swagger/

It provides:
- Interactive API testing
- Example requests/responses
- Schema for all endpoints

# Admin Panel

Access the Django Admin interface at:

- http://127.0.0.1:8000/admin/

Login using your superuser credentials.

From here, you can:
- Add or edit Movies 
- Create Shows 
- Manage Bookings 

# Business Logic Implemented

- Prevent double booking for the same seat (unique constraint)
- Prevent overbooking beyond total seats
- Users can cancel only their own bookings
- Seat booking uses transaction.atomic() & select_for_update() for concurrency safety
- JWT-secured endpoints for bookings

# Tech Stack

1.Language: Python 3
2.Framework: Django, Django REST Framework
3.Auth: SimpleJWT
4.Docs: drf-yasg (Swagger UI)
5.Database: SQLite (default, easy setup)

# Example Workflow

1. Create movies and shows in Admin panel
2. Signup/Login via API → obtain access token
3. Book a seat using /api/shows/<id>/book/
4. View all bookings using /api/my-bookings/
5. Cancel booking with /api/bookings/<id>/cancel/

# Example Test Commands (via cURL)
# Signup
curl -X POST http://127.0.0.1:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username":"esha","password":"password123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"esha","password":"password123"}'

# List Movies
curl http://127.0.0.1:8000/api/movies/

# Book a seat (requires access token)
curl -X POST http://127.0.0.1:8000/api/shows/1/book/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"seat_number": 5}'


# Folder Structure
backend_assignment/
│
├── movieticket/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── booking/              # Core app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── requirements.txt
├── manage.py
└── README.md

# Conclusion

This project demonstrates a production-ready backend foundation with:
- Secure JWT authentication
- RESTful API structure
- Database transaction handling
-Interactive Swagger documentation