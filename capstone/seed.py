"""file name - seed.py, project name - capstone, author - S. M. Hussain, date 21st may 2026."""
from bookings.models import Sport, Turf, Booking
from django.contrib.auth import get_user_model
import os
import django
import random
from datetime import datetime, timedelta, date, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstone.settings")
django.setup()

User = get_user_model()


def clear_database():
    print("🧹 Cleaning out old database records...")
    Booking.objects.all().delete()
    Turf.objects.all().delete()
    Sport.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()


def seed_data():
    print("🌱 Initiating localized complex seed process...")

    sports_data = ["Football", "Cricket", "Hockey", "Handball"]
    sport_objects = {}

    for name in sports_data:
        sport, created = Sport.objects.get_or_create(name=name)
        sport_objects[name] = sport
        print(f"   Created Sport: {name}")

    turf_data = [
        {"name": "Complex Arena A - Main Turf", "sports": ["Football", "Hockey"]},
        {"name": "Complex Arena B - Pitch Ground", "sports": ["Cricket", "Football"]},
        {"name": "Complex Court C - Indoor Hardwood", "sports": ["Handball"]},
        {"name": "Complex Court D - Multi-Sport Cage", "sports": ["Cricket", "Handball"]}
    ]

    all_turfs = []
    for t_info in turf_data:
        turf, created = Turf.objects.get_or_create(name=t_info["name"])
        for s_name in t_info["sports"]:
            turf.supported_sports.add(sport_objects[s_name])
        all_turfs.append(turf)
        print(f"   Configured Facility: {turf.name} -> (Supports: {', '.join(t_info['sports'])})")

    print("👤 Generating 50 mock community users...")

    first_names = [
        "Rohit", "Ananya", "Sayantan", "Priya", "Rahul", "Sourav", "Debarati", "Amit",
        "Sneha", "Subham", "Riya", "Ayan", "Arjun", "Pooja", "Vikram", "Neha", "Rajesh",
        "Tanushree", "Deepak", "Sandip", "Abhishek", "Mousumi", "Nilanjan", "Ishita"
    ]
    last_names = [
        "Das", "Kundu", "Banerjee", "Chatterjee", "Mukherjee", "Sen", "Roy", "Dutta",
        "Ghosh", "Sarkar", "Mitra", "Paul", "Choudhury", "Bose", "Guha", "Pal"
    ]

    generated_identities = set()
    user_count = 1

    while len(generated_identities) < 50:
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        username = f"{fn.lower()}_{random.randint(10, 99)}"
        email = f"{username}@example.com"

        if username not in generated_identities:
            generated_identities.add(username)

            strikes = 0
            if user_count in [10, 20]:
                strikes = random.randint(1, 2)
            elif user_count in [30, 40]:
                strikes = 3

            user, created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={
                    "identity_card_number": f"ID-{random.randint(10000, 99999)}",
                    "strike_count": strikes
                }
            )
            if created:
                user.set_password("password123")
                user.save()

            if user_count <= 5 or strikes > 0:
                print(f"   [User {user_count}/50] Created: {user.username} | Member ID: {user.member_id} | Strikes: {user.strike_count} (Status: {'Banned' if user.is_banned else 'Active'})")

            user_count += 1

    print(f"🎉 Success! Complex setup complete. 50 users registered and ready for manual testing.")


if __name__ == "__main__":
    clear_database()
    seed_data()
