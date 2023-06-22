# Project Title

Servicios Students Projects

## Table of Contents
- [Documentation](#documentation)
  - [Entity-Relationship Diagrams](#Entity-Relationship-Diagrams)
  - [Technical Documentation: Worker Management Deploy Service](#Technical Documentation: Worker Management Deploy Service)
   - [Usage](#Usage)
- [Deployment](#deployment)
 - [Database Migration](#Database Migration)
- [Installation](#installation)
- [Database Migration](#database-migration)
- [Running the Server](#running-the-server)
- [Authors](#authors)


## Documentation

Each service uses a PostgresSQL database which is automatically generated after using the migrations embedded in the code, before any deployment, it is important to highlight that the databases must be previously created with the specific name mentioned in the installation instructions...

The following is the Entity-Relationship Diagram for each of the services:

#Entity Relationship Diagrams

ERD DB Users Service
![ERD DB Users Service](https://i.postimg.cc/XY8MhVt3/users.png)

ERD DB Academic Service

![ERD DB Academic Service](https://i.postimg.cc/nLJzKcBJ/Academic.png)

ERD DB Projects Service

![ERD DB Users Service](https://i.postimg.cc/76PZcsKt/Projects.png)

# Technical Documentation: Worker Management Deploy Service 
Worker management is a key functionality in many applications that require concurrent tasks to be performed in separate threads. The provided code implements the Worker and ManageWorker classes that allow managing the execution of workers in separate threads in a controlled manner.

# Worker class
The Worker class represents a worker and is responsible for executing a task in a separate thread. It has the following attributes:

guid (str): Unique identifier of the worker.
thread (Thread): Thread object that executes the task.
delegate (any): Delegate that is invoked when the worker finishes.
The Worker class provides the following methods:

run(): Starts the execution of the worker thread.
finish(): Invoke the delegate to indicate that the worker has finished.
ManageWorker class
The ManageWorker class is in charge of managing workers and controlling their execution in separate threads. It has the following attributes:

workers (dict): Dictionary that stores the workers in execution.
max_workers (int): Maximum number of workers allowed.
The ManageWorker class provides the following methods:

queue(target: any, kwargs: dict) -> Worker: Queue a new worker for execution. It receives a target (target) and a dictionary of arguments (kwargs) to be used to create a new thread and execute the target. Returns a Worker object representing the queued worker.
_queue(guid: str, target: any, kwargs: dict) -> Worker: Internal method used by queue() to create a new worker with the provided target and arguments. It generates a unique identifier (guid) for the worker and uses it to create a Worker object.
finish(guid: str): Method invoked when a worker has finished. It receives the unique identifier (guid) of the worker and removes it from the list of workers in execution.
isAvaibleSlot() -> bool: Checks if there are available slots for more workers. Returns a boolean value indicating if the number of workers in execution is less than the maximum number of workers allowed.
# Usage
To use worker management, the following steps must be followed:

Create an instance of ManageWorker with the desired maximum number of workers.
Call the queue(target, kwargs) method of ManageWorker to queue a new worker. Provide the target (target) and the arguments (kwargs) needed to execute the worker task.
The queue() method will return a Worker object representing the queued worker.
The worker will be automatically executed in a separate thread.
If necessary, the finish(guid) method of ManageWorker can be called by passing the unique identifier (guid) of the worker to indicate that it has finished.
It is important to keep in mind the limitations of the maximum number of workers (max_workers) to avoid system saturation.

Provided worker management simplifies the execution of concurrent tasks in separate threads and enables efficient control of the running workers!

## Deployment

This repository contains the necessary steps to deploy the service. Please follow the instructions below to get started. Use this for each service.

## Installation

Install the required dependencies by running the following command in your terminal:

   ```bash
   pip install -r requirements.txt
   ```

## Database Migration

Make sure you have an existing PostgreSQL database with the name students_project_users. If you don't have one, create a new database.

For the academic service, the name of the database is 'students_project_academic', and for the projects service, it is 'students_project_projects'.

Migrate the database schema by running the following command


   ```bash
   python manage.py migrate
   ```
   
This will apply any pending migrations and create the necessary tables in the database.

Verify that the database now has the required tables.

## Running the Server

Start the service by running the following command:


   ```bash
   python manage.py runserver 8002
   ```
Here, 8002 represents the port number on which the server will run. Feel free to change it if needed.

Once the server is running, you can access the service by opening your web browser and navigating to http://localhost:8002, "localhost" represents your host or the server's IP address if you are using one.
## Authors

- [@JhoanMancilla](https://github.com/JhoanMancilla)

- [@FelipeM09](https://github.com/FelipeM09)
- [@CRISTIANLOPEZ16](https://github.com/CRISTIANLOPEZ16)