import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app
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

def app():
    st.title("Firebase Login")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        ref = db.reference("/")  # root level where all users are listed
        users = ref.get()

        if not users:
            st.error("No data found in Firebase.")
            return

        matched = False

        for uid, data in users.items():
            stored_username = data.get("Username")
            stored_password = str(data.get("password"))  # force to string for comparison

            if stored_username == username_input and stored_password == str(password_input):
                matched = True
                st.success(f"Welcome {stored_username}!")
                st.write(f"User ID: {uid}")
                st.write(f"Bill: {data.get('Bill')}")
                st.write(f"Product: {data.get('product')}")
                st.write(f"Quantity: {data.get('quantity')}")
                break

        if not matched:
            st.error("Username or password incorrect.")

if __name__ == "__main__":
    app()
