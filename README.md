# FauxFoundry 🦊

*A powerful synthetic test data generator powered by AI*

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Overview

FauxFoundry is an intelligent synthetic test data generator that leverages cutting-edge AI models to create realistic datasets from natural language descriptions. Built with a sophisticated 3-agent architecture, it transforms simple prompts into comprehensive, structured datasets perfect for testing, development, and prototyping.

## ✨ Key Features

- ** 3-Agent Architecture**: Sequential processing with specialized AI agents for optimal results
- ** Modern UI**: Sleek Streamlit interface with custom CSS styling
- ** Dual AI Models**: Google Gemini for schema generation, OpenAI GPT-4o-mini for data creation
- ** Real-time Progress**: Live progress tracking and status updates
- ** Multiple Export Formats**: Download as CSV or JSON schema
- ** Responsive Design**: Works seamlessly on desktop and mobile devices
- ** Extensible**: Support for custom data types and formats

##  Quick Start

### Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- pip package manager
- API keys for:
  - [Google Gemini](https://makersuite.google.com/app/apikey)
  - [OpenAI](https://platform.openai.com/api-keys)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fauxfoundry.git
   cd fauxfoundry
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   Open your browser and navigate to `http://localhost:8501`

## 🏗️ Project Structure

```
fauxfoundry/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .streamlit/           
│   └── config.toml       # Streamlit configuration
├── README.md             # This file
└── assets/               # Screenshots and demo files
```

## 🎯 How It Works

FauxFoundry uses a sophisticated 3-agent system:

### 🔍 Agent 1: Schema Analyzer (Google Gemini)
- **Input**: Natural language description
- **Process**: Extracts data schema and requirements
- **Output**: Structured JSON with column definitions

```json
{
  "attributes": {
    "name": "string",
    "age": "integer", 
    "department": "string",
    "salary": "float"
  },
  "num_rows": 100,
  "description": "Employee database"
}
```

### 🎲 Agent 2: Data Generator (OpenAI GPT-4o-mini)
- **Input**: Schema from Agent 1
- **Process**: Creates realistic synthetic data
- **Output**: Formatted data table with realistic relationships

### 🔄 Agent 3: Format Converter (Python)
- **Input**: Generated data
- **Process**: Converts to desired output format
- **Output**: Clean CSV/JSON ready for download

## 📊 Supported Data Types

FauxFoundry supports a wide variety of data types:

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text data | "John Doe", "Product Name" |
| `integer` | Whole numbers | 25, 1001, -5 |
| `float` | Decimal numbers | 29.99, 3.14159 |
| `boolean` | True/false values | true, false |
| `date` | Date values | "2024-01-15" |
| `email` | Email addresses | "user@example.com" |
| `phone` | Phone numbers | "+1-555-123-4567" |
| `address` | Physical addresses | "123 Main St, City, State" |
| `url` | Web URLs | "https://example.com" |

## 💡 Usage Examples

### E-commerce Dataset
```
"Create a product catalog with product_name, category, price, rating, in_stock status, and seller_name. Generate 50 products."
```

### Employee Records
```
"Generate employee data including employee_id, full_name, department, salary, hire_date, and email. Need 25 records."
```

### Customer Feedback
```
"Create customer reviews with customer_id, product_rating, review_text, purchase_date, and recommendation status. Generate 30 entries."
```

##  Deployment

### Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app" and select your forked repository
   - Set main file path to `app.py`
   - Click "Deploy"

3. **Configure API Keys** (Optional)
   - In your app settings, add secrets:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   OPENAI_API_KEY = "your_openai_api_key"
   ```

### Local Development

For development with custom configuration:

```bash
# Create custom Streamlit config
mkdir .streamlit
cat > .streamlit/config.toml << EOF
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
port = 8501
EOF

# Run with custom config
streamlit run app.py
```

## 🛠️ Configuration

### Environment Variables

Set these environment variables for production:

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

### Customization Options

- **Models**: Easily switch between different AI models
- **Styling**: Customize the UI with CSS modifications
- **Data Types**: Extend support for additional data types
- **Export Formats**: Add new output formats

## 🔧 Advanced Features

### Performance Optimization

- **Caching**: Intelligent caching for improved response times
- **Batch Processing**: Efficient handling of large datasets
- **Error Recovery**: Robust error handling and retry logic

### Security

- **API Key Management**: Secure handling of sensitive credentials
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Built-in protection against abuse

## 🐛 Troubleshooting

### Common Issues

**API Key Errors**
- Verify your API keys are correct and active
- Check your API quotas and billing status

**Generation Failures**
- Simplify complex prompts
- Ensure stable internet connection
- Verify model availability

**Export Issues**
- Check data format consistency
- Verify special character handling

### Debug Mode

Enable debug mode in the application for detailed error information and troubleshooting assistance.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini** for intelligent schema analysis
- **OpenAI** for powerful data generation capabilities
- **Streamlit** for the amazing web framework
- **Community** for feedback and contributions

## 📞 Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/yourusername/fauxfoundry/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/fauxfoundry/discussions)
- **Documentation**: Check our [Wiki](https://github.com/yourusername/fauxfoundry/wiki)

---

<div align="center">
  <p>
    <a href="https://github.com/yourusername/fauxfoundry">⭐ Star this repo</a> •
    <a href="https://github.com/yourusername/fauxfoundry/issues">🐛 Report Bug</a> •
    <a href="https://github.com/yourusername/fauxfoundry/issues">💡 Request Feature</a>
  </p>
</div>
