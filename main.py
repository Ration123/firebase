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

def app():
    st.title("Display All Firebase Data")

    ref = db.reference("/")  # Root reference since users are stored at root
    data = ref.get()

    if not data:
        st.write("No data found in Firebase.")
        return

    # Display all data in a table-like format
    for key, user in data.items():
        st.subheader(f"User ID: {key}")
        st.write(f"Username: {user.get('Username')}")
        st.write(f"Password: {user.get('password')}")
        st.write(f"Bill: {user.get('Bill')}")
        st.write(f"Product: {user.get('product')}")
        st.write(f"Quantity: {user.get('quantity')}")
        st.markdown("---")

if __name__ == "__main__":
    app()
