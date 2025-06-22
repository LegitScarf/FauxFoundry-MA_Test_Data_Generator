import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import json
import time
from datetime import datetime
import re

# Configure page
st.set_page_config(
    page_title="🔥 FauxFaundry",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark attractive styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main background and text styling */
    .stApp {
        background: #000000;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }
    
    /* Main container styling - solid dark containers */
    .main-container {
        background: #111111;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #333333;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcf7f, #4d96ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .main-subtitle {
        font-size: 1.3rem;
        color: #cccccc;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #333333;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        border-color: #555555;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #cccccc;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Step indicators */
    .step-container {
        background: #1a1a1a;
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        border: 1px solid #333333;
    }
    
    .step-number {
        background: #ff6b6b;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.2rem;
        color: white;
    }
    
    .step-text {
        font-size: 1.1rem;
        font-weight: 500;
        color: #ffffff;
    }
    
    /* Success/Error messages */
    .success-message {
        background: #1a4d3a;
        color: #4ade80;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
        border: 1px solid #22c55e;
    }
    
    .error-message {
        background: #4d1a1a;
        color: #f87171;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
        border: 1px solid #ef4444;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #111111 !important;
    }
    
    .css-1lcbmhc {
        background: #111111 !important;
        border-right: 1px solid #333333 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%);
        color: #000000;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #1a1a1a !important;
        border-radius: 12px;
        border: 2px solid #333333 !important;
        padding: 0.75rem;
        font-size: 1rem;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {
        background: #1a1a1a !important;
        border-radius: 12px;
        border: 2px solid #333333 !important;
        padding: 0.75rem;
        font-size: 1rem;
        color: #ffffff !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: #333333 !important;
    }
    
    .stSlider > div > div > div > div {
        background: #ff6b6b !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #ffffff !important;
    }
    
    /* Metric styling */
    .metric-container {
        background: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #333333;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* DataFrame styling */
    .dataframe {
        background: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background: #1a1a1a !important;
        border: 1px solid #333333 !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        border-color: #ff6b6b !important;
        background: #333333 !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: #ff6b6b !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Text color overrides */
    .stMarkdown, .stText {
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .main-subtitle {
            font-size: 1rem;
        }
        
        .feature-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Mock functions for demonstration (replace with your actual implementation)
def schema_designer_agent(domain):
    """Mock schema designer - replace with your OpenAI implementation"""
    schemas = {
        "e-commerce": [
            "CustomerID (Integer)",
            "ProductName (String)",
            "Price (Float)",
            "Category (String)",
            "OrderDate (Date)"
        ],
        "finance": [
            "AccountID (Integer)",
            "TransactionAmount (Float)",
            "TransactionType (String)",
            "Balance (Float)",
            "Timestamp (DateTime)"
        ],
        "healthcare": [
            "PatientID (Integer)",
            "Age (Integer)",
            "Diagnosis (String)",
            "Treatment (String)",
            "Cost (Float)"
        ],
        "default": [
            "ID (Integer)",
            "Name (String)",
            "Value (Float)",
            "Category (String)",
            "Date (Date)"
        ]
    }
    return "\n".join(schemas.get(domain.lower(), schemas["default"]))

def generate_mock_data(schema_lines, num_rows):
    """Generate mock data for demonstration"""
    import random
    from datetime import datetime, timedelta
    
    columns = []
    for line in schema_lines:
        if '(' in line:
            col_name = line.split('(')[0].strip()
            columns.append(col_name)
    
    data = []
    for i in range(num_rows):
        row = []
        for col in columns:
            if 'ID' in col.upper():
                row.append(i + 1)
            elif 'NAME' in col.upper():
                row.append(f"Sample_{i+1}")
            elif 'PRICE' in col.upper() or 'AMOUNT' in col.upper() or 'COST' in col.upper():
                row.append(round(random.uniform(10, 1000), 2))
            elif 'DATE' in col.upper():
                base_date = datetime.now() - timedelta(days=random.randint(0, 365))
                row.append(base_date.strftime("%Y-%m-%d"))
            elif 'CATEGORY' in col.upper():
                row.append(random.choice(['A', 'B', 'C', 'Premium', 'Standard']))
            else:
                row.append(f"Value_{i+1}")
        data.append(row)
    
    return pd.DataFrame(data, columns=columns)

def main():
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="main-header">
            <div class="main-title">🔥 FauxFaundry</div>
            <div class="main-subtitle">Forge realistic synthetic datasets with AI-powered precision</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Domain selection
        domain = st.selectbox(
            "🎯 Select Domain",
            ["E-commerce", "Finance", "Healthcare", "Custom"],
            help="Choose a domain for your synthetic data"
        )
        
        if domain == "Custom":
            custom_domain = st.text_input("Enter custom domain:", placeholder="e.g., logistics, education")
            domain = custom_domain if custom_domain else "default"
        
        # Number of rows
        num_rows = st.slider(
            "📊 Number of Rows",
            min_value=10,
            max_value=1000,
            value=50,
            step=10,
            help="Select how many rows of data to generate"
        )
        
        # Export format
        export_format = st.selectbox(
            "💾 Export Format",
            ["CSV", "JSON", "Excel"],
            help="Choose your preferred export format"
        )
        
        # Model selection
        st.markdown("### 🧠 AI Models")
        use_openai = st.checkbox("Use OpenAI GPT-4", value=True, help="Use OpenAI for schema design")
        use_local = st.checkbox("Use Local Model", value=True, help="Use local model for data generation")
        
        st.markdown("---")
        st.markdown("### 📈 Statistics")
        if 'generated_data' in st.session_state:
            st.markdown(f"""
            <div class="metric-container">
                <h4>Generated Rows</h4>
                <h2>{len(st.session_state.generated_data)}</h2>
            </div>
            <div class="metric-container">
                <h4>Columns</h4>
                <h2>{len(st.session_state.generated_data.columns)}</h2>
            </div>
            """, unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Features showcase
        st.markdown("""
        <div class="main-container">
            <h2 style="text-align: center; color: #ffffff; margin-bottom: 2rem;">✨ Key Features</h2>
        """, unsafe_allow_html=True)
        
        # Feature cards
        features_col1, features_col2 = st.columns(2)
        
        with features_col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">AI-Powered Schema Design</div>
                <div class="feature-description">Automatically generates optimal database schemas using advanced AI models</div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Multi-Agent Architecture</div>
                <div class="feature-description">Coordinated AI agents working together for superior data quality</div>
            </div>
            """, unsafe_allow_html=True)
        
        with features_col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Domain-Specific Data</div>
                <div class="feature-description">Generates realistic data tailored to your specific industry and use case</div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Multiple Export Formats</div>
                <div class="feature-description">Export your data in CSV, JSON, or Excel formats for immediate use</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Quick stats or demo
        st.markdown("""
        <div class="main-container">
            <h3 style="color: #ffffff; text-align: center;">🚀 Quick Start</h3>
            <ol style="color: #cccccc; line-height: 1.8;">
                <li>Select your domain</li>
                <li>Choose number of rows</li>
                <li>Pick export format</li>
                <li>Click Generate!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Generation section
    st.markdown("""
    <div class="main-container">
        <h2 style="text-align: center; color: #ffffff; margin-bottom: 2rem;">🔥 Forge Your Dataset</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔥 Forge Synthetic Data", key="generate_btn"):
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Schema Design
            status_text.markdown("""
            <div class="step-container">
                <div class="step-number">1</div>
                <div class="step-text">🧠 Designing schema...</div>
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(25)
            time.sleep(1)
            
            schema = schema_designer_agent(domain)
            
            # Step 2: Data Generation
            status_text.markdown("""
            <div class="step-container">
                <div class="step-number">2</div>
                <div class="step-text">✍️ Generating data...</div>
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(50)
            time.sleep(1)
            
            # Step 3: Validation
            status_text.markdown("""
            <div class="step-container">
                <div class="step-number">3</div>
                <div class="step-text">🧪 Validating data...</div>
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(75)
            time.sleep(1)
            
            # Generate mock data for demo
            schema_lines = schema.strip().split('\n')
            generated_data = generate_mock_data(schema_lines, num_rows)
            
            # Step 4: Complete
            status_text.markdown("""
            <div class="step-container">
                <div class="step-number">4</div>
                <div class="step-text">✅ Complete!</div>
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # Store in session state
            st.session_state.generated_data = generated_data
            st.session_state.schema = schema
            
            # Success message
            st.markdown("""
            <div class="success-message">
                🎉 Successfully forged {} rows of synthetic data!
            </div>
            """.format(num_rows), unsafe_allow_html=True)
            
            # Clear progress
            progress_bar.empty()
            status_text.empty()
    
    # Display results
    if 'generated_data' in st.session_state:
        st.markdown("""
        <div class="main-container">
            <h3 style="color: #ffffff;">📋 Generated Schema</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.code(st.session_state.schema, language="text")
        
        st.markdown("""
        <div class="main-container">
            <h3 style="color: #ffffff;">📊 Generated Data Preview</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Data preview
        st.dataframe(
            st.session_state.generated_data,
            use_container_width=True,
            height=400
        )
        
        # Download section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if export_format == "CSV":
                csv_data = st.session_state.generated_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"fauxfaundry_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if export_format == "JSON":
                json_data = st.session_state.generated_data.to_json(orient="records", indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"fauxfaundry_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            if export_format == "Excel":
                # For Excel, we'll use CSV for now since it's easier to handle
                csv_data = st.session_state.generated_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Excel",
                    data=csv_data,
                    file_name=f"fauxfaundry_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Data visualization
        if len(st.session_state.generated_data.columns) > 1:
            st.markdown("""
            <div class="main-container">
                <h3 style="color: #ffffff;">📈 Data Visualization</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple visualization
            numeric_columns = st.session_state.generated_data.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_columns) > 0:
                fig = px.histogram(
                    st.session_state.generated_data,
                    x=numeric_columns[0],
                    title=f"Distribution of {numeric_columns[0]}",
                    color_discrete_sequence=['#ff6b6b']
                )
                fig.update_layout(
                    plot_bgcolor='#1a1a1a',
                    paper_bgcolor='#111111',
                    font=dict(family="Inter", size=12, color="#ffffff"),
                    title_font_color="#ffffff"
                )
                fig.update_xaxes(gridcolor='#333333', color='#ffffff')
                fig.update_yaxes(gridcolor='#333333', color='#ffffff')
                st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666666; font-size: 0.9rem;">
        <hr style="border: none; height: 1px; background: #333333;">
        <p>Built with ❤️ using Streamlit • Multi-Agent AI Architecture • FauxFaundry</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
