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

# Utility: Get UID from Firebase
def get_user_uid(username, password):
    ref = db.reference("/")
    data = ref.get()
    for uid, user in data.items():
        if user.get("Username") == username and str(user.get("password")) == str(password):
            return uid
    return None

# App starts here
def app():
    st.title("Ration Ordering Portal")

    # Session initialization
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.uid = ""
        st.session_state.username = ""
        st.session_state.user_data = {}

    # If not logged in, show login form
    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            uid = get_user_uid(username, password)
            if uid:
                user_ref = db.reference(f"/{uid}")
                user_data = user_ref.get()
                st.session_state.logged_in = True
                st.session_state.uid = uid
                st.session_state.username = username
                st.session_state.user_data = user_data
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
        return  # Stop further code until logged in

    # User is logged in
    user_data = st.session_state.user_data
    user_ref = db.reference(f"/{st.session_state.uid}")

    if user_data.get("Bill"):
        st.success("✅ Order already placed!")
        st.write(f"**Product**: {user_data.get('product')}")
        st.write(f"**Quantity**: {user_data.get('quantity')}g")
        st.write(f"**Transaction ID**: {user_data.get('transaction_id')}")
        
    else:
        st.subheader("🛒 Place Your Order")
        product = st.selectbox("Select Product", ["Rice"])
        quantity = st.number_input("Enter quantity in grams", min_value=100, step=100, key="quantity_input")
        price = (quantity // 100) * 10
        st.write(f"💰 Total Price: ₹{price}")

        st.markdown("### 📲 Scan & Pay")
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=keerthivasang2004@oksbi&pn=RationStore&am={price}", caption="Scan with any UPI app")

        transaction_id = st.text_input("Enter UPI Transaction ID", key="txn_input")

        if st.button("Place Order"):
            if not transaction_id.strip():
                st.error("⚠️ Please enter a valid UPI Transaction ID.")
            else:
                user_ref.update({
                    "product": product,
                    "quantity": quantity,
                    "Bill": True,
                    "transaction_id": transaction_id
                })
                st.success("✅ Order placed successfully!")
                # Refresh user data in session
                st.session_state.user_data = user_ref.get()

if __name__ == "__main__":
    app()
