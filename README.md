# Connectly API

A simple Django + Django REST Framework project for learning CRUD, validation/relationships, security, and design patterns. The service exposes endpoints for users, posts, comments, and authentication, backed by a local SQLite database.

## Quick Start

### Prerequisites

- Python 3.11+ (works with 3.12 as well)
- Pip and a virtual environment tool (`venv`)

### Setup

```bash
cd connectly_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Apply migrations and start the server
python manage.py migrate
python manage.py runserver

# Running the server under HTTPS
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
```

Server runs at <http://127.0.0.1:8000>.

SQLite database file: `db.sqlite3`.

## API Endpoints

Base path: `/posts/`

- `GET /posts/users/` — List users
- `POST /posts/users/` — Create user
- `GET /posts/posts/` — List posts
- `POST /posts/posts/` — Create post
- `GET /posts/posts/{id}/` — Retrieve a post
- `POST /posts/posts/create/` — Create post (factory example)
- `GET /posts/comments/` — List comments
- `POST /posts/comments/` — Create comment
- `POST /posts/login/` — Login

Note: Endpoints come from the app-level routing in `posts/urls.py`, included under the project path `posts/` via `connectly_project/urls.py`.

## Postman Collections

Local collections (import these into Postman):

- `Connectly week-1-2-crud.postman_collection.json`
- `Connectly week-3-validation-and-relationships.postman_collection.json`
- `Connectly week-4-security.postman_collection.json`
- `Connectly week-5-design-patterns.postman_collection.json`

They are located in the project root: `connectly_project/`.

Shared results (Google Drive):

- [Week 1–2: CRUD Operations](https://drive.google.com/drive/folders/1p0mhQaZ1vEVitmxaspCFtBUsHbyypJtL?usp=sharing)
- [Week 3: Validation and Relationships](https://drive.google.com/drive/folders/1-ujCBZ6WadqjI9MAqbn4rZBD-mZ_RZui?usp=sharing)
- [Week 4: Security](https://drive.google.com/drive/folders/1Fz-BHUqr73NKCqg6T4-KmVJu2z9RoTt4?usp=sharing)
- [Week 5: Design Patterns](https://drive.google.com/drive/folders/1s7h1fQSYJ-kk9PF9vhLDIRbt9JBG9oFV?usp=sharing)

## Development Notes

- Project settings: `connectly_project/connectly_project/settings.py`
- App code: `connectly_project/posts/`
- URLs: `connectly_project/connectly_project/urls.py` and `connectly_project/posts/urls.py`

### Run Tests

```bash
cd connectly_project
source .venv/bin/activate
python manage.py test
```

### Formatting

Black is included; to format:

```bash
cd connectly_project
source .venv/bin/activate
black .
```

## Table of Contributions

| Name | Role |
| --- | --- |
| Jorje Jun Barrera | Configured Git repository and handled commits |
| Dexter R. Oraa | Documentation |
| Kyle Gabriel Tubera | Documentation |
| Cherlita Timogan | Security API testing and documentation support |
