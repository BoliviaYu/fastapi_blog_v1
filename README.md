# FastAPI blog v1


## What is this?

This is a simple example of using the [`FastAPI`](https://fastapi.tiangolo.com/) to build a blog backend.

## what is included?

### Project Structure

```
./backend
├── app
│   ├── config.py
│   ├── db
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── session.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── users.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services
│   │   ├── deps.py
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── users.py
│   └── uvicorn_config.json
├── logs
│   ├── ...
└── utils
```

### Project Delivery

- `2024-05-12` include `main.py` and `./app/db/`, which is the main entry point of the application and the database connection.
- `2024-05-14` include `./app/models/`, which is the model of the database using sqlalchemy (see [sqlalchemy](https://docs.sqlalchemy.org/en/20/orm/tutorial.html) ).
- `2024-05-16` include `./app/schemas/`, which is the schema of the pydantic model (see [pydantic](https://pydantic-docs.helpmanual.io/usage/models/#field-customization) ). And `./app/services`, which is the real implementation of the API.
- `2024-05-19` complete the `./app/routers/users.py`, which is the router of the users API.