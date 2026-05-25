# SoftDesk API

SoftDesk API is a Django REST Framework project for managing collaborative software projects, issues, contributors, and comments. It uses JWT authentication and exposes a REST API that can be consumed by an API client, a frontend application, or a mobile application.

## Features

- User registration and JWT login
- Project CRUD
- Contributor-based project access
- Issue CRUD inside projects
- Comment CRUD inside issues
- Object-level permissions
- SQLite database for local development
- CORS support for local frontend/API GUI usage
- OpenAPI schema generation with drf-spectacular

## Requirements

- Python 3.10 or later
- `uv` package manager
- SQLite, included with Python

The project was developed and tested with Django 5.x and Django REST Framework.

## Project structure

```text
.
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── softdeskapp/
│   ├── models/
│   ├── serializers/
│   ├── permissions/
│   ├── views/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── urls.py
├── manage.py
├── pyproject.toml
└── db.sqlite3
```

## Installation

Clone the repository or extract the project archive, then open a terminal at the project root, where `manage.py` is located.

```powershell
cd .\Python_RESTful_API_Using_Django_REST_Project_9
```

Create and synchronize the virtual environment with `uv`:

```powershell
uv sync
```

If the project does not already contain all dependencies in `pyproject.toml`, install them manually:

```powershell
uv add django djangorestframework djangorestframework-simplejwt django-cors-headers drf-spectacular
```

## Environment configuration

For local development, the project uses SQLite and the default Django development server.

The important settings are located in `config/settings.py`.

Make sure the following applications are enabled:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",

    "softdeskapp",
]
```

Make sure the custom user model is configured:

```python
AUTH_USER_MODEL = "softdeskapp.User"
```

Make sure the Django REST Framework configuration uses JWT authentication:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

## CORS configuration

If you use a local API GUI or frontend on `localhost:8080`, configure CORS in `config/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_CREDENTIALS = True
```

The CORS middleware must be placed near the top of the middleware list, before `CommonMiddleware`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

If your client uses JWT through the `Authorization: Bearer <token>` header and does not use cookies, you can usually avoid sending browser credentials from the frontend.

## Database setup

Run Django checks first:

```powershell
uv run .\manage.py check
```

Create migrations:

```powershell
uv run .\manage.py makemigrations
```

Apply migrations:

```powershell
uv run .\manage.py migrate
```

Create an admin user:

```powershell
uv run .\manage.py createsuperuser
```

## Running the development server

Start the server:

```powershell
uv run .\manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

The Django admin will be available at:

```text
http://127.0.0.1:8000/admin/
```

If port `8000` is already in use, run the server on another port:

```powershell
uv run .\manage.py runserver 8001
```

## Authentication flow

### 1. Register a user

```http
POST /api/signup/
Content-Type: application/json
```

Example body:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### 2. Obtain a JWT token

```http
POST /api/token/
Content-Type: application/json
```

Example body:

```json
{
  "username": "testuser",
  "password": "password123"
}
```

Example response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### 3. Use the access token

For protected endpoints, add this HTTP header:

```http
Authorization: Bearer <access_token>
```

### 4. Refresh the access token

```http
POST /api/token/refresh/
Content-Type: application/json
```

Example body:

```json
{
  "refresh": "<refresh_token>"
}
```

## Main API endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/signup/` | Register a new user |
| `POST` | `/api/token/` | Obtain JWT access and refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh the access token |

### Projects

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/projects/` | List projects accessible to the authenticated user |
| `POST` | `/api/projects/` | Create a project |
| `GET` | `/api/projects/{project_id}/` | Retrieve a project |
| `PUT` | `/api/projects/{project_id}/` | Replace a project |
| `PATCH` | `/api/projects/{project_id}/` | Partially update a project |
| `DELETE` | `/api/projects/{project_id}/` | Delete a project |

### Issues

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/projects/{project_id}/issues/` | List project issues |
| `POST` | `/api/projects/{project_id}/issues/` | Create an issue in a project |
| `GET` | `/api/projects/{project_id}/issues/{issue_id}/` | Retrieve an issue |
| `PUT` | `/api/projects/{project_id}/issues/{issue_id}/` | Replace an issue |
| `PATCH` | `/api/projects/{project_id}/issues/{issue_id}/` | Partially update an issue |
| `DELETE` | `/api/projects/{project_id}/issues/{issue_id}/` | Delete an issue |

