import streamlit as st
import pandas as pd
import datetime
from dataclasses import dataclass
from typing import List, Dict
import uuid

# Page configuration
st.set_page_config(
    page_title="Make-to-Order Manufacturing Flow",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
    /* Color Palette Variables */
    :root {
        --primary-color: #3c4b33;
        --secondary-color: #efb9a5;
        --accent-color: #e9c770;
        --background-color: #eeeced;
        --info-color: #c7d6e3;
        --success-color: #bfc694;
        --light-color: #ffe6dd;
        --dark-green: #6f8d5e;
        --light-brown: #CD853F;
        --black: #000000;
    }
    
    /* Global light brown font styling */
    .main .block-container {
        color: var(--light-brown) !important;
    }
    
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div, li {
        color: var(--light-brown) !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stTextArea label {
        color: var(--light-brown) !important;
    }
    
    .stMetric label, .stMetric .metric-value {
        color: var(--light-brown) !important;
    }
    
    .stDataFrame, .stTable, .dataframe {
        color: var(--light-brown) !important;
    }
    
    .stDataFrame td, .stDataFrame th, .dataframe td, .dataframe th {
        color: var(--light-brown) !important;
    }
    
    /* Main styling */
    .main {
        background-color: var(--background-color);
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--dark-green));
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: var(--light-color) !important;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .process-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid var(--accent-color);
        color: var(--light-brown) !important;
    }
    
    .process-card h3, .process-card h4, .process-card p, .process-card li {
        color: var(--light-brown) !important;
    }
    
    .status-card {
        background-color: var(--light-color);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid var(--secondary-color);
        color: var(--light-brown) !important;
    }
    
    .status-card h4, .status-card p {
        color: var(--light-brown) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--primary-color);
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: var(--dark-green);
        color: white !important;
    }
    
    /* Success styling */
    .success-message {
        background-color: var(--success-color);
        color: var(--light-brown) !important;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    .success-message h4, .success-message p {
        color: var(--light-brown) !important;
    }
    
    /* Info styling */
    .info-box {
        background-color: var(--info-color);
        color: var(--light-brown) !important;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--primary-color);
    }
    
    /* Flow diagram styling */
    .flow-step {
        background-color: var(--accent-color);
        color: var(--light-brown) !important;
        padding: 1rem;
        margin: 0.5rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        border: 2px solid var(--primary-color);
    }
    
    .flow-step h4, .flow-step p {
        color: var(--light-brown) !important;
    }
    
    .flow-arrow {
        text-align: center;
        font-size: 2rem;
        color: var(--light-brown) !important;
        margin: 0.5rem 0;
    }
    
    /* Company examples styling */
    .company-example {
        background-color: var(--secondary-color);
        color: var(--light-brown) !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        text-align: center;
    }
    
    .company-example h4, .company-example p {
        color: var(--light-brown) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Data models
@dataclass
class Product:
    id: str
    name: str
    category: str
    price: float
    sustainability_score: int

@dataclass
class SalesOrder:
    id: str
    customer_name: str
    product: Product
    quantity: int
    order_date: datetime.datetime
    status: str
    total_amount: float

@dataclass
class ProductionOrder:
    id: str
    sales_order_id: str
    product: Product
    quantity: int
    start_date: datetime.datetime
    status: str
    completion_percentage: int

@dataclass
class Delivery:
    id: str
    production_order_id: str
    delivery_date: datetime.datetime
    status: str
    tracking_number: str

# Initialize session state
def initialize_session_state():
    if 'sales_orders' not in st.session_state:
        st.session_state.sales_orders = []
    if 'production_orders' not in st.session_state:
        st.session_state.production_orders = []
    if 'deliveries' not in st.session_state:
        st.session_state.deliveries = []
    if 'order_counter' not in st.session_state:
        st.session_state.order_counter = 1

# Sample products
def get_sample_products():
    return [
        Product("PKG001", "Eco-Friendly Bouquet Wrapper", "Flower Shop", 15.99, 95),
        Product("PKG002", "Biodegradable Gift Box", "Gift Store", 8.50, 90),
        Product("PKG003", "Compostable Food Container", "Food & Beverage", 12.75, 88),
        Product("PKG004", "Recycled Paper Bag", "General", 3.25, 85),
        Product("PKG005", "Plant-Based Drink Cup", "Food & Beverage", 6.99, 92),
        Product("PKG006", "Sustainable Gift Wrap", "Gift Store", 4.50, 87),
    ]

# Main application
def main():
    load_css()
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📦 Make-to-Order Manufacturing Flow</h1>
        <p>Sustainable Packaging Kits - An Eco-Friendly Solution for Reducing Environmental Waste</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🌱 Navigation")
    page = st.sidebar.selectbox("Select Process Step", [
        "🏠 Overview",
        "📋 Sales Order Creation (VA01)",
        "🏭 Production Order Management",
        "✅ Production Confirmation",
        "🚚 Delivery & Billing Cycle",
        "📊 Order Documentation"
    ])
    
    if page == "🏠 Overview":
        show_overview()
    elif page == "📋 Sales Order Creation (VA01)":
        show_sales_order_creation()
    elif page == "🏭 Production Order Management":
        show_production_order_management()
    elif page == "✅ Production Confirmation":
        show_production_confirmation()
    elif page == "🚚 Delivery & Billing Cycle":
        show_delivery_billing()
    elif page == "📊 Order Documentation":
        show_order_documentation()

def show_overview():
    st.header("🌍 Sustainable Packaging Solutions")
    
    companies = [
        ("🌸 Flower Shops", "Bouquet wrappers & packaging"),
        ("🎁 Gift Stores", "Gift wrappers & packaging"),
        ("🍽️ Food & Beverage", "Food and drink packaging")
    ]
    
    for company, description in companies:
        st.markdown(f"""
        <div class="company-example">
            <h4>{company}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Current status overview
    st.header("📊 Current System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales Orders", len(st.session_state.sales_orders))
    with col2:
        st.metric("Active Production Orders", len(st.session_state.production_orders))
    with col3:
        st.metric("Completed Deliveries", len(st.session_state.deliveries))
    with col4:
        # Calculate actual average sustainability score from orders
        if st.session_state.sales_orders:
            sustainability_scores = [order.product.sustainability_score for order in st.session_state.sales_orders]
            sustainability_avg = sum(sustainability_scores) / len(sustainability_scores)
            st.metric("Avg Sustainability Score", f"{sustainability_avg:.1f}%")
        else:
            st.metric("Avg Sustainability Score", "0%")

def show_sales_order_creation():
    st.header("📋 Sales Order Creation (VA01)")
    
    st.markdown("""
    <div class="info-box">
        <strong>Sprint 1 Objective:</strong> Configure and test sales order creation as the customer trigger for the MTO process.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("sales_order_form"):
        st.subheader("Create New Sales Order")

        col1, col2 = st.columns(2)

        with col1:
            customer_name = st.text_input("Customer Name", placeholder="Enter customer company name")
            products = get_sample_products()
            product_options = [f"{p.name} - ${p.price}" for p in products]
            selected_product_idx = st.selectbox(
                "Select Product", ["-- Select --"] + list(range(len(product_options))),
                format_func=lambda x: "-- Select --" if x == "-- Select --" else product_options[x]
            )
            quantity = st.number_input("Quantity", min_value=1, max_value=1000, value=1)

        with col2:
            if selected_product_idx == "-- Select --":
                st.markdown(f"""
<div class="status-card">
    <h4>Product Details</h4>
    <p><strong>Category:</strong> </p>
    <p><strong>Price:</strong> </p>
    <p><strong>Sustainability Score:</strong> </p>
</div>
""", unsafe_allow_html=True)
                st.markdown(
                    '<div class="success-message" style="background-color: #d4ede1; color: #CD853F; padding: 1rem; border-radius: 5px; margin: 1rem 0; font-weight: bold;">'
                    '<strong>Total Order Amount:</strong> '
                    '</div>', unsafe_allow_html=True)
                total_amount = 0
            else:
                selected_product = products[selected_product_idx]
                st.markdown(f"""
<div class="status-card">
    <h4>Product Details</h4>
    <p><strong>Category:</strong> {selected_product.category}</p>
    <p><strong>Price:</strong> ${selected_product.price}</p>
    <p><strong>Sustainability Score:</strong> {selected_product.sustainability_score}%</p>
</div>
""", unsafe_allow_html=True)
                total_amount = selected_product.price * quantity
                st.success(f"**Total Order Amount: ${total_amount:.2f}**")

        submitted = st.form_submit_button("Create Sales Order")
        if submitted and customer_name and selected_product_idx != "-- Select --":
            order_id = f"SO{st.session_state.order_counter:04d}"
            st.session_state.order_counter += 1
            new_order = SalesOrder(
                id=order_id,
                customer_name=customer_name,
                product=products[selected_product_idx],
                quantity=quantity,
                order_date=datetime.datetime.now(),
                status="Created",
                total_amount=total_amount
            )
            st.session_state.sales_orders.append(new_order)
            st.success(f"✅ Sales Order {order_id} created successfully!")
            st.balloons()
    
    # Display existing sales orders
    if st.session_state.sales_orders:
        st.subheader("📋 Current Sales Orders")
        
        orders_data = []
        for order in st.session_state.sales_orders:
            orders_data.append({
                "Order ID": order.id,
                "Customer": order.customer_name,
                "Product": order.product.name,
                "Quantity": order.quantity,
                "Total Amount": f"${order.total_amount:.2f}",
                "Status": order.status,
                "Order Date": order.order_date.strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(orders_data)
        st.dataframe(df, use_container_width=True)

def show_production_order_management():
    st.header("🏭 Production Order Management")
    
    st.markdown("""
    <div class="info-box">
        <strong>Sprint 2 & 3 Objectives:</strong> Enable automatic planned order generation from sales orders and convert them into production orders.
    </div>
    """, unsafe_allow_html=True)
    
    # Show sales orders ready for production
    pending_orders = [order for order in st.session_state.sales_orders if order.status == "Created"]
    
    if pending_orders:
        st.subheader("📋 Sales Orders Ready for Production")
        
        for order in pending_orders:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="status-card">
                    <h4>Order {order.id}</h4>
                    <p><strong>Customer:</strong> {order.customer_name}</p>
                    <p><strong>Product:</strong> {order.product.name}</p>
                    <p><strong>Quantity:</strong> {order.quantity}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Total:** ${order.total_amount:.2f}")
                st.markdown(f"**Sustainability:** {order.product.sustainability_score}%")
            
            with col3:
                if st.button(f"Create Production Order", key=f"prod_{order.id}"):
                    # Create production order
                    prod_order_id = f"PO{len(st.session_state.production_orders) + 1:04d}"
                    
                    production_order = ProductionOrder(
                        id=prod_order_id,
                        sales_order_id=order.id,
                        product=order.product,
                        quantity=order.quantity,
                        start_date=datetime.datetime.now(),
                        status="Planned",
                        completion_percentage=0
                    )
                    
                    st.session_state.production_orders.append(production_order)
                    
                    # Update sales order status
                    order.status = "In Production"
                    
                    st.success(f"✅ Production Order {prod_order_id} created!")
                    st.rerun()
    else:
        st.info("No sales orders ready for production. Create a sales order first.")
    
    # Display current production orders (exclude those already shipped)
    active_production_orders = []
    for prod_order in st.session_state.production_orders:
        # Find corresponding sales order
        sales_order = next((so for so in st.session_state.sales_orders if so.id == prod_order.sales_order_id), None)
        # Only show if sales order is not delivered
        if sales_order and sales_order.status != "Delivered":
            active_production_orders.append(prod_order)
    
    if active_production_orders:
        st.subheader("🏭 Current Production Orders")
        
        for prod_order in active_production_orders:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="process-card">
                    <h4>Production Order {prod_order.id}</h4>
                    <p><strong>Linked Sales Order:</strong> {prod_order.sales_order_id}</p>
                    <p><strong>Product:</strong> {prod_order.product.name}</p>
                    <p><strong>Quantity:</strong> {prod_order.quantity}</p>
                    <p><strong>Status:</strong> {prod_order.status}</p>
                    <p><strong>Start Date:</strong> {prod_order.start_date.strftime("%Y-%m-%d %H:%M")}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                st.progress(prod_order.completion_percentage / 100)
                st.caption(f"Completion: {prod_order.completion_percentage}%")
            
            with col2:
                if prod_order.status == "Planned":
                    if st.button(f"Start Production", key=f"start_{prod_order.id}"):
                        prod_order.status = "In Progress"
                        prod_order.completion_percentage = 25
                        st.rerun()
                elif prod_order.status == "In Progress" and prod_order.completion_percentage < 100:
                    if st.button(f"Update Progress", key=f"update_{prod_order.id}"):
                        prod_order.completion_percentage = min(100, prod_order.completion_percentage + 25)
                        if prod_order.completion_percentage == 100:
                            prod_order.status = "Completed"
                        st.rerun()

def show_production_confirmation():
    st.header("✅ Production Confirmation")
    
    st.markdown("""
    <div class="info-box">
        <strong>Sprint 3 Objective:</strong> Convert planned orders into production orders and confirm accuracy of linkage.
    </div>
    """, unsafe_allow_html=True)
    
    # Only show completed orders that haven't been delivered yet
    completed_orders = []
    for order in st.session_state.production_orders:
        if order.status == "Completed":
            # Find corresponding sales order
            sales_order = next((so for so in st.session_state.sales_orders if so.id == order.sales_order_id), None)
            # Only include if sales order is not delivered
            if sales_order and sales_order.status != "Delivered":
                completed_orders.append(order)
    
    # Only show in-progress orders that haven't been delivered yet
    in_progress_orders = []
    for order in st.session_state.production_orders:
        if order.status == "In Progress":
            # Find corresponding sales order
            sales_order = next((so for so in st.session_state.sales_orders if so.id == order.sales_order_id), None)
            # Only include if sales order is not delivered
            if sales_order and sales_order.status != "Delivered":
                in_progress_orders.append(order)
    
    if completed_orders:
        st.subheader("✅ Completed Production Orders")
        
        for order in completed_orders:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="success-message">
                    <h4>✅ Production Order {order.id} - COMPLETED</h4>
                    <p><strong>Product:</strong> {order.product.name}</p>
                    <p><strong>Quantity Produced:</strong> {order.quantity}</p>
                    <p><strong>Linked Sales Order:</strong> {order.sales_order_id}</p>
                    <p><strong>Completion Date:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Find corresponding sales order
                sales_order = next((so for so in st.session_state.sales_orders if so.id == order.sales_order_id), None)
                if sales_order and sales_order.status not in ["Ready for Delivery", "Delivered"]:
                    if st.button(f"Confirm & Ready for Delivery", key=f"confirm_{order.id}"):
                        sales_order.status = "Ready for Delivery"
                        st.success("Order confirmed and ready for delivery!")
                        st.rerun()
    
    if in_progress_orders:
        st.subheader("🔄 Production Orders in Progress")
        
        for order in in_progress_orders:
            st.markdown(f"""
            <div class="status-card">
                <h4>Production Order {order.id}</h4>
                <p><strong>Product:</strong> {order.product.name}</p>
                <p><strong>Progress:</strong> {order.completion_percentage}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(order.completion_percentage / 100)
    
    if not completed_orders and not in_progress_orders:
        st.info("No production orders to confirm. Start production orders first.")

def show_delivery_billing():
    st.header("🚚 Delivery & Billing Cycle")
    
    st.markdown("""
    <div class="info-box">
        <strong>Sprint 4 Objective:</strong> Execute delivery and billing cycle to ensure customer satisfaction.
    </div>
    """, unsafe_allow_html=True)
    
    # Orders ready for delivery
    ready_orders = [order for order in st.session_state.sales_orders if order.status == "Ready for Delivery"]
    
    if ready_orders:
        st.subheader("📦 Orders Ready for Delivery")
        
        for order in ready_orders:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="process-card">
                    <h4>Sales Order {order.id}</h4>
                    <p><strong>Customer:</strong> {order.customer_name}</p>
                    <p><strong>Product:</strong> {order.product.name}</p>
                    <p><strong>Quantity:</strong> {order.quantity}</p>
                    <p><strong>Total Amount:</strong> ${order.total_amount:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"Process Delivery", key=f"deliver_{order.id}"):
                    prod_order = next((po for po in st.session_state.production_orders if po.sales_order_id == order.id), None)
                    if prod_order:
                        delivery_id = f"DEL{len(st.session_state.deliveries) + 1:04d}"
                        tracking_number = f"TRK{uuid.uuid4().hex[:8].upper()}"

                        delivery = Delivery(
                            id=delivery_id,
                            production_order_id=prod_order.id,  
                            delivery_date=datetime.datetime.now(),
                            status="Shipped",
                            tracking_number=tracking_number
                        )

                        st.session_state.deliveries.append(delivery)
                        order.status = "Delivered"

                        st.success(f"✅ Delivery {delivery_id} created! Tracking: {tracking_number}")
                        st.rerun()
    
    # Billing section
    delivered_orders = [order for order in st.session_state.sales_orders if order.status == "Delivered"]
    
    if delivered_orders:
        st.subheader("💰 Billing & Invoicing")
        
        total_revenue = sum(order.total_amount for order in delivered_orders)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Orders Delivered", len(delivered_orders))
        with col2:
            st.metric("Total Revenue", f"${total_revenue:.2f}")
        with col3:
            avg_order = total_revenue / len(delivered_orders) if delivered_orders else 0
            st.metric("Average Order Value", f"${avg_order:.2f}")
        
        # Invoice generation
        st.subheader("📄 Generate Invoices")
        
        for order in delivered_orders:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="status-card">
                    <h4>Invoice for Order {order.id}</h4>
                    <p><strong>Customer:</strong> {order.customer_name}</p>
                    <p><strong>Amount:</strong> ${order.total_amount:.2f}</p>
                    <p><strong>Delivery Date:</strong> {datetime.datetime.now().strftime("%Y-%m-%d")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"Generate Invoice", key=f"invoice_{order.id}"):
                    st.success(f"📄 Invoice INV-{order.id} generated!")
    
    # Delivery tracking
    if st.session_state.deliveries:
        st.subheader("📍 Delivery Tracking")
        
        delivery_data = []
        for delivery in st.session_state.deliveries:
            delivery_data.append({
                "Delivery ID": delivery.id,
                "Production Order": delivery.production_order_id,
                "Tracking Number": delivery.tracking_number,
                "Status": delivery.status,
                "Delivery Date": delivery.delivery_date.strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(delivery_data)
        st.dataframe(df, use_container_width=True)

def show_order_documentation():
    st.header("📊 Order Documentation & Reports")
    
    st.markdown("""
    <div class="info-box">
        <strong>Final Documentation:</strong> Complete order tracking and comprehensive reporting for all manufacturing processes.
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics
    st.subheader("📈 Order Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(st.session_state.sales_orders)
        st.metric("Total Orders Created", total_orders)
    
    with col2:
        completed_production = len([o for o in st.session_state.production_orders if o.status == "Completed"])
        st.metric("Production Completed", completed_production)
    
    with col3:
        delivered_orders = len([o for o in st.session_state.sales_orders if o.status == "Delivered"])
        st.metric("Orders Delivered", delivered_orders)
    
    with col4:
        if st.session_state.sales_orders:
            total_revenue = sum(o.total_amount for o in st.session_state.sales_orders if o.status == "Delivered")
            st.metric("Total Revenue", f"${total_revenue:.2f}")
        else:
            st.metric("Total Revenue", "$0.00")
    
    # Complete order tracking table
    if st.session_state.sales_orders:
        st.subheader("📋 Complete Order Tracking")
        
        tracking_data = []
        for sales_order in st.session_state.sales_orders:
            # Find linked production order
            prod_order = next((po for po in st.session_state.production_orders if po.sales_order_id == sales_order.id), None)
            
            # Find delivery record
            delivery = None
            if prod_order:
                delivery = next((d for d in st.session_state.deliveries if d.production_order_id == prod_order.id), None)
            
            tracking_data.append({
                "Sales Order": sales_order.id,
                "Customer": sales_order.customer_name,
                "Product": sales_order.product.name,
                "Quantity": sales_order.quantity,
                "Amount": f"${sales_order.total_amount:.2f}",
                "Production Order": prod_order.id if prod_order else "Not Created",
                "Production Status": prod_order.status if prod_order else "Pending",
                "Delivery ID": delivery.id if delivery else "Not Shipped",
                "Tracking Number": delivery.tracking_number if delivery else "N/A",
                "Order Status": sales_order.status,
                "Sustainability Score": f"{sales_order.product.sustainability_score}%"
            })
        
        df = pd.DataFrame(tracking_data)
        st.dataframe(df, use_container_width=True)
        
        # Export functionality
        st.subheader("📥 Export Documentation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate Order Report"):
                st.success("✅ Order report generated successfully!")
                st.info("Report includes: Order tracking, production status, delivery information, and sustainability metrics.")
        
        with col2:
            if st.button("📊 Export to CSV"):
                st.success("✅ Data exported to CSV format!")
                st.info("CSV file contains complete order documentation for external analysis.")
    
    else:
        st.info("No orders available for documentation. Create some orders to see the complete tracking system.")
    
    # Process completion status
    st.subheader("✅ Process Completion Status")
    
    if st.session_state.sales_orders:
        completion_stages = {
            "Orders Created": len(st.session_state.sales_orders),
            "Production Started": len([o for o in st.session_state.production_orders if o.status in ["In Progress", "Completed"]]),
            "Production Completed": len([o for o in st.session_state.production_orders if o.status == "Completed"]),
            "Orders Delivered": len([o for o in st.session_state.sales_orders if o.status == "Delivered"])
        }
        
        for stage, count in completion_stages.items():
            progress = (count / len(st.session_state.sales_orders)) * 100 if st.session_state.sales_orders else 0
            st.markdown(f"**{stage}:** {count}/{len(st.session_state.sales_orders)} ({progress:.1f}%)")
            st.progress(progress / 100)
    
    st.success("📋 Order documentation system is fully operational and ready for production use!")

if __name__ == "__main__":
    main()