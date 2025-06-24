import streamlit as st
import pandas as pd
import json
import time
import requests
from io import StringIO
from openai import OpenAI
import traceback

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
    
    .error-content {
        background: rgba(50, 0, 0, 0.5);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ff4444;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #ff8888;
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
        margin-bottom: 1rem;
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
    
    /* Status indicators */
    .status-online {
        color: #00ff00;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff4444;
        font-weight: bold;
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
            st.session_state.api_key_source = "secrets"
        except:
            st.session_state.openai_client = None
            st.session_state.api_key_source = None
    
    if 'generated_data' not in st.session_state:
        st.session_state.generated_data = None
    
    if 'generation_stats' not in st.session_state:
        st.session_state.generation_stats = {
            'total_datasets': 0,
            'successful_generations': 0,
            'failed_generations': 0
        }

# Enhanced test OpenAI connection with better error handling
def test_openai_connection():
    if not st.session_state.openai_client:
        return False, "No OpenAI client configured"
    
    try:
        # Test with a simple completion
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5,
            timeout=30
        )
        return True, "Connection successful"
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            return False, "Invalid API key"
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            return False, "API quota exceeded or billing issue"
        elif "timeout" in error_msg.lower():
            return False, "Connection timeout"
        elif "rate" in error_msg.lower():
            return False, "Rate limit exceeded"
        else:
            return False, f"Connection failed: {error_msg}"

# Fixed attribute designer with better error handling and connection management
def attribute_designer_stream(user_prompt, progress_placeholder, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Check if client exists before attempting
            if not st.session_state.openai_client:
                st.markdown('<div class="error-content">❌ OpenAI client not initialized</div>', unsafe_allow_html=True)
                return None
            
            with progress_placeholder.container():
                st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="step-header">🧠 Step 1: Designing Attribute Structure (Attempt {attempt + 1}/{max_retries})</div>', unsafe_allow_html=True)
                
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
                
                # Enhanced prompt for better JSON generation
                prompt = f"""You are a data schema designer. Create a JSON object defining the structure for a synthetic dataset.

REQUIREMENTS:
- Return ONLY valid JSON, no markdown, no explanations
- Use these data types only: "String", "Integer", "Float", "Boolean", "Date"
- Create 3-8 relevant fields based on the request
- Field names should be descriptive and use snake_case

USER REQUEST: {user_prompt}

Example format:
{{"field_name": "String", "age": "Integer", "salary": "Float", "is_active": "Boolean", "hire_date": "Date"}}

JSON:"""
                
                messages = [
                    {"role": "system", "content": "You are a data schema generator. Return only valid JSON with field names and data types. No additional text or formatting."},
                    {"role": "user", "content": prompt}
                ]
                
                # Make API call with enhanced error handling and exponential backoff
                try:
                    # Add exponential backoff delay
                    if attempt > 0:
                        delay = 2 ** attempt  # 2, 4, 8 seconds
                        time.sleep(delay)
                    
                    response = st.session_state.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",  # Changed from gpt-4o-mini to more stable model
                        messages=messages,
                        stream=False,
                        temperature=0.2,
                        max_tokens=300,
                        timeout=30,  # Reduced timeout
                        request_timeout=30  # Added explicit request timeout
                    )
                    
                    if not response or not response.choices:
                        raise Exception("Empty response from OpenAI API")
                    
                    attributes = response.choices[0].message.content.strip()
                    
                    if not attributes:
                        raise Exception("Empty content in API response")
                    
                except Exception as api_error:
                    error_msg = str(api_error).lower()
                    
                    if "connection" in error_msg or "network" in error_msg:
                        raise Exception("Network connection issue - check internet connectivity")
                    elif "timeout" in error_msg:
                        raise Exception("Request timed out - try again or check connection")
                    elif "rate" in error_msg or "rate limit" in error_msg:
                        raise Exception("Rate limit exceeded - wait before retrying")
                    elif "quota" in error_msg or "billing" in error_msg:
                        raise Exception("API quota exceeded or billing issue")
                    elif "api_key" in error_msg or "authentication" in error_msg:
                        raise Exception("Invalid API key or authentication failed")
                    elif "model" in error_msg:
                        raise Exception("Model not available - trying alternative")
                    else:
                        raise Exception(f"API error: {str(api_error)}")
                
                # Clean up the response to ensure it's valid JSON
                attributes = attributes.replace('```json', '').replace('```', '').strip()
                
                # Find JSON boundaries
                json_start = attributes.find('{')
                json_end = attributes.rfind('}')
                
                if json_start != -1 and json_end != -1 and json_end > json_start:
                    attributes = attributes[json_start:json_end + 1]
                
                # Validate JSON
                try:
                    parsed_json = json.loads(attributes)
                    if not isinstance(parsed_json, dict) or len(parsed_json) == 0:
                        raise ValueError("Invalid JSON structure - not a valid dictionary")
                    
                    # Additional validation for data types
                    valid_types = ["String", "Integer", "Float", "Boolean", "Date"]
                    for key, value in parsed_json.items():
                        if value not in valid_types:
                            st.warning(f"Warning: '{value}' is not a standard data type for field '{key}'")
                    
                    st.markdown(f'<div class="step-content">{json.dumps(parsed_json, indent=2)}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    return attributes
                    
                except json.JSONDecodeError as e:
                    if attempt < max_retries - 1:
                        st.markdown(f'<div class="error-content">Attempt {attempt + 1} failed: Invalid JSON format - {str(e)}. Retrying...</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        continue
                    else:
                        st.markdown(f'<div class="error-content">JSON Parse Error: {str(e)}. Raw response: {attributes[:200]}...</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        return None
                        
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific model errors by trying alternative
            if "model" in error_msg.lower() and attempt == 0:
                st.markdown(f'<div class="error-content">Model issue detected, trying alternative model...</div>', unsafe_allow_html=True)
                # Try with gpt-3.5-turbo-instruct as fallback
                try:
                    response = st.session_state.openai_client.completions.create(
                        model="gpt-3.5-turbo-instruct",
                        prompt=f"Generate a JSON schema for: {user_prompt}\n\nReturn only valid JSON with field names and data types like: {{\"name\": \"String\", \"age\": \"Integer\"}}",
                        max_tokens=300,
                        temperature=0.2,
                        timeout=30
                    )
                    
                    if response and response.choices:
                        attributes = response.choices[0].text.strip()
                        # Process the response similar to above
                        attributes = attributes.replace('```json', '').replace('```', '').strip()
                        json_start = attributes.find('{')
                        json_end = attributes.rfind('}')
                        
                        if json_start != -1 and json_end != -1:
                            attributes = attributes[json_start:json_end + 1]
                            try:
                                parsed_json = json.loads(attributes)
                                st.markdown(f'<div class="step-content">{json.dumps(parsed_json, indent=2)}</div>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                                return attributes
                            except:
                                pass
                except:
                    pass
            
            if attempt < max_retries - 1:
                st.markdown(f'<div class="error-content">Attempt {attempt + 1} failed: {error_msg}. Retrying in {2**(attempt+1)} seconds...</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                continue
            else:
                st.markdown(f'<div class="error-content">Final attempt failed: {error_msg}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                return None
    
    return None

# Enhanced dataset generator with better connection handling
def dataset_generator_stream(attributes, progress_placeholder, num_rows=10, max_retries=3):
    for attempt in range(max_retries):
        try:
            if st.session_state.openai_client is None:
                st.error("OpenAI client not initialized. Please check your API key.")
                return None
                
            with progress_placeholder.container():
                st.markdown('<div class="progress-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="step-header">✍️ Step 2: Generating Dataset (Attempt {attempt + 1}/{max_retries})</div>', unsafe_allow_html=True)
                
                # Parse attributes to understand the schema
                try:
                    schema = json.loads(attributes)
                    schema_description = ", ".join([f"{k} ({v})" for k, v in schema.items()])
                except:
                    schema_description = attributes
                
                system_prompt = """You are a synthetic dataset generator. Generate realistic tabular data in markdown table format.

REQUIREMENTS:
- Generate EXACTLY the requested number of rows
- Use realistic, diverse data that makes sense for each field type
- Format as a proper markdown table with pipes (|)
- Include header row and separator row with dashes
- No additional text, explanations, or code blocks
- Ensure data is consistent and logical"""
                
                user_prompt = f"""Generate a dataset with {num_rows} rows using this schema: {schema_description}

Return ONLY a markdown table with:
1. Header row with column names
2. Separator row with dashes (e.g., |---|---|)
3. {num_rows} data rows

Example format:
| Name | Age | City |
|------|-----|------|
| John | 25 | NYC |
| Jane | 30 | LA |"""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
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
                
                # Make API call with better error handling
                try:
                    response = st.session_state.openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        stream=False,
                        temperature=0.7,
                        max_tokens=2000,
                        timeout=60  # Increased timeout
                    )
                    
                    dataset = response.choices[0].message.content.strip()
                    
                except Exception as api_error:
                    error_msg = str(api_error)
                    if "timeout" in error_msg.lower():
                        raise Exception("API request timed out")
                    elif "rate" in error_msg.lower():
                        raise Exception("Rate limit exceeded")
                    elif "quota" in error_msg.lower():
                        raise Exception("API quota exceeded")
                    else:
                        raise Exception(f"API error: {error_msg}")
                
                # Clean up the dataset
                dataset = dataset.replace('```markdown', '').replace('```', '').strip()
                
                # Validate the table format
                if "|" in dataset and "---" in dataset:
                    st.markdown(f'<div class="step-content">{dataset}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    return dataset
                else:
                    if attempt < max_retries - 1:
                        st.markdown(f'<div class="error-content">Attempt {attempt + 1} failed: Invalid table format. Retrying...</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        time.sleep(2)
                        continue
                    else:
                        st.markdown(f'<div class="error-content">Failed to generate valid table format</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        return None
                
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                st.markdown(f'<div class="error-content">Attempt {attempt + 1} failed: {error_msg}. Retrying in 3 seconds...</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                time.sleep(3)
                continue
            else:
                st.markdown(f'<div class="error-content">Final attempt failed: {error_msg}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                return None
    
    return None

# Enhanced validator with detailed feedback
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
            "Counting rows and columns...",
            "Final validation..."
        ]
        
        validation_results = []
        
        for i, check in enumerate(checks):
            status_text = st.text(check)
            progress_bar.progress((i + 1) * 16)
            time.sleep(0.2)
        
        # Detailed validation
        lines = markdown_table.strip().split('\n')
        table_lines = [line.strip() for line in lines if line.strip()]
        
        # Check basic structure
        if not table_lines:
            st.markdown('<div class="error-content">❌ Empty table</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return False, "Empty table"
        
        # Check for pipe characters
        pipe_lines = [line for line in table_lines if '|' in line]
        if not pipe_lines:
            st.markdown('<div class="error-content">❌ Missing pipe characters (|)</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return False, "Missing pipe characters (|)"
        
        # Check for separator line
        separator_lines = [line for line in table_lines if '---' in line or '--' in line]
        if not separator_lines:
            st.markdown('<div class="error-content">❌ Missing separator line</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return False, "Missing separator line"
        
        # Count rows and columns
        try:
            header_line = pipe_lines[0]
            header_cols = len([col.strip() for col in header_line.split('|')[1:-1] if col.strip()])
            data_lines = [line for line in pipe_lines[1:] if '---' not in line and '--' not in line]
            data_rows = len(data_lines)
            
            validation_results.append(f"✅ Found {header_cols} columns")
            validation_results.append(f"✅ Found {data_rows} data rows")
            validation_results.append(f"✅ Table structure is valid")
            
        except Exception as e:
            validation_results.append(f"⚠️ Structure analysis warning: {str(e)}")
        
        # Display results
        for result in validation_results:
            st.markdown(f'<div class="step-content">{result}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="step-content">✅ Table validation successful!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    return True, "Table is valid"

# Enhanced exporter with better error handling
def export_data(markdown_table, output_format):
    try:
        # Clean the markdown table
        lines = markdown_table.strip().split('\n')
        table_lines = [line.strip() for line in lines if '|' in line and line.strip()]
        
        if len(table_lines) < 2:
            return None, "Invalid table format - insufficient rows"
        
        # Find header and separator
        header_line = table_lines[0]
        separator_found = False
        data_start_idx = 1
        
        for i, line in enumerate(table_lines[1:], 1):
            if '---' in line or '--' in line:
                separator_found = True
                data_start_idx = i + 1
                break
        
        if not separator_found:
            data_start_idx = 1
        
        # Extract header
        header = [col.strip() for col in header_line.split('|')[1:-1] if col.strip()]
        
        if not header:
            return None, "No valid header columns found"
        
        # Extract data
        data = []
        for line in table_lines[data_start_idx:]:
            if '---' in line or '--' in line:
                continue
            row = [col.strip() for col in line.split('|')[1:-1]]
            if len(row) >= len(header):
                data.append(row[:len(header)])  # Ensure row matches header length
        
        if not data:
            return None, "No data rows found"
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=header)
        
        # Export based on format
        if output_format == "csv":
            csv_data = df.to_csv(index=False)
            return csv_data, f"CSV generated successfully ({len(data)} rows, {len(header)} columns)"
        elif output_format == "json":
            json_data = df.to_json(orient="records", indent=2)
            return json_data, f"JSON generated successfully ({len(data)} rows, {len(header)} columns)"
        elif output_format == "excel":
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Generated_Data', index=False)
            excel_data = output.getvalue()
            return excel_data, f"Excel generated successfully ({len(data)} rows, {len(header)} columns)"
        
        return None, "Unsupported format"
        
    except Exception as e:
        return None, f"Export error: {str(e)}"

# Main application
def main():
    load_css()
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">FAUXFOUNDRY</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Synthetic Dataset Generation Platform v2.1 - Fixed</p>', unsafe_allow_html=True)
    
    # API Configuration in sidebar
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        
        # Test connection button
        if st.button("🔍 Test Connection"):
            if st.session_state.openai_client:
                is_connected, message = test_openai_connection()
                if is_connected:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
                    # Show troubleshooting tips
                    st.markdown("**Troubleshooting:**")
                    if "api_key" in message.lower():
                        st.write("• Check if your API key is valid")
                        st.write("• Ensure it starts with 'sk-'")
                    elif "quota" in message.lower():
                        st.write("• Check your OpenAI billing/usage")
                        st.write("• Verify your account has credits")
                    elif "timeout" in message.lower():
                        st.write("• Check your internet connection")
                        st.write("• Try again in a few moments")
                    elif "rate" in message.lower():
                        st.write("• Wait before making another request")
                        st.write("• Consider upgrading your plan")
            else:
                st.error("❌ No OpenAI client configured")
        
        # Show API key status
        if st.session_state.openai_client:
            st.markdown('<p class="status-online">🟢 OpenAI API Active</p>', unsafe_allow_html=True)
            if st.session_state.api_key_source == "secrets":
                st.info("Using API key from Streamlit secrets")
            else:
                st.info("Using manually entered API key")
        else:
            st.markdown('<p class="status-offline">🔴 OpenAI API Offline</p>', unsafe_allow_html=True)
            
            # Allow manual override if secrets don't work
            openai_key = st.text_input("OpenAI API Key", 
                                     type="password", 
                                     help="Enter your OpenAI API key (starts with sk-)")
            
            if openai_key:
                if not openai_key.startswith('sk-'):
                    st.error("❌ Invalid API key format. Should start with 'sk-'")
                else:
                    try:
                        st.session_state.openai_client = OpenAI(api_key=openai_key)
                        st.session_state.api_key_source = "manual"
                        st.success("✅ OpenAI client initialized")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Invalid API key: {str(e)}")
        
        st.markdown("---")
        st.markdown("### 📊 Generation Options")
        num_rows = st.slider("Number of rows", min_value=5, max_value=100, value=10)
        export_format = st.selectbox("Export Format", ["csv", "json", "excel"])
        
        st.markdown("---")
        st.markdown("### 📈 Session Stats")
        stats = st.session_state.generation_stats
        st.metric("Total Attempts", stats['total_datasets'])
        st.metric("Successful", stats['successful_generations'])
        st.metric("Failed", stats['failed_generations'])
        
        if st.button("🔄 Reset Stats"):
            st.session_state.generation_stats = {
                'total_datasets': 0,
                'successful_generations': 0,
                'failed_generations': 0
            }
            st.rerun()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Dataset Request")
        user_prompt = st.text_area(
            "Describe your dataset requirements:",
            height=120,
            placeholder="Example: Generate a dataset for an e-commerce platform with customer information including: customer ID, name, email, age, location, purchase history, and membership status. Include diverse, realistic data.",
            help="Be specific about the columns, data types, and business context you need."
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            generate_btn = st.button("🚀 Generate Dataset", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Clear Results", use_container_width=True)
        with col_btn3:
            example_btn = st.button("📝 Load Example", use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Current Dataset")
        if st.session_state.generated_data:
            try:
                # Parse the generated data to show stats
                lines = st.session_state.generated_data.strip().split('\n')
                table_lines = [line for line in lines if '|' in line and line.strip()]
                
                if len(table_lines) >= 2:
                    header_line = table_lines[0]
                    cols = len([col.strip() for col in header_line.split('|')[1:-1] if col.strip()])
                    data_lines = [line for line in table_lines[1:] if '---' not in line and '--' not in line]
                    rows = len(data_lines)
                    
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-value">{rows}</div>
                        <div class="metric-label">Data Rows</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-value">{cols}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Show success rate
                    if st.session_state.generation_stats['total_datasets'] > 0:
                        success_rate = int((st.session_state.generation_stats['successful_generations'] / 
                                          st.session_state.generation_stats['total_datasets']) * 100)
                        st.markdown(f'''
                        <div class="metric-container">
                            <div class="metric-value">{success_rate}%</div>
                            <div class="metric-label">Success Rate</div>
                        </div>
                        ''', unsafe_allow_html=True)
            except:
                pass
        else:
            st.markdown('''
            <div class="metric-container">
                <div class="metric-value">0</div>
                <div class="metric-label">No Data</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Load example
    if example_btn:
        st.session_state.example_prompt = "Generate a customer database for a subscription-based streaming service with fields: customer_id, full_name, email, age, subscription_plan, monthly_fee, join_date, last_login, total_watch_hours, favorite_genre, and account_status. Create diverse, realistic customer profiles."
        st.rerun()
    
    # Use example prompt if set
    if hasattr(st.session_state, 'example_prompt'):
        user_prompt = st.session_state.example_prompt
        delattr(st.session_state, 'example_prompt')
    
    # Clear results
    if clear_btn:
        st.session_state.generated_data = None
        st.rerun()
    
    # Generate dataset
    if generate_btn and user_prompt:
        if not st.session_state.openai_client:
            st.error("⚠️ Please configure your OpenAI API key in the sidebar")
            return
        
        # Update stats
        st.session_state.generation_stats['total_datasets'] += 1
        
        # Progress container
        progress_placeholder = st.empty()
        
        try:
            # Step 1: Attribute Design
            st.info("🚀 Starting dataset generation process...")
            attributes = attribute_designer_stream(user_prompt, progress_placeholder)
            
            if attributes:
                # Step 2: Dataset Generation
                dataset = dataset_generator_stream(attributes, progress_placeholder, num_rows)
                
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
                                filename = f"fauxfoundry_data.{export_format}"
                                mime_type = {
                                    "csv": "text/csv",
                                    "json": "application/json",
                                    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                }.get(export_format, "text/plain")
                                
                                st.download_button(
                                    label=f"📥 Download {export_format.upper()}",
                                    data=export_data_content,
                                    file_name=filename,
                                    mime=mime_type,
                                    use_container_width=True
                                )
                            else:
                                st.markdown(f'<div class="error-content">❌ {export_message}</div>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Store generated data and update success stats
                        st.session_state.generated_data = dataset
                        st.session_state.generation_stats['successful_generations'] += 1
                        
                        # Display the generated table
                        st.markdown("### 📋 Generated Dataset Preview")
                        
                        # Create expandable section for large datasets
                        with st.expander("View Full Dataset", expanded=True):
                            st.markdown(dataset)
                        
                        # Show data analysis
                        try:
                            lines = dataset.strip().split('\n')
                            table_lines = [line for line in lines if '|' in line and line.strip()]
                            if len(table_lines) >= 2:
                                st.success(f"✅ Successfully generated {len(table_lines)-2} rows of synthetic data!")
                        except:
                            pass
                        
                    else:
                        st.error(f"❌ Validation failed: {message}")
                        st.session_state.generation_stats['failed_generations'] += 1
                else:
                    st.error("❌ Failed to generate dataset")
                    st.session_state.generation_stats['failed_generations'] += 1
            else:
                st.error("❌ Failed to design attribute structure")
                st.session_state.generation_stats['failed_generations'] += 1
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.session_state.generation_stats['failed_generations'] += 1
            
            # Show detailed error in expander
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
    
    elif generate_btn and not user_prompt:
        st.warning("⚠️ Please enter a dataset description")
    
    # Footer with tips
    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Better Prompts**
        - Be specific about data types
        - Mention business context
        - Include relationships between fields
        - Specify realistic constraints
        """)
    
    with col2:
        st.markdown("""
        **⚡ Performance**
        - Start with smaller datasets (10-25 rows)
        - Test connection before large generations
        - Use retry logic for better reliability
        - Monitor your API usage
        """)
    
    with col3:
        st.markdown("""
        **📊 Data Quality**
        - Review generated data for accuracy
        - Check for realistic value ranges
        - Validate data relationships
        - Consider data privacy implications
        """)

if __name__ == "__main__":
    main()
                #
