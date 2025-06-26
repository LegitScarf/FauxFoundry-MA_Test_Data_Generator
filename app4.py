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
    page_title="Synthetic Data Generator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
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
        <h1>🔬 Synthetic Test Data Generator</h1>
        <p>AI-Powered Data Generation with Google Gemini & OpenAI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize generator
    if 'generator' not in st.session_state:
        st.session_state.generator = SyntheticDataGenerator()
    
    # Sidebar for API keys
    with st.sidebar:
        st.header("🔑 API Configuration")
        
        # Gemini API Key
        gemini_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio"
        )
        
        # OpenAI API Key  
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Get your API key from OpenAI platform"
        )
        
        # Setup clients
        if gemini_key and openai_key:
            if st.button("🔧 Configure APIs"):
                with st.spinner("Configuring APIs..."):
                    gemini_success = st.session_state.generator.setup_gemini(gemini_key)
                    openai_success = st.session_state.generator.setup_openai(openai_key)
                    
                    if gemini_success and openai_success:
                        st.success("✅ APIs configured successfully!")
                        st.session_state.apis_configured = True
                    else:
                        st.error("❌ Failed to configure APIs")
                        st.session_state.apis_configured = False
        
        # Status indicator
        if hasattr(st.session_state, 'apis_configured') and st.session_state.apis_configured:
            st.success("🟢 APIs Ready")
        else:
            st.warning("🟡 APIs Not Configured")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Data Generation Request")
        
        # User input
        user_prompt = st.text_area(
            "Describe the dataset you want to generate:",
            placeholder="Example: Create me a dataset about school children with columns: name, class, roll number, age, and gender. I want 15 rows of data.",
            height=150
        )
        
        # Generate button
        if st.button("🚀 Generate Dataset", disabled=not hasattr(st.session_state, 'apis_configured') or not st.session_state.apis_configured):
            if not user_prompt:
                st.error("Please provide a description of the dataset you want to generate.")
                return
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Agent 1: Generate Attributes
                status_text.text("🤖 Agent 1: Analyzing request and generating attributes...")
                progress_bar.progress(10)
                
                with st.spinner("Generating attributes schema..."):
                    attributes = st.session_state.generator.generate_attributes(user_prompt)
                
                progress_bar.progress(33)
                
                # Display attributes
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.subheader("🎯 Agent 1 Output - Attributes Schema")
                st.json(attributes)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Agent 2: Generate Dataset
                status_text.text("🤖 Agent 2: Generating synthetic dataset...")
                progress_bar.progress(50)
                
                with st.spinner("Creating synthetic data..."):
                    markdown_table = st.session_state.generator.generate_dataset(attributes)
                
                progress_bar.progress(66)
                
                # Display dataset
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.subheader("📊 Agent 2 Output - Generated Dataset")
                st.markdown(markdown_table)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Agent 3: Convert to CSV
                status_text.text("🤖 Agent 3: Converting to CSV format...")
                progress_bar.progress(80)
                
                with st.spinner("Converting to CSV..."):
                    csv_data = st.session_state.generator.markdown_to_csv(markdown_table)
                
                progress_bar.progress(100)
                status_text.text("✅ Dataset generation completed!")
                
                # Store results
                st.session_state.csv_data = csv_data
                st.session_state.attributes = attributes
                
                # Success message
                st.markdown('<div class="success-message">🎉 Dataset generated successfully!</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="error-message">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                progress_bar.empty()
                status_text.empty()
    
    with col2:
        st.header("📈 Generation Stats")
        
        if hasattr(st.session_state, 'attributes'):
            attrs = st.session_state.attributes
            
            # Metrics
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Columns", len(attrs.get('attributes', {})))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Rows", attrs.get('num_rows', 0))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download section
            if hasattr(st.session_state, 'csv_data'):
                st.header("💾 Download")
                
                # CSV download
                st.download_button(
                    label="📥 Download CSV",
                    data=st.session_state.csv_data,
                    file_name="synthetic_dataset.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # JSON schema download
                st.download_button(
                    label="📥 Download Schema",
                    data=json.dumps(st.session_state.attributes, indent=2),
                    file_name="dataset_schema.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("Generate a dataset to see statistics and download options.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>🔬 Synthetic Data Generator | Powered by Google Gemini & OpenAI GPT-4o-mini</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
