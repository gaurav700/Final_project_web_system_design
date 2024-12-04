# Dosa Restaurant API

This project implements a REST API for a Dosa restaurant using **FastAPI** and an **SQLite** database. The API provides endpoints for managing customers, items, and orders, supporting CRUD operations.

## Features

- **Customer Management**: Add, update, delete, and fetch customer details.
- **Item Management**: Add, update, delete, and fetch menu items.
- **Order Management**: Create, update, delete, and fetch customer orders, including item details.

## Technologies Used

- **FastAPI**: Python web framework for building APIs.
- **Uvicorn**: ASGI server for serving the FastAPI app.
- **SQLite**: Relational database used to store customer, item, and order data.

## Setup and Installation

### Prerequisites

Make sure Python 3.7+ is installed on your system.

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/gaurav700/Final_project_web_system_design.git
cd Final_project_web_system_design
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate your dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

Before running the API, initialize the SQLite database by running:

```bash
python init_db.py
```

This will create the `db.sqlite` file with the necessary tables and relations.

## Running the Application

Run the FastAPI app using Uvicorn:

```bash
uvicorn main:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

### Access the API Documentation

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` to interact with the API using Swagger UI.
- **ReDoc UI**: Visit `http://127.0.0.1:8000/redoc` for an alternative API documentation view.

## Endpoints

### 1. **Customer Endpoints**

- **POST `/customers`**: Create a new customer.
- **GET `/customers/{id}`**: Retrieve a customer by ID.
- **DELETE `/customers/{id}`**: Delete a customer by ID.
- **PUT `/customers/{id}`**: Update customer details.

### 2. **Item Endpoints**

- **POST `/items`**: Add a new item to the menu.
- **GET `/items/{id}`**: Retrieve an item by ID.
- **DELETE `/items/{id}`**: Delete an item by ID.
- **PUT `/items/{id}`**: Update an item in the menu.

### 3. **Order Endpoints**

- **POST `/orders`**: Create a new order.
- **GET `/orders/{id}`**: Retrieve an order by ID.
- **DELETE `/orders/{id}`**: Delete an order by ID.
- **PUT `/orders/{id}`**: Update an order.

## Testing

You can use **Postman** or **curl** to test the API. Make sure to use the correct HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) and appropriate URLs for each endpoint.
