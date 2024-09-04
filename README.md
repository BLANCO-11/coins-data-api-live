---

# Cryptocurrency Data API with Spring Boot and Python Scraper

This project is a containerized application that consists of a Spring Boot API and a Python-based web scraper. The application scrapes cryptocurrency data from the web and stores it in a PostgreSQL database. The Spring Boot API serves this data to clients via RESTful endpoints.

## Project Structure

- **Spring Boot Application**: Hosts the API that serves cryptocurrency data.
- **Python Scraper**: Fetches and updates cryptocurrency data from online sources and stores it in the PostgreSQL database.
- **PostgreSQL Database**: Stores the scraped cryptocurrency data.
- **Docker**: Containerizes the Spring Boot application, Python scraper, and PostgreSQL database for easy deployment.

## Prerequisites

Before running the application, ensure that you have the following installed on your machine:

- Docker
- Docker Compose

## Setup and Run

Follow the steps below to set up and run the application:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/BLANCO-11/coins-data-api-live
   cd coins-data-api-live
   ```

2. **Build and Run the Containers**:

   Use Docker Compose to build and start the containers:

   ```bash
   docker-compose up --build
   ```

   This command will:

   - Build the Docker image for the Spring Boot application.
   - Build the Docker image for the Python scraper.
   - Start the PostgreSQL database container.

3. **Access the API**:

   Once the containers are up and running, the Spring Boot API will be available at:

   ```
   http://localhost:8080
   ```

   You can access the endpoints to retrieve cryptocurrency data.

4. **Stop the Containers**:

   To stop the containers, press `Ctrl+C` in the terminal where the containers are running, or run:

   ```bash
   docker-compose down
   ```

## Configuration

- **Database**: The PostgreSQL database is configured with default credentials in the `docker-compose.yml` file. You can change the configuration according to your needs.
- **Python Scraper**: The scraper script is designed to run periodically and update the database with the latest cryptocurrency data.

# NOTE
- If you are having any file ownership/privilege issues, move the dump.sql file to parent directory of the project root folder and update the docker-compose.yml to this:
```
volumes:
      - pgdata:/var/lib/postgresql/data
      - ..//dump.sql:/docker-entrypoint-initdb.d/dump.sql #This part should point to dump.sql file   <<------------
```

---
