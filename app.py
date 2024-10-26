import streamlit as st
import tensorflow as tf
import numpy as np
import webbrowser

# Initialize user credentials in session state
if 'USER_CREDENTIALS' not in st.session_state:
    st.session_state['USER_CREDENTIALS'] = {}

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    

    if st.button("Login"):
        if username in st.session_state['USER_CREDENTIALS'] and st.session_state['USER_CREDENTIALS'][username] == password:
            st.success("Login successful")
            st.session_state['logged_in'] = True
        else:
            st.error("Invalid credentials")
    image1 = "login.jpg"
    st.image(image1, use_column_width=True)

def signup():
    st.title("Sign Up")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password == confirm_password:
            if new_username in st.session_state['USER_CREDENTIALS']:
                st.error("Username already exists")
            else:
                st.session_state['USER_CREDENTIALS'][new_username] = new_password
                st.success("Account created successfully! You can now log in.")
        else:
            st.error("Passwords do not match")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Only show Login/Sign Up menu when the user is not logged in
    if not st.session_state['logged_in']:
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            login()
        elif choice == "Sign Up":
            signup()
    else:
        # No menu when logged in, just show the welcome message and the main app content
        st.sidebar.write("Logged in")
        st.sidebar.title("Dashboard")
        app_mode=st.sidebar.selectbox("select page",["Home","About","Disease Recognition","Buy","Add Item"])
        def model_prediction(test_image):
            model = tf.keras.models.load_model("trained_plant_disease_model.keras")
            image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr]) #convert single image to batch
            predictions = model.predict(input_arr)
            return np.argmax(predictions) #return index of max element
        #homepage
        if (app_mode=="Home"):
            st.header("FARM VISTA")
            st.write("--Application by Sanjana and Mukta")
            st.subheader("A PLANT DISEASE DETECTION SYSTEM")
            image = "farm.jpg"
            st.image(image, use_column_width=True)

        #aboutpage
        elif(app_mode=="About"):
            st.header("About")
            st.markdown(""" Farmvista is a comprehensive platform designed to revolutionize the agricultural marketplace and empower farmers with cutting-edge technology. It offers a seamless way to buy and sell farm products, connecting producers directly with buyers for a more efficient trade experience.

In addition, Farmvista integrates advanced image recognition technology to help farmers identify plant diseases. Simply upload a picture of your plant, and the system will not only diagnose potential diseases but also recommend tailored solutions to ensure optimal plant health.

Farmvista bridges the gap between modern technology and traditional farming, making agriculture smarter and more accessible for everyone.
""")
            image2 = "about.jpg"
            st.image(image2, use_column_width=True)
            
        
        #prediction
        elif(app_mode=="Disease Recognition"):
            st.header("Disease Prediction and Solution")
            test_image=st.file_uploader("choose a image:")
            if (st.button("show image")):
                st.image(test_image,use_column_width=True)
            if(st.button("Predict")):
            
                st.write("Our Prediction")
                result_index = model_prediction(test_image)
        #Reading Labels
                class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                      'Tomato___healthy']
                st.success("Model is Predicting it's a {}".format(class_name[result_index]))
        
        #additempage
        elif(app_mode=="Add Item"):
            import sqlite3
            conn = sqlite3.connect('veggies.db')
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                   product_name TEXT NOT NULL,
                   price_per_unit REAL NOT NULL
                                             )
                                        ''')
            conn.commit()
            st.title("Add Farm Products")
            product_name = st.text_input("Product Name")
            price_per_unit = st.number_input("Price per Unit (kg or unit)", min_value=0.0, step=0.01)
            # Button to add product to database
            if st.button("Add Product"):
                if product_name and price_per_unit > 0:
                    c.execute("INSERT INTO products (product_name, price_per_unit) VALUES (?, ?)",
                  (product_name, price_per_unit))
                    conn.commit()
                    st.success(f"Product '{product_name}' added with price Rs.{price_per_unit}/unit.")
                else:
                    st.error("Please enter both product name and price.")

# Display the list of products
            st.subheader("Available Products")

            products = c.execute("SELECT product_name, price_per_unit FROM products").fetchall()

            if products:
                for product, price in products:
                    st.write(f"{product}: Rs.{price}/unit")
            else:
                st.write("No products available.")
            conn.close()        
        #buy
        elif(app_mode=="Buy"):
            import sqlite3
            conn = sqlite3.connect('veggies.db')
            c = conn.cursor()
            c.execute("SELECT product_name, price_per_unit FROM products")
            products = c.fetchall()

            st.title("Buy Farm Products")

            if not products:
                st.warning("No products available. Please add products on the 'Add Item' page.")
            else:
                product_names = [product[0] for product in products]
                selected_product = st.selectbox("Select a product to buy", product_names)
                price_per_unit = dict(products)[selected_product]
                st.write(f"Price per unit of {selected_product}: Rs.{price_per_unit:.2f}")
                quantity = st.number_input(f"How many units of {selected_product} would you like to buy?", min_value=1)
                total_price = quantity * price_per_unit
                st.write(f"Total price: Rs.{total_price:.2f}")
                if st.button("Buy"):
                    st.success(f"You have successfully bought {quantity} units of {selected_product} for Rs.{total_price:.2f}")
                    mailto_link = "mailto:example@example.com?subject=Buying%20product&body=Buying%20the%20selected%20product"
                    js_code = f'window.open("{mailto_link}");'
                    st.components.v1.html(f'<script>{js_code}</script>', height=0)
 
            st.subheader("Available Products")
            for product, price in products:
                st.write(f"{product}: Rs.{price}/unit")

# Close the connection
            conn.close()




if __name__ == "__main__":
    main()
