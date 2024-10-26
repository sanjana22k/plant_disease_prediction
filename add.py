import streamlit as st
import sqlite3

# Initialize connection to the SQLite database
conn = sqlite3.connect('veggies.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price_per_unit REAL NOT NULL
    )
''')
conn.commit()

# Streamlit app
st.title("Add Farm Products")

# Input fields for product and price
product_name = st.text_input("Product Name")
price_per_unit = st.number_input("Price per Unit (kg or unit)", min_value=0.0, step=0.01)

# Button to add product to database
if st.button("Add Product"):
    if product_name and price_per_unit > 0:
        c.execute("INSERT INTO products (product_name, price_per_unit) VALUES (?, ?)",
                  (product_name, price_per_unit))
        conn.commit()
        st.success(f"Product '{product_name}' added with price ${price_per_unit}/unit.")
    else:
        st.error("Please enter both product name and price.")

# Display the list of products
st.subheader("Available Products")

products = c.execute("SELECT product_name, price_per_unit FROM products").fetchall()

if products:
    for product, price in products:
        st.write(f"{product}: ${price}/unit")
else:
    st.write("No products available.")

# Close connection
conn.close()
