import streamlit as st
import pandas as pd
import json
import time
from io import StringIO
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="FauxFoundry",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern black UI
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ffff);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        text-align: center;
        color: #a0a0a0;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Input styling */
    .stTextArea textarea {
        background: rgba(20, 20, 30, 0.8) !important;
        border: 2px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(0, 255, 255, 0.8) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #00ffff, #0080ff) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4) !important;
    }
    
    /* Progress styling */
    .progress-container {
        background: rgba(20, 20, 30, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .step-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #00ffff;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }
    
    .step-content {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #00ffff;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #e0e0e0;
    }
    
    /* Table styling */
    .dataframe {
        background: rgba(20, 20, 30, 0.9) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(10, 10, 20, 0.95) !important;
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(20, 20, 30, 0.8);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 0, 255, 0.2);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ff00ff;
        font-family: 'Orbitron', monospace;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'openai_client' not in st.session_state:
        # Try to load API key from Streamlit secrets first
        try:
            openai_api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.openai_client = OpenAI(api_key=openai_api_key)
        except:
            st.session_state.openai_client = None
    if 'generated_data' not in st.session_state:
        st.session_state.generated_data = None

# Simplified attribute designer using OpenAI only
def attribute_designer_stream(user_prompt, progress_placeholder):
    try:
        with progress_placeholder.container():
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            st.markdown('<div class="step-header">🧠 Step 1: Designing Attribute Structure</div>', unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("Analyzing data requirements...")
                elif i < 60:
                    status_text.text("Identifying column types...")
                elif i < 90:
                    status_text.text("Generating attribute schema...")
                else:
                    status_text.text("Finalizing structure...")
                time.sleep(0.01)
            
            # Use OpenAI for attribute design
            prompt = f"""You are a data schema designer. Analyze the user's request and return ONLY a valid JSON object with field names and their data types.

Rules:
- Return only valid JSON, no additional text
- Use common data types: "String", "Integer", "Float", "Boolean", "Date"
- Field names should be clear and descriptive

User request: {user_prompt}

JSON schema:"""
            
            messages = [
                {"role": "system", "content": "You are a data schema analyzer. Return only valid JSON with no additional text."},
                {"role": "user", "content": prompt}
            ]
            
            response = st.session_state.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=False,
                temperature=0.3,
                max_tokens=500
            )
            
            attributes = response.choices[0].message.content.strip()
            
            # Clean up the response to ensure it's valid JSON
            if not attributes.startswith('{'):
                json_start = attributes.find('{')
                if json_start != -1:
                    attributes = attributes[json_start:]
            
            if not attributes.endswith('}'):
                json_end = attributes.rfind('}')
                if json_end != -1:
                    attributes = attributes[:json_end + 1]
            
            # Test if it's valid JSON
            try:
                json.loads(attributes)
            except:
                attributes = '{"error": "Invalid JSON generated"}'
            
            st.markdown(f'<div class="step-content">{attributes}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        return attributes
        
    except Exception as e:
        st.error(f"Error in attribute designer: {str(e)}")
        return '{"error": "Failed to generate attributes"}'

# Enhanced dataset generator with streaming
def dataset_generator_stream(attributes, progress_placeholder):
    try:
        if st.session_state.openai_client is None:
            st.error("OpenAI client not initialized. Please check your API key.")
            return None
            
        with progress_placeholder.container():
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            st.markdown('<div class="step-header">✍️ Step 2: Generating Dataset</div>', unsafe_allow_html=True)
            
            system_prompt = """You are a synthetic test dataset generator. Generate accurate tabular test datasets as per the received JSON structure. Respond with a clean markdown table format."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a dataset with these attributes: {attributes}. Create 10 rows of realistic data in markdown table format."}
            ]
            
            # Simulate streaming by showing progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("Analyzing data structure...")
                elif i < 60:
                    status_text.text("Generating realistic data...")
                elif i < 90:
                    status_text.text("Formatting table...")
                else:
                    status_text.text("Finalizing dataset...")
                time.sleep(0.02)
            
            response = st.session_state.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=False
            )
            
            dataset = response.choices[0].message.content
            st.markdown(f'<div class="step-content">{dataset}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        return dataset
        
    except Exception as e:
        st.error(f"Error in dataset generator: {str(e)}")
        return None

# Enhanced validator with streaming
def validator_stream(markdown_table, progress_placeholder):
    with progress_placeholder.container():
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-header">🧪 Step 3: Validating Dataset</div>', unsafe_allow_html=True)
        
        # Simulate validation process
        progress_bar = st.progress(0)
        checks = [
            "Checking table structure...",
            "Validating pipe characters...",
            "Verifying separator lines...",
            "Checking data consistency...",
            "Final validation..."
        ]
        
        for i, check in enumerate(checks):
            st.text(check)
            progress_bar.progress((i + 1) * 20)
            time.sleep(0.3)
        
        # Actual validation
        if "|" not in markdown_table:
            st.markdown('<div class="step-content">❌ Missing pipe characters (|)</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return False, "Missing pipe characters (|)"
        
        if "---" not in markdown_table:
            st.markdown('<div class="step-content">❌ Missing separator line</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return False, "Missing separator line"
        
        st.markdown('<div class="step-content">✅ Table validation successful!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    return True, "Table is valid"

# Enhanced exporter
def export_data(markdown_table, output_format):
    try:
        # Clean the markdown table
        lines = markdown_table.strip().split('\n')
        table_lines = [line for line in lines if '|' in line and line.strip()]
        
        if len(table_lines) < 2:
            return None, "Invalid table format"
        
        # Convert to DataFrame
        header = [col.strip() for col in table_lines[0].split('|')[1:-1]]
        data = []
        
        for line in table_lines[2:]:  # Skip header and separator
            row = [col.strip() for col in line.split('|')[1:-1]]
            if len(row) == len(header):
                data.append(row)
        
        df = pd.DataFrame(data, columns=header)
        
        if output_format == "csv":
            csv_data = df.to_csv(index=False)
            return csv_data, "CSV generated successfully"
        elif output_format == "json":
            json_data = df.to_json(orient="records", indent=2)
            return json_data, "JSON generated successfully"
        
        return None, "Unsupported format"
        
    except Exception as e:
        return None, f"Export error: {str(e)}"

# Main application
def main():
    load_css()
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">FAUXFOUNDRY</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Synthetic Dataset Generation Platform</p>', unsafe_allow_html=True)
    
    # API Configuration in sidebar
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        
        # Show API key status
        if st.session_state.openai_client:
            st.success("✅ OpenAI API configured")
        else:
            st.warning("⚠️ OpenAI API not configured")
            
            # Allow manual override if secrets don't work
            openai_key = st.text_input("OpenAI API Key (Optional Override)", 
                                     type="password", 
                                     help="Only needed if automatic configuration fails")
            
            if openai_key:
                try:
                    st.session_state.openai_client = OpenAI(api_key=openai_key)
                    st.success("✅ OpenAI client initialized")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Invalid API key: {str(e)}")
        
        st.markdown("### 📊 Export Options")
        export_format = st.selectbox("Output Format", ["csv", "json"])
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Dataset Request")
        user_prompt = st.text_area(
            "Describe your dataset requirements:",
            height=120,
            placeholder="Example: Generate a dataset containing student information with columns: ID, Name, Class, Age, Gender, and Math Score. I need 15 rows of data.",
            help="Be specific about the columns, data types, and number of rows you need."
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_btn = st.button("🚀 Generate Dataset", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Clear Results", use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Statistics")
        if st.session_state.generated_data:
            try:
                # Parse the generated data to show stats
                lines = st.session_state.generated_data.strip().split('\n')
                table_lines = [line for line in lines if '|' in line and line.strip()]
                
                if len(table_lines) >= 2:
                    rows = len(table_lines) - 2  # Exclude header and separator
                    cols = len([col for col in table_lines[0].split('|')[1:-1] if col.strip()])
                    
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-value">{rows}</div>
                        <div class="metric-label">Rows Generated</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-value">{cols}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    ''', unsafe_allow_html=True)
            except:
                pass
        else:
            st.markdown('''
            <div class="metric-container">
                <div class="metric-value">0</div>
                <div class="metric-label">Datasets Generated</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Clear results
    if clear_btn:
        st.session_state.generated_data = None
        st.rerun()
    
    # Generate dataset
    if generate_btn and user_prompt:
        if not st.session_state.openai_client:
            st.error("⚠️ Please configure your OpenAI API key in the sidebar")
            return
        
        # Progress container
        progress_placeholder = st.empty()
        
        # Step 1: Attribute Design
        attributes = attribute_designer_stream(user_prompt, progress_placeholder)
        
        if attributes and "error" not in attributes.lower():
            # Step 2: Dataset Generation
            dataset = dataset_generator_stream(attributes, progress_placeholder)
            
            if dataset:
                # Step 3: Validation
                valid, message = validator_stream(dataset, progress_placeholder)
                
                if valid:
                    # Step 4: Export
                    with progress_placeholder.container():
                        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                        st.markdown('<div class="step-header">📦 Step 4: Preparing Export</div>', unsafe_allow_html=True)
                        
                        export_data_content, export_message = export_data(dataset, export_format)
                        
                        if export_data_content:
                            st.markdown(f'<div class="step-content">✅ {export_message}</div>', unsafe_allow_html=True)
                            
                            # Download button
                            filename = f"synthetic_data.{export_format}"
                            st.download_button(
                                label=f"📥 Download {export_format.upper()}",
                                data=export_data_content,
                                file_name=filename,
                                mime=f"text/{export_format}"
                            )
                        else:
                            st.markdown(f'<div class="step-content">❌ {export_message}</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Store generated data
                    st.session_state.generated_data = dataset
                    
                    # Display the generated table
                    st.markdown("### 📋 Generated Dataset Preview")
                    st.markdown(dataset)
                    
                else:
                    st.error(f"Validation failed: {message}")
            else:
                st.error("Failed to generate dataset")
        else:
            st.error("Failed to design attributes")
    
    elif generate_btn and not user_prompt:
        st.warning("⚠️ Please enter a dataset description")

if __name__ == "__main__":
    main()
                
                #
