# Pickleball Platform Backend

A Django-based backend API for a pickleball court management and booking platform.

## Features

- User Management (Registration, Authentication, Profile)
- Court Management (Listing, Booking, Availability)
- Guide Management (Listing, Booking, Availability)
- Review System (Ratings and Comments)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Users

- `POST /users/register/` - Register new user
- `POST /users/login/` - User login
- `GET /users/<id>/` - Get user details
- `PATCH /users/update/<id>/` - Update user information
- `DELETE /users/delete/<id>/` - Delete user

### Courts

- `GET /courts/` - List all courts
- `GET /courts/<id>/` - Get court details
- `GET /courts/available/` - Check court availability
- `POST /courts/book/` - Book a court
- `GET /courts/bookings/` - List court bookings

### Guides

- `GET /guides/` - List all guides
- `GET /guides/<id>/` - Get guide details
- `GET /guides/available/` - Check guide availability
- `POST /guides/book/` - Book a guide
- `GET /guides/bookings/` - List guide bookings

### Reviews

- `GET /reviews/` - List all reviews
- `POST /reviews/create/` - Create a review
- `GET /reviews/<id>/` - Get review details
- `PATCH /reviews/update/<id>/` - Update a review
- `DELETE /reviews/delete/<id>/` - Delete a review

## Deployment

The project is configured for deployment on Vercel. To deploy:

1. Install Vercel CLI:

   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:

   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

## Development Team

- [Your Name] - Project Lead
- [Team Member 1] - Backend Developer
- [Team Member 2] - Backend Developer
- [Team Member 3] - Frontend Developer

## License

This project is licensed under the MIT License - see the LICENSE file for details.
