import streamlit as st

st.set_page_config(
    page_title="TechWorld - Electronics & Gadgets",
    page_icon="💻",
    layout="wide"
)

# Custom CSS for TechWorld Theme (Dark Blue #0A2647, Tech Blue #00B4D8)
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #00B4D8;
        color: white;
        border-radius: 5px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0A2647;
        color: white;
    }
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Session State for Cart, Wishlist, Orders, and User Login
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# Product Catalog Database (including MacBook Pro and other gadgets)
products = [
    {
        "id": 1,
        "name": "iPhone 15 Pro",
        "brand": "Apple",
        "price": 999.99,
        "category": "Smartphones",
        "specs": "6.1-inch, A17 Pro, 256GB",
        "rating": 4.9,
        "image": "📱"
    },
    {
        "id": 2,
        "name": "MacBook Pro 16",
        "brand": "Apple",
        "price": 2499.99,
        "category": "Laptops & Tablets",
        "specs": "M3 Max, 36GB, 1TB",
        "rating": 4.8,
        "image": "💻"
    },
    {
        "id": 3,
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "price": 1299.99,
        "category": "Smartphones",
        "specs": "6.8-inch, Snapdragon 8 Gen 3, 512GB",
        "rating": 4.8,
        "image": "📱"
    },
    {
        "id": 4,
        "name": "Dell XPS 15",
        "brand": "Dell",
        "price": 1799.99,
        "category": "Laptops & Tablets",
        "specs": "15.6 4K OLED, i7-13700H, 16GB RAM",
        "rating": 4.7,
        "image": "💻"
    },
    {
        "id": 5,
        "name": "Sony WH-1000XM5",
        "brand": "Sony",
        "price": 399.99,
        "category": "Audio & Wearables",
        "specs": "Wireless Noise Cancelling Headphones",
        "rating": 4.9,
        "image": "🎧"
    },
    {
        "id": 6,
        "name": "Apple Watch Series 9",
        "brand": "Apple",
        "price": 399.99,
        "category": "Audio & Wearables",
        "specs": "GPS, Always-On Retina Display",
        "rating": 4.7,
        "image": "⌚"
    }
]

# Sidebar Navigation
st.sidebar.title("💻 TechWorld")
st.sidebar.markdown("**Electronics & Gadgets Store**")
menu = st.sidebar.radio("Navigation", [
    "Home", 
    "Product Catalog", 
    "Shopping Cart", 
    "Wishlist", 
    "Checkout", 
    "User Account", 
    "About Us", 
    "Contact Us"
])

# Cart item count badge
cart_count = sum(item['quantity'] for item in st.session_state.cart)
st.sidebar.markdown(f"🛒 **Cart Items:** {cart_count}")

