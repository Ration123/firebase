import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

# 🚀 Page Config
st.set_page_config(page_title="Ration Shop Stock Monitor", page_icon="📦")

# ✅ Firebase Credentials (from .streamlit/secrets.toml)
firebase_secrets = dict(st.secrets["firebase"])
firebase_secrets["private_key"] = firebase_secrets["private_key"].replace('\\n', '\n')

# ✅ Initialize Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_secrets)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://your-database.firebaseio.com/'  # Replace with your URL
        })
        st.success("✅ Firebase connected successfully!")
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {e}")

# 🔍 Fetch stock data from Firebase
def get_stock_data():
    try:
        ref = db.reference('/ration_stock')
        data = ref.get()
        return data
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

# 📊 Plotting Function
def plot_stock_chart(names, quantities):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, quantities, color='seagreen')

    # Label quantities on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height} kg', ha='center', va='bottom', fontsize=10)

    ax.set_title("Rice Stock Quantity", fontsize=14)
    ax.set_ylabel("Quantity (kg)")
    ax.set_xlabel("Rice Types")
    ax.set_ylim(0, max(quantities) + 20)
    return fig

# 🖥️ UI Start
st.title("📦 Ration Shop Stock Monitor")

data = get_stock_data()

if data:
    names = []
    quantities = []
    qualities = []

    for rice_type, values in data.items():
        names.append(rice_type)
        quantities.append(values.get("quantity", 0))
        qualities.append(values.get("quality", "Unknown"))

    st.subheader("📊 Stock Overview")
    st.pyplot(plot_stock_chart(names, quantities))

    st.subheader("📝 Rice Quality Grades")
    for name, qual in zip(names, qualities):
        st.markdown(f"**{name}**: Grade **{qual}**")

else:
    st.warning("No stock data found in Firebase.")


