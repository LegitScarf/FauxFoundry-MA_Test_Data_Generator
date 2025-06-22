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
    page_title="FauxFaundry",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimal dark styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Main background and text styling */
    .stApp {
        background: #000000;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }
    
    /* Remove all default padding and margins */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .app-title {
        font-size: 4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        color: #888888;
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Main form area */
    .form-section {
        margin-bottom: 3rem;
    }
    
    .section-title {
        font-size: 1.2rem;
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 1px solid #333333;
        padding-bottom: 0.5rem;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
        min-height: 200px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 1px #ffffff !important;
    }
    
    /* Button styling */
    .generate-button {
        display: flex;
        justify-content: center;
        margin: 3rem 0;
    }
    
    .stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 3rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    
    .stButton > button:hover {
        background: #f0f0f0 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Results section */
    .results-section {
        margin-top: 3rem;
        border-top: 1px solid #333333;
        padding-top: 3rem;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        margin: 2rem 0;
    }
    
    .stDataFrame > div {
        background: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
    }
    
    .stCodeBlock code {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
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
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: #ffffff !important;
        background: #222222 !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: #ffffff !important;
        height: 2px !important;
    }
    
    .stProgress > div {
        background: #333333 !important;
    }
    
    /* Status message styling */
    .status-message {
        text-align: center;
        color: #888888;
        font-size: 0.9rem;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Success message */
    .success-message {
        background: #001a00;
        color: #00ff00;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        border: 1px solid #004400;
    }
    
    /* Example section */
    .example-section {
        background: #0a0a0a;
        border: 1px solid #222222;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .example-title {
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1rem;
    }
    
    .example-text {
        color: #cccccc;
        font-size: 0.9rem;
        line-height: 1.6;
        font-family: 'JetBrains Mono', monospace;
        background: #000000;
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid #333333;
        white-space: pre-wrap;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2.5rem;
        }
        
        .download-section {
            flex-direction: column;
            align-items: center;
        }
        
        .stButton > button {
            padding: 0.75rem 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def generate_synthetic_data_from_prompt(user_prompt):
    """
    Parse user prompt and generate synthetic data
    This is a mock implementation - replace with your actual AI model
    """
    # Extract domain, columns, and row count from prompt
    # This is simplified parsing - you'd want more robust NLP here
    
    # Mock parsing
    lines = user_prompt.lower().split('\n')
    num_rows = 10  # default
    
    # Try to find number of rows
    for line in lines:
        if 'rows' in line:
            numbers = re.findall(r'\d+', line)
            if numbers:
                num_rows = int(numbers[0])
                break
    
    # Mock data generation based on common HR fields mentioned in example
    if 'human resources' in user_prompt.lower() or 'employee' in user_prompt.lower():
        import random
        from datetime import datetime, timedelta
        
        # HR data
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Emily', 'James', 'Maria']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations', 'Customer Success']
        roles = ['Manager', 'Senior Developer', 'Analyst', 'Coordinator', 'Director', 'Specialist', 'Associate']
        
        data = []
        for i in range(num_rows):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            emp_id = f"EMP{1000 + i + 1}"
            department = random.choice(departments)
            role = random.choice(roles)
            
            # Random joining date in last 5 years
            start_date = datetime.now() - timedelta(days=5*365)
            random_days = random.randint(0, 5*365)
            joining_date = start_date + timedelta(days=random_days)
            
            email = f"{first_name.lower()}.{last_name.lower()}@company.com"
            salary = random.randint(40000, 120000)
            
            data.append({
                'Full Name': f"{first_name} {last_name}",
                'Employee ID': emp_id,
                'Department': department,
                'Role': role,
                'Joining Date': joining_date.strftime('%Y-%m-%d'),
                'Email Address': email,
                'Salary (USD)': f"${salary:,}"
            })
        
        return pd.DataFrame(data)
    
    else:
        # Generic data for other domains
        data = []
        for i in range(num_rows):
            data.append({
                'ID': i + 1,
                'Name': f"Item_{i+1}",
                'Value': round(random.uniform(10, 1000), 2),
                'Category': random.choice(['A', 'B', 'C']),
                'Date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
            })
        
        return pd.DataFrame(data)

def main():
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">FauxFaundry</div>
        <div class="app-subtitle">Generate synthetic data with natural language</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main form
    st.markdown('<div class="section-title">Describe Your Data Requirements</div>', unsafe_allow_html=True)
    
    # Example section
    with st.expander("💡 See Example Prompt", expanded=False):
        example_prompt = '''Generate 15 rows of synthetic test data in the **Human Resources** domain.

The output should be in **tabular format** using Markdown syntax. Each row should represent an employee record. Include the following columns:

- Full Name
- Employee ID  
- Department
- Role
- Joining Date
- Email Address
- Salary (in USD)

Make the data look realistic and varied. Ensure that the Employee IDs follow a consistent pattern (e.g., EMP1234), and salaries range from $40,000 to $120,000.

Output only the table and nothing else.'''
        
        st.markdown(f'<div class="example-text">{example_prompt}</div>', unsafe_allow_html=True)
    
    # User input
    user_prompt = st.text_area(
        "Enter your data generation prompt:",
        height=250,
        placeholder="Describe what kind of synthetic data you want to generate. Include:\n• Domain (e.g., HR, Finance, E-commerce)\n• Number of rows\n• Column names and types\n• Any specific requirements or constraints\n• Output format preferences",
        help="Be as specific as possible about your requirements"
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Generate Data", key="generate"):
            if user_prompt.strip():
                # Progress indicator
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                # Simulate processing steps
                status_placeholder.markdown('<div class="status-message">🧠 Analyzing prompt...</div>', unsafe_allow_html=True)
                progress_bar.progress(25)
                time.sleep(0.8)
                
                status_placeholder.markdown('<div class="status-message">🔥 Generating synthetic data...</div>', unsafe_allow_html=True)
                progress_bar.progress(75)
                time.sleep(1.2)
                
                status_placeholder.markdown('<div class="status-message">✅ Finalizing output...</div>', unsafe_allow_html=True)
                progress_bar.progress(100)
                time.sleep(0.5)
                
                # Generate data
                try:
                    generated_data = generate_synthetic_data_from_prompt(user_prompt)
                    st.session_state.generated_data = generated_data
                    st.session_state.user_prompt = user_prompt
                    
                    # Clear progress
                    progress_bar.empty()
                    status_placeholder.empty()
                    
                    # Success message
                    st.markdown(f'''
                    <div class="success-message">
                        ✅ Successfully generated {len(generated_data)} rows of synthetic data
                    </div>
                    ''', unsafe_allow_html=True)
                    
                except Exception as e:
                    progress_bar.empty()
                    status_placeholder.empty()
                    st.error(f"Error generating data: {str(e)}")
            else:
                st.warning("Please enter a data generation prompt first.")
    
    # Display results
    if 'generated_data' in st.session_state:
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Generated Data</div>', unsafe_allow_html=True)
        
        # Show the data
        st.dataframe(
            st.session_state.generated_data,
            use_container_width=True,
            height=400
        )
        
        # Download options
        st.markdown('<div class="section-title">Export Options</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv_data = st.session_state.generated_data.to_csv(index=False)
            st.download_button(
                "📄 CSV",
                data=csv_data,
                file_name=f"fauxfaundry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = st.session_state.generated_data.to_json(orient="records", indent=2)
            st.download_button(
                "📋 JSON",
                data=json_data,
                file_name=f"fauxfaundry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col3:
            # Excel (using CSV for simplicity)
            st.download_button(
                "📊 Excel",
                data=csv_data,
                file_name=f"fauxfaundry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col4:
            # Markdown table
            markdown_table = st.session_state.generated_data.to_markdown(index=False)
            st.download_button(
                "📝 Markdown",
                data=markdown_table,
                file_name=f"fauxfaundry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        # Data preview in different formats
        st.markdown('<div class="section-title">Preview Formats</div>', unsafe_allow_html=True)
        
        format_tab1, format_tab2 = st.columns(2)
        
        with format_tab1:
            st.markdown("**Markdown Table:**")
            markdown_table = st.session_state.generated_data.to_markdown(index=False)
            st.code(markdown_table, language="markdown")
        
        with format_tab2:
            st.markdown("**JSON Format:**")
            json_preview = st.session_state.generated_data.head(3).to_json(orient="records", indent=2)
            st.code(json_preview, language="json")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
