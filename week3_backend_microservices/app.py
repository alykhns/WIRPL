import streamlit as st
import requests

API = "http://localhost:3000/api"

st.set_page_config(
    page_title="Lumiere",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }
[data-testid="stSidebar"] .stRadio label { 
    font-size: 15px !important; padding: 6px 0 !important; 
}

/* Header */
.lumiere-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 50%, #533483 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    color: white;
}
.lumiere-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    margin: 0;
    letter-spacing: -0.5px;
}
.lumiere-header p { margin: 0.3rem 0 0; opacity: 0.6; font-size: 13px; }

/* Product card */
.product-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem;
    border: 1px solid #f0f0f5;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    height: 100%;
    transition: box-shadow 0.2s;
}
.product-card:hover { box-shadow: 0 6px 24px rgba(83,52,131,0.12); }
.product-image {
    background: linear-gradient(135deg, #f0eeff, #e8f4ff);
    border-radius: 10px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    margin-bottom: 1rem;
}
.product-name { font-weight: 500; font-size: 15px; color: #1a1a2e; margin-bottom: 4px; }
.product-price { color: #533483; font-weight: 600; font-size: 17px; margin-bottom: 4px; }
.product-stock { color: #888; font-size: 12px; margin-bottom: 12px; }
.badge-available { 
    background: #eafaf1; color: #1e8449; 
    padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 500;
}
.badge-low { 
    background: #fef9e7; color: #b7950b; 
    padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 500;
}

/* Section title */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: #1a1a2e;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #f0eeff;
}

/* Metric card */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border: 1px solid #f0f0f5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    text-align: center;
}
.metric-value { font-size: 2rem; font-weight: 600; color: #533483; }
.metric-label { font-size: 12px; color: #888; margin-top: 2px; }

/* Cart item */
.cart-item {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    border: 1px solid #f0f0f5;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Order card */
.order-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border: 1px solid #f0f0f5;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.status-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}
.status-order   { background: #eaf0ff; color: #2e5bce; }
.status-pay     { background: #fff3e0; color: #e65100; }
.status-delivery{ background: #e8f5e9; color: #2e7d32; }
.status-cancel  { background: #fce4ec; color: #c62828; }

/* Auth form */
.auth-container {
    max-width: 420px;
    margin: 3rem auto;
    background: white;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 8px 40px rgba(83,52,131,0.12);
}

/* Sticker success */
.success-banner {
    background: linear-gradient(135deg, #eafaf1, #d5f5e3);
    border-left: 4px solid #27ae60;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin: 1rem 0;
    color: #1e8449;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──
for key, val in [("token", None), ("user", None), ("cart", [])]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ──
with st.sidebar:
    st.markdown("## ✨ Lumiere")
    st.caption("Multisystem E-Commerce")
    st.divider()

    if st.session_state.token:
        st.success(f"👤 {st.session_state.user['username']}")
        cart_count = len(st.session_state.cart)
        if cart_count > 0:
            st.info(f"🛒 {cart_count} item di keranjang")
        page = st.radio("Navigasi", [
            "🏠 Beranda", "🛍️ Produk", "🛒 Keranjang",
            "📦 Orders", "🔍 Lacak Paket"
        ])
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.cart = []
            st.rerun()
    else:
        page = "🔐 Auth"

# ── Header ──
st.markdown("""
<div class="lumiere-header">
    <h1>✨ Lumiere</h1>
    <p>Multisystem Architecture · Week 3 · Node.js + Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────
# PAGE: AUTH
# ────────────────────────────────
if not st.session_state.token:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔑 Login", "📝 Daftar"])

        with tab_login:
            email = st.text_input("Email", placeholder="nama@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("Masuk →", use_container_width=True, type="primary"):
                try:
                    res = requests.post(f"{API}/auth/login", json={"email": email, "password": password})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.token = data["token"]
                        st.session_state.user = data["user"]
                        st.rerun()
                    else:
                        st.error(res.json().get("error", "Login gagal"))
                except:
                    st.error("❌ Tidak bisa konek ke server. Pastikan Node.js jalan!")

        with tab_register:
            r_username = st.text_input("Username")
            r_email    = st.text_input("Email", key="reg_email")
            r_password = st.text_input("Password", type="password", key="reg_pass")
            c1, c2     = st.columns(2)
            r_fname    = c1.text_input("Nama Depan")
            r_lname    = c2.text_input("Nama Belakang")
            if st.button("Daftar Sekarang", use_container_width=True, type="primary"):
                try:
                    res = requests.post(f"{API}/auth/register", json={
                        "username": r_username, "email": r_email,
                        "password": r_password, "first_name": r_fname, "last_name": r_lname
                    })
                    if res.status_code == 201:
                        st.success("✅ Berhasil! Silakan login.")
                    else:
                        st.error(res.json().get("error", "Gagal register"))
                except:
                    st.error("❌ Tidak bisa konek ke server.")

# ────────────────────────────────
# PAGE: BERANDA
# ────────────────────────────────
elif page == "🏠 Beranda":
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)

    try:
        products = requests.get(f"{API}/products").json()
        orders   = requests.get(f"{API}/orders").json()
        couriers = requests.get(f"{API}/logistics/couriers").json()
        methods  = requests.get(f"{API}/payment/methods").json()
    except:
        products, orders, couriers, methods = [], [], [], []

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, icon in [
        (c1, len(products), "Total Produk", "📦"),
        (c2, len(orders),   "Total Orders", "📋"),
        (c3, len(couriers), "Kurir Aktif",  "🚚"),
        (c4, len(methods),  "Metode Bayar", "💳"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size:2rem">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🏷️ Produk Terbaru")
    cols = st.columns(4)
    for i, p in enumerate(products[:4]):
        emoji = ["👗","📱","🪑","💄","⚽","📚","👟","🎮"][i % 8]
        stock_badge = (
            '<span class="badge-available">Tersedia</span>' if p["stock"] > 10
            else '<span class="badge-low">Stok Sedikit</span>'
        )
        cols[i % 4].markdown(f"""
        <div class="product-card">
            <div class="product-image">{emoji}</div>
            <div class="product-name">{p['product_name']}</div>
            <div class="product-price">Rp {float(p['price']):,.0f}</div>
            <div class="product-stock">Stok: {p['stock']} &nbsp; {stock_badge}</div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────
# PAGE: PRODUK
# ────────────────────────────────
elif page == "🛍️ Produk":
    st.markdown('<div class="section-title">Katalog Produk</div>', unsafe_allow_html=True)

    try:
        products = requests.get(f"{API}/products").json()
    except:
        st.error("❌ Gagal memuat produk"); products = []

    # Search & Filter
    col_search, col_sort = st.columns([3, 1])
    search = col_search.text_input("🔍 Cari produk...", placeholder="Ketik nama produk")
    sort   = col_sort.selectbox("Urutkan", ["Terbaru", "Harga ↑", "Harga ↓", "Stok ↑"])

    if search:
        products = [p for p in products if search.lower() in p["product_name"].lower()]
    if sort == "Harga ↑":
        products = sorted(products, key=lambda x: float(x["price"]))
    elif sort == "Harga ↓":
        products = sorted(products, key=lambda x: float(x["price"]), reverse=True)
    elif sort == "Stok ↑":
        products = sorted(products, key=lambda x: x["stock"])

    st.caption(f"Menampilkan {len(products)} produk")
    st.divider()

    emojis = ["👗","📱","🪑","💄","⚽","📚","👟","🎮","🧴","🎒","⌚","🖥️"]
    cols = st.columns(3)
    for i, p in enumerate(products):
        emoji = emojis[i % len(emojis)]
        stock_badge = (
            '<span class="badge-available">Tersedia</span>' if p["stock"] > 10
            else '<span class="badge-low">Stok Sedikit</span>'
        )
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <div class="product-image">{emoji}</div>
                <div class="product-name">{p['product_name']}</div>
                <div class="product-price">Rp {float(p['price']):,.0f}</div>
                <div class="product-stock">Stok: {p['stock']} &nbsp; {stock_badge}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"🛒 Tambah ke Keranjang", key=f"add_{p['product_id']}",
                         use_container_width=True):
                st.session_state.cart.append(p)
                st.toast(f"✅ {p['product_name']} ditambahkan!", icon="🛒")

# ────────────────────────────────
# PAGE: KERANJANG
# ────────────────────────────────
elif page == "🛒 Keranjang":
    st.markdown('<div class="section-title">Keranjang Belanja</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("🛒 Keranjang kamu masih kosong. Yuk belanja dulu!")
    else:
        col_cart, col_summary = st.columns([2, 1])

        with col_cart:
            st.subheader(f"Item ({len(st.session_state.cart)})")
            total = 0
            to_remove = []
            emojis = ["👗","📱","🪑","💄","⚽","📚","👟","🎮","🧴","🎒","⌚","🖥️"]
            for i, item in enumerate(st.session_state.cart):
                emoji = emojis[i % len(emojis)]
                col_a, col_b = st.columns([4, 1])
                col_a.markdown(f"""
                <div class="cart-item">
                    <span style="font-size:1.5rem">{emoji}</span>
                    <span style="flex:1; margin-left:12px">
                        <b>{item['product_name']}</b><br>
                        <span style="color:#533483">Rp {float(item['price']):,.0f}</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
                if col_b.button("🗑️", key=f"rm_{i}"):
                    to_remove.append(i)
                total += float(item["price"])
            for idx in reversed(to_remove):
                st.session_state.cart.pop(idx)
                st.rerun()

        with col_summary:
            st.subheader("Ringkasan")
            st.markdown(f"""
            <div class="order-card">
                <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                    <span style="color:#666">Subtotal</span>
                    <span>Rp {total:,.0f}</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                    <span style="color:#666">Ongkir</span>
                    <span style="color:#27ae60">Gratis</span>
                </div>
                <hr style="margin:12px 0; border:none; border-top:1px solid #f0f0f5">
                <div style="display:flex;justify-content:space-between">
                    <b>Total</b>
                    <b style="color:#533483; font-size:1.1rem">Rp {total:,.0f}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            try:
                methods  = requests.get(f"{API}/payment/methods").json()
                couriers = requests.get(f"{API}/logistics/couriers").json()
            except:
                methods, couriers = [], []

            method_map  = {f"{m['provider']} ({m['method_name']})": m["method_id"] for m in methods}
            courier_map = {f"{c['courier_name']} - {c['service_type']}": c["courier_id"] for c in couriers}

            sel_method  = st.selectbox("💳 Pembayaran", list(method_map.keys()))
            sel_courier = st.selectbox("🚚 Kurir", list(courier_map.keys()))

            if st.button("✅ Checkout Sekarang", use_container_width=True, type="primary"):
                items = [{"product_id": p["product_id"], "quantity": 1, "price": p["price"]}
                         for p in st.session_state.cart]
                payload = {
                    "buyer_id": st.session_state.user["user_id"],
                    "institution_id": 1,
                    "total_amount": total,
                    "items": items,
                    "payment_method_id": method_map[sel_method],
                    "courier_id": courier_map[sel_courier],
                }
                try:
                    res = requests.post(f"{API}/orders/checkout", json=payload)
                    if res.status_code == 201:
                        data = res.json()
                        st.balloons()
                        st.success(f"🎉 Checkout berhasil! Order #{data['order_id']}")
                        st.info(f"📦 Nomor Resi: **{data['tracking_number']}**")
                        st.session_state.cart = []
                    else:
                        st.error("Checkout gagal: " + str(res.json()))
                except Exception as e:
                    st.error(f"Error: {e}")

# ────────────────────────────────
# PAGE: ORDERS
# ────────────────────────────────
elif page == "📦 Orders":
    st.markdown('<div class="section-title">Riwayat Order</div>', unsafe_allow_html=True)
    try:
        orders = requests.get(f"{API}/orders").json()
    except:
        st.error("❌ Gagal memuat orders"); orders = []

    if not orders:
        st.info("Belum ada order.")
    else:
        status_class = {
            "order": "status-order", "pay": "status-pay",
            "delivery": "status-delivery", "cancel": "status-cancel"
        }
        for o in orders:
            sc = status_class.get(o.get("order_status", "order"), "status-order")
            with st.expander(f"📋 Order #{o['order_id']}  —  Rp {float(o['total_amount']):,.0f}"):
                st.markdown(f"""
                <span class="status-pill {sc}">{o.get('order_status','—').upper()}</span>
                <span style="color:#888; font-size:13px; margin-left:10px">{o.get('created_at','')}</span>
                """, unsafe_allow_html=True)
                try:
                    detail = requests.get(f"{API}/orders/{o['order_id']}").json()
                    col_p, col_s = st.columns(2)
                    with col_p:
                        st.markdown("**💳 Payment**")
                        pay = detail.get("payment")
                        if pay:
                            st.write(f"Status: `{pay.get('status','—')}`")
                            st.write(f"Jumlah: Rp {float(pay.get('amount',0)):,.0f}")
                        else:
                            st.caption("Belum ada data payment")
                    with col_s:
                        st.markdown("**🚚 Pengiriman**")
                        ship = detail.get("shipment")
                        if ship:
                            st.write(f"Kurir: `{ship.get('courier_name','—')}`")
                            st.write(f"Resi: `{ship.get('tracking_number','—')}`")
                            st.write(f"Status: `{ship.get('shipping_status','—')}`")
                        else:
                            st.caption("Belum ada data pengiriman")
                except:
                    st.caption("Gagal memuat detail")

# ────────────────────────────────
# PAGE: LACAK PAKET
# ────────────────────────────────
elif page == "🔍 Lacak Paket":
    st.markdown('<div class="section-title">Lacak Paket</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    tracking_no = col1.text_input("Masukkan Nomor Resi", placeholder="LMR-1234567890")
    lacak = col2.button("🔍 Lacak", use_container_width=True, type="primary")

    if lacak and tracking_no:
        try:
            res = requests.get(f"{API}/logistics/track/{tracking_no}")
            if res.status_code == 200:
                data = res.json()
                ship = data["shipment"]
                st.markdown(f"""
                <div class="order-card">
                    <b>📦 {ship['tracking_number']}</b><br>
                    <span style="color:#533483">🚚 {ship['courier_name']} — {ship['service_type']}</span><br>
                    <span style="color:#888; font-size:13px">Status: <b>{ship['shipping_status'].upper()}</b></span>
                </div>
                """, unsafe_allow_html=True)

                st.subheader("📍 Riwayat Perjalanan")
                if data["history"]:
                    for h in data["history"]:
                        st.markdown(f"- **{h['recorded_at']}** — {h['location']}: {h['status_note']}")
                else:
                    st.caption("Belum ada riwayat tracking.")
            else:
                st.error("❌ Nomor resi tidak ditemukan.")
        except:
            st.error("❌ Gagal konek ke server.")