### Comments

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/projects/{project_id}/issues/{issue_id}/comments/` | List issue comments |
| `POST` | `/api/projects/{project_id}/issues/{issue_id}/comments/` | Create a comment on an issue |
| `GET` | `/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Retrieve a comment |
| `PUT` | `/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Replace a comment |
| `PATCH` | `/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Partially update a comment |
| `DELETE` | `/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Delete a comment |

## Permission rules

The API enforces object-level permissions.

### Projects

- Only authenticated users can create projects.
- A project is visible only to its author and contributors.
- Only the project author can update or delete the project.
- Contributors can read the project but cannot update or delete it unless they are the author.

### Issues

- Only project contributors can create and read issues inside the project.
- The issue author is automatically set to the authenticated user.
- If no assignee is provided, the assignee defaults to the issue author.
- Only the issue author can update or delete the issue.

### Comments

- Only project contributors can create and read comments on an issue.
- The comment author is automatically set to the authenticated user.
- Only the comment author can update or delete the comment.

## Example requests

### Create a project

```http
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "title": "SoftDesk API",
  "description": "REST API for collaborative project management.",
  "type": "BACKEND"
}
```

### Create an issue

```http
POST /api/projects/1/issues/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "title": "Add JWT authentication",
  "description": "Implement JWT login and protected endpoints.",
  "priority": "HIGH",
  "tag": "TASK",
  "status": "TODO"
}
```

### Create a comment

```http
POST /api/projects/1/issues/1/comments/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "description": "I will start working on this issue."
}
```

## OpenAPI documentation

The project uses `drf-spectacular` to generate OpenAPI documentation.

Run the development server and open:

```text
http://127.0.0.1:8000/api/schema/
http://127.0.0.1:8000/api/docs/swagger/
http://127.0.0.1:8000/api/docs/redoc/
```

To generate an `openapi.yaml` file:

```powershell
uv run .\manage.py spectacular --file openapi.yaml --validate
```

For stricter validation:

```powershell
uv run .\manage.py spectacular --file openapi.yaml --validate --fail-on-warn
```

## Running tests

Run the test suite with:

```powershell
uv run .\manage.py test
```

Run Django system checks with:

```powershell
uv run .\manage.py check
```

## Troubleshooting

### `404 Page not found at /api/signup/`

This means the signup route is missing from `softdeskapp/urls.py`.

Add:

```python
from .views.account_views import SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    # other routes...
]
```

### `Manager isn't available; 'auth.User' has been swapped for 'softdeskapp.User'`

This means a file imports Django's default `User` model directly.

Do not use:

```python
from django.contrib.auth.models import User
```

Use:

```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

For model relations, use:

```python
from django.conf import settings

settings.AUTH_USER_MODEL
```

### CORS error with `credentials: include`

Add this setting:

```python
CORS_ALLOW_CREDENTIALS = True
```

If the client only uses JWT Bearer tokens, remove `credentials: "include"` from the frontend request unless cookies are required.

### HTML error page instead of JSON

When `DEBUG = True`, Django may return an HTML debug page for routing errors before Django REST Framework handles the request. Check that the URL exists in `config.urls` or `softdeskapp.urls`.

## Development notes

- Do not let clients send `author_user` manually. The backend should set it from `request.user`.
- Do not expose all model fields with `fields = "__all__"` unless it is intentional.
- Always filter querysets by the authenticated user's accessible resources.
- Use object-level permissions for update and delete rules.
- Keep the generated `openapi.yaml` aligned with the real Django routes.

## License

This project is intended for educational use as part of the OpenClassrooms Django REST API project.
