# Task Management System (Java + Spring Boot + MySQL)

## Quick start
1. Create a MySQL database (example name: `taskdb`). Note credentials.
2. Update `src/main/resources/application.properties` with your MySQL settings.
3. Build and run:
   - `mvn clean package`
   - `java -jar target/task-management-system-0.0.1-SNAPSHOT.jar`
4. REST endpoints start at `http://localhost:8080/api/tasks`

## Docker (optional)
A sample `docker-compose.yml` is included to run MySQL quickly.

## What’s included
- Basic CRUD REST API for Task entity
- JPA repository and service layer
- MySQL configuration placeholder
