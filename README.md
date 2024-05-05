# WEB APP開發 期末專案後端

本專案為提供後端 API 與初始化過的資料庫以供前端在本地部屬使用.

## Installation

To run the backend service locally, make sure you have Docker and Docker Compose installed on your system.

1. Clone this repository:
   ```bash
   git clone https://github.com/Dereto/wap-final.git
   ```

2. Navigate to the project directory:
   ```bash
   cd wap-final
   ```

3. Start the backend services using Docker Compose:
   ```bash
   docker-compose up
   ```

## Configuration

The backend service can be configured using environment variables. You can find the available configuration options in the `.env.example` file. Copy this file to `.env` and update the values as needed.
I'll give you the content for now.
   ```bash
SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"

PG_HOST="db"
PG_PORT="5432"
PG_USERNAME="test"
PG_PASSWORD="123"
PG_DBNAME="test"
   ```


## Usage

Once the backend services are up and running, you can access the API endpoints at `http://localhost:8000`.

### API Endpoints

- **GET /**: Check connection to backend.
- **POST /login**: Retrieves token for identification.
- **POST /logout**: Erase login token.
- **GET /user**: Retrieves all user data.
- **GET /user/{id}**: Retrieves certain user data.
- **POST /user**: Create new user.
- **PUT /user/{id}**: Updates user password, don't use it for now.

For detailed documentation on each endpoint, refer to [API Documentation](localhost:8000/docs) (please start service beforehand).

## Database Setup

The backend service uses a PostgreSQL database, which is managed automatically by Docker Compose. Database initialization are handled automatically on startup.
You can access database at port 5432.

## Troubleshooting

If you encounter any issues while running the backend service, try the following:

- Make sure Docker and Docker Compose are installed correctly.
- Check the logs for any error messages.
- Ensure that the required ports (e.g., 8000 for the fastapi) are not being used by other services.