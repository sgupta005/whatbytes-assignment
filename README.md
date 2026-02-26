# WhatBytes Healthcare Backend API

A RESTful healthcare backend API built with **Django REST Framework** and **JWT authentication**. It allows users to manage patients, doctors, and their mappings.

---

## 🚀 Live Deployment

The API is deployed on **AWS (EC2 + RDS PostgreSQL + Nginx + Gunicorn)** and is publicly accessible:

**Base URL:** `http://3.110.158.67`

### Quick Test

You can test the API immediately with these pre-seeded credentials:

| Field | Value |
|-------|-------|
| **Username** | `testuser` |
| **Password** | `TestPass123!` |

```bash
# Login to get a JWT token
curl -X POST http://3.110.158.67/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPass123!"}'
```

> A ready-to-import **Postman collection** is available in the repository as `postman_collection.json`.

---

## Tech Stack

- **Framework**: Django + Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt`
- **Database**: PostgreSQL (AWS RDS)
- **Server**: Gunicorn + Nginx on AWS EC2

---

## Authentication

All endpoints (except registration and login) require a JWT Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

## API Endpoints

### 🔐 Auth — `/api/auth/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register/` | No | Register a new user |
| `POST` | `/api/auth/login/` | No | Login and get JWT tokens |
| `POST` | `/api/auth/token/refresh/` | No | Refresh access token |

#### `POST /api/auth/register/`

**Request body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string (min 8 chars)",
  "first_name": "string",
  "last_name": "string (optional)"
}
```

**Response `201`:**
```json
{
  "user": { "id": 1, "username": "...", "email": "...", "first_name": "...", "last_name": "..." },
  "tokens": { "access": "...", "refresh": "..." }
}
```

#### `POST /api/auth/login/`

**Request body:**
```json
{ "username": "string", "password": "string" }
```

**Response `200`:**
```json
{ "access": "...", "refresh": "..." }
```

#### `POST /api/auth/token/refresh/`

**Request body:**
```json
{ "refresh": "string" }
```

---

### 🧑‍🤝‍🧑 Patients — `/api/patients/`

> All endpoints require authentication. Users can only access their own patients.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/patients/` | List all patients (owned by user) |
| `POST` | `/api/patients/` | Create a new patient |
| `GET` | `/api/patients/{id}/` | Retrieve a patient |
| `PUT` | `/api/patients/{id}/` | Update a patient |
| `PATCH` | `/api/patients/{id}/` | Partially update a patient |
| `DELETE` | `/api/patients/{id}/` | Delete a patient |

**Patient fields:**
```json
{
  "name": "string",
  "age": "integer",
  "gender": "string",
  "phone": "string",
  "email": "string",
  "address": "string",
  "medical_history": "string"
}
```

*Read-only fields:* `id`, `created_by`, `created_at`, `updated_at`

---

### 👨‍⚕️ Doctors — `/api/doctors/`

> All endpoints require authentication. Only the creator can update or delete a doctor.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/doctors/` | List all doctors |
| `POST` | `/api/doctors/` | Create a new doctor |
| `GET` | `/api/doctors/{id}/` | Retrieve a doctor |
| `PUT` | `/api/doctors/{id}/` | Update a doctor (creator only) |
| `PATCH` | `/api/doctors/{id}/` | Partially update a doctor (creator only) |
| `DELETE` | `/api/doctors/{id}/` | Delete a doctor (creator only) |

**Doctor fields:**
```json
{
  "name": "string",
  "specialization": "string",
  "phone": "string",
  "email": "string",
  "experience_years": "integer"
}
```

*Read-only fields:* `id`, `created_by`, `created_at`, `updated_at`

---

### 🔗 Patient-Doctor Mappings — `/api/mappings/`

> All endpoints require authentication. Users can only manage mappings for their own patients.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/mappings/` | List all mappings (for user's patients) |
| `POST` | `/api/mappings/` | Assign a doctor to a patient |
| `GET` | `/api/mappings/{id}/` | Retrieve a specific mapping |
| `DELETE` | `/api/mappings/{id}/` | Remove a mapping (creator only) |
| `GET` | `/api/mappings/{patient_id}/` | List all doctors assigned to a patient |

**Mapping request body:**
```json
{
  "patient": "integer (patient ID)",
  "doctor": "integer (doctor ID)"
}
```

**Mapping response includes nested `patient_detail` and `doctor_detail` objects.**

---

## Setup

```bash
# Install dependencies
uv sync

# Set up environment variables (copy .env.example)
cp .env .env.local

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (`True`/`False`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |

### Seed Sample Data

To populate the database with a test user, sample patients, doctors, and mappings:

```bash
python manage.py seed_data
```

This creates:
- **User:** `testuser` / `TestPass123!`
- **3 Patients:** Amit Patel, Sneha Kapoor, Rohan Gupta
- **3 Doctors:** Dr. Priya Sharma (Cardiologist), Dr. Rajan Mehta (Neurologist), Dr. Sunita Verma (GP)
- **4 Mappings** linking patients to their assigned doctors

The command is idempotent — safe to run multiple times.

---

## Postman Collection

A ready-to-import Postman collection is included at `postman_collection.json`.

**How to use:**
1. Open Postman → **Import** → select `postman_collection.json`
2. Run **Auth → Login** — the access token is saved automatically
3. All other requests use the token automatically via collection variables

The collection points to the live server (`http://3.110.158.67`) by default.
