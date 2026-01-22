.

🚍 TrackMate – Backend for Smart Trip Tracking Application

🔧 Backend-Focused Repository | Django REST APIs for Trip Tracking & Analytics

TrackMate is a smart trip tracking application designed to help users automatically record trips, analyze distance, duration, travel cost, and carbon emissions, and gain insights into their travel behavior. The application promotes sustainable mobility by making users aware of their environmental impact through data-driven analytics.

This repository contains the complete backend implementation of the TrackMate application.

⚠️ Repository Scope

Note: This repository includes only the backend services of the TrackMate application.
The frontend/mobile application communicates with this backend via REST APIs.
UI screenshots are shared for reference and demonstration purposes only.

🧠 Backend Overview
The TrackMate backend acts as the core engine of the application. It handles user authentication, trip lifecycle management, emission calculations, data persistence, and analytics required to power the TrackMate dashboard and related features.

The backend is designed with modularity and scalability in mind, following clean separation of concerns across apps.

✨ Backend Features

🔐 Authentication & User Management
User registration and login
Secure authentication using tokens/JWT
User profile creation and management

🛣️ Trip Lifecycle Management

Start and end trip handling
Storage of trip start & end locations
Distance and duration tracking
Travel mode recording (walking, train, etc.)
Auto-handling of trip status

🌱 Carbon Emission Calculation
CO₂ emission calculation per trip
Emission metrics based on distance and travel mode
Backend support for eco-impact analysis

📊 Trip History & Analytics

Fetch complete trip history for users
Aggregated trip statistics for dashboards
Monthly and per-trip analytics support


📅 Planned & Scheduled Trips

Backend support for scheduled trips
Enables future trip planning features

🏗️ Backend Architecture (High-Level)
Client (Mobile)
        ↓
   REST APIs
        ↓
 Business Logic (Django Apps)
        ↓
     Database


Each Django app focuses on a specific responsibility, ensuring maintainability and extensibility.

🗂️ Project Structure
Track_Mate/
├── auth_app/        # Authentication & authorization logic
├── profile_app/     # User profile management
├── trips/           # Trip models, APIs, and business logic
├── trackmate/       # Core utilities and project settings
├── manage.py        # Django project entry point
├── requirements.txt # Python dependencies
├── .env             # Environment variables 
└── README.md        # Project documentation

🧰 Technology Stack (Backend)
Component	       Technology
Language	        Python
Framework	        Django
API Framework	    Django REST Framework
Database	        PostgreSQL,SQLite 
Authentication	    Token / JWT-based
Environment Config	 python-dotenv

📡 API Endpoints 
Endpoints may vary based on implementation.

Endpoint	Method	Description
/auth/register/	POST	User registration
/auth/login/	POST	User login
/profile/	    GET	    Retrieve user profile
/trips/start/	POST	Start a trip
/trips/end/	    POST	End a trip
/trips/history/	GET	    Fetch trip history
/stats/	        GET	    Emission & trip analytics