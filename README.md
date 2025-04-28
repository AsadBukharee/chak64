# Chak64 API

A Django REST Framework API for managing community posts, problems, campaigns, and donations.

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_app_password
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh JWT token

### Users
- `POST /api/users/register/` - Register a new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user information
- `GET /api/users/verify/{cnic}/` - Verify a resident by CNIC

### Posts
- `GET /api/posts/` - List all posts
- `GET /api/posts/recent/` - List recent posts
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/` - Create a new post (authenticated)
- `PUT /api/posts/{id}/` - Update a post (authenticated)
- `DELETE /api/posts/{id}/` - Delete a post (authenticated)
- `GET /api/posts/date-range/` - List posts within a date range

### Problems
- `GET /api/problems/` - List all problems
- `GET /api/problems/{id}/` - Get problem details
- `POST /api/problems/` - Create a new problem
- `POST /api/problems/{id}/vote/` - Vote for a problem
- `POST /api/problems/{id}/comments/` - Add a comment to a problem

### Campaigns
- `GET /api/campaigns/` - List all campaigns
- `GET /api/campaigns/{id}/` - Get campaign details
- `POST /api/campaigns/` - Create a new campaign (admin only)
- `PUT /api/campaigns/{id}/` - Update campaign details (admin only)
- `GET /api/campaigns/{id}/donors/` - List donors for a campaign

### Donations
- `POST /api/donations/` - Record a new donation
- `GET /api/donations/campaigns/{id}/` - List donations for a campaign
- `GET /api/donations/user/{id}/` - List donations by a user

### Sponsors
- `POST /api/sponsors/` - Record a new sponsorship
- `GET /api/sponsors/fund-types/` - Get available fund types
- `GET /api/sponsors/reports/` - Get sponsorship reports (admin only)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Get a token by sending a POST request to `/api/auth/login/` with your credentials
2. Include the token in the Authorization header of subsequent requests:
```
Authorization: Bearer <your_token>
```

## Development

- The project uses Django REST Framework for API development
- PostgreSQL is used as the database
- Cloudinary is used for media storage
- JWT is used for authentication
- CORS is enabled for frontend integration 