import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to authenticate user login using username and password from Firebase
def authenticate_user(username, password):
    users_ref = db.collection('users')  # Assuming you have a collection named 'users'
    user_snapshot = users_ref.where('Username', '==', username).get()

    for user in user_snapshot:
        # Check password (plain password in Firestore)
        stored_password = user.to_dict().get('password', '')
        if password == stored_password:
            return user.id  # Return the RFID number if authentication is successful
    return None

# Function to get user data by RFID
def get_user_data(rfid):
    user_ref = db.collection('users').document(rfid)
    user_data = user_ref.get()
    return user_data.to_dict()

# Main app logic
def app():
    st.title("Login Portal")

    # Input for Username and Password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Authenticate user
        rfid = authenticate_user(username, password)
        if rfid:
            st.success(f"Welcome {username}!")

            # Get user data
            user_data = get_user_data(rfid)
            bill = user_data['Bill']
            product = user_data['product']
            quantity = user_data['quantity']

            if bill:
                # If Bill is true, show the details of what the user has already bought
                st.subheader("Your Purchase History:")
                st.write(f"Product: {product}")
                st.write(f"Quantity: {quantity}")
                st.write("You have already purchased this product.")

            else:
                # If Bill is false, allow user to place an order
                st.subheader("Your Current Order:")
                st.write(f"Product: {product}")
                st.write(f"Quantity: {quantity}")

                # Allow user to update the order
                st.subheader("Update Your Order")
                new_product = st.text_input("Product", value=product)
                new_quantity = st.number_input("Quantity", value=quantity, min_value=1)

                if st.button("Place Order"):
                    # Update order in Firebase
                    db.collection('users').document(rfid).update({
                        'product': new_product,
                        'quantity': new_quantity,
                        'Bill': True  # Mark the bill as true (purchase complete)
                    })
                    st.success("Order placed successfully!")
                    st.write(f"You have ordered {new_quantity} of {new_product}.")

        else:
            st.error("Invalid username or password.")

if __name__ == "__main__":
    app()
