# FINAL PROJECT - TurfHub

By **Syed Moin Hussain**

GitHub username: **syedmoinhussain9**
edX username: **syed_0009**

City and Country: Kolkata, West Bengal, India

---

## Video Demo

Video Demo: <URL [HERE](https://youtu.be/OwWzKAw9t5I)>

---

# Description

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

# Distinctiveness and Complexity

This project is intentionally designed to be structurally and functionally different from all previous CS50W projects.

First, TurfHub is not a social network. There are no social feeds, posts, likes, messaging systems, followers, or community interactions. Instead, the entire platform revolves around real-time sports scheduling operations and multi-user booking validation.

Second, TurfHub is not an e-commerce application. There are no products, payments, carts, bidding systems, or checkout pipelines involving financial transactions. The platform instead functions as a scheduling and operations management system focused on enforcing turf reservation integrity.

The project introduces complexity through multiple interconnected engineering systems.

## Multi-User Scheduling Engine

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

## Dual-Layer Validation Architecture

One of the major technical goals of the project was implementing validation at multiple architectural layers.

### Frontend Validation

JavaScript dynamically:

* checks player availability
* prevents duplicate selections
* blocks banned users
* manages dynamic teammate forms
* controls roster size
* displays instant warning feedback

### Backend Validation

Django models and views independently verify:

* overlapping turf reservations
* overlapping player schedules
* invalid booking windows
* unsupported sport selections
* roster restrictions
* disciplinary restrictions

This layered architecture ensures database integrity even if frontend protections are bypassed.

## Custom User Moderation System

The project extends Django’s AbstractUser model to implement:

* custom member IDs
* attendance strike tracking
* automated permanent banning
* account deactivation logic
* profile image support

The moderation workflow directly affects system permissions and booking eligibility, creating interconnected application state management between user behavior and operational access.

## Administrative Referee Verification Workflow

The staff dashboard creates a second operational layer inside the platform.

Staff members can:

* review confirmed bookings
* settle completed matches
* issue disciplinary strikes
* automatically trigger bans

This introduces a workflow-based moderation system instead of a static administration panel.

## Real-Time Availability API

The application includes a dedicated JSON API endpoint used by frontend JavaScript to asynchronously validate player availability.

This system allows the UI to instantly reject invalid bookings before form submission, improving responsiveness and usability while reducing unnecessary server operations.

## Mobile-Responsive UX System

The interface was designed to work across desktop and mobile devices using:

* responsive CSS grids
* adaptive navigation
* dynamic flex layouts
* scalable form structures
* responsive cards and tables

Special focus was placed on usability and operational clarity during live booking workflows.

---

# Project Structure

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

# File Descriptions

## models.py

Contains all database models:

* Custom User model
* Sport model
* Turf model
* Booking model

Implements:

* booking overlap detection
* automated banning logic
* validation rules
* relational model constraints

---

## views.py

Handles:

* authentication
* booking creation
* booking cancellation
* profile rendering
* referee verification workflows
* API responses
* scheduling validation

This file contains the majority of the application business logic.

---

## booking.js

Implements frontend interaction systems:

* asynchronous availability checking
* dynamic teammate generation
* roster validation
* duplicate prevention
* sticky warning banners
* booking UI interactivity

---

## styles.css

Contains:

* responsive layout system
* navigation styling
* dashboard layouts
* alerts and notification styling
* mobile responsiveness
* profile and booking interface styling

---

## admin.py

Customizes Django admin panel with:

* strike visibility
* moderation controls
* user restriction management

---

## seed.py

Used to populate the database with initial sports, turfs, and testing data during development.

---

# How to Run the Application

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 3. Create administrator account

```bash
python manage.py createsuperuser
```

---

## 4. Run the development server

```bash
python manage.py runserver
```

---

## 5. Open application

Visit:

```text
http://127.0.0.1:8000/
```

---

# Requirements

```text
Django>=5.0,<6.0
asgiref>=3.7.2
sqlparse>=0.4.4
tzdata>=2023.3
```

---

# Additional Notes

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
