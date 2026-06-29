# Studio Freelance Marketplace

A fully functional, modern freelance marketplace platform built with Django. This platform connects clients with top-tier freelancers and creators.

## Features

- **Multi-Tenant Architecture**: Supports dual roles—Freelancers (Workers) and Clients (Employers).
- **Social Authentication**: Secure, one-click sign in using Google and GitHub via `django-allauth`.
- **Worker Profiles & Portfolios**: Freelancers can showcase their skills, set hourly rates, and upload multimedia portfolio items (images and videos).
- **Client Booking System**: Clients can easily find talent and submit detailed project booking requests.
- **Admin Approval Gate**: All new worker profiles go into a "Pending Review" state. They remain hidden from the marketplace until approved by the platform administrator to ensure quality.
- **Dual Dashboards**: 
  - *Worker Dashboard*: Manage incoming client requests and connect developer GitHub profiles.
  - *Client Dashboard*: Track the status of sent booking requests.
- **Modern UI**: Sleek, responsive, dark-themed UI built with custom CSS and Google Fonts (Inter).

## Technology Stack
- **Backend**: Python, Django
- **Authentication**: `django-allauth` (Google, GitHub OAuth2)
- **Database**: SQLite (default, easily portable to PostgreSQL)
- **Frontend**: HTML5, Vanilla CSS

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Abdallh312/Bookingses.git
cd Bookingses
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Ensure `django`, `django-allauth`, `pillow`, and `requests` are installed)*

### 4. Setup the Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver 8080
```
Navigate to `http://127.0.0.1:8080/` to view the site!

## Social Authentication Setup
To activate Google and GitHub sign-ins:
1. Log into the Django Admin at `/admin/`.
2. Under **Social Accounts > Social applications**, add a new application.
3. Choose the provider (Google/GitHub), and paste your `Client ID` and `Secret Key`.
4. Add your site (`example.com`) to the "Chosen sites" box and save.
