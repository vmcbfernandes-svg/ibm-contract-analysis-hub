# IBM TLS Offerings Contract Analysis Hub

A comprehensive web-based application for automated contract analysis and financial forecasting, powered by Streamlit and IBM Bob.

## Features

- 📤 **Upload & Analyze**: Upload Excel contract files for instant automated analysis
- 📊 **Interactive Dashboard**: Visualize portfolio metrics, trends, and insights
- 💬 **AI Chat Assistant**: Ask questions about your data in natural language with Bob
- 📥 **Export Reports**: Download analysis results in Excel format
- ⚙️ **Configurable Settings**: Customize analysis parameters

## Key Metrics Analyzed

- Total Contract Value (TCV)
- Annual Recurring Revenue (ARR)
- Auto-Renewal adoption rates
- CMSL (Comprehensive Maintenance Service Level) adoption
- EOS (End of Service) violations
- Revenue opportunities and upsell potential

## Installation

### Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run contract_analysis_app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **Upload Contract Data**: Navigate to "Upload & Analyze" and upload your Excel files
2. **View Dashboard**: Explore interactive visualizations and key metrics
3. **Chat with Bob**: Ask questions about your analysis in natural language
4. **Download Reports**: Export results to Excel for further analysis

## Data Format

The app expects Excel files with a "Component Details" sheet containing contract information including:
- Country
- Auto Renewal Flag
- Brand, Product Family, Machine Type, Model, Serial Number
- EOS Date
- Service details (Name, Level, SLA Type)
- Contract dates and status
- Total Contract Value (USD)

## Security

- Contract data files (*.xlsx, *.xls, *.csv) are excluded from version control
- Sensitive data should not be committed to the repository
- Use Streamlit secrets for any API keys or credentials

## Deployment

This app can be deployed to:
- Streamlit Community Cloud (recommended)
- Hugging Face Spaces
- IBM Cloud Code Engine
- Any platform supporting Python and Streamlit

## License

IBM Internal Use

## Made with IBM Bob

This application was created with assistance from IBM Bob, your AI-powered development assistant.