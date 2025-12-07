# ConnectNet Backend

Simple social network backend built with FastAPI, SQLAlchemy and SQLite.

## Overview

Provides user, post, comment, like and follow functionality with:
- REST endpoints (FastAPI)
- SQLite DB by default (`ConnectNet.db`)
- Alembic migrations
- Password hashing (pbkdf2_sha256)
- CORS configured (adjust for production)

Tested for Python 3.8.
## Requirements

- Python 3.8
- See `requirements.txt` (example packages: fastapi, uvicorn, SQLAlchemy, alembic, pydantic, passlib)

## Quickstart (Linux)

1. Clone repo
```bash
git clone <repo-url>
cd ConnectNet_backend
```

2. Create virtualenv and install
```bash
python3.8 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

3. Create database / run migrations or seed data
- Apply Alembic migrations (preferred)
```bash
alembic -c alembic.ini upgrade head
```
- Or create tables and seed sample data
```bash
python seeds.py
```

4. Run the app
```bash
uvicorn main:app --reload --port 8000
```
Open http://localhost:8000/docs for interactive API docs.

## Default DB

By default the app uses SQLite at `./ConnectNet.db`. Change `SQLALCHEMY_DATABASE_URL` in `database.py` or configure Alembic (`alembic.ini`) for different DBs.

## Useful commands

- Show current alembic revision:
```bash
alembic -c alembic.ini current
```
- Generate migration (autogenerate):
```bash
alembic -c alembic.ini revision --autogenerate -m "message"
```
- Stamp DB as up-to-date:
```bash
alembic -c alembic.ini stamp head
```
- Run seed script:
```bash
python seeds.py
```
- Inspect SQLite file:
```bash
sqlite3 ./ConnectNet.db ".tables"
sqlite3 ./ConnectNet.db "select * from users limit 5;"
```

## API (summary)

- GET /                -> Returns users and posts with comments & likes (root used for frontend)
- POST /auth/login     -> Login (returns user info on success)
- POST /users          -> Create user
- POST /posts          -> Create post
- GET  /posts          -> List posts (with user, comments, likes)
- POST /comments       -> Add comment
- GET  /comments/post/{post_id}
- POST /likes/{user_id}/{post_id}
- DELETE /likes/{user_id}/{post_id}
- POST /follows/{follower_id}/{following_id}
- DELETE /follows/{follower_id}/{following_id}
See `/docs` for full OpenAPI spec and examples.

## Notes & recommendations

- CORS is enabled with `allow_origins=["*"]` for development. Restrict origins in production.
- Passwords are hashed with `pbkdf2_sha256`.
- For production, use a proper RDBMS (Postgres/MySQL), secure config (env vars), and HTTPS.
- Add pagination for list endpoints when integrating with a frontend.
- Use Alembic migrations in CI/CD rather than `Base.metadata.create_all()` in production.

## Troubleshooting

- If Alembic prints only info lines, run `alembic -c alembic.ini current --verbose` or check `migrations/` exists.
- If endpoints return empty data, ensure `ConnectNet.db` exists and has been seeded or migrations applied.


## Support and contact details

GitHub - github.com/HidayaMohamed
email - hidayamohaed002@gmail.com



## License
The content of this site is licensed under the MIT license Copyright (c) 2025.

