# fitness-booking-api

This project is a simple booking system for a fictional fitness studio. Users can view available classes, book a class, and check their bookings. It is built using Django and Django REST Framework. Users can:

- View all upcoming fitness classes
- Book a class with available slots
- View all bookings made using a client email
- Create class types and fitness classes
- See lists of all created class types, bookings and classes
- Enjoy input validation and IST timezone handling
- Run unit tests to verify core functionality

 Tech Stack

- Python 3.x  
- Django  
- Django REST Framework  
- SQLite (default database)  
- Postman for API testing  
- Virtual Environment: `venv`  

1. clone the github repository

    git clone https://github.com/fairoosa/fitness-booking-api.git
    cd fitness-booking-api

2. Create and activate virtual environment

    python -m venv venv
    venv\Scripts\activate 
          
3. Install dependencies

    pip install -r requirements.txt

4. Run migrations

    python manage.py migrate

5. Start the development server

    python manage.py runserver
    The API will be available at:
    http://localhost:8000/

API Endpoints
1. GET /classes/
    Returns a list of upcoming fitness classes.

    Example Response
    [
    {
        "id": 1,
        "class_type": 1,
        "class_name": "Yoga",
        "instructor": "Jane Doe",
        "start_time": "2025-06-30 10:00:00 IST",
        "end_time": "2025-06-30 11:00:00 IST",
        "available_slots": 5
    }
    ]
2. POST /book/
    Book a class.

    Request Body
    {
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
    }
    Possible Responses
    201 Created — Booking successful

    400 Bad Request — When:

    Class is full

    Email is invalid

    Duplicate booking

3. GET /bookings/?email=client@example.com
    Returns all bookings made by the given email address.

    Example Response
    [
    {
        "id": 2,
        "class_id": 1,
        "client_name": "John Doe",
        "client_email": "john@example.com"
    }
    ]
    
4. GET /book/
    Returns all bookings in the system

5. GET /class-types/
    Lists all available class types.
    Example Response
    [
    {
        "id": 1,
        "class_name": "Yoga"
    },
    {
        "id": 2,
        "class_name": "HIIT"
    }
    ]
6. POST /class-types/
    Request Body

    Creates a new class type.
    {
    "class_name": "Zumba"
    }
    Response
    
    {
    "id": 3,
    "class_name": "Zumba"
    }

Using Postman
You can test all endpoints using Postman:

    GET http://localhost:8000/classes/

    POST http://localhost:8000/book/

    GET http://localhost:8000/bookings/?email=john@example.com

    GET http://localhost:8000/book/

    POST http://localhost:8000/classes/

    POST http://127.0.0.1:8000/class-types/

    GET http://127.0.0.1:8000/class-types/

Running Tests
To run unit tests:
    python manage.py test
    All test cases are defined in user_management/tests.py.


