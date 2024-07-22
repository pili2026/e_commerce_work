# E-commerce

## Introduction

This `E_commerce` project implements an API service that includes RESTful APIs, database migrations, and tests. The service is built using `FastAPI` and `Postgres (TimescaleDB)`.

## Getting Started

To run the project locally, follow the steps below.

### Clone the Project

First, clone the repository:
```
git clone https://github.com/pili2026/e_commerce_work.git
cd e_commerce_work
```

### Build and Run with Docker Compose

To build the Docker images and run the necessary services and web server, use the following command:
```
docker-compose -f docker-compose-local.yml up --build
```

This command will build the necessary Docker images and run TimescaleDB, the database migration service, and the web API server with the latest version of the database schema.

### Interactive API Docs

Navigate to `http://{ip_address}:8000/docs` to see the automatic interactive API documentation (provided by Swagger UI).

![API Documentation](static/api_doc.PNG)

Some APIs require **authentication (login)** to obtain a **token** before they can be used, such as operations related to orders.

#### Authentication

When the service is started via Docker Compose, two users and two products are created by default:
```
# Users
Role: manager
Account: manager
Password: manager1234

Role: customer
Account: customer
Password: customer1234

# Products
Name: Router
Price: 20
Stock: 10
Total: 10

Name: Switch
Price: 10
Stock: 10
Total: 10
```

Authentication can be done in two ways:

1. **API Docs Authentication**
   1. Select Authorize
   ![Authorize](static/auth.PNG)
   2. Input username (account) and password to log in
   ![Authorize Login](static/auth_2.PNG)
2. **Call the Login API**
   1. Input username (account) and password to log in
   ![Login API](static/login.PNG)
   2. Get a token to operate the API.

Afterwards, you can perform operations with the corresponding permissions in the API documentation.

## Using Postman for API Testing
We have provided two files for Postman to help you test the APIs:

* A Postman collection: `FastAPI Collection.postman_collection.json`
* A Postman environment: `e_commerce_environment.json`

### Import the Collection and Environment into Postman
1. Open Postman.
2. Click the `Import` button in the top left corner.
3. Select the `Upload Files` tab.
4. Click Choose Files and select `FastAPI Collection.postman_collection.json` and `e_commerce_environment.json` from your file system.
5. Click the `Import` button to import the files.

### Configure the Environment
1. Go to the `Environments` tab on the left sidebar.
2. Find the imported environment `e_commerce_environment` and select it.
3. Make sure the environment variables are correctly set up, particularly the `host` variable, which should point to your local server (e.g., http://localhost:8000).
4. Click `Save` to save any changes.

### Run the Collection
1. Go to the `Collections` tab on the left sidebar.
2. Find the imported collection `e_commerce_collection`.
3. Click the `Run` button to execute the collection requests.


## Project Architecture

```
.
├── bin                # Scripts
├── migration          # Database migration configuration files
├── res                # Configuration-related files
├── docker_entrypoint  # Docker-related shell scripts, serving as entry points for operations
├── test               # Test code, including unit and integration tests
└── src                # Entry point of the project
    ├── repository     # Manages database operations
    │   ├── error_code # Error codes from database operations
    │   └── model      # Database models
    ├── restful_api    # Implements RESTful web services
    │   ├── handler    # Processes RESTful API requests and responses
    │   └── schema     # Defines the structure for RESTful API requests and responses
    ├── service        # Business logic programs
    │   └── model      # Models used by the service layer
    ├── seed           # Scripts/files for seeding the database with initial data
    └── util           # Development tools and utilities
```

### Entrypoint

The entry point for the project is located within the `src` folder.

To set up the environment, add a `.env` file with the following configuration:
```
PYTHONPATH=./src:./test:$PYTHONPATH
```

## DB Migration

### Prerequisites

Initialize the migration folder using:
```
alembic init migration
```

### Create a New Revision

1. Define database changes in the ORM models under `src/repository/model`.
2. Manually import your ORM modules in `__init__.py` under `src/repository/model` for Alembic to reference.
3. Create a new revision with Alembic:
   - **Usage**
     ```
     alembic -x config_path={project_config_path} revision --autogenerate -m {revision_message}
     ```
   - **Example**
     ```
     alembic -x config_path=./res/config.yml revision --autogenerate -m "Init table"
     ```

### Update Database to a Target Revision

1. Update the `DB_MIGRATION_REVISION` variable in `config.yml` with the target version.
   - **Example**
     ```
     DB_MIGRATION_REVISION: head         # Upgrade to the latest revision
     DB_MIGRATION_REVISION: base         # Downgrade to the initial revision
     DB_MIGRATION_REVISION: "+1"         # Upgrade to the next revision
     DB_MIGRATION_REVISION: "-1"         # Downgrade to the previous revision
     DB_MIGRATION_REVISION: 6dcc4580e67e # Update to a specific revision
     ```
2. Run `run_db_migration.py` to update the database to the specified version:
   - **Usage**
     ```
     python ./bin/run_db_migration.py --config_path={project_config_path}
     ```
   - **Example**
     ```
     python ./bin/run_db_migration.py --config_path=./res/config.yml
     ```

### Merge Multiple Revisions into One

1. Identify all manually created migration code (outside Alembic autogenerated comments). For example:
   ```python
   def downgrade() -> None:
       # ### commands auto generated by Alembic - please adjust! ###
       op.drop_table("users")
       op.drop_table("role_permissions")
       # ### end Alembic commands ###
       sa.Enum(name="role_name_enum").drop(op.get_bind(), checkfirst=False)       # Manually created
       sa.Enum(name="permission_name_enum").drop(op.get_bind(), checkfirst=False) # Manually created
   ```
2. Determine the base revision for the new merged revision.
3. Delete all migration revisions created after this base revision.
4. Follow the steps in **Create a New Revision** to generate a new merged revision.
5. Manually add back all manually created code identified in step 1.

## Run Unit Tests

1. Install related packages:
   ```
   pip install -r requirements-dev.txt
   ```
2. Execute tests using VS Code.