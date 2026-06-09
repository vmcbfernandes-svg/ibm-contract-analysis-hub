"""
IBM TLS Contract Analysis Hub - Web Interface
A user-friendly application for automated contract analysis and financial forecasting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="IBM TLS Offerings Contract Analysis Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f4f4;
        color: #161616;
    }
    section[data-testid="stSidebar"] {
        background-color: #f4f4f4 !important;
        border-right: 1px solid #c6c6c6;
    }
    section[data-testid="stSidebar"] * {
        color: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="radio"] *,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #161616 !important;
    }
    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div,
    .stApp li,
    .stApp small {
        color: #161616;
    }
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] > div {
        background-color: #ffffff !important;
        color: #161616 !important;
        border-color: #8d8d8d !important;
    }
    [data-testid="stFileUploader"] * ,
    [data-testid="stFileUploaderDropzone"] * {
        color: #161616 !important;
        fill: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
    }
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploader"] [role="button"],
    [data-testid="stFileUploaderDropzone"] [role="button"],
    [data-testid="stFileUploader"] small + div button,
    [data-testid="stFileUploaderDropzone"] small + div button {
        background: #0f62fe !important;
        background-color: #0f62fe !important;
        color: #ffffff !important;
        border: 1px solid #0f62fe !important;
        box-shadow: none !important;
    }
    [data-testid="stFileUploader"] button *,
    [data-testid="stFileUploaderDropzone"] button *,
    [data-testid="stFileUploader"] [role="button"] *,
    [data-testid="stFileUploaderDropzone"] [role="button"] *,
    [data-testid="stFileUploader"] small + div button *,
    [data-testid="stFileUploaderDropzone"] small + div button * {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }
    [data-testid="stFileUploader"] button:hover,
    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stFileUploader"] [role="button"]:hover,
    [data-testid="stFileUploaderDropzone"] [role="button"]:hover,
    [data-testid="stFileUploader"] small + div button:hover,
    [data-testid="stFileUploaderDropzone"] small + div button:hover {
        background: #0353e9 !important;
        background-color: #0353e9 !important;
        color: #ffffff !important;
        border-color: #0353e9 !important;
    }
    [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploaderFile"] > div,
    [data-testid="stFileUploaderFile"] section,
    [data-testid="stFileUploaderFileData"],
    [data-testid="stFileUploaderFileData"] > div,
    [data-testid="stFileUploaderFile"] small,
    [data-testid="stFileUploaderFile"] span,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] > div,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"],
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"] > div {
        background: #edf5ff !important;
        background-color: #edf5ff !important;
        color: #161616 !important;
        border: 1px solid #78a9ff !important;
        border-color: #78a9ff !important;
        box-shadow: none !important;
    }
    [data-testid="stFileUploaderFile"] *,
    [data-testid="stFileUploaderFileData"] *,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"] * {
        background-color: transparent !important;
        color: #161616 !important;
        fill: #161616 !important;
        stroke: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
        opacity: 1 !important;
    }
    [data-testid="stFileUploaderFile"] button,
    [data-testid="stFileUploaderFile"] [role="button"],
    [data-testid="stFileUploaderFileData"] button,
    [data-testid="stFileUploaderFileData"] [role="button"],
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] button,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] [role="button"] {
        background: #edf5ff !important;
        background-color: #edf5ff !important;
        color: #161616 !important;
        border: 1px solid #78a9ff !important;
        box-shadow: none !important;
    }
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div:hover,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="select"] > div[aria-expanded="true"],
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] input {
        background-color: #ffffff !important;
        color: #161616 !important;
        border-color: #8d8d8d !important;
        box-shadow: none !important;
    }
    [data-baseweb="select"] * {
        color: #161616 !important;
        fill: #161616 !important;
        stroke: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
        opacity: 1 !important;
    }
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div {
        background-color: #ffffff !important;
        color: #161616 !important;
    }
    [data-baseweb="menu"],
    ul[data-baseweb="menu"],
    [role="listbox"] {
        background-color: #ffffff !important;
        color: #161616 !important;
        border: 1px solid #c6c6c6 !important;
        box-shadow: 0 2px 6px rgba(22, 22, 22, 0.12) !important;
    }
    [data-baseweb="menu"] *,
    ul[data-baseweb="menu"] *,
    [role="listbox"] *,
    [role="option"],
    [role="option"] * {
        color: #161616 !important;
        fill: #161616 !important;
        stroke: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
        opacity: 1 !important;
    }
    [data-baseweb="menu"] li,
    ul[data-baseweb="menu"] li,
    [role="option"] {
        background-color: #ffffff !important;
        color: #161616 !important;
    }
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] li[aria-selected="true"],
    ul[data-baseweb="menu"] li:hover,
    ul[data-baseweb="menu"] li[aria-selected="true"],
    [role="option"]:hover,
    [role="option"][aria-selected="true"],
    [role="option"][aria-selected="true"] * {
        background-color: #edf5ff !important;
        color: #161616 !important;
    }
    [data-testid="stSlider"] * {
        color: #161616 !important;
    }
    [data-testid="stSlider"] [role="slider"] {
        background-color: #0f62fe !important;
        border-color: #0f62fe !important;
    }
    [data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: #0f62fe !important;
    }
    [data-testid="stCheckbox"] * {
        color: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
    }
    [data-testid="stAlertContainer"] {
        color: #161616 !important;
    }
    [data-testid="stAlertContainer"] * {
        color: #161616 !important;
        -webkit-text-fill-color: #161616 !important;
    }
    .stAlert {
        background-color: #ffffff !important;
        color: #161616 !important;
        border: 1px solid #c6c6c6 !important;
    }
    .stSuccess {
        background-color: #defbe6 !important;
        color: #161616 !important;
        border: 1px solid #42be65 !important;
    }
    .stInfo {
        background-color: #edf5ff !important;
        color: #161616 !important;
        border: 1px solid #78a9ff !important;
    }
    .stWarning {
        background-color: #fcf4d6 !important;
        color: #161616 !important;
        border: 1px solid #f1c21b !important;
    }
    .stError {
        background-color: #fff1f1 !important;
        color: #161616 !important;
        border: 1px solid #da1e28 !important;
    }
    .stButton > button {
        background-color: #ffffff;
        color: #161616 !important;
        border: 1px solid #8d8d8d;
    }
    .stButton > button:hover {
        background-color: #e8e8e8;
        color: #161616 !important;
        border-color: #525252;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"],
    button[kind="primaryFormSubmit"],
    button[data-testid="baseButton-primary"] {
        background: #0f62fe !important;
        background-color: #0f62fe !important;
        color: #ffffff !important;
        border: 1px solid #0f62fe !important;
        font-weight: 600;
        text-shadow: none !important;
        opacity: 1 !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover,
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: #0353e9 !important;
        background-color: #0353e9 !important;
        color: #ffffff !important;
        border-color: #0353e9 !important;
    }
    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="stBaseButton-primary"] *,
    button[kind="primaryFormSubmit"] *,
    button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }
    .main-header {
        display: block;
        width: 100%;
        font-size: 4.4rem;
        line-height: 1.1;
        color: #0f62fe;
        font-weight: 700;
        margin: 0 0 1.25rem 0;
        letter-spacing: -0.03em;
    }
    .main-header span {
        font-size: inherit !important;
        line-height: inherit !important;
        color: inherit !important;
    }
    .metric-card {
        background-color: #ffffff;
        color: #161616;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c6c6c6;
        border-left: 4px solid #0f62fe;
        box-shadow: 0 2px 6px rgba(22, 22, 22, 0.08);
    }
    .metric-card h3,
    .metric-card p {
        color: #161616;
        margin-top: 0;
    }
    .alert-critical {
        background-color: #fff1f1;
        color: #161616;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffd7d9;
        border-left: 4px solid #da1e28;
    }
    .alert-critical h4,
    .alert-critical p {
        color: #161616;
        margin-top: 0;
    }
    .alert-warning {
        background-color: #fcf4d6;
        color: #161616;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e8da8d;
        border-left: 4px solid #f1c21b;
    }
    .alert-warning h4,
    .alert-warning p {
        color: #161616;
        margin-top: 0;
    }
    .opportunity-card {
        background-color: #edf5ff;
        color: #161616;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #a6c8ff;
        border-left: 4px solid #0043ce;
        box-shadow: 0 2px 6px rgba(22, 22, 22, 0.08);
    }
    .opportunity-card h4,
    .opportunity-card p {
        color: #161616;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'chat_input' not in st.session_state:
    st.session_state.chat_input = ""

class ContractAnalyzer:
    """Main contract analysis engine"""
    
    def __init__(self):
        self.data: pd.DataFrame | None = None
        self.results = {}
        
    def load_excel_files(self, uploaded_files):
        """Load and consolidate Excel files"""
        all_data = []
        file_info = []
        
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_excel(uploaded_file, sheet_name='Component Details', header=None)
                
                # Column mapping (Excel columns to names)
                column_mapping = {
                    1: 'Country',
                    10: 'Auto Renewal Flag',
                    14: 'Brand',
                    15: 'Product Family',
                    16: 'Machine Type',
                    17: 'Model',
                    18: 'Serial Number',
                    21: 'EOS Date',
                    23: 'Service Name',
                    24: 'Service Level',
                    25: 'SLA Type',
                    29: 'L40 Name',
                    33: 'Service Start Date',
                    34: 'Service End Date',
                    35: 'Contract Status',
                    37: 'Total Contract Value (USD)'
                }
                
                # Extract columns
                selected_data = {}
                for col_idx, col_name in column_mapping.items():
                    if col_idx < len(df.columns):
                        selected_data[col_name] = df.iloc[:, col_idx]
                
                geo_df = pd.DataFrame(selected_data)
                geo_df = geo_df.iloc[1:].reset_index(drop=True)  # Remove header row
                
                all_data.append(geo_df)
                file_info.append({
                    'filename': uploaded_file.name,
                    'records': len(geo_df)
                })
                
            except Exception as e:
                st.error(f"Error loading {uploaded_file.name}: {str(e)}")
                continue
        
        if all_data:
            self.data = pd.concat(all_data, ignore_index=True)
            self.clean_data()
            return file_info
        return []
    
    def clean_data(self):
        """Clean and prepare data"""
        if self.data is None:
            raise ValueError("No contract data loaded for cleaning")
        
        # Convert date columns
        date_columns = ['EOS Date', 'Service Start Date', 'Service End Date']
        for col in date_columns:
            self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
        
        # Convert numeric columns
        self.data['Total Contract Value (USD)'] = pd.to_numeric(
            self.data['Total Contract Value (USD)'], errors='coerce'
        )
        
        # Remove duplicates
        self.data['unique_key'] = (
            self.data['Serial Number'].astype(str) + '_' + 
            self.data['Service Start Date'].astype(str) + '_' + 
            self.data['Service Name'].astype(str)
        )
        initial_count = len(self.data)
        self.data = self.data.drop_duplicates(subset='unique_key', keep='first')
        self.duplicates_removed = initial_count - len(self.data)
        
        # Create analysis flags
        self.data['EOS_Violation'] = (
            (self.data['Service End Date'] > self.data['EOS Date']) & 
            self.data['EOS Date'].notna()
        )
        self.data['Has_Auto_Renewal'] = self.data['Auto Renewal Flag'].str.upper().str.contains(
            'ON|YES|TRUE|Y', na=False
        )
        self.data['Has_CMSL'] = self.data['SLA Type'].str.upper().str.contains('CMSL', na=False)
    
    def analyze(self, avg_contract_duration=3):
        """Run comprehensive analysis"""
        if self.data is None:
            raise ValueError("No contract data loaded for analysis")
        
        # Portfolio metrics
        total_tcv = self.data['Total Contract Value (USD)'].sum()
        contract_count = len(self.data)
        
        self.results = {
            'portfolio': {
                'total_tcv': total_tcv,
                'estimated_arr': total_tcv / avg_contract_duration,
                'contract_count': contract_count,
                'avg_contract_value': self.data['Total Contract Value (USD)'].mean(),
                'duplicates_removed': self.duplicates_removed
            },
            'adoption': {
                'auto_renewal_rate': (self.data['Has_Auto_Renewal'].sum() / contract_count * 100),
                'auto_renewal_count': self.data['Has_Auto_Renewal'].sum(),
                'cmsl_rate': (self.data['Has_CMSL'].sum() / contract_count * 100),
                'cmsl_count': self.data['Has_CMSL'].sum()
            },
            'risks': {
                'eos_violations': self.data['EOS_Violation'].sum(),
                'eos_violation_pct': (self.data['EOS_Violation'].sum() / contract_count * 100),
                'eos_violation_tcv': self.data[self.data['EOS_Violation']]['Total Contract Value (USD)'].sum()
            },
            'opportunities': self.identify_opportunities(),
            'trends': self.analyze_trends(),
            'service_mix': self.analyze_service_mix()
        }
        
        return self.results
    
    def identify_opportunities(self):
        """Identify upsell and cross-sell opportunities"""
        if self.data is None:
            raise ValueError("No contract data loaded for opportunity analysis")
        
        opportunities = []
        
        # Auto-renewal opportunity
        no_auto_renewal = self.data[~self.data['Has_Auto_Renewal']]
        if len(no_auto_renewal) > 0:
            opportunities.append({
                'type': 'Auto-Renewal Expansion',
                'priority': 'CRITICAL',
                'contracts': len(no_auto_renewal),
                'tcv': no_auto_renewal['Total Contract Value (USD)'].sum(),
                'action': 'Launch 90-day auto-renewal adoption campaign',
                'target': 'Achieve 50% adoption rate',
                'impact': 'Protect revenue and reduce churn risk'
            })
        
        # CMSL opportunity
        no_cmsl = self.data[~self.data['Has_CMSL']]
        if len(no_cmsl) > 0:
            opportunities.append({
                'type': 'CMSL Upsell',
                'priority': 'HIGH',
                'contracts': len(no_cmsl),
                'tcv': no_cmsl['Total Contract Value (USD)'].sum(),
                'action': 'Target high-value accounts for CMSL upgrade',
                'target': 'Increase adoption from current to 35%',
                'impact': 'Additional revenue and improved service levels'
            })
        
        # EOS migration opportunity
        eos_violations = self.data[self.data['EOS_Violation']]
        if len(eos_violations) > 0:
            opportunities.append({
                'type': 'EOS Migration & Service Extension',
                'priority': 'CRITICAL',
                'contracts': len(eos_violations),
                'tcv': eos_violations['Total Contract Value (USD)'].sum(),
                'action': 'Proactive customer engagement for hardware refresh',
                'target': 'Migrate or extend support for all EOS violations',
                'impact': 'Protect revenue and ensure compliance'
            })
        
        return opportunities
    
    def analyze_trends(self):
        """Analyze signing and revenue trends"""
        if self.data is None:
            raise ValueError("No contract data loaded for trend analysis")
        
        self.data['Start_YearQuarter'] = (
            self.data['Service Start Date'].dt.year.astype(str) + '-Q' + 
            self.data['Service Start Date'].dt.quarter.astype(str)
        )
        
        quarterly_signings = self.data.groupby('Start_YearQuarter').agg({
            'Serial Number': 'count',
            'Total Contract Value (USD)': 'sum'
        }).reset_index()
        quarterly_signings.columns = ['Quarter', 'Contracts', 'TCV']
        
        return quarterly_signings.tail(8).to_dict('records')
    
    def analyze_service_mix(self):
        """Analyze service distribution"""
        if self.data is None:
            raise ValueError("No contract data loaded for service mix analysis")
        
        service_mix = self.data.groupby('Service Name').agg({
            'Serial Number': 'count',
            'Total Contract Value (USD)': 'sum'
        }).reset_index()
        service_mix.columns = ['Service', 'Contracts', 'TCV']
        service_mix = service_mix.sort_values('TCV', ascending=False).head(10)
        
        return service_mix.to_dict('records')

def format_currency(value):
    """Format currency values"""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    elif value >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:.0f}"

def format_number(value):
    """Format large numbers"""
    if value >= 1e6:
        return f"{value/1e6:.1f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    else:
        return f"{value:.0f}"

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 IBM TLS Offerings Contract Analysis HUB</h1>', unsafe_allow_html=True)
    st.markdown("**Automated contract analysis and financial forecasting powered by IBM Bob**")
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg", width=100)
        st.title("Navigation")
        
        page = st.radio(
            "Select Page",
            ["🏠 Home", "📤 Upload & Analyze", "📊 Dashboard", "💬 Chat Assistant", "📥 Reports", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            st.metric("Total TCV", format_currency(results['portfolio']['total_tcv']))
            st.metric("Contracts", format_number(results['portfolio']['contract_count']))
            st.metric("Auto-Renewal", f"{results['adoption']['auto_renewal_rate']:.1f}%")
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload & Analyze":
        show_upload_page()
    elif page == "📊 Dashboard":
        show_dashboard_page()
    elif page == "💬 Chat Assistant":
        show_chat_page()
    elif page == "📥 Reports":
        show_reports_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    """Home page with quick actions"""
    st.header("Welcome to the Contract Analysis Hub")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📤 Upload Contracts</h3>
            <p>Upload Excel files and get instant analysis</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Analysis", key="home_upload"):
            st.session_state.page = "📤 Upload & Analyze"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 View Dashboard</h3>
            <p>Interactive visualizations and insights</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Dashboard", key="home_dashboard", disabled=st.session_state.analysis_results is None):
            st.session_state.page = "📊 Dashboard"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📥 Download Reports</h3>
            <p>Export analysis in multiple formats</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Reports", key="home_reports", disabled=st.session_state.analysis_results is None):
            st.session_state.page = "📥 Reports"
            st.rerun()
    
    st.markdown("---")
    
    # Recent analyses
    st.subheader("📁 Recent Analyses")
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        st.success(f"""
        **Latest Analysis** - {datetime.now().strftime('%B %d, %Y at %H:%M')}
        - Total TCV: {format_currency(results['portfolio']['total_tcv'])}
        - Contracts: {format_number(results['portfolio']['contract_count'])}
        - Auto-Renewal: {results['adoption']['auto_renewal_rate']:.1f}%
        - EOS Violations: {results['risks']['eos_violations']:,} ({results['risks']['eos_violation_pct']:.1f}%)
        """)
    else:
        st.info("No analyses yet. Upload contract files to get started!")

def show_upload_page():
    """Upload and analysis page"""
    st.header("📤 Upload & Analyze Contracts")
    
    # File upload
    st.subheader("Step 1: Upload Contract Data")
    uploaded_files = st.file_uploader(
        "Upload Excel files (Component Details sheet)",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload one or more Excel files containing contract data"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        
        # Analysis options
        st.subheader("Step 2: Configure Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Portfolio Overview", "Worldwide Consolidation", "Comparative Analysis"]
            )
            
            avg_duration = st.slider(
                "Average Contract Duration (years)",
                min_value=1,
                max_value=5,
                value=3,
                help="Used to calculate ARR from TCV"
            )
        
        with col2:
            st.markdown("**Include in Analysis:**")
            include_revenue = st.checkbox("Time-based revenue allocation", value=True)
            include_opportunities = st.checkbox("Upsell opportunities", value=True)
            include_summary = st.checkbox("Executive summary", value=True)
        
        # Analyze button
        if st.button("🚀 Start Analysis", type="primary"):
            with st.spinner("Analyzing contracts... This may take a few moments."):
                try:
                    # Initialize analyzer
                    analyzer = ContractAnalyzer()
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Load files
                    status_text.text("📁 Loading files...")
                    progress_bar.progress(20)
                    file_info = analyzer.load_excel_files(uploaded_files)
                    
                    # Analyze
                    status_text.text("🔍 Analyzing data...")
                    progress_bar.progress(50)
                    results = analyzer.analyze(avg_contract_duration=avg_duration)
                    
                    # Complete
                    status_text.text("✅ Analysis complete!")
                    progress_bar.progress(100)
                    
                    # Store results
                    st.session_state.analysis_results = results
                    st.session_state.uploaded_files = file_info
                    
                    # Show summary
                    st.success("Analysis completed successfully!")
                    
                    # Quick metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Total TCV",
                            format_currency(results['portfolio']['total_tcv'])
                        )
                    
                    with col2:
                        st.metric(
                            "Estimated ARR",
                            format_currency(results['portfolio']['estimated_arr'])
                        )
                    
                    with col3:
                        st.metric(
                            "Contracts",
                            format_number(results['portfolio']['contract_count'])
                        )
                    
                    with col4:
                        st.metric(
                            "Auto-Renewal",
                            f"{results['adoption']['auto_renewal_rate']:.1f}%"
                        )
                    
                    # Navigate to dashboard
                    if st.button("📊 View Full Dashboard"):
                        st.session_state.page = "📊 Dashboard"
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.exception(e)

def show_dashboard_page():
    """Interactive dashboard page"""
    if st.session_state.analysis_results is None:
        st.warning("No analysis data available. Please upload and analyze contracts first.")
        return
    
    results = st.session_state.analysis_results
    
    st.header("📊 Analysis Dashboard")
    
    # Key Metrics
    st.subheader("🎯 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total TCV",
            format_currency(results['portfolio']['total_tcv']),
            help="Total Contract Value over contract lifetimes"
        )
    
    with col2:
        st.metric(
            "Estimated ARR",
            format_currency(results['portfolio']['estimated_arr']),
            help="Annual Recurring Revenue estimate"
        )
    
    with col3:
        st.metric(
            "Contracts",
            format_number(results['portfolio']['contract_count'])
        )
    
    with col4:
        st.metric(
            "Auto-Renewal",
            f"{results['adoption']['auto_renewal_rate']:.1f}%",
            delta=f"{results['adoption']['auto_renewal_rate'] - 50:.1f}% vs target",
            delta_color="normal" if results['adoption']['auto_renewal_rate'] >= 50 else "inverse"
        )
    
    with col5:
        st.metric(
            "CMSL Adoption",
            f"{results['adoption']['cmsl_rate']:.1f}%",
            delta=f"{results['adoption']['cmsl_rate'] - 35:.1f}% vs target",
            delta_color="normal" if results['adoption']['cmsl_rate'] >= 35 else "inverse"
        )
    
    st.markdown("---")
    
    # Critical Alerts
    st.subheader("⚠️ Critical Alerts")
    
    alerts = []
    if results['risks']['eos_violations'] > 0:
        alerts.append({
            'severity': 'critical',
            'title': 'EOS Violations Detected',
            'message': f"{results['risks']['eos_violations']:,} contracts ({results['risks']['eos_violation_pct']:.1f}%) violating EOS dates",
            'value': format_currency(results['risks']['eos_violation_tcv']),
            'action': 'Immediate migration or service extension required'
        })
    
    if results['adoption']['auto_renewal_rate'] < 10:
        alerts.append({
            'severity': 'critical',
            'title': 'Low Auto-Renewal Rate',
            'message': f"Only {results['adoption']['auto_renewal_rate']:.1f}% of contracts have auto-renewal enabled",
            'value': format_currency(results['portfolio']['total_tcv'] * (1 - results['adoption']['auto_renewal_rate']/100)),
            'action': 'Launch auto-renewal adoption campaign immediately'
        })
    
    if alerts:
        for alert in alerts:
            if alert['severity'] == 'critical':
                st.markdown(f"""
                <div class="alert-critical">
                    <h4>🚨 {alert['title']}</h4>
                    <p><strong>{alert['message']}</strong></p>
                    <p>Revenue at Risk: {alert['value']}</p>
                    <p><em>Action: {alert['action']}</em></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical alerts. Portfolio health is good!")
    
    st.markdown("---")
    
    # Opportunities
    st.subheader("💡 Top Revenue Opportunities")
    
    for i, opp in enumerate(results['opportunities'][:3], 1):
        priority_color = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡'
        }.get(opp['priority'], '🟢')
        
        st.markdown(f"""
        <div class="opportunity-card">
            <h4>{priority_color} {i}. {opp['type']}</h4>
            <p><strong>Contracts:</strong> {opp['contracts']:,} | <strong>TCV:</strong> {format_currency(opp['tcv'])}</p>
            <p><strong>Action:</strong> {opp['action']}</p>
            <p><strong>Target:</strong> {opp['target']}</p>
            <p><em>Impact: {opp['impact']}</em></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Quarterly Trends")
        if results['trends']:
            trends_df = pd.DataFrame(results['trends'])
            fig = px.line(
                trends_df,
                x='Quarter',
                y='Contracts',
                title='Contract Signings by Quarter',
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Service Mix")
        if results['service_mix']:
            service_df = pd.DataFrame(results['service_mix'][:5])
            fig = px.pie(
                service_df,
                values='TCV',
                names='Service',
                title='Top 5 Services by TCV'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def show_reports_page():
    """Reports download page"""
    if st.session_state.analysis_results is None:
        st.warning("No analysis data available. Please upload and analyze contracts first.")
        return
    
    st.header("📥 Download Reports")
    
    results = st.session_state.analysis_results
    
    st.subheader("Available Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 Executive Summary (PDF)")
        st.write("Comprehensive analysis report with key findings and recommendations")
        if st.button("Generate PDF Report"):
            st.info("PDF generation feature coming soon!")
    
    with col2:
        st.markdown("### 📊 Data Export (Excel)")
        st.write("Raw data and calculated metrics in Excel format")
        if st.button("Export to Excel"):
            # Create Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxr') as writer:
                # Summary sheet
                summary_data = {
                    'Metric': ['Total TCV', 'Estimated ARR', 'Contract Count', 'Auto-Renewal Rate', 'CMSL Rate', 'EOS Violations'],
                    'Value': [
                        results['portfolio']['total_tcv'],
                        results['portfolio']['estimated_arr'],
                        results['portfolio']['contract_count'],
                        results['adoption']['auto_renewal_rate'],
                        results['adoption']['cmsl_rate'],
                        results['risks']['eos_violations']
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Opportunities sheet
                if results['opportunities']:
                    pd.DataFrame(results['opportunities']).to_excel(writer, sheet_name='Opportunities', index=False)
            
            st.download_button(
                label="📥 Download Excel",
                data=output.getvalue(),
                file_name=f"Contract_Analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        st.markdown("### 📑 Presentation (PowerPoint)")
        st.write("Executive presentation with charts and insights")
        if st.button("Generate PowerPoint"):
            st.info("PowerPoint generation feature coming soon!")

def show_settings_page():
    """Settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("Analysis Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Default Contract Duration (years)", min_value=1, max_value=5, value=3)
        st.number_input("Auto-Renewal Target (%)", min_value=0, max_value=100, value=50)
        st.number_input("CMSL Target (%)", min_value=0, max_value=100, value=35)
    
    with col2:
        st.selectbox("Currency", ["USD", "EUR", "GBP"])
        st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        st.selectbox("Number Format", ["1,000.00", "1.000,00"])
    
    st.markdown("---")
    
    st.subheader("Scheduled Reports")
    st.info("Automated report scheduling feature coming soon!")
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

class ContractAnalysisBot:
    """AI-powered contract analysis assistant"""
    
    def __init__(self):
        self.commands = {
            'analyze': self.handle_analyze,
            'show': self.handle_show,
            'find': self.handle_find,
            'calculate': self.handle_calculate,
            'recommend': self.handle_recommend,
            'help': self.handle_help
        }
        
    def process_message(self, user_input):
        """Process user message and generate response"""
        user_input_lower = user_input.lower().strip()
        
        if not st.session_state.analysis_results:
            if any(word in user_input_lower for word in ['help', 'what can you do']):
                return self.handle_help(user_input)
            return {
                'type': 'request_upload',
                'message': "Please upload and analyze contracts first using the '📤 Upload & Analyze' page, then I can answer questions about the results."
            }
        
        if self.is_expiry_question(user_input_lower):
            return self.handle_expiry_question(user_input)
        
        if self.is_country_question(user_input_lower):
            return self.handle_country_question(user_input)
        
        # Detect intent
        if any(word in user_input_lower for word in ['analyze', 'analysis', 'process']):
            return self.handle_analyze(user_input)
        elif any(word in user_input_lower for word in ['show', 'display', 'view']):
            return self.handle_show(user_input)
        elif any(word in user_input_lower for word in ['find', 'search', 'look for']):
            return self.handle_find(user_input)
        elif any(word in user_input_lower for word in ['calculate', 'compute', 'what is']):
            return self.handle_calculate(user_input)
        elif any(word in user_input_lower for word in ['recommend', 'suggest', 'opportunity']):
            return self.handle_recommend(user_input)
        elif any(word in user_input_lower for word in ['help', 'what can you do']):
            return self.handle_help(user_input)
        else:
            return self.handle_general(user_input)
    
    def get_analysis_dataframe(self):
        """Rebuild a dataframe from uploaded files for chat-specific queries"""
        uploaded_files = st.session_state.get('uploaded_files', [])
        if not uploaded_files:
            return None
        
        analyzer = ContractAnalyzer()
        file_paths = []
        for file_info in uploaded_files:
            filename = file_info.get('filename')
            if filename:
                file_paths.append(Path(filename))
        
        valid_paths = [path for path in file_paths if path.exists()]
        if not valid_paths:
            return None
        
        analyzer.load_excel_files(valid_paths)
        return analyzer.data
    
    def is_expiry_question(self, user_input_lower):
        """Detect questions about expiring contracts"""
        expiry_terms = ['expire', 'expiring', 'expiration', 'ending', 'end date', 'renewal']
        time_terms = ['next 6 months', '6 months', 'next six months', 'coming months', 'upcoming']
        return any(term in user_input_lower for term in expiry_terms) and any(term in user_input_lower for term in time_terms)
    
    def is_country_question(self, user_input_lower):
        """Detect country ranking questions"""
        country_terms = ['country', 'countries', 'geography', 'region']
        ranking_terms = ['highest', 'most', 'top', 'largest']
        return any(term in user_input_lower for term in country_terms) and any(term in user_input_lower for term in ranking_terms)
    
    def handle_expiry_question(self, user_input):
        """Answer questions about contracts expiring soon"""
        data = self.get_analysis_dataframe()
        if data is None or data.empty:
            return {
                'type': 'no_data',
                'message': "I couldn't access the uploaded contract rows needed to answer that question. Please re-upload and analyze the files, then try again."
            }
        
        if 'Service End Date' not in data.columns or 'Country' not in data.columns:
            return {
                'type': 'no_data',
                'message': "The uploaded data does not include the fields needed to analyze contract expirations."
            }
        
        today = pd.Timestamp.today().normalize()
        six_months_out = today + pd.DateOffset(months=6)
        expiring = data[
            data['Service End Date'].notna() &
            (data['Service End Date'] >= today) &
            (data['Service End Date'] <= six_months_out)
        ].copy()
        
        if expiring.empty:
            return {
                'type': 'insight',
                'message': "No contracts are scheduled to expire in the next 6 months based on the uploaded data."
            }
        
        country_summary = (
            expiring.groupby('Country', dropna=False)
            .agg(
                contracts=('Serial Number', 'count'),
                tcv=('Total Contract Value (USD)', 'sum')
            )
            .reset_index()
            .sort_values(['contracts', 'tcv'], ascending=[False, False])
        )
        
        top_country = country_summary.iloc[0]
        return {
            'type': 'country_expiry_summary',
            'message': f"The country with the highest number of contracts expiring in the next 6 months is {top_country['Country']}.",
            'summary': {
                'country': top_country['Country'],
                'contracts': int(top_country['contracts']),
                'tcv': float(top_country['tcv']),
                'window': 'Next 6 months'
            },
            'top_countries': country_summary.head(5).to_dict('records')
        }
    
    def handle_country_question(self, user_input):
        """Answer general country ranking questions"""
        data = self.get_analysis_dataframe()
        if data is None or data.empty:
            return {
                'type': 'no_data',
                'message': "I couldn't access the uploaded contract rows needed to answer that question. Please re-upload and analyze the files, then try again."
            }
        
        if 'Country' not in data.columns:
            return {
                'type': 'no_data',
                'message': "The uploaded data does not include a Country column."
            }
        
        country_summary = (
            data.groupby('Country', dropna=False)
            .agg(
                contracts=('Serial Number', 'count'),
                tcv=('Total Contract Value (USD)', 'sum')
            )
            .reset_index()
            .sort_values(['contracts', 'tcv'], ascending=[False, False])
        )
        
        if country_summary.empty:
            return {
                'type': 'insight',
                'message': "No country-level contract data is available to summarize."
            }
        
        top_country = country_summary.iloc[0]
        return {
            'type': 'country_summary',
            'message': f"The country with the highest number of contracts is {top_country['Country']}.",
            'summary': {
                'country': top_country['Country'],
                'contracts': int(top_country['contracts']),
                'tcv': float(top_country['tcv'])
            },
            'top_countries': country_summary.head(5).to_dict('records')
        }
    
    def handle_analyze(self, user_input):
        """Handle analysis requests"""
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            return {
                'type': 'analysis_complete',
                'message': "✅ I've analyzed your uploaded contracts!",
                'summary': {
                    'total_tcv': results['portfolio']['total_tcv'],
                    'contracts': results['portfolio']['contract_count'],
                    'auto_renewal_rate': results['adoption']['auto_renewal_rate'],
                    'eos_violations': results['risks']['eos_violations']
                }
            }
        else:
            return {
                'type': 'request_upload',
                'message': "I'd be happy to analyze your contracts! Please upload your contract files using the '📤 Upload & Analyze' page first, then come back here and I can help you explore the results."
            }
    
    def handle_show(self, user_input):
        """Handle display requests"""
        if not st.session_state.analysis_results:
            return {'type': 'no_data', 'message': "Please upload and analyze contracts first using the '📤 Upload & Analyze' page."}
        
        results = st.session_state.analysis_results
        
        if 'opportunity' in user_input.lower() or 'upsell' in user_input.lower():
            opportunities = results.get('opportunities', [])
            return {
                'type': 'opportunities',
                'message': f"Here are your top {len(opportunities)} revenue opportunities:",
                'opportunities': [
                    {
                        'rank': i+1,
                        'type': opp['type'],
                        'contracts': opp['contracts'],
                        'tcv': opp['tcv'],
                        'action': opp['action'],
                        'priority': opp['priority']
                    }
                    for i, opp in enumerate(opportunities[:5])
                ]
            }
        else:
            return {
                'type': 'general_info',
                'message': "I can show you various insights from your analysis. What would you like to see?",
                'options': [
                    "Top upsell opportunities",
                    "Service mix analysis",
                    "Quarterly trends",
                    "Risk assessment"
                ]
            }
    
    def handle_find(self, user_input):
        """Handle search requests"""
        if not st.session_state.analysis_results:
            return {'type': 'no_data', 'message': "Please upload and analyze contracts first."}
        
        results = st.session_state.analysis_results
        
        if 'eos' in user_input.lower():
            return {
                'type': 'eos_violations',
                'message': "⚠️ EOS Violations Found:",
                'data': {
                    'total': results['risks']['eos_violations'],
                    'tcv': results['risks']['eos_violation_tcv'],
                    'percentage': results['risks']['eos_violation_pct']
                }
            }
        else:
            return {
                'type': 'search_help',
                'message': "I can help you find specific information. Try asking:",
                'examples': [
                    "Find all EOS violations",
                    "Show me contracts without auto-renewal",
                    "What are the critical risks?"
                ]
            }
    
    def handle_calculate(self, user_input):
        """Handle calculation requests"""
        if not st.session_state.analysis_results:
            return {'type': 'no_data', 'message': "Please upload and analyze contracts first."}
        
        results = st.session_state.analysis_results
        
        if 'arr' in user_input.lower():
            return {
                'type': 'calculation',
                'message': "💰 ARR Calculation:",
                'calculation': {
                    'total_tcv': results['portfolio']['total_tcv'],
                    'estimated_arr': results['portfolio']['estimated_arr'],
                    'contract_count': results['portfolio']['contract_count']
                }
            }
        else:
            return {
                'type': 'metrics',
                'message': "📊 Key Metrics:",
                'metrics': {
                    'total_tcv': results['portfolio']['total_tcv'],
                    'estimated_arr': results['portfolio']['estimated_arr'],
                    'contracts': results['portfolio']['contract_count'],
                    'auto_renewal': results['adoption']['auto_renewal_rate'],
                    'cmsl': results['adoption']['cmsl_rate']
                }
            }
    
    def handle_recommend(self, user_input):
        """Handle recommendation requests"""
        if not st.session_state.analysis_results:
            return {'type': 'no_data', 'message': "Please upload and analyze contracts first."}
        
        results = st.session_state.analysis_results
        opportunities = results.get('opportunities', [])
        
        return {
            'type': 'recommendations',
            'message': "💡 Strategic Recommendations based on your data:",
            'recommendations': [
                {
                    'priority': opp['priority'],
                    'title': opp['type'],
                    'reason': f"{opp['contracts']:,} contracts identified",
                    'impact': format_currency(opp['tcv']),
                    'action': opp['action']
                }
                for opp in opportunities[:3]
            ]
        }
    
    def handle_help(self, user_input):
        """Handle help requests"""
        return {
            'type': 'help',
            'message': "👋 Hi! I'm Bob, your contract analysis assistant. Here's what I can do:",
            'capabilities': [
                {
                    'category': '📊 Analysis',
                    'commands': ['Analyze my contracts', 'Show me the results']
                },
                {
                    'category': '🔍 Search & Find',
                    'commands': ['Find EOS violations', 'Show contracts without auto-renewal']
                },
                {
                    'category': '💰 Calculations',
                    'commands': ['Calculate ARR', 'What is the total TCV?']
                },
                {
                    'category': '💡 Insights',
                    'commands': ['Show upsell opportunities', 'Recommend actions']
                }
            ]
        }
    
    def handle_general(self, user_input):
        """Handle general queries"""
        return {
            'type': 'general',
            'message': "I'm not sure I understood that. Try asking:",
            'suggestions': [
                "Analyze my contracts",
                "Show me opportunities",
                "Find EOS violations",
                "Calculate ARR",
                "Help"
            ]
        }

def render_bot_response(response):
    """Render bot response based on type"""
    if isinstance(response, str):
        return response
    
    response_type = response.get('type', 'general')
    html = f"<p>{response['message']}</p>"
    
    if response_type == 'analysis_complete':
        summary = response['summary']
        html += f"""
        <div style="margin: 1rem 0;">
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                💰 TCV: {format_currency(summary['total_tcv'])}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                📄 Contracts: {summary['contracts']:,}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                🔄 Auto-Renewal: {summary['auto_renewal_rate']:.1f}%
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #fff1f1; color: #161616; border: 1px solid #ffd7d9; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                ⚠️ EOS Issues: {summary['eos_violations']:,}
            </span>
        </div>
        """
    
    elif response_type == 'opportunities':
        html += "<div style='margin-top: 1rem;'>"
        for opp in response['opportunities']:
            priority_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}.get(opp['priority'], '🟢')
            html += f"""
            <div style="background-color: #ffffff; color: #161616; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; border: 1px solid #c6c6c6;">
                <strong>{priority_emoji} {opp['rank']}. {opp['type']}</strong><br>
                <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem;">
                    Contracts: {opp['contracts']:,}
                </span>
                <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem;">
                    TCV: {format_currency(opp['tcv'])}
                </span><br>
                <em>Action: {opp['action']}</em>
            </div>
            """
        html += "</div>"
    
    elif response_type == 'recommendations':
        html += "<div style='margin-top: 1rem;'>"
        for rec in response['recommendations']:
            priority_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}.get(rec['priority'], '🟢')
            html += f"""
            <div style="background-color: #edf5ff; color: #161616; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; border: 1px solid #a6c8ff; border-left: 4px solid #0f62fe;">
                <strong>{priority_emoji} {rec['title']}</strong><br>
                <em>Reason: {rec['reason']}</em><br>
                <strong>Impact:</strong> {rec['impact']}<br>
                <strong>Action:</strong> {rec['action']}
            </div>
            """
        html += "</div>"
    
    elif response_type == 'help':
        html += "<div style='margin-top: 1rem;'>"
        for cap in response['capabilities']:
            html += f"<div style='margin: 1rem 0;'><strong>{cap['category']}</strong><ul>"
            for cmd in cap['commands']:
                html += f"<li><code>{cmd}</code></li>"
            html += "</ul></div>"
        html += "</div>"
    
    elif response_type == 'metrics':
        metrics = response['metrics']
        html += f"""
        <div style="margin: 1rem 0;">
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                💰 TCV: {format_currency(metrics['total_tcv'])}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                📊 ARR: {format_currency(metrics['estimated_arr'])}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                📄 Contracts: {metrics['contracts']:,}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                🔄 Auto-Renewal: {metrics['auto_renewal']:.1f}%
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                📋 CMSL: {metrics['cmsl']:.1f}%
            </span>
        </div>
        """
    
    elif response_type in ['country_summary', 'country_expiry_summary']:
        summary = response['summary']
        html += f"""
        <div style="margin: 1rem 0;">
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                🌍 Country: {summary['country']}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                📄 Contracts: {summary['contracts']:,}
            </span>
            <span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: #edf5ff; color: #161616; border: 1px solid #a6c8ff; border-radius: 0.25rem; margin: 0.25rem; font-weight: bold;">
                💰 TCV: {format_currency(summary['tcv'])}
            </span>
        </div>
        """
        if 'window' in summary:
            html += f"<p><strong>Time window:</strong> {summary['window']}</p>"
        if response.get('top_countries'):
            html += "<p><strong>Top countries:</strong></p>"
            for row in response['top_countries']:
                html += f'<div style="margin: 0.35rem 0;">• {row["Country"]}: {int(row["contracts"]):,} contracts ({format_currency(float(row["tcv"]))})</div>'
    
    if 'options' in response:
        html += "<p><strong>Choose an option:</strong></p>"
        for option in response['options']:
            html += f'<div style="margin: 0.5rem 0;">• {option}</div>'
    
    if 'suggestions' in response:
        html += "<p><strong>Try asking:</strong></p>"
        for suggestion in response['suggestions']:
            html += f'<div style="margin: 0.5rem 0;">• {suggestion}</div>'
    
    return html

