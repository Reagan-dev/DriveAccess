# DriveAccess
DriveAccess is a complete backend system that enables verified and qualified users to lease different types of vehicles for a reasonable fee.  The platform allows admins to manage vehicles, qualifications, and payments, while drivers can browse available vehicles they qualify for, request leases, and make payments.

## table of contents
- project overview
- Features
- Technologies Used
- Installation
- Environment Variables
- Endpoints
- Deployment
- Contact

## project overview

DriveAccess is a backend system whose aim is to combat unemployment by providing access to affordable vehicle leasing.
Where buying vehicles like motorbikes or public service vans (matatus) is out of reach, DriveAccess provides qualified and vetted users to lease them at low prices.

## features
- User authentication (login and registration based on JWT).
- Role-based access (Admin vs. user).
- Vehicle management (Add, view, update, delete vehicles).
- Lease management (Assign vehicle to user).
- Secure API endpoints.
- payment management

## ERD
https://miro.com/app/board/uXjVJUkaIZk=/?moveToWidget=3458764638363587646&cot=14

## technologies used
Backend: Python, Django, Django REST Framework
Database: PostgreSQL(for production), SQLite (for development)
Authentication: JWT (SimpleJWT)
Tools: Postman for API testing, version control, and Visual Studio Code

## installation
- Clone the repository
- Create and activate a virtual environment
- Install dependencies
- create a superuser
_ run the server

## environment variables

### database url
https://driveaccess-54a0.onrender.com/

## API Endpoints

### Authentication
- *POST* /api/token/
- *POST* /api/token/refresh/

### accounts
- *POST* /api/accounts/register/
- *POST* /api/accounts/login/
- *POST* /api/accounts/logout/

### vehicles
- *GET* /api/vehicles/vehicles/  (all registered users are allowed to view all vehicles)
- *POST* /api/vehicles/vehicles/create/  (only admins are required to create vehicles)
- *PATCH* /api/vehicles/vehicles/<uuid:vehicle_id>/ (again only admins are required)

### qualifications
- *GET* /api/qualifications/qualifications/  (registered users only also admins)
- *POST* /api/qualifications/qualifications/ (users can create qualifications)
- *GET* /api/qualifications/qualifications/<uuid:qualification_id>/  (getting a single qualification)
- *PATCH* /api/qualifications/qualifications/<uuid:qualification_id>/ (updating a qualification. should be registered)
- *DELETE* /api/qualifications/qualifications/<uuid:qualification_id>/
- *POST* /api/qualifications/qualifications/<uuid:qualification_id>/approve/  (only admins can approve payments)

### leases
- *POST* /api/leases/leases/ (create a lease only admins are allowed)
- *PUT* /api/leases/leases/<uuid:lease_id>/  (update a lease onlu admins allowed)
- *DELETE* /api/leases/leases/<uuid:lease_id>/ (delete a lease only admins are allowed)
- *POST* /api/leases/leases/<uuid:lease_id>/approve/  (only admins are allowed to approve a lease)
- *POST* /api/leases/leases/<uuid:lease_id>/reject/  (only admins are allowed to reject lease)
- *POST* /api/leases/leases/<uuid:lease_id>/return/  (only admins are allowed)

### payments
- *POST* /api/peyments/payments/  (only users are allowed to create payments and for the lease they only made)
- *GET* /api/peyments/payments/  (only admins are allowed)
- *GET* /api/payments/payments/<uuid:payment_id>/  (onlu admins)
- *PUT* /api/payments/payments/<uuid:payment_id>/  (only admins are allowed to update payments)
- *DELETE* /api/payments/payments/<uuid:payment_id>/  (only admins)
- *POST*  /api/payments/payments/<uuid:payment_id>/approve/  (only admins)
- *POST*  /api/payments/payments/<uuid:payment_id>/reject/  (onlu admins are allowed to reject payments)

## deployment
host on render

## contacts
- name: Reagan Simiyu
- email: reagansimiyu38@gmail.com
- GitHub: https://github.com/Reagan-dev/

