import os
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from login.models import User

first_names = [
    "Aarav", "Vivaan", "Aditya", "Krishna", "Aryan",
    "Ishaan", "Kabir", "Om", "Rohan", "Yash",
    "Diya", "Anaya", "Meera", "Saanvi", "Ira",
    "Aadhya", "Kavya", "Avni", "Riya", "Tanya"
]

last_names = [
    "Sharma", "Verma", "Patel", "Reddy", "Iyer",
    "Das", "Jain", "Kapoor", "Malhotra", "Mehta"
]

genders = ["M", "F", "O"]
sexualities = ["Straight", "Gay", "Bisexual", "Prefer not to say"]
used_phones = set()

for i in range(20):
    first = first_names[i]
    last = random.choice(last_names)
    username = f"{first.lower()}{i}"
    email = f"{first.lower()}{last.lower()}@example.com"

    while True:
        phone = f"{random.choice(['9', '8', '7'])}{random.randint(100000000, 999999999)}"
        if phone not in used_phones:
            used_phones.add(phone)
            break

    dob = date(2000 + (i % 5), random.randint(1, 12), random.randint(1, 28))
    gender = random.choice(genders)
    sexuality = random.choice(sexualities)

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            first_name=first,
            last_name=last,
            dob=dob,
            gender=gender,
            sexuality=sexuality,
            password="Test@1234",
            is_active=True,
            phone_verified=True,
            email_verified=True
        )
        print(f"✅ Created: {user.username} | {user.phone}")
    else:
        print(f"⚠️ Already exists: {username}")
