import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping


class Command(BaseCommand):
    help = "Seeds the database with sample data for demonstration/testing purposes"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database with sample data...")

        # Create test user
        user, created = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "testuser@example.com",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        if created:
            user.set_password("TestPass123!")
            user.save()
            self.stdout.write(self.style.SUCCESS("  ✓ Created user: testuser / TestPass123!"))
        else:
            self.stdout.write(self.style.WARNING("  ~ User 'testuser' already exists, skipping."))

        # Create doctors
        doctors_data = [
            {
                "name": "Dr. Priya Sharma",
                "specialization": "Cardiologist",
                "phone": "9988776655",
                "email": "priya.sharma@hospital.com",
                "experience_years": 12,
            },
            {
                "name": "Dr. Rajan Mehta",
                "specialization": "Neurologist",
                "phone": "9876543210",
                "email": "rajan.mehta@hospital.com",
                "experience_years": 8,
            },
            {
                "name": "Dr. Sunita Verma",
                "specialization": "General Physician",
                "phone": "9123456789",
                "email": "sunita.verma@hospital.com",
                "experience_years": 15,
            },
        ]
        doctors = []
        for d in doctors_data:
            doc, created = Doctor.objects.get_or_create(
                email=d["email"],
                defaults={**d, "created_by": user},
            )
            doctors.append(doc)
            status = "✓ Created" if created else "~ Already exists"
            self.stdout.write(
                self.style.SUCCESS(f"  {status}: Doctor '{doc.name}'")
                if created
                else f"  {status}: Doctor '{doc.name}'"
            )

        # Create patients
        patients_data = [
            {
                "name": "Amit Patel",
                "age": 45,
                "gender": "M",
                "phone": "9001234567",
                "email": "amit.patel@example.com",
                "address": "12 Gandhi Nagar, Ahmedabad",
                "medical_history": "Type 2 diabetes, controlled with medication",
            },
            {
                "name": "Sneha Kapoor",
                "age": 32,
                "gender": "F",
                "phone": "9112345678",
                "email": "sneha.kapoor@example.com",
                "address": "88 Bandra West, Mumbai",
                "medical_history": "Hypertension, allergic to penicillin",
            },
            {
                "name": "Rohan Gupta",
                "age": 28,
                "gender": "M",
                "phone": "9223456789",
                "email": "rohan.gupta@example.com",
                "address": "34 Koramangala, Bengaluru",
                "medical_history": "No significant history",
            },
        ]
        patients = []
        for p in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=p["email"],
                defaults={**p, "created_by": user},
            )
            patients.append(patient)
            status = "✓ Created" if created else "~ Already exists"
            self.stdout.write(
                self.style.SUCCESS(f"  {status}: Patient '{patient.name}'")
                if created
                else f"  {status}: Patient '{patient.name}'"
            )

        # Create mappings: assign multiple doctors per patient
        mappings = [
            (patients[0], doctors[0]),  # Amit → Dr. Priya (Cardiologist)
            (patients[0], doctors[2]),  # Amit → Dr. Sunita (GP)
            (patients[1], doctors[1]),  # Sneha → Dr. Rajan (Neurologist)
            (patients[2], doctors[2]),  # Rohan → Dr. Sunita (GP)
        ]
        for patient, doctor in mappings:
            mapping, created = PatientDoctorMapping.objects.get_or_create(
                patient=patient,
                doctor=doctor,
            )
            status = "✓ Created" if created else "~ Already exists"
            self.stdout.write(
                self.style.SUCCESS(f"  {status}: Mapping {patient.name} → {doctor.name}")
                if created
                else f"  {status}: Mapping {patient.name} → {doctor.name}"
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Done! Seed data loaded successfully."))
        self.stdout.write("")
        self.stdout.write("Test credentials:")
        self.stdout.write("  Username: testuser")
        self.stdout.write("  Password: TestPass123!")
        self.stdout.write("  Login at: /api/auth/login/")
