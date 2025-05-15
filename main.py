import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app using st.secrets
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets.FIREBASE.type,
        "project_id": st.secrets.FIREBASE.project_id,
        "private_key_id": st.secrets.FIREBASE.private_key_id,
        "private_key": st.secrets.FIREBASE.private_key.replace("\\n", "\n"),
        "client_email": st.secrets.FIREBASE.client_email,
        "client_id": st.secrets.FIREBASE.client_id,
        "auth_uri": st.secrets.FIREBASE.auth_uri,
        "token_uri": st.secrets.FIREBASE.token_uri,
        "auth_provider_x509_cert_url": st.secrets.FIREBASE.auth_provider_x509_cert_url,
        "client_x509_cert_url": st.secrets.FIREBASE.client_x509_cert_url
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': st.secrets.FIREBASE.databaseURL
    })

# Function to authenticate user
def authenticate_user(username, password):
    ref = db.reference("users")
    users = ref.get()
    if users:
        for uid, user in users.items():
            if user.get("Username") == username and user.get("password") == password:
                return uid
    return None

# Function to get user data
def get_user_data(uid):
    return db.reference(f"users/{uid}").get()

# Streamlit App
def app():
    st.title("Realtime Vending Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        uid = authenticate_user(username, password)
        if uid:
            user_data = get_user_data(uid)
            st.success(f"Welcome {username}!")

            bill = user_data.get("Bill")
            product = user_data.get("product")
            quantity = user_data.get("quantity")

            if bill:
                st.subheader("Your Purchase History:")
                st.write(f"Product: {product}")
                st.write(f"Quantity: {quantity}")
                st.write("You have already purchased this product.")
            else:
                st.subheader("Your Current Order:")
                st.write(f"Product: {product}")
                st.write(f"Quantity: {quantity}")

                new_product = st.text_input("Update Product", value=product)
                new_quantity = st.number_input("Update Quantity", value=int(quantity), min_value=1)

                if st.button("Place Order"):
                    db.reference(f"users/{uid}").update({
                        "product": new_product,
                        "quantity": new_quantity,
                        "Bill": True
                    })
                    st.success("Order placed successfully!")

        else:
            st.error("Invalid username or password.")

if __name__ == "__main__":
    app()
