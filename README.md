# wall-app-api

<!-- [![Build Status](https://travis-ci.org/Hercilio1/wall-app-api.svg?branch=master)](https://travis-ci.org/Hercilio1/wall-app-api) -->

This is the API of the Wall App. Checkout the Frontend (client) project here: https://github.com/Hercilio1/wall-app.

This project is online on: wall-app-api.hercilio.ortiz.nom.br/swagger/


## Project Overview

This project leverages the power of DRF ([Django Rest Framework](https://www.django-rest-framework.org/)) to provide a robust and scalable API. Following the Django framework pattern, it meticulously implements Views, Serializers, and Models for each entity, embodying a clean and maintainable codebase.

### Key Entities

#### Users

The users entity represents the core users of the application.

#### Entries

Entries serve as the backbone of the application, representing wall postings in a seamless manner.

### Technology Stack

- **Django Rest Framework (DRF):**
  Harnessing the capabilities of DRF ensures a streamlined development process and feature-rich APIs.

- **PostgreSQL:**
  The project persists data efficiently using PostgreSQL, a powerful and open-source relational database.

- **Docker:**
  Docker is employed to create a consistent and portable environment, facilitating easy deployment and reducing setup complexities.


## Getting Started

To run the project locally, follow these steps:

1. Install Docker on your machine.

2. Clone the repository:

   ```bash
   git clone https://github.com/Hercilio1/wall-app-api.git
   ```

3. Start the dev server for local development:

    ```bash
    docker-compose up
    ```

### Using Swagger

Swagger has been seamlessly integrated into the API, providing a live documentation platform and a convenient space for testing various API endpoints.

#### Access Swagger UI

Open your web browser and navigate to the Swagger UI endpoint. In a typical setup, this is often found at: http://localhost:8000/swagger/

### Helpful commands

Use the following command for running commands inside the docker container:

```bash
docker-compose run --rm web [command]
```

Example:

```bash
docker-compose run --rm web python migrate.py makemigrations
```

### Local Limitations

While using the local environment, please be aware of the following limitations:

1. **SSL and Security Layers:**
   The local environment lacks SSL implementation and additional security layers. For enhanced security features, consider deploying the application in a production environment.

2. **Email Sending via SMTP:**
   The local setup is configured to log emails in the console and does not support sending emails through SMTP. This limitation is intentional in the development environment to prevent unintended email communications. In a production environment, appropriate SMTP configurations can be implemented for email functionality.


## Deploying in Production

To deploy the application in a production environment, follow these steps:

1. Locate the file named `docker-compose.prod.yml` in the project root. This file contains the production configuration for our Docker environment.

2. Duplicate the following sample environment files and remove the `.sample` suffix:

   - `.env.prod.sample`: Stores API environment variables. This file is essential for the proper functioning of the application.
   - `.env.prod.db.sample`: Stores database variables, necessary for creating and connecting to the database.

3. After duplicating the files, update the variable values in the newly created `.env.prod` and `.env.prod.db` files according to your production environment requirements.

By completing these steps, you'll have the necessary configurations in place for deploying the application in a production environment. Now you just need to run the following command:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```
