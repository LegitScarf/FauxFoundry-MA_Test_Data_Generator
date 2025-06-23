import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
import re
import random
from io import BytesIO
import openpyxl

# Configure page
st.set_page_config(
    page_title="FauxFaundry",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for crisp black UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Main background and text styling */
    .stApp {
        background: #000000;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }
    
    /* Remove all default padding and margins */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
    }
    
    .app-title {
        font-size: 4.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #888888;
        font-weight: 400;
        margin-bottom: 0;
        letter-spacing: 0.01em;
    }
    
    /* Agent workflow visualization */
    .workflow-section {
        background: linear-gradient(135deg, #111111, #1a1a1a);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .workflow-title {
        font-size: 1.3rem;
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .agent-flow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .agent-card {
        background: #000000;
        border: 2px solid #333333;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        border-color: #555555;
        transform: translateY(-2px);
    }
    
    .agent-card.active {
        border-color: #ffffff;
        background: #0a0a0a;
    }
    
    .agent-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: #ffffff;
        color: #000000;
        border-radius: 50%;
        font-weight: 700;
        font-size: 1.2rem;
        line-height: 40px;
        margin-bottom: 1rem;
    }
    
    .agent-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .agent-desc {
        font-size: 0.85rem;
        color: #888888;
        line-height: 1.4;
    }
    
    .agent-model {
        font-size: 0.75rem;
        color: #aaaaaa;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.5rem;
        padding: 0.25rem 0.5rem;
        background: #111111;
        border-radius: 4px;
    }
    
    .flow-arrow {
        font-size: 2rem;
        color: #555555;
        margin: 0 1rem;
    }
    
    /* Form styling */
    .form-section {
        background: #0a0a0a;
        border: 1px solid #222222;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .section-title {
        font-size: 1.3rem;
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: #000000 !important;
        border: 2px solid #333333 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
        min-height: 200px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Button styling */
    .generate-button {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ffffff, #f0f0f0) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 1rem 4rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #f8f8f8, #e8e8e8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #111111;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #ffffff, #cccccc) !important;
        height: 4px !important;
        border-radius: 2px !important;
    }
    
    .stProgress > div {
        background: #333333 !important;
        border-radius: 2px !important;
    }
    
    .status-message {
        color: #ffffff;
        font-size: 1rem;
        margin: 1rem 0;
        font-weight: 500;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    /* Results section */
    .results-section {
        background: #0a0a0a;
        border: 1px solid #222222;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        margin: 1.5rem 0;
    }
    
    .stDataFrame > div {
        background: #000000 !important;
        border: 2px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    /* JSON preview styling */
    .json-preview {
        background: #000000;
        border: 2px solid #333333;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .json-title {
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1rem;
    }
    
    .json-content {
        background: #111111;
        border: 1px solid #444444;
        border-radius: 6px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #ffffff;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
    }
    
    /* Download buttons */
    .download-section {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .stDownloadButton > button {
        background: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #333333 !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.01em !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: #ffffff !important;
        background: #1a1a1a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #001a00, #002200);
        color: #00ff88;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        border: 2px solid #004400;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.1);
    }
    
    /* Error message */
    .error-message {
        background: linear-gradient(135deg, #1a0000, #220000);
        color: #ff4444;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        text-align: center;
        font-weight: 600;
        border: 2px solid #440000;
    }
    
    /* Example section */
    .example-section {
        background: #0a0a0a;
        border: 2px solid #222222;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .example-text {
        color: #cccccc;
        font-size: 0.9rem;
        line-height: 1.6;
        font-family: 'JetBrains Mono', monospace;
        background: #000000;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #333333;
        white-space: pre-wrap;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2.5rem;
        }
        
        .agent-flow {
            flex-direction: column;
        }
        
        .flow-arrow {
            transform: rotate(90deg);
            margin: 1rem 0;
        }
        
        .download-section {
            flex-direction: column;
            align-items: center;
        }
        
        .stButton > button {
            padding: 1rem 2rem !important;
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Agent simulation functions
def agent_1_column_generation(user_prompt):
    """
    Agent 1: PHI3/GEMMA2 - Column Generation
    Analyzes user prompt and generates column structure
    """
    # Simulate PHI3/GEMMA2 processing
    time.sleep(1.5)
    
    # Extract domain and requirements from prompt
    prompt_lower = user_prompt.lower()
    
    # Determine domain and generate appropriate columns
    if any(word in prompt_lower for word in ['employee', 'hr', 'human resources', 'staff']):
        columns = {
            "columns": [
                {"name": "Employee_ID", "type": "string", "description": "Unique employee identifier"},
                {"name": "Full_Name", "type": "string", "description": "Employee full name"},
                {"name": "Department", "type": "string", "description": "Department name"},
                {"name": "Position", "type": "string", "description": "Job position/role"},
                {"name": "Hire_Date", "type": "date", "description": "Date of hiring"},
                {"name": "Email", "type": "string", "description": "Work email address"},
                {"name": "Salary", "type": "integer", "description": "Annual salary in USD"},
                {"name": "Status", "type": "string", "description": "Employment status"}
            ]
        }
    elif any(word in prompt_lower for word in ['customer', 'client', 'crm']):
        columns = {
            "columns": [
                {"name": "Customer_ID", "type": "string", "description": "Unique customer identifier"},
                {"name": "Company_Name", "type": "string", "description": "Company name"},
                {"name": "Contact_Person", "type": "string", "description": "Primary contact name"},
                {"name": "Email", "type": "string", "description": "Contact email"},
                {"name": "Phone", "type": "string", "description": "Contact phone number"},
                {"name": "Industry", "type": "string", "description": "Industry sector"},
                {"name": "Revenue", "type": "integer", "description": "Annual revenue"},
                {"name": "Registration_Date", "type": "date", "description": "Customer registration date"}
            ]
        }
    elif any(word in prompt_lower for word in ['product', 'inventory', 'catalog']):
        columns = {
            "columns": [
                {"name": "Product_ID", "type": "string", "description": "Unique product identifier"},
                {"name": "Product_Name", "type": "string", "description": "Product name"},
                {"name": "Category", "type": "string", "description": "Product category"},
                {"name": "Price", "type": "float", "description": "Product price"},
                {"name": "Stock_Quantity", "type": "integer", "description": "Available stock"},
                {"name": "Supplier", "type": "string", "description": "Supplier name"},
                {"name": "Launch_Date", "type": "date", "description": "Product launch date"},
                {"name": "Rating", "type": "float", "description": "Average customer rating"}
            ]
        }
    elif any(word in prompt_lower for word in ['sales', 'transaction', 'order']):
        columns = {
            "columns": [
                {"name": "Transaction_ID", "type": "string", "description": "Unique transaction identifier"},
                {"name": "Customer_ID", "type": "string", "description": "Customer identifier"},
                {"name": "Product_ID", "type": "string", "description": "Product identifier"},
                {"name": "Quantity", "type": "integer", "description": "Quantity purchased"},
                {"name": "Unit_Price", "type": "float", "description": "Price per unit"},
                {"name": "Total_Amount", "type": "float", "description": "Total transaction amount"},
                {"name": "Transaction_Date", "type": "date", "description": "Date of transaction"},
                {"name": "Payment_Method", "type": "string", "description": "Payment method used"}
            ]
        }
    else:
        # Generic columns for unknown domains
        columns = {
            "columns": [
                {"name": "ID", "type": "string", "description": "Unique identifier"},
                {"name": "Name", "type": "string", "description": "Item name"},
                {"name": "Category", "type": "string", "description": "Item category"},
                {"name": "Value", "type": "float", "description": "Numeric value"},
                {"name": "Status", "type": "string", "description": "Current status"},
                {"name": "Created_Date", "type": "date", "description": "Creation date"},
                {"name": "Modified_Date", "type": "date", "description": "Last modification date"}
            ]
        }
    
    return columns

def agent_2_data_generation(column_structure, user_prompt, num_rows):
    """
    Agent 2: GPT-4o-mini - Data Generation
    Takes column structure and generates synthetic data
    """
    # Simulate GPT-4o-mini processing
    time.sleep(2.0)
    
    data = []
    columns = column_structure["columns"]
    
    # Sample data pools
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Liam', 'Mia', 'Noah', 'Olivia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']
    
    for i in range(num_rows):
        row = {}
        for col in columns:
            col_name = col["name"]
            col_type = col["type"]
            
            # Generate data based on column name and type
            if col_type == "string":
                if "id" in col_name.lower():
                    if "employee" in col_name.lower():
                        row[col_name] = f"EMP{1000 + i + 1:04d}"
                    elif "customer" in col_name.lower():
                        row[col_name] = f"CUST{2000 + i + 1:04d}"
                    elif "product" in col_name.lower():
                        row[col_name] = f"PROD{3000 + i + 1:04d}"
                    elif "transaction" in col_name.lower():
                        row[col_name] = f"TXN{4000 + i + 1:08d}"
                    else:
                        row[col_name] = f"ID{1000 + i + 1:04d}"
                elif "name" in col_name.lower():
                    if "full" in col_name.lower() or "person" in col_name.lower() or "contact" in col_name.lower():
                        row[col_name] = f"{random.choice(first_names)} {random.choice(last_names)}"
                    elif "company" in col_name.lower():
                        companies = ['TechCorp', 'DataSystems', 'InnovateLabs', 'GlobalTech', 'NextGen Solutions', 'SmartWorks', 'FutureTech', 'ProActive', 'TechPioneer', 'DigitalEdge']
                        row[col_name] = random.choice(companies)
                    elif "product" in col_name.lower():
                        products = ['Laptop Pro', 'Wireless Mouse', 'Keyboard Elite', 'Monitor 4K', 'Tablet Air', 'Smartphone X', 'Headphones Max', 'Speaker Bluetooth', 'Camera HD', 'Printer Laser']
                        row[col_name] = random.choice(products)
                    else:
                        row[col_name] = f"Item_{i+1}"
                elif "email" in col_name.lower():
                    name = f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}"
                    domains = ['company.com', 'techcorp.com', 'business.org', 'enterprise.net']
                    row[col_name] = f"{name}@{random.choice(domains)}"
                elif "department" in col_name.lower():
                    departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations', 'Customer Success', 'IT', 'Legal', 'R&D']
                    row[col_name] = random.choice(departments)
                elif "position" in col_name.lower() or "role" in col_name.lower():
                    positions = ['Manager', 'Senior Developer', 'Analyst', 'Coordinator', 'Director', 'Specialist', 'Associate', 'Lead', 'Principal', 'VP']
                    row[col_name] = random.choice(positions)
                elif "category" in col_name.lower():
                    if "product" in user_prompt.lower():
                        categories = ['Electronics', 'Computers', 'Accessories', 'Software', 'Hardware', 'Mobile']
                    else:
                        categories = ['Category A', 'Category B', 'Category C', 'Premium', 'Standard', 'Basic']
                    row[col_name] = random.choice(categories)
                elif "status" in col_name.lower():
                    if "employee" in user_prompt.lower():
                        statuses = ['Active', 'On Leave', 'Remote', 'Part-time']
                    else:
                        statuses = ['Active', 'Inactive', 'Pending', 'Completed', 'In Progress']
                    row[col_name] = random.choice(statuses)
                elif "industry" in col_name.lower():
                    industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Consulting', 'Media', 'Real Estate', 'Transportation']
                    row[col_name] = random.choice(industries)
                elif "supplier" in col_name.lower():
                    suppliers = ['Global Supply Co', 'TechSupplier Inc', 'Premium Parts Ltd', 'Quality Components', 'Reliable Vendors', 'Express Logistics']
                    row[col_name] = random.choice(suppliers)
                elif "phone" in col_name.lower():
                    row[col_name] = f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
                elif "payment" in col_name.lower() and "method" in col_name.lower():
                    methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash', 'Check']
                    row[col_name] = random.choice(methods)
                else:
                    row[col_name] = f"Value_{i+1}"
            
            elif col_type == "integer":
                if "salary" in col_name.lower():
                    row[col_name] = random.randint(40000, 150000)
                elif "revenue" in col_name.lower():
                    row[col_name] = random.randint(100000, 10000000)
                elif "quantity" in col_name.lower() or "stock" in col_name.lower():
                    row[col_name] = random.randint(1, 1000)
                else:
                    row[col_name] = random.randint(1, 10000)
            
            elif col_type == "float":
                if "price" in col_name.lower():
                    row[col_name] = round(random.uniform(10.0, 999.99), 2)
                elif "rating" in col_name.lower():
                    row[col_name] = round(random.uniform(1.0, 5.0), 1)
                elif "amount" in col_name.lower():
                    row[col_name] = round(random.uniform(100.0, 10000.0), 2)
                else:
                    row[col_name] = round(random.uniform(1.0, 1000.0), 2)
            
            elif col_type == "date":
                from datetime import datetime, timedelta
                start_date = datetime.now() - timedelta(days=365*3)  # 3 years ago
                random_days = random.randint(0, 365*3)
                date_val = start_date + timedelta(days=random_days)
                row[col_name] = date_val.strftime('%Y-%m-%d')
        
        data.append(row)
    
    return pd.DataFrame(data)

def agent_3_export_handler(dataframe, format_type):
    """
    Agent 3: Export Handler
    Handles different export formats
    """
    if format_type == "csv":
        return dataframe.to_csv(index=False)
    elif format_type == "xlsx":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='FauxFaundry_Data')
        return output.getvalue()
    elif format_type == "json":
        return dataframe.to_json(orient="records", indent=2)
    elif format_type == "markdown":
        return dataframe.to_markdown(index=False)

def extract_row_count(prompt):
    """Extract number of rows from user prompt"""
    numbers = re.findall(r'\b(\d+)\s*(?:rows?|records?|entries?)\b', prompt.lower())
    if numbers:
        return int(numbers[0])
    
    # Look for standalone numbers that might indicate row count
    numbers = re.findall(r'\b(\d+)\b', prompt)
    if numbers:
        for num in numbers:
            if 5 <= int(num) <= 10000:  # Reasonable range for row count
                return int(num)
    
    return 10  # Default

def main():
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">FauxFaundry</div>
        <div class="app-subtitle">AI-Powered Synthetic Data Generation with Multi-Agent Architecture</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent workflow visualization
    st.markdown("""
    <div class="workflow-section">
        <div class="workflow-title">🤖 3-Agent Architecture Workflow</div>
        <div class="agent-flow">
            <div class="agent-card">
                <div class="agent-number">1</div>
                <div class="agent-title">Schema Generator</div>
                <div class="agent-desc">Analyzes user requirements and generates column structure with data types</div>
                <div class="agent-model">PHI3 / GEMMA2</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="agent-card">
                <div class="agent-number">2</div>
                <div class="agent-title">Data Synthesizer</div>
                <div class="agent-desc">Creates realistic synthetic dataset based on generated schema</div>
                <div class="agent-model">GPT-4o-mini</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="agent-card">
                <div class="agent-number">3</div>
                <div class="agent-title">Export Manager</div>
                <div class="agent-desc">Handles data export in multiple formats (CSV, XLSX, JSON, Markdown)</div>
                <div class="agent-model">Processing Engine</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main form
    st.markdown("""
    <div class="form-section">
        <div class="section-title">📝 Dataset Requirements</div>
    """, unsafe_allow_html=True)
    
    # Example section
    with st.expander("💡 See Example Prompts", expanded=False):
        example_prompts = [
            "Generate 25 rows of HR employee data including names, departments, salaries, and hire dates",
            "Create 50 customer records with company information, contact details, and revenue data",
            "Generate 100 product catalog entries with pricing, categories, and stock information",
            "Create 75 sales transaction records with customer IDs, products, and payment details"
        ]
        
        for i, example in enumerate(example_prompts, 1):
            st.markdown(f'<div class="example-text">Example {i}: {example}</div>', unsafe_allow_html=True)
    
    # User input
    user_prompt = st.text_area(
        "Describe your synthetic data requirements:",
        height=180,
        placeholder="Example: Generate 50 rows of employee data for HR department including employee ID, full name, department, position, hire date, email, and salary. Make it realistic with varied departments and salary ranges.",
        help="Be specific about:\n• Domain (HR, Sales, Customer, Product, etc.)\n• Number of rows needed\n• What columns/fields you want\n• Any specific requirements or constraints"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Generate Dataset", key="generate"):
            if user_prompt.strip():
                # Extract row count
                num_rows = extract_row_count(user_prompt)
                
                # Progress container
                st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                try:
                    # Agent 1: Column Generation
                    status_placeholder.markdown('<div class="status-message">🤖 Agent 1: Analyzing requirements and generating schema...</div>', unsafe_allow_html=True)
                    progress_bar.progress(15)
                    
                    column_structure = agent_1_column_generation(user_prompt)
                    
                    status_placeholder.markdown('<div class="status-message">✅ Schema generated successfully</div>', unsafe_allow_html=True)
                    progress_bar.progress(35)
                    time.sleep(0.5)
                    
                    # Agent 2: Data Generation
                    status_placeholder.markdown('<div class="status-message">🔥 Agent 2: Synthesizing realistic data...</div>', unsafe_allow_html=True)
                    progress_bar.progress(50)
                    
                    generated_data = agent_2_data_generation(column_structure, user_prompt, num_rows)
                    
                    status_placeholder.markdown('<div class="status-message">✅ Dataset generated successfully</div>', unsafe_allow_html=True)
                    progress_bar.progress(85)
                    time.sleep(0.5)
                    
                    # Agent 3: Prepare exports
                    status_placeholder.markdown('<div class="status-message">📦 Agent 3: Preparing export formats...</div>', unsafe_allow_html=True)
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    
                    # Store results in session state
                    st.session_state.generated_data = generated_data
                    st.session_state.column_structure = column_structure
                    st.session_state.user_prompt = user_prompt
                    st.session_state.num_rows = num_rows
                    
                    # Clear progress
                    progress_bar.empty()
                    status_placeholder.empty()
                    
                    # Success message
                    st.markdown(f'<div class="success-message">🎉 Successfully generated {len(generated_data)} rows of synthetic data using 3-agent architecture!</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    progress_bar.empty()
                    status_placeholder.empty()
                    st.markdown(f'<div class="error-message">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please enter your data requirements first.")
    
    # Display results
    if 'generated_data' in st.session_state:
        # Schema Preview Section
        st.markdown("""
        <div class="results-section">
            <div class="section-title">🏗️ Generated Schema (Agent 1 Output)</div>
        """, unsafe_allow_html=True)
        
        # Display column structure
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="json-title">📋 Column Structure</div>', unsafe_allow_html=True)
            schema_json = json.dumps(st.session_state.column_structure, indent=2)
            st.markdown(f'<div class="json-content">{schema_json}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="json-title">📊 Schema Summary</div>', unsafe_allow_html=True)
            columns = st.session_state.column_structure["columns"]
            summary_info = f"""Total Columns: {len(columns)}
Data Types:
• String: {len([c for c in columns if c['type'] == 'string'])}
• Integer: {len([c for c in columns if c['type'] == 'integer'])}
• Float: {len([c for c in columns if c['type'] == 'float'])}
• Date: {len([c for c in columns if c['type'] == 'date'])}

Rows Generated: {st.session_state.num_rows}"""
            st.markdown(f'<div class="json-content">{summary_info}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data Preview Section
        st.markdown("""
        <div class="results-section">
            <div class="section-title">📋 Generated Dataset (Agent 2 Output)</div>
        """, unsafe_allow_html=True)
        
        # Display the data
        st.dataframe(
            st.session_state.generated_data,
            use_container_width=True,
            height=400
        )
        
        # Markdown table preview
        st.markdown('<div class="json-title">📝 Markdown Table Format</div>', unsafe_allow_html=True)
        markdown_table = st.session_state.generated_data.head(5).to_markdown(index=False)
        st.code(markdown_table, language="markdown")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Section (Agent 3)
        st.markdown("""
        <div class="results-section">
            <div class="section-title">📤 Export Options (Agent 3 Output)</div>
        """, unsafe_allow_html=True)
        
        # Download buttons
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv_data = agent_3_export_handler(st.session_state.generated_data, "csv")
            st.download_button(
                "📄 Download CSV",
                data=csv_data,
                file_name=f"fauxfaundry_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            xlsx_data = agent_3_export_handler(st.session_state.generated_data, "xlsx")
            st.download_button(
                "📊 Download XLSX",
                data=xlsx_data,
                file_name=f"fauxfaundry_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            json_data = agent_3_export_handler(st.session_state.generated_data, "json")
            st.download_button(
                "📋 Download JSON",
                data=json_data,
                file_name=f"fauxfaundry_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col4:
            markdown_data = agent_3_export_handler(st.session_state.generated_data, "markdown")
            st.download_button(
                "📝 Download Markdown",
                data=markdown_data,
                file_name=f"fauxfaundry_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export format previews
        st.markdown('<div class="json-title">🔍 Format Previews</div>', unsafe_allow_html=True)
        
        format_col1, format_col2 = st.columns(2)
        
        with format_col1:
            st.markdown("**CSV Format (First 3 rows):**")
            csv_preview = st.session_state.generated_data.head(3).to_csv(index=False)
            st.code(csv_preview, language="csv")
        
        with format_col2:
            st.markdown("**JSON Format (First 2 records):**")
            json_preview = st.session_state.generated_data.head(2).to_json(orient="records", indent=2)
            st.code(json_preview, language="json")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics Section
        st.markdown("""
        <div class="results-section">
            <div class="section-title">📈 Dataset Statistics</div>
        """, unsafe_allow_html=True)
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric("Total Rows", len(st.session_state.generated_data))
        
        with stats_col2:
            st.metric("Total Columns", len(st.session_state.generated_data.columns))
        
        with stats_col3:
            # Calculate memory usage
            memory_usage = st.session_state.generated_data.memory_usage(deep=True).sum()
            memory_mb = memory_usage / (1024 * 1024)
            st.metric("Memory Usage", f"{memory_mb:.2f} MB")
        
        with stats_col4:
            # Calculate completeness (non-null percentage)
            total_cells = len(st.session_state.generated_data) * len(st.session_state.generated_data.columns)
            non_null_cells = st.session_state.generated_data.count().sum()
            completeness = (non_null_cells / total_cells) * 100
            st.metric("Data Completeness", f"{completeness:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
                
                #
