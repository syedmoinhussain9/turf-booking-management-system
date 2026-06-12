# FINAL PROJECT - TurfHub

By **Syed Moin Hussain**

GitHub username: **syedmoinhussain9**
edX username: **syed_0009**

City and Country: Kolkata, West Bengal, India

---

## Video Demo

Video Demo: <URL [HERE](https://youtu.be/OwWzKAw9t5I)>

---

## Description

TurfHub is a full-stack sports facility scheduling and turf reservation management system built using Django and JavaScript. The platform was engineered to simulate a real-world turf operations workflow where multiple users coordinate sports sessions while the backend continuously validates scheduling integrity, player eligibility, and venue availability.

Unlike a traditional CRUD-based booking platform, TurfHub focuses heavily on automated conflict detection and rule enforcement. The system introduces a structured booking pipeline where a user acting as a captain can organize a sports session by selecting a turf, a sport category, a match date, and up to nine teammates. During this process, the application performs both client-side and server-side validation checks to ensure that no invalid or conflicting bookings are allowed into the database.

The application uses Django for backend architecture, relational database modeling, authentication, and validation logic. Vanilla JavaScript is used extensively on the frontend to create a responsive, dynamic user experience without requiring page reloads. AJAX-powered validation calls allow the interface to instantly detect conflicts such as banned players, duplicate teammate selections, or unavailable users already participating in another confirmed booking.

The project also includes a staff moderation and referee verification workflow. Administrators can access a protected verification dashboard where they review active matches and either mark them as completed or issue disciplinary strikes against captains who fail to appear. Once a player accumulates three strikes, the system automatically bans and deactivates the account using logic embedded directly inside the custom Django user model.

The latest version of the project also includes multiple UI and UX improvements compared to the original submission. These include:

* cleaner responsive layouts
* improved warning and notification systems
* dynamic sticky validation banners
* improved navigation flow
* enhanced profile interface
* better booking interaction feedback
* more polished mobile responsiveness

The platform was designed as a realistic sports scheduling environment rather than a demonstration-only academic project.

---

## Distinctiveness and Complexity

The primary objective of TurfHub was not simply to create a booking website, but to create a system capable of enforcing scheduling rules across multiple interconnected entities. During development, one of the largest challenges was ensuring that the application could prevent invalid booking states before they reached the database. This required designing validation logic that operates across users, bookings, sports, and turf facilities simultaneously rather than validating a single form in isolation.

Unlike many web applications where records are largely independent, bookings within TurfHub create dependencies between multiple database objects. A single booking affects facility availability, participant availability, disciplinary eligibility, and future scheduling decisions. As a result, much of the project's complexity comes from managing relationships and constraints rather than from basic CRUD operations.

A significant architectural decision was implementing validation at multiple layers. Client-side JavaScript was used to provide immediate feedback to users and improve usability, while server-side Django validation remained the final authority responsible for enforcing business rules. Maintaining consistency between these layers required careful design because the same scheduling rules needed to be respected regardless of how requests were submitted.

Another source of complexity was the implementation of user moderation as part of the application's core workflow. Rather than treating account management as a separate administrative concern, disciplinary actions directly influence scheduling permissions. This required extending Django's authentication system with custom fields, custom behaviors, and automated restriction logic that affects how users interact with the rest of the platform.

The project also required asynchronous communication between the frontend and backend. JavaScript interacts with dedicated validation endpoints to verify user eligibility and availability before bookings are submitted. This introduced additional complexity because application state must remain synchronized between browser interactions and database records while still preserving data integrity.

From a software engineering perspective, TurfHub combines custom user management, relational database modeling, asynchronous JavaScript interactions, administrative workflows, scheduling conflict detection, and responsive user interfaces into a single system. The complexity of the project comes not from any one individual feature but from the interaction between these components and the business rules that govern them.

For these reasons, I believe TurfHub satisfies the distinctiveness and complexity requirements of the CS50W final project. The project required designing and implementing a rule-driven scheduling system with interconnected workflows, multiple validation layers, custom authentication behavior, and administrative moderation capabilities that extend beyond the functionality developed in previous course projects.


### 1. Multi-User Scheduling Engine

The core complexity of TurfHub comes from its booking coordination system. Each booking connects:

* one captain
* multiple teammates
* one turf
* one sport
* one reserved time window

The backend continuously validates whether:

* a turf is already occupied
* a player is already participating in another confirmed booking
* banned users are being added
* duplicate teammates exist
* the selected turf supports the selected sport
* the booking date is valid
* the team size exceeds allowed limits

This transforms the project into a constraint-driven scheduling engine rather than a simple database form submission system.

### 2. Dual-Layer Validation Architecture

One of the major technical goals of the project was implementing validation at multiple architectural layers.

### 3. Frontend Validation

JavaScript dynamically:

* checks player availability
* prevents duplicate selections
* blocks banned users
* manages dynamic teammate forms
* controls roster size
* displays instant warning feedback

### 4. Backend Validation

Django models and views independently verify:

* overlapping turf reservations
* overlapping player schedules
* invalid booking windows
* unsupported sport selections
* roster restrictions
* disciplinary restrictions

This layered architecture ensures database integrity even if frontend protections are bypassed.

### 5. Custom User Moderation System

The project extends Django’s AbstractUser model to implement:

* custom member IDs
* attendance strike tracking
* automated permanent banning
* account deactivation logic
* profile image support

The moderation workflow directly affects system permissions and booking eligibility, creating interconnected application state management between user behavior and operational access.

### 6. Administrative Referee Verification Workflow

The staff dashboard creates a second operational layer inside the platform.

Staff members can:

* review confirmed bookings
* settle completed matches
* issue disciplinary strikes
* automatically trigger bans

This introduces a workflow-based moderation system instead of a static administration panel.

### 7. Real-Time Availability API

The application includes a dedicated JSON API endpoint used by frontend JavaScript to asynchronously validate player availability.

This system allows the UI to instantly reject invalid bookings before form submission, improving responsiveness and usability while reducing unnecessary server operations.

### 8. Mobile-Responsive UX System

The interface was designed to work across desktop and mobile devices using:

* responsive CSS grids
* adaptive navigation
* dynamic flex layouts
* scalable form structures
* responsive cards and tables

Special focus was placed on usability and operational clarity during live booking workflows.

---

## Project Structure

```text
📦capstone
 ┣ 📂bookings
 ┃ ┣ 📂migrations
 ┃ ┃ ┣ 📜0001_initial.py
 ┃ ┃ ┣ 📜0002_user_profile_picture_url.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂static
 ┃ ┃ ┣ 📂css
 ┃ ┃ ┃ ┗ 📜styles.css
 ┃ ┃ ┗ 📂js
 ┃ ┃ ┃ ┗ 📜booking.js
 ┃ ┣ 📂templates
 ┃ ┃ ┗ 📂bookings
 ┃ ┃ ┃ ┣ 📜admin_dashboard.html
 ┃ ┃ ┃ ┣ 📜base.html
 ┃ ┃ ┃ ┣ 📜bookings.html
 ┃ ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┃ ┣ 📜profile.html
 ┃ ┃ ┃ ┗ 📜register.html
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┗ 📜views.py
 ┣ 📂capstone
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜wsgi.py
 ┣ 📜README.md
 ┣ 📜db.sqlite3
 ┣ 📜manage.py
 ┣ 📜requirements.txt
 ┗ 📜seed.py
```

---

## File Descriptions

## capstone/**init**.py

### Purpose

Marks the `capstone` directory as a Python package.

This file is intentionally empty and allows Python to recognize the folder as an importable package.

### Responsibilities

* Package initialization
* Python module recognition
* Namespace creation

### Dependencies

None.

---

## capstone/asgi.py

### Purpose

ASGI entry point for asynchronous deployments.

### Overview

This file exposes the Django ASGI application object used by modern asynchronous web servers such as:

* Daphne
* Uvicorn
* Hypercorn

ASGI is useful for:

* WebSockets
* Real-time notifications
* Async API processing
* Long-lived connections

---

### Workflow

#### 1. Load Environment Variable

```python
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'capstone.settings'
)
```

Specifies which settings file Django should use.

---

#### 2. Create ASGI Application

```python
application = get_asgi_application()
```

Creates the ASGI callable exposed to the server.

---

### Runtime Flow

```text
Browser
   ↓
ASGI Server (Uvicorn/Daphne)
   ↓
capstone/asgi.py
   ↓
Django Application
   ↓
Views
   ↓
Response
```

---

## capstone/settings.py

### Purpose

Central configuration file for the entire Django project.

---

#### Overview

Controls:

* Installed apps
* Database
* Authentication
* Static files
* Templates
* Middleware
* Security

---

### Project Paths

#### BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

Represents project root directory.

Example:

```text
capstone/
├── bookings/
├── capstone/
├── manage.py
├── db.sqlite3
```

---

## Security Settings

### SECRET_KEY

```python
SECRET_KEY = '...'
```

Used for:

* Session signing
* Password reset tokens
* CSRF protection
* Cryptographic operations

#### Production Note

Should be moved into:

```env
.env
```

and never committed to Git.

---

### DEBUG

```python
DEBUG = True
```

#### Development

Shows:

* Stack traces
* Detailed errors
* Debug pages

#### Production

Must be:

```python
DEBUG = False
```

---

### ALLOWED_HOSTS

```python
ALLOWED_HOSTS = []
```

Specifies valid domains.

Example:

```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "yourdomain.com"
]
```

---

## Installed Applications

```python
INSTALLED_APPS
```

### Custom App

```python
bookings
```

Contains:

* Models
* Views
* Templates
* Business logic

---

### Django Core Apps

#### admin

Administrative dashboard.

#### auth

Authentication system.

#### contenttypes

Model metadata.

#### sessions

Session management.

#### messages

Flash messages.

#### staticfiles

Static asset handling.

---

#### Middleware Stack

Middleware executes before and after requests.

---

#### SecurityMiddleware

Security enhancements.

---

#### SessionMiddleware

Manages user sessions.

---

#### CommonMiddleware

URL normalization and common HTTP processing.

---

#### CsrfViewMiddleware

Prevents CSRF attacks.

---

#### AuthenticationMiddleware

Associates users with requests.

---

#### MessageMiddleware

Enables Django messages framework.

---

#### XFrameOptionsMiddleware

Protects against clickjacking.

---

## Template Configuration

```python
TEMPLATES
```

#### APP_DIRS

```python
True
```

Automatically discovers:

```text
templates/
```

folders inside applications.

---

## Database Configuration

### Engine

```python
sqlite3
```

#### Database File

```python
db.sqlite3
```

Location:

```text
project_root/db.sqlite3
```

---

### Purpose

Stores:

* Users
* Sports
* Turfs
* Bookings
* Sessions
* Authentication data

---

## Password Validation

Validators enabled:

#### UserAttributeSimilarityValidator

Prevents passwords similar to usernames.

---

#### MinimumLengthValidator

Enforces minimum password length.

---

#### CommonPasswordValidator

Blocks common passwords.

---

#### NumericPasswordValidator

Blocks numeric-only passwords.

---

## Internationalization

### Language

```python
LANGUAGE_CODE = 'en-us'
```

---

### Timezone

```python
TIME_ZONE = 'UTC'
```

---

### Localization

```python
USE_I18N = True
USE_TZ = True
```

---

## Static Files

### URL Prefix

```python
STATIC_URL = 'static/'
```

---

### Static Directory

```python
STATICFILES_DIRS
```

Points to:

```text
bookings/static/
```

Contains:

```text
CSS
JavaScript
Images
Icons
```

---

## Custom User Model

```python
AUTH_USER_MODEL = 'bookings.User'
```

Tells Django to use:

```python
bookings.models.User
```

instead of:

```python
django.contrib.auth.models.User
```

---

## capstone/urls.py

### Purpose

Central URL router for the application.

---

## URL Routing Table

| URL                   | View                         | Purpose            |
| --------------------- | ---------------------------- | ------------------ |
| /                     | index                        | Landing page       |
| /profile/             | profile_view                 | User profile       |
| /sandbox/             | sandbox_dashboard            | Booking simulator  |
| /login/               | login_view                   | Login              |
| /register/            | register_view                | Registration       |
| /logout/              | logout_view                  | Logout             |
| /api/check-player/    | check_player_availability    | Availability API   |
| /booking/cancel/<id>/ | cancel_booking               | Cancel booking     |
| /staff/verify/        | admin_verification_dashboard | Verification panel |
| /admin/               | Django Admin                 | Administration     |

---

## Request Flow

```text
Browser
   ↓
urls.py
   ↓
View Function
   ↓
Model Query
   ↓
Template Rendering
   ↓
Response
```

---

## capstone/wsgi.py

### Purpose

WSGI deployment entry point.

---

### Overview

Used by traditional web servers:

* Gunicorn
* Apache mod_wsgi
* uWSGI

---

### Runtime Flow

```text
Browser
   ↓
NGINX
   ↓
Gunicorn
   ↓
wsgi.py
   ↓
Django
```

---

### Application Object

```python
application = get_wsgi_application()
```

Creates WSGI callable.

---

## manage.py

### Purpose

Command-line management utility.

---

### Responsibilities

Provides access to:

```bash
python manage.py runserver
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
python manage.py shell
python manage.py test
```

---

### Execution Flow

```text
Terminal Command
   ↓
manage.py
   ↓
Django Management System
   ↓
Requested Operation
```

---

## seed.py

### Purpose

Automated database population utility.

---

### Objective

Creates realistic testing data including:

* Sports
* Facilities
* Users
* Strike records

---

## Seed Pipeline

```text
Clear Existing Data
        ↓
Create Sports
        ↓
Create Turfs
        ↓
Assign Supported Sports
        ↓
Generate 50 Users
        ↓
Assign Strike Records
        ↓
Save Credentials
```

---

## clear_database()

### Purpose

Removes existing seed data.

#### Deletes

```python
Booking
Turf
Sport
Users
```

#### Preserves

```python
Superusers
```

---

## seed_data()

### Purpose

Populates application data.

---

### Stage 1

Create Sports

```text
Football
Cricket
Hockey
Handball
```

---

### Stage 2

Create Facilities

#### Arena A

Supports:

```text
Football
Hockey
```

#### Arena B

Supports:

```text
Cricket
Football
```

#### Court C

Supports:

```text
Handball
```

#### Court D

Supports:

```text
Cricket
Handball
```

---

### Stage 3

Generate Users

Creates:

```text
50 Mock Players
```

Generated from random combinations of:

```text
First Names
Last Names
```

---

### Stage 4

Assign Strike Records

#### User Groups

| Users | Strikes |
| ----- | ------- |
| 1-9   | 0       |
| 10    | 1-2     |
| 20    | 1-2     |
| 30    | 3       |
| 40    | 3       |

---

### Auto-Ban Testing

Users with:

```python
strike_count >= 3
```

become:

```python
is_banned = True
is_active = False
```

allowing moderation logic to be tested.

---

### Default Credentials

All generated users receive:

```text
Password:
password123
```

---

### Execution

Run:

```bash
python seed.py
```

---

## db.sqlite3

### Purpose

Primary SQLite database file.

---

### Stores

#### Authentication

* Users
* Password hashes
* Sessions
* Permissions

#### Booking System

* Sports
* Turfs
* Bookings
* Teammates

#### Administrative Data

* Admin users
* Strike records
* Ban status

---

### Lifecycle

```text
Models
   ↓
Migrations
   ↓
SQLite Database
   ↓
Queries
   ↓
Application
```

---

## Project Startup Sequence

```text
manage.py runserver
        ↓
settings.py loads
        ↓
urls.py loads
        ↓
Middleware initializes
        ↓
Database connects
        ↓
Application starts
        ↓
User Requests Processed
```

## `bookings/__init__.py`

This file marks the `bookings` directory as a Python package. No custom code was added to this file.

## `bookings/admin.py`

Configures Django's administrative interface for the project.

This file registers all major application models (`User`, `Sport`, `Turf`, and `Booking`) with Django's admin panel and extends Django's built-in `UserAdmin` class through a custom `CustomUserAdmin` implementation.

Additional administrative controls were added for:

* Member identification numbers
* Identity card numbers
* Strike tracking
* Ban status management

The customized admin interface allows staff members to manage player disciplinary records and monitor user status directly through Django's administration dashboard.

## `bookings/apps.py`

Application configuration file generated by Django.

This file defines the `BookingsConfig` class and registers the bookings application with the Django project. No significant custom logic was added.

## `bookings/models.py`

This file contains the core database architecture and business rules of TurfHub.

The application uses four primary models:

### User Model

A custom user model extending Django's `AbstractUser`.

Additional fields include:

* Member ID generation
* Identity card number storage
* Strike tracking
* Ban status tracking
* Profile picture URL support

The model also contains custom save logic that automatically:

* Generates unique member IDs for newly registered users
* Automatically bans users who accumulate three strikes
* Disables banned accounts by setting `is_active=False`

### Sport Model

Represents individual sports available within the platform.

Sports are linked to turf facilities and booking records through relational database relationships.

### Turf Model

Represents available sports facilities.

Each turf maintains a many-to-many relationship with supported sports, allowing the system to enforce sport-specific facility restrictions.

### Booking Model

Represents scheduled sports sessions.

This model stores:

* Captain assignments
* Teammate rosters
* Turf reservations
* Sport selections
* Match dates
* Start and end times
* Booking status information

The model contains extensive validation logic through custom `clean()` methods.

Validation rules include:

* End time must occur after start time
* Selected sport must be supported by the chosen turf
* Turf scheduling conflicts are prohibited
* Overlapping reservations are automatically rejected

The model also overrides the save process to ensure validation executes before database persistence.

Because many of the platform's scheduling rules are enforced directly within this model, it serves as the primary business-rule enforcement layer of the application.

## `bookings/tests.py`

Default Django testing file generated during project creation.

No custom automated tests were implemented for this project.

## `bookings/views.py`

This file contains the primary application workflow and request-handling logic.

The views coordinate interactions between users, templates, models, and validation systems.

Major views include:

### `index()`

Renders the landing page and provides facility information to visitors. The view also checks whether the authenticated user is currently banned.

### `login_view()`

Handles user authentication using Django's authentication framework and provides login feedback messages.

### `register_view()`

Processes new user registration, validates submitted credentials, creates accounts, and automatically authenticates newly registered users.

### `logout_view()`

Handles session termination and user logout functionality.

### `profile_view()`

Provides the user dashboard.

This view allows users to:

* Update profile pictures
* View strike counts
* Review upcoming matches
* Inspect booking history
* Monitor participation statistics

### `cancel_booking()`

Allows captains to cancel their own confirmed bookings while preventing modifications to already completed or cancelled sessions.

### `admin_verification_dashboard()`

Provides the administrative moderation workflow.

Staff members can:

* Review active bookings
* Mark matches as completed
* Issue disciplinary strikes for attendance violations

This workflow directly interacts with the strike and banning system implemented in the custom user model.

### `check_player_availability()`

AJAX endpoint used by the frontend validation system.

The endpoint checks:

* Player availability
* Existing booking conflicts
* Ban status

The JavaScript booking interface calls this endpoint in real time to prevent invalid roster selections before form submission.

### `sandbox_dashboard()`

The largest and most complex view in the application.

This view implements the complete booking creation workflow and performs extensive validation including:

* Team size limits
* Date validation
* Turf scheduling conflicts
* Banned player detection
* Duplicate participation prevention
* Captain eligibility verification
* Booking creation
* Teammate assignment

The view also supplies all dynamic data required by the booking dashboard, including users, sports, facilities, and recent booking activity.

Because it coordinates frontend interactions, backend validation, database persistence, and scheduling enforcement, this view represents the operational core of TurfHub.

---



## bookings/migrations/0001_initial.py

This migration file was generated automatically by Django based on the database models that I designed in models.py. It creates the initial database schema for the application, including the custom User model, Sport model, Turf model, and Booking model. The migration establishes the relationships between these models, including foreign key and many-to-many associations used throughout the booking system.

## bookings/migrations/0002_user_profile_picture_url.py

This migration file was generated by Django after I added support for profile picture URLs within the custom User model. It updates the database schema by introducing a new URLField used for storing user profile image links.

## Static

### bookings/static/js/booking.js

This file contains the client-side booking validation system. It dynamically manages captain selection, teammate selection, roster size enforcement, duplicate player detection, availability checks, and warning notifications. The file communicates asynchronously with a Django API endpoint using fetch requests to determine whether selected users are banned or already committed to another booking on the same date.

The script also manages dynamic creation and removal of teammate input fields, automatic population of logged-in user information, date-based validation updates, and responsive warning banners. Much of the application's interactive behavior is implemented in this file, allowing users to receive immediate feedback before submitting a booking request.

Key responsibilities include:

* Dynamic captain selection
* Dynamic teammate management
* Duplicate teammate detection
* Team size enforcement
* Player availability verification through AJAX requests
* Banned player detection
* Date-sensitive booking validation
* Warning banner management
* Automatic form state updates
* Client-side scheduling conflict prevention

### bookings/static/css/styles.css

This file contains the custom styling used throughout the TurfHub booking dashboard. It defines responsive layouts that switch between stacked mobile views and multi-column desktop layouts. The stylesheet includes custom card components, booking tables, form controls, status badges, warning banners, user availability indicators, teammate management controls, and dashboard presentation elements.

Special attention was given to mobile responsiveness through media queries and adaptive layouts. The stylesheet was designed to improve usability during the booking workflow while maintaining visual consistency across different screen sizes.

## Templates

### `templates/bookings/base.html`

The main layout template used throughout the application. It contains the shared navigation bar, Bootstrap integration, static asset loading, authentication-aware navigation controls, and reusable page structure inherited by all other templates.

### `templates/bookings/index.html`

The landing page of TurfHub. This template displays available sports facilities, presents the platform overview, and provides navigation entry points for registration, login, and booking operations. Dynamic facility information is rendered using data supplied from Django views.

### `templates/bookings/login.html`

Provides the user authentication interface. This template renders the login form, displays authentication error messages, and submits credentials to Django's authentication system.

### `templates/bookings/register.html`

Handles new user registration. The page collects account credentials, validates user input through backend processing, and provides feedback when registration errors occur.

### `templates/bookings/bookings.html`

The primary scheduling interface of the application. This template contains the complete booking workflow, including captain selection, teammate selection, turf selection, sport selection, date and time scheduling, user status monitoring, booking history display, and frontend integration with JavaScript-based validation systems.

The page also contains the dynamic datalist used for user searching and serves as the main interface for testing booking conflict detection and scheduling rules.

### `templates/bookings/profile.html`

Provides the authenticated user dashboard. Users can update their profile picture URL, review strike counts, view upcoming matches, inspect booking history, and manage bookings for which they are designated as captain.

The page combines account management functionality with scheduling information in a single profile interface.

### `templates/bookings/admin_dashboard.html`

Administrative moderation interface used by referee or staff accounts. This dashboard allows administrators to review scheduled matches, mark matches as completed, and issue disciplinary strikes to captains who fail attendance verification.

This template serves as the operational management component of the platform's moderation system.

---

## How to Run the Application

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 3. Create administrator account

```bash
python manage.py createsuperuser
```

---

### 4. Run the development server

```bash
python manage.py runserver
```

---

### 5. Open application

Visit:

```text
http://127.0.0.1:8000/
```

---

## Requirements

```text
Django>=6.0.5
asgiref>=3.7.2
sqlparse>=0.4.4
tzdata>=2023.3
```

---

## Additional Notes

* The system uses Django’s authentication framework with a custom extended user model.
* Validation exists both on the frontend and backend for reliability and security.
* JavaScript improves UX but does not replace backend validation.
* The project was intentionally designed around operational scheduling logic instead of social interaction systems or e-commerce workflows.
* The application architecture is modular and can be extended in the future with:

  * payment systems
  * analytics dashboards
  * automated scheduling optimization
  * notification systems
  * REST API integrations