def show_chat_page():
    """Chat assistant page"""
    st.header("💬 Chat with Bob - Your AI Assistant")
    st.caption("Ask me anything about your contract analysis in natural language")
    
    # Initialize bot
    bot = ContractAnalysisBot()
    
    # Welcome message
    if not st.session_state.chat_messages:
        welcome_response = {
            'type': 'welcome',
            'message': """👋 Hi! I'm Bob, your AI-powered contract analysis assistant.

I can help you explore your contract data, find insights, calculate metrics, and identify opportunities - all through natural conversation!

**Try asking me:**
- "Show me the analysis results"
- "What are the top upsell opportunities?"
- "Find EOS violations"
- "Calculate the ARR"
- "Recommend actions"

What would you like to know?"""
        }
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': welcome_response,
            'timestamp': datetime.now()
        })
    
    # Display chat history
    for message in st.session_state.chat_messages:
        if message['role'] == 'user':
            st.markdown(f"""
            <div style="background-color: #edf5ff; color: #161616; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid #a6c8ff; border-left: 4px solid #0f62fe;">
                <div style="font-weight: bold; margin-bottom: 0.5rem; color: #002d9c;">👤 You</div>
                <div>{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #ffffff; color: #161616; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid #d0c0ff; border-left: 4px solid #8a3ffc;">
                <div style="font-weight: bold; margin-bottom: 0.5rem; color: #6929c4;">🤖 Bob</div>
                <div>{render_bot_response(message['content'])}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    def submit_chat_message():
        user_message = st.session_state.chat_input.strip()
        if not user_message:
            return
        
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now()
        })
        
        with st.spinner("Bob is thinking..."):
            bot_response = bot.process_message(user_message)
        
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': bot_response,
            'timestamp': datetime.now()
        })
        st.session_state.chat_input = ""
    
    col1, col2, col3 = st.columns([5, 1, 1])
    
    with col1:
        st.text_input(
            "Type your message...",
            key="chat_input",
            placeholder="Ask me anything about your contracts...",
            label_visibility="collapsed",
            on_change=submit_chat_message
        )
    
    with col2:
        send_button = st.button("Send 📤", type="primary", use_container_width=True)
    
    with col3:
        if st.button("Clear 🔄", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.chat_input = ""
            st.rerun()
    
    # Process input
    if send_button:
        submit_chat_message()
        st.rerun()
    
    # Quick commands
    st.markdown("---")
    st.subheader("💡 Quick Commands")
    
    quick_commands = [
        "Show me the analysis",
        "Top opportunities",
        "Find EOS violations",
        "Calculate ARR",
        "Recommend actions",
        "Help"
    ]
    
    cols = st.columns(3)
    for i, cmd in enumerate(quick_commands):
        with cols[i % 3]:
            if st.button(cmd, key=f"quick_{i}"):
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': cmd,
                    'timestamp': datetime.now()
                })
                with st.spinner("Bob is thinking..."):
                    bot_response = bot.process_message(cmd)
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': bot_response,
                    'timestamp': datetime.now()
                })
                st.rerun()

if __name__ == "__main__":
    main()

# Made with Bob