# ----------------- HOME PAGE -----------------
if menu == "Home":
    st.title("Welcome to TechWorld 🚀")
    st.markdown("### Next-Gen Electronics & Gadgets at Your Fingertips")
    
    with st.container():
        st.info("🔥 **Special Offer:** Get $100 off on all Laptops and Gadgets using promo code `TECH100` at checkout!")
    
    st.markdown("## Featured Categories")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### 📱 Smartphones")
        st.write("Apple, Samsung, Google, OnePlus")
    with col2:
        st.markdown("### 💻 Laptops")
        st.write("MacBook, Dell XPS, HP, Surface")
    with col3:
        st.markdown("### 🎧 Audio")
        st.write("Headphones, Earbuds, Speakers")
    with col4:
        st.markdown("### ⌚ Wearables")
        st.write("Smartwatches, Fitness Bands")

    st.markdown("## 🔥 Featured Products")
    cols = st.columns(3)
    for idx, prod in enumerate(products[:3]):
        with cols[idx]:
            st.markdown(f"""
            <div class="product-card">
                <h2>{prod['image']}</h2>
                <h4>{prod['name']}</h4>
                <p><b>Brand:</b> {prod['brand']}</p>
                <p><b>Specs:</b> {prod['specs']}</p>
                <p><b>Price:</b> ${prod['price']:.2f}</p>
                <p>⭐ {prod['rating']} / 5.0</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Add to Cart", key=f"home_{prod['id']}"):
                found = False
                for cart_item in st.session_state.cart:
                    if cart_item['id'] == prod['id']:
                        cart_item['quantity'] += 1
                        found = True
                        break
                if not found:
                    st.session_state.cart.append({**prod, 'quantity': 1})
                st.success(f"Added {prod['name']} to cart!")

# ----------------- PRODUCT CATALOG -----------------
elif menu == "Product Catalog":
    st.title("📦 Product Catalog")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search_query = st.text_input("🔍 Search products...")
    with col_f2:
        categories = ["All"] + list(set(p['category'] for p in products))
        selected_cat = st.selectbox("Category Filter", categories)
    with col_f3:
        selected_brand = st.selectbox("Brand Filter", ["All"] + list(set(p['brand'] for p in products)))

    # Filtering logic
    filtered_products = products
    if search_query:
        filtered_products = [p for p in filtered_products if search_query.lower() in p['name'].lower() or search_query.lower() in p['brand'].lower()]
    if selected_cat != "All":
        filtered_products = [p for p in filtered_products if p['category'] == selected_cat]
    if selected_brand != "All":
        filtered_products = [p for p in filtered_products if p['brand'] == selected_brand]

    st.write(f"Showing {len(filtered_products)} products")

    for prod in filtered_products:
        with st.container():
            col_img, col_info, col_act = st.columns([1, 3, 2])
            with col_img:
                st.markdown(f"<h1>{prod['image']}</h1>", unsafe_allow_html=True)
            with col_info:
                st.subheader(prod['name'])
                st.write(f"**Brand:** {prod['brand']} | **Category:** {prod['category']}")
                st.write(f"**Specifications:** {prod['specs']}")
                st.write(f"⭐ Rating: {prod['rating']} / 5.0")
            with col_act:
                st.markdown(f"### **${prod['price']:.2f}**")
                if st.button("Add to Cart", key=f"cat_{prod['id']}"):
                    found = False
                    for item in st.session_state.cart:
                        if item['id'] == prod['id']:
                            item['quantity'] += 1
                            found = True
                            break
                    if not found:
                        st.session_state.cart.append({**prod, 'quantity': 1})
                    st.success("Added to cart!")
                if st.button("❤️ Add to Wishlist", key=f"wish_{prod['id']}"):
                    if prod not in st.session_state.wishlist:
                        st.session_state.wishlist.append(prod)
                        st.success("Added to wishlist!")
                    else:
                        st.warning("Already in wishlist!")
        st.divider()

# ----------------- SHOPPING CART -----------------
elif menu == "Shopping Cart":
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Explore our catalog to add items!")
    else:
        subtotal = 0
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"**{item['name']}**")
                st.caption(item['specs'])
            with col2:
                st.write(f"${item['price']:.2f}")
            with col3:
                new_qty = st.number_input("Qty", min_value=1, value=item['quantity'], key=f"qty_{item['id']}")
                st.session_state.cart[i]['quantity'] = new_qty
            with col4:
                if st.button("❌ Remove", key=f"rem_{item['id']}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            subtotal += item['price'] * item['quantity']
            st.divider()
            
        st.markdown(f"### Subtotal: ${subtotal:.2f}")
        
        promo = st.text_input("Promo Code (Try `TECH100`)")
        discount = 0
        if promo == "TECH100":
            discount = 100
            st.success("Promo code applied: $100 off!")
        elif promo != "":
            st.error("Invalid promo code")
            
        total = max(0, subtotal - discount)
        st.markdown(f"## Total: ${total:.2f}")
        
        if st.button("Proceed to Checkout ➡️"):
            st.info("Please navigate to **Checkout** in the sidebar to finalize your order.")

# ----------------- WISHLIST -----------------
elif menu == "Wishlist":
    st.title("❤️ Your Wishlist")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty.")
    else:
        for i, item in enumerate(st.session_state.wishlist):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{item['name']}** - ${item['price']:.2f}")
            with col2:
                if st.button("Move to Cart", key=f"w_cart_{item['id']}"):
                    st.session_state.cart.append({**item, 'quantity': 1})
                    st.session_state.wishlist.pop(i)
                    st.success("Moved to cart!")
                    st.rerun()
            with col3:
                if st.button("Remove", key=f"w_rem_{item['id']}"):
                    st.session_state.wishlist.pop(i)
                    st.rerun()
            st.divider()

# ----------------- CHECKOUT -----------------
elif menu == "Checkout":
    st.title("💳 Secure Checkout")
    if not st.session_state.cart:
        st.warning("Your cart is empty. Please add items before checking out.")
    else:
        with st.form("checkout_form"):
            st.subheader("Shipping Address")
            name = st.text_input("Full Name")
            address = st.text_input("Street Address")
            city = st.text_input("City")
            pincode = st.text_input("Postal Code")
            
            st.subheader("Payment Method")
            payment_method = st.selectbox("Choose Payment", ["Credit/Debit Card", "UPI / PhonePe", "Cash on Delivery"])
            
            submitted = st.form_submit_button("Place Order")
            if submitted:
                if name and address and city:
                    order_summary = {
                        "items": list(st.session_state.cart),
                        "name": name,
                        "address": address,
                        "payment": payment_method
                    }
                    st.session_state.orders.append(order_summary)
                    st.session_state.cart = []
                    st.success("🎉 Order placed successfully! Thank you for shopping with TechWorld.")
                else:
                    st.error("Please fill in all shipping details.")

# ----------------- USER ACCOUNT -----------------
elif menu == "User Account":
    st.title("👤 User Account")
    if not st.session_state.logged_in:
        st.subheader("Login / Register")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Please enter a valid email.")
    else:
        st.write(f"Welcome back, **{st.session_state.user_email}**!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.rerun()
            
        st.subheader("📦 Order History")
        if not st.session_state.orders:
            st.info("No past orders found.")
        else:
            for idx, order in enumerate(st.session_state.orders):
                st.markdown(f"**Order #{idx+1}** - Shipped to: {order['name']}, {order['address']} via {order['payment']}")
                st.divider()

# ----------------- ABOUT US -----------------
elif menu == "About Us":
    st.title("ℹ️ About TechWorld")
    st.write("TechWorld is a comprehensive online electronics and gadgets store offering smartphones, laptops, audio devices, smartwatches, and tech accessories.")
    st.write("This application was built as part of the Web Development Internship online task.")

# ----------------- CONTACT US -----------------
elif menu == "Contact Us":
    st.title("📞 Contact Us")
    st.write("Have questions or need support? Get in touch with our team.")
    with st.form("contact_form"):
        st.text_input("Your Name")
        st.text_input("Your Email")
        st.text_area("Message")
        if st.form_submit_button("Send Message"):
            st.success("Thank you! Your message has been sent successfully.")