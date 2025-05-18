import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import qrcode
from io import BytesIO

# Firebase Initialization
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

# Generate QR Code
def generate_qr_code(upi_id, name, amount):
    upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
    qr = qrcode.make(upi_link)
    buffer = BytesIO()
    qr.save(buffer)
    return buffer

# Main App
def app():
    st.title("Rice Order with UPI Payment (Firebase Connected)")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        ref = db.reference("/")
        users = ref.get()

        if not users:
            st.error("No users found in Firebase.")
            return

        uid = None
        user_data = None
        for key, val in users.items():
            if val.get("Username") == username_input and str(val.get("password")) == str(password_input):
                uid = key
                user_data = val
                break

        if not uid:
            st.error("Invalid username or password.")
            return

        st.success(f"Welcome {user_data.get('Username')}!")

        if user_data.get("Bill") is True:
            st.info("You have already purchased this product.")
            st.write(f"Product: {user_data.get('product')}")
            st.write(f"Quantity: {user_data.get('quantity')} grams")
            quantity={user_data.get('quantity')}
            price = quantity * 10
            st.write(f"Total Amount: ₹{price}")
            if "transaction_id" in user_data:
                st.write(f"Transaction ID: {user_data.get('transaction_id')}")
        else:
            st.subheader("Place Your Order")

            product = st.selectbox("Select Product", ["Rice"])
            quantity = st.number_input("Enter Quantity in grams (e.g., 100, 200)", min_value=100, step=100)

            if quantity:
                # Price: ₹10 per 100g
                price = (quantity // 100) * 10
                st.write(f"Total Price: ₹{price}")

                st.write("Scan the QR code to pay:")
                qr_img = generate_qr_code("keerthivasang2004@oksbi", "Keerthi Store", price)
                st.image(qr_img, caption="Scan this with any UPI app")

                txn_id = st.text_input("Enter UPI Transaction ID after payment")

                if st.button("Place Order"):
                    if txn_id.strip() == "":
                        st.error("Please enter a valid UPI transaction ID.")
                    else:
                        db.reference(f"{uid}").update({
                            "product": product,
                            "quantity": str(quantity),
                            "Bill": True,
                            "transaction_id": txn_id
                        })
                        st.success("Order placed and updated in Firebase!")

if __name__ == "__main__":
    app()
