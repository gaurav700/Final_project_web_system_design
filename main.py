from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Models
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    timestamp: int
    notes: str | None = None
    items: list[int] 



# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


# Customers
@app.post("/customers")
def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
        return {"id": cursor.lastrowid, "name": customer.name, "phone": customer.phone}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Phone number must be unique")
    finally:
        conn.close()

@app.get("/customers/{id}")
def get_customer(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return dict(customer)
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": id, "name": customer.name, "phone": customer.phone}


# Items
@app.post("/items")
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    conn.close()
    return {"id": cursor.lastrowid, "name": item.name, "price": item.price}

@app.get("/items/{id}")
def get_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    item = cursor.fetchone()
    conn.close()
    if item:
        return dict(item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{id}")
def delete_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

@app.put("/items/{id}")
def update_item(id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": id, "name": item.name, "price": item.price}


# Orders
@app.post("/orders")
def create_order(order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
                   (order.customer_id, order.timestamp, order.notes))
    order_id = cursor.lastrowid
    for item_id in order.items:
        cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))
    conn.commit()
    conn.close()
    return {"id": order_id, "customer_id": order.customer_id, "timestamp": order.timestamp, "notes": order.notes, "items": order.items}

@app.get("/orders/{id}")
def get_order(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("SELECT item_id FROM order_items WHERE order_id = ?", (id,))
    items = [row["item_id"] for row in cursor.fetchall()]
    conn.close()
    return {**dict(order), "items": items}

@app.delete("/orders/{id}")
def delete_order(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.put("/orders/{id}")
def update_order(id: int, order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET customer_id = ?, timestamp = ?, notes = ? WHERE id = ?",
                   (order.customer_id, order.timestamp, order.notes, id))
    cursor.execute("DELETE FROM order_items WHERE order_id = ?", (id,))
    for item_id in order.items:
        cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (id, item_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": id, "customer_id": order.customer_id, "timestamp": order.timestamp, "notes": order.notes, "items": order.items}
