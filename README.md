# DriveAccess

> A qualification-gated vehicle leasing backend — connecting verified drivers to affordable Matatu and Motorcycle leases across the East African market.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.3-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.0-092E20?style=flat-square&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com/)

**Live API:** `https://driveaccess-54a0.onrender.com`
&nbsp;·&nbsp;
**ERD:** [View on Miro](https://miro.com/app/board/uXjVJUkaIZk=/)

---

## Overview

DriveAccess solves a real access problem in the East African transport sector: qualified drivers — those holding valid driving and PSV licences — often can't afford to own the vehicles they're licensed to operate. DriveAccess acts as the backend infrastructure connecting those drivers to vehicle owners, with an admin-supervised approval layer ensuring safety, compliance, and accountability at every step.

The platform manages the full leasing lifecycle: user registration → qualification submission and admin verification → vehicle browsing → lease application → payment processing — all through a clean, role-scoped REST API.

---

## Architecture

### Layered Architecture with Domain-Separated Django Apps

```
driveaccess_backend/
├── accounts/          # Custom user model, registration, JWT auth
├── vehicles/          # Vehicle inventory, types, status management
├── qualifications/    # Driver licence submission and admin approval
├── leases/            # Lease lifecycle — creation, approval, return
└── payments/          # Payment initiation, approval, and tracking
```

### Request Flow

```
Client Request
      │
      ▼
┌─────────────────────────────────────────────────┐
│              Django Middleware                  │
│  CORS Headers · CSRF · Security · CSP           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           JWT Authentication Layer              │
│    Token validation · Role check (admin/user)   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│         DRF Views + Serializers                 │
│   Business logic · Input validation · RBAC      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           Django ORM → PostgreSQL               │
│   UUID PKs · FK constraints · Status fields     │
└─────────────────────────────────────────────────┘
```

---

## Key Features

- **Qualification-Gated Leasing** — drivers must submit and receive admin approval for a `driving_license` or `PSV_license` before they can lease any vehicle
- **Vehicle Type Matching** — fleet includes Matatus and Motorcycles; availability exposed via filterable public endpoint
- **Admin-Supervised Lifecycle** — leases, qualification approvals, and payments all go through explicit admin approve/reject actions — nothing advances automatically
- **Role-Based Access Control** — clean separation between admin capabilities (fleet management, approvals) and user capabilities (qualification submission, payments)
- **Flexible Lease Pricing** — `hourly`, `daily`, and `weekly` lease types with cost computed from the vehicle's `hourly_rate`
- **Payment Tracking** — supports `credit_card`, `mobile_money`, and `bank_transfer`; payment status transitions from `pending` → `completed` or `failed`
- **JWT Auth with Rotation** — 5-minute access tokens, 1-day refresh tokens, automatic rotation, and blacklisting on logout
- **Live and Deployed** — production deployment on Render with managed PostgreSQL, Gunicorn, and WhiteNoise static serving

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.2.3 + Django REST Framework 3.16.0 |
| Authentication | JWT (SimpleJWT 5.5.1) — rotation + blacklisting |
| Database | SQLite (dev) · PostgreSQL (production) |
| Validation | Pydantic 2.11.7 + DRF serializers |
| Deployment | Render (PaaS) + Gunicorn 23.0.0 |
| Static Files | WhiteNoise 6.9.0 with compression |
| Image Handling | Pillow 11.3.0 |
| Security | django-cors-headers · django-csp · PBKDF2 password hashing |

---

## Database Schema

```
User (UUID PK — email-based auth)
 ├── name, phone_number (unique), is_admin, is_verified
 ├── Qualification (1:many)
 │    ├── qualification_type: driving_license | PSV_license
 │    ├── issue_date, expiry_date
 │    └── approved: bool (set by admin)
 ├── Lease (1:many)
 │    ├── vehicle_id (FK → Vehicle)
 │    ├── lease_type: hourly | daily | weekly
 │    ├── status: pending | active | returned | rejected
 │    ├── start_time, end_time, total_cost
 │    └── Payment (1:many)
 │         ├── amount, payment_method, payment_date
 │         └── status: pending | completed | failed
 └── Payment (1:many — direct reference)

Vehicle (UUID PK)
 ├── type: matatu | motorcycle
 ├── model, licence_plate (unique), location
 ├── hourly_rate (decimal)
 └── status: available | leased | maintenance
```

**Key constraints:**
- One active lease per vehicle at a time — enforced at the application layer
- Payments must reference the authenticated user's own leases — no cross-user payment creation
- Qualification approval is a prerequisite for lease eligibility
- All PKs are UUIDs — prevents ID enumeration across vehicles, leases, and payment records

---

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL (production) or SQLite (development — works out of the box)

### Installation

```bash
# Clone the repository
git clone https://github.com/Reagan-dev/DriveAccess.git
cd DriveAccess

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root. See `.env.example` for all required variables:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (omit to use SQLite in development)
DATABASE_URL=postgresql://user:password@localhost:5432/driveaccess_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Run the Application

```bash
# Apply migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

API available at `http://localhost:8000`.

---

## API Overview

All endpoints are prefixed with `/api/`. Authentication uses `Authorization: Bearer <access_token>`.

### Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/accounts/register/` | Register a new driver account | No |
| `POST` | `/api/token/` | Login — returns JWT access + refresh | No |
| `POST` | `/api/token/refresh/` | Refresh access token | No |
| `POST` | `/api/accounts/logout/` | Blacklist refresh token | Required |

### Vehicles

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/vehicles/vehicles/` | List vehicles — filterable by type and status | No |
| `POST` | `/api/vehicles/vehicles/create/` | Add vehicle to fleet | Admin |
| `PATCH` | `/api/vehicles/vehicles/<uuid>/` | Update vehicle details or status | Admin |

### Qualifications

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/qualifications/qualifications/` | List qualifications | Required |
| `POST` | `/api/qualifications/qualifications/` | Submit a licence for verification | Required |
| `GET` | `/api/qualifications/qualifications/<uuid>/` | Get qualification detail | Required |
| `PATCH` | `/api/qualifications/qualifications/<uuid>/` | Update qualification | Required |
| `DELETE` | `/api/qualifications/qualifications/<uuid>/` | Remove qualification | Required |
| `POST` | `/api/qualifications/qualifications/<uuid>/approve/` | Approve qualification | Admin |

### Leases

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/leases/leases/` | Create a lease for a qualified driver | Admin |
| `PUT` | `/api/leases/leases/<uuid>/` | Update lease details | Admin |
| `DELETE` | `/api/leases/leases/<uuid>/` | Delete lease | Admin |
| `POST` | `/api/leases/leases/<uuid>/approve/` | Activate lease | Admin |
| `POST` | `/api/leases/leases/<uuid>/reject/` | Reject lease application | Admin |
| `POST` | `/api/leases/leases/<uuid>/return/` | Mark vehicle as returned | Admin |

### Payments

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/payments/payments/` | Initiate payment for own lease | User |
| `GET` | `/api/payments/payments/` | List payments (own only for users, all for admin) | Required |
| `GET` | `/api/payments/payments/<uuid>/` | Get payment detail | Required |
| `PUT` | `/api/payments/payments/<uuid>/` | Update payment | Admin |
| `DELETE` | `/api/payments/payments/<uuid>/` | Delete payment | Admin |
| `POST` | `/api/payments/payments/<uuid>/approve/` | Mark payment completed | Admin |
| `POST` | `/api/payments/payments/<uuid>/reject/` | Mark payment failed | Admin |

### Example: Register and Submit a Qualification

```bash
# 1. Register a driver account
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "driver@example.com",
    "name": "John Kamau",
    "phone_number": "+254712345678",
    "password": "securepass123"
  }'

# 2. Login to get tokens
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "driver@example.com", "password": "securepass123"}'

# 3. Submit driving licence for verification
curl -X POST http://localhost:8000/api/qualifications/qualifications/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "qualification_type": "PSV_license",
    "issue_date": "2022-06-01",
    "expiry_date": "2027-06-01"
  }'
```

---

## Core Workflows

### Driver Onboarding → First Lease

```
Register account
    → Submit qualification (driving_license / PSV_license)
        → Admin approves qualification
            → Admin creates lease (assigns vehicle + lease type)
                → Admin approves lease → status: active
                    → Driver initiates payment
                        → Admin approves payment → status: completed
                            → Driver returns vehicle → status: returned
```

### Lease State Machine

```
        [Admin creates]
              │
              ▼
           PENDING
          /        \
    [approve]     [reject]
        │               │
        ▼               ▼
      ACTIVE         REJECTED
        │
    [return]
        │
        ▼
     RETURNED
```

### Vehicle Status Transitions

```
AVAILABLE → [lease approved] → LEASED → [vehicle returned] → AVAILABLE
AVAILABLE → [admin action]   → MAINTENANCE → [admin action] → AVAILABLE
```

---

## Role Permissions Summary

| Action | Driver (User) | Admin |
|---|---|---|
| Browse vehicles | ✅ | ✅ |
| Submit qualification | ✅ | ✅ |
| Approve qualification | ❌ | ✅ |
| Create / manage leases | ❌ | ✅ |
| Approve / reject leases | ❌ | ✅ |
| Initiate payment | ✅ (own leases only) | ✅ |
| Approve / reject payment | ❌ | ✅ |
| Manage vehicle fleet | ❌ | ✅ |
| View all payments | ❌ | ✅ |

---

## Design Decisions

**Why admin-supervised approvals for leases and payments?** DriveAccess operates in a domain (public service vehicles) where regulatory compliance is a legal requirement — not a UX choice. Requiring admin sign-off on qualifications and lease activations creates an explicit accountability layer that a fully automated flow cannot provide.

**Why qualification-gated leasing?** A Matatu or Motorcycle lease to an unqualified driver is a liability, not a product. The `approved` boolean on the Qualification model is the enforcement point — unapproved qualifications block lease eligibility at the business logic layer.

**Why `hourly_rate` as the base pricing unit?** Daily and weekly rates are computed as multiples of the hourly rate, keeping pricing flexible without requiring separate rate fields per lease type. Changing a vehicle's rate updates all future cost calculations automatically.

**Why UUID PKs?** Sequential integer IDs on lease or payment records would allow any authenticated user to probe other users' financial data by guessing IDs. UUIDs make enumeration attacks computationally infeasible.

---

## Project Structure

```
DriveAccess/
├── accounts/              # Custom AbstractBaseUser, email auth, JWT
├── vehicles/              # Vehicle model, fleet management views
├── qualifications/        # Licence submission, approval workflow
├── leases/                # Lease model, lifecycle views, state transitions
├── payments/              # Payment model, multi-method processing
├── driveaccess_backend/   # Django settings, root URLs, WSGI
├── requirements.txt
├── .env.example
├── Procfile               # gunicorn driveaccess_backend.wsgi:application
└── manage.py
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built with Django REST Framework · PostgreSQL · Deployed on Render*
*Targeting the East African transport and vehicle leasing market*
