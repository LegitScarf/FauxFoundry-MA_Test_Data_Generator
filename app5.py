import streamlit as st
import json
import csv
import io
import pandas as pd
import google.generativeai as genai
from openai import OpenAI
import re
from typing import Dict, Any
import time

# Configure page
st.set_page_config(
    page_title="FauxFoundry",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sci-Fi Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;500;600&display=swap');
    
    /* Global Dark Theme */
    .stApp {
        background: #0a0a0a;
        color: #e0e0e0;
    }
    
    .main > div {
        background: #0a0a0a;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00f5ff, #0080ff);
        border-radius: 10px;
    }
    
    /* Main Header */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        border: 2px solid transparent;
        border-image: linear-gradient(45deg, #00f5ff, #0080ff, #8000ff) 1;
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #00f5ff, #ffffff, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
        margin-bottom: 0.5rem;
        letter-spacing: 4px;
    }
    
    .main-header p {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.2rem;
        color: #00f5ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
    }
    
    /* Agent Cards */
    .agent-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #333;
        border-left: 4px solid #00f5ff;
        margin: 1.5rem 0;
        box-shadow: 
            0 4px 8px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(0, 245, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00f5ff, #8000ff, #00f5ff);
        animation: pulse-border 2s ease-in-out infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #0d4f3c 0%, #1a5f4a 100%);
        color: #00ff88;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #00ff88;
        margin: 1rem 0;
        font-family: 'Exo 2', sans-serif;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
    }
    
    .error-message {
        background: linear-gradient(135deg, #4a1a1a 0%, #5a2a2a 100%);
        color: #ff4444;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #ff4444;
        margin: 1rem 0;
        font-family: 'Exo 2', sans-serif;
        box-shadow: 0 0 15px rgba(255, 68, 68, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00f5ff, #0080ff);
        color: #000;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2.5rem;
        font-weight: 600;
        font-family: 'Exo 2', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0, 245, 255, 0.5);
        background: linear-gradient(45deg, #0080ff, #8000ff);
        color: white;
    }
    
    .stButton > button:disabled {
        background: #333;
        color: #666;
        box-shadow: none;
        transform: none;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 
            0 4px 8px rgba(0, 0, 0, 0.3),
            0 0 15px rgba(0, 245, 255, 0.1);
    }
    
    .metric-card h3 {
        color: #00f5ff;
        font-family: 'Orbitron', monospace;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    .css-1v0mbdj {
        border-right: 2px solid #333;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1a1a1a;
        color: #e0e0e0;
        border: 1px solid #333;
        border-radius: 8px;
        font-family: 'Exo 2', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00f5ff;
        box-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00f5ff, #0080ff, #8000ff);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Orbitron', monospace;
        color: #00f5ff;
    }
    
    h2 {
        border-bottom: 2px solid #333;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* JSON Display */
    .stJson {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
    }
    
    /* Status Indicators */
    .status-ready {
        color: #00ff88;
        background: #0d4f3c;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-family: 'Exo 2', sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }
    
    .status-warning {
        color: #ffaa00;
        background: #4a3d0d;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-family: 'Exo 2', sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(255, 170, 0, 0.3);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        border-top: 2px solid #333;
        text-align: center;
        color: #666;
        padding: 2rem 0;
        margin-top: 3rem;
        font-family: 'Exo 2', sans-serif;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    
    .footer .brand {
        color: #00f5ff;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
    }
    
    /* Animation for loading states */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 245, 255, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 245, 255, 0.8); }
    }
    
    .loading-glow {
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Data Table Styling */
    .stDataFrame {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
    }
    
    /* Download Section */
    .download-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333;
        margin: 1rem 0;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

class SyntheticDataGenerator:
    def __init__(self):
        self.gemini_client = None
        self.openai_client = None
        
    def setup_gemini(self, api_key: str):
        """Setup Google Gemini client"""
        try:
            genai.configure(api_key=api_key)
            self.gemini_client = genai.GenerativeModel('gemini-1.5-flash')
            return True
        except Exception as e:
            st.error(f"Failed to setup Gemini: {str(e)}")
            return False
    
    def setup_openai(self, api_key: str):
        """Setup OpenAI client"""
        try:
            self.openai_client = OpenAI(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Failed to setup OpenAI: {str(e)}")
            return False
    
    def generate_attributes(self, user_prompt: str) -> Dict[str, Any]:
        """Agent 1: Generate attributes using Google Gemini"""
        if not self.gemini_client:
            raise Exception("Gemini client not configured")
        
        prompt = f"""
        Based on the following user request, create a JSON schema that defines the data attributes and their types.
        
        User Request: {user_prompt}
        
        Please analyze the request and create a JSON object with the following structure:
        {{
            "attributes": {{
                "column_name": "data_type",
                ...
            }},
            "num_rows": number_of_rows_requested,
            "dataset_description": "brief description of the dataset"
        }}
        
        Supported data types: string, integer, float, boolean, date, email, phone, address, url
        
        Return ONLY the JSON object, no additional text or explanation.
        """
        
        try:
            response = self.gemini_client.generate_content(prompt)
            
            # Extract JSON from response
            json_text = response.text.strip()
            
            # Clean up the response to extract JSON
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0]
            elif "```" in json_text:
                json_text = json_text.split("```")[1]
            
            # Parse JSON
            attributes = json.loads(json_text.strip())
            return attributes
            
        except Exception as e:
            raise Exception(f"Error generating attributes: {str(e)}")
    
    def generate_dataset(self, attributes: Dict[str, Any]) -> str:
        """Agent 2: Generate dataset using OpenAI GPT-4o-mini"""
        if not self.openai_client:
            raise Exception("OpenAI client not configured")
        
        attr_dict = attributes.get("attributes", {})
        num_rows = attributes.get("num_rows", 10)
        description = attributes.get("dataset_description", "")
        
        # Create column headers
        columns = list(attr_dict.keys())
        
        prompt = f"""
        Generate a realistic synthetic dataset with the following specifications:
        
        Dataset Description: {description}
        Number of rows: {num_rows}
        
        Columns and their types:
        {json.dumps(attr_dict, indent=2)}
        
        Requirements:
        1. Generate realistic, diverse data that makes sense for each column type
        2. Ensure data consistency and logical relationships between columns
        3. Return the data in markdown table format
        4. Include proper headers
        5. Make sure all data is appropriate and follows the specified data types
        
        Return ONLY the markdown table, no additional text or explanation.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a synthetic data generator. Generate realistic, diverse datasets in markdown table format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error generating dataset: {str(e)}")
    
    def markdown_to_csv(self, markdown_table: str) -> str:
        """Agent 3: Convert markdown table to CSV"""
        try:
            lines = markdown_table.strip().split('\n')
            
            # Find the table start
            table_lines = []
            in_table = False
            
            for line in lines:
                if '|' in line and not in_table:
                    in_table = True
                    table_lines.append(line)
                elif '|' in line and in_table:
                    table_lines.append(line)
                elif in_table and '|' not in line:
                    break
            
            if not table_lines:
                raise Exception("No table found in markdown")
            
            # Process table lines
            csv_lines = []
            for i, line in enumerate(table_lines):
                # Skip separator lines (contains only |, -, :, and spaces)
                if re.match(r'^[\|\-\:\s]+$', line):
                    continue
                
                # Clean and split the line
                cells = [cell.strip() for cell in line.split('|')]
                # Remove empty cells at start/end
                cells = [cell for cell in cells if cell]
                
                if cells:
                    csv_lines.append(','.join(f'"{cell}"' for cell in cells))
            
            return '\n'.join(csv_lines)
            
        except Exception as e:
            raise Exception(f"Error converting to CSV: {str(e)}")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>FAUXFOUNDRY</h1>
        <p>Synthetic Test Data Generator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize generator
    if 'generator' not in st.session_state:
        st.session_state.generator = SyntheticDataGenerator()
    
    # Sidebar for API keys
    with st.sidebar:
        st.markdown("## ⚡ NEURAL INTERFACE")
        
        # Gemini API Key
        gemini_key = st.text_input(
            "🔮 Gemini Neural Link",
            type="password",
            help="Initialize Gemini consciousness"
        )
        
        # OpenAI API Key  
        openai_key = st.text_input(
            "🧠 OpenAI Neural Core",
            type="password",
            help="Activate GPT neural matrix"
        )
        
        # Setup clients
        if gemini_key and openai_key:
            if st.button("🔧 INITIALIZE NEURAL NETWORK"):
                with st.spinner("Synchronizing neural pathways..."):
                    gemini_success = st.session_state.generator.setup_gemini(gemini_key)
                    openai_success = st.session_state.generator.setup_openai(openai_key)
                    
                    if gemini_success and openai_success:
                        st.markdown('<div class="success-message">⚡ Neural network synchronized!</div>', unsafe_allow_html=True)
                        st.session_state.apis_configured = True
                    else:
                        st.markdown('<div class="error-message">❌ Neural sync failed</div>', unsafe_allow_html=True)
                        st.session_state.apis_configured = False
        
        # Status indicator
        if hasattr(st.session_state, 'apis_configured') and st.session_state.apis_configured:
            st.markdown('<div class="status-ready">🟢 NEURAL LINK ACTIVE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">🟡 NEURAL LINK OFFLINE</div>', unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 📡 DATA SYNTHESIS REQUEST")
        
        # User input
        user_prompt = st.text_area(
            "Transmit your data requirements:",
            placeholder="EXAMPLE TRANSMISSION: Create me a dataset about space colony inhabitants with columns: name, sector, ID number, age, and occupation. I want 20 rows of synthetic data.",
            height=150
        )
        
        # Generate button
        if st.button("🚀 INITIATE DATA SYNTHESIS", disabled=not hasattr(st.session_state, 'apis_configured') or not st.session_state.apis_configured):
            if not user_prompt:
                st.markdown('<div class="error-message">❌ No transmission received. Please provide synthesis parameters.</div>', unsafe_allow_html=True)
                return
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Agent 1: Generate Attributes
                status_text.markdown("🤖 **NEURAL AGENT 01**: Analyzing transmission and parsing data schema...")
                progress_bar.progress(10)
                
                with st.spinner("Executing schema analysis protocol..."):
                    attributes = st.session_state.generator.generate_attributes(user_prompt)
                
                progress_bar.progress(33)
                
                # Display attributes
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.markdown("### 🎯 AGENT 01 OUTPUT - Schema Matrix")
                st.json(attributes)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Agent 2: Generate Dataset
                status_text.markdown("🤖 **NEURAL AGENT 02**: Fabricating synthetic data matrix...")
                progress_bar.progress(50)
                
                with st.spinner("Running data synthesis algorithms..."):
                    markdown_table = st.session_state.generator.generate_dataset(attributes)
                
                progress_bar.progress(66)
                
                # Display dataset
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.markdown("### 📊 AGENT 02 OUTPUT - Synthetic Data Matrix")
                st.markdown(markdown_table)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Agent 3: Convert to CSV
                status_text.markdown("🤖 **NEURAL AGENT 03**: Converting to portable data format...")
                progress_bar.progress(80)
                
                with st.spinner("Executing format conversion protocol..."):
                    csv_data = st.session_state.generator.markdown_to_csv(markdown_table)
                
                progress_bar.progress(100)
                status_text.markdown("✅ **DATA SYNTHESIS COMPLETE**")
                
                # Store results
                st.session_state.csv_data = csv_data
                st.session_state.attributes = attributes
                
                # Success message
                st.markdown('<div class="success-message">⚡ Synthetic data matrix successfully generated!</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ SYNTHESIS ERROR: {str(e)}</div>', unsafe_allow_html=True)
                progress_bar.empty()
                status_text.empty()
    
    with col2:
        st.markdown("## 📈 SYNTHESIS METRICS")
        
        if hasattr(st.session_state, 'attributes'):
            attrs = st.session_state.attributes
            
            # Metrics
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Data Columns", len(attrs.get('attributes', {})))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Data Rows", attrs.get('num_rows', 0))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download section
            if hasattr(st.session_state, 'csv_data'):
                st.markdown("## 💾 DATA EXTRACTION")
                
                st.markdown('<div class="download-section">', unsafe_allow_html=True)
                
                # CSV download
                st.download_button(
                    label="📥 EXTRACT CSV MATRIX",
                    data=st.session_state.csv_data,
                    file_name="fauxfoundry_dataset.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # JSON schema download
                st.download_button(
                    label="📥 EXTRACT SCHEMA MAP",
                    data=json.dumps(st.session_state.attributes, indent=2),
                    file_name="fauxfoundry_schema.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🔄 Initiate data synthesis to view metrics and extraction options.")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><span class="brand">FAUXFOUNDRY</span> | Synthetic Test Data Generator</p>
        <p>Powered by Gemini & GPT-4o Matrix | Built with Streamlit</p>
        <p>⚡ Synthetic Intelligence Laboratory ⚡</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
