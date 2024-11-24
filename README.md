# One-Time-Secret Management API

Project based on Django API for managing secrets. 
Allows to generate and retrieve secrets. 
The secrets are stored securily in Postgres DB with encryption algorithm and have expiration time.
The application is containerized and can be run with Docker.

## Prerequisites
- Docker
- Docker Compose

## Getting Started
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hani-momo/onetimesecret-api-service.git
   cd onetimesecret-api-service

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Set up Environment Variables**:
   Create a .env file and set the following list of environment variables:
   (and rename the variables in docker-compose.yml accordingly)
   ```bash
   DEBUG=1
   SECRET_KEY=your_secret_key
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=secret_pg
   SQL_USER=postgres
   SQL_PASSWORD=postgres
   SQL_HOST=db
   SQL_PORT=5432

4. **Set Executable Permissions for the entrypoint script**
   ```bash
   chmod +x secret_manager/entrypoint.sh

5. **Run the Containers and Migrations**
   ```bash
   docker-compose up --build -d
   docker-compose exec django python manage.py migrate

## API Usage (curl)
   ```bash
1. Generate a New Secret
   curl -X POST "http://localhost:8000/api/generate/" -H "Content-Type: application/json" -d '{"secret": "your_secret", "passphrase": "your_passphrase", "ttl": 600}'
Response: {"secret_key": "generated_secret_key"}

2. Retrieve a Secret
   curl -X GET "http://localhost:8000/api/secrets/generated_secret_key/?" -H "Content-Type: application/json" --data-urlencode "passphrase=your_passphrase"
Response: {"secret": "your_secret"}

Example:
1. curl -X POST "http://localhost:8000/api/generate/" -H "Content-Type: application/json" -d '{"secret": "i forgot to turn off the oven", "passphrase": "remember", "ttl": 600}'

--> {"secret_key":"eN_x0CT94B1ap6YOG0GkQ5PtjpBUpy9ZoF1J3hLRsqA="}

2. curl -X GET "http://localhost:8000/api/secrets/eN_x0CT94B1ap6YOG0GkQ5PtjpBUpy9ZoF1J3hLRsqA=/?passphrase=remember"

--> {"secret":"i forgot to turn off the oven"}
