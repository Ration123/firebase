import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
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

# Get all user data from Firebase
ref = db.reference("users")
users = ref.get()

# Streamlit app
st.title("Firebase User Data")

if users:
    for uid, data in users.items():
        st.markdown("----")
        st.write(f"**User ID**: `{uid}`")
        st.write(f"**Username**: {data.get('Username')}")
        st.write(f"**Password**: {data.get('password')}")
        st.write(f"**Product**: {data.get('product')}")
        st.write(f"**Quantity**: {data.get('quantity')}")
        st.write(f"**Bill**: {data.get('Bill')}")
else:
    st.warning("No user data found in Firebase.")
