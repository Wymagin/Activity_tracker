# Activity Tracker

Activity Tracker is a web application for tracking activities. This project is built using Django and PostgreSQL, and is containerized using Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Wymagin/Activity_tracker.git
cd Activity_tracker
```

## Build and Run the Application

### Build the Docker containers and start the application:

```bash
docker-compose up --build
```
The application will be available at http://localhost:8000.

### Running Migrations
To apply database migrations, run:

```bash
docker-compose run web python manage.py migrate
```

### Creating a Superuser

To create a superuser for accessing the Django admin, run:

```bash
docker-compose run web python manage.py createsuperuser
```
### Stopping the Application

To stop the application, run:
```bash
docker-compose down
```

## Project Structure

activity_tracker/: The Django project directory.

Dockerfile: The Dockerfile for building the web service container.

docker-compose.yml: The Docker Compose configuration file.

### Environment Variables
The application uses the following environment variables:

DJANGO_SECRET_KEY: The secret key for Django.

POSTGRES_DB: The PostgreSQL database name.

POSTGRES_USER: The PostgreSQL user.

POSTGRES_PASSWORD: The PostgreSQL user password.

These variables can be set in a .env file in the project root.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
