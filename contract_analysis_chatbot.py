"""
IBM TLS Contract Analysis Chatbot - Conversational Assistant
An AI-powered assistant for contract analysis through natural language
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Bob - Contract Analysis Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f4f4;
        color: #161616;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        color: #161616;
    }
    .user-message {
        background-color: #edf5ff;
        border: 1px solid #a6c8ff;
        border-left: 4px solid #0f62fe;
    }
    .bot-message {
        background-color: #ffffff;
        border: 1px solid #d0c0ff;
        border-left: 4px solid #8a3ffc;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #161616;
    }
    .quick-action {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background-color: #0f62fe;
        color: #ffffff;
        border-radius: 0.25rem;
        cursor: pointer;
        text-decoration: none;
    }
    .metric-inline {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        background-color: #edf5ff;
        color: #161616;
        border: 1px solid #a6c8ff;
        border-radius: 0.25rem;
        margin: 0.25rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'context' not in st.session_state:
    st.session_state.context = {
        'last_analysis': None,
        'current_files': [],
        'user_preferences': {}
    }

class ContractAnalysisBot:
    """AI-powered contract analysis assistant"""
    
    def __init__(self):
        self.commands = {
            'analyze': self.handle_analyze,
            'show': self.handle_show,
            'compare': self.handle_compare,
            'find': self.handle_find,
            'calculate': self.handle_calculate,
            'recommend': self.handle_recommend,
            'help': self.handle_help
        }
        
    def process_message(self, user_input):
        """Process user message and generate response"""
        user_input_lower = user_input.lower()
        
        # Detect intent
        if any(word in user_input_lower for word in ['analyze', 'analysis', 'process']):
            return self.handle_analyze(user_input)
        elif any(word in user_input_lower for word in ['show', 'display', 'view']):
            return self.handle_show(user_input)
        elif any(word in user_input_lower for word in ['compare', 'comparison', 'vs']):
            return self.handle_compare(user_input)
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
    
    def handle_analyze(self, user_input):
        """Handle analysis requests"""
        # Check if files are available
        if not st.session_state.context['current_files']:
            return {
                'type': 'request_files',
                'message': "I'd be happy to analyze your contracts! I can see you have contract files in your workspace. Would you like me to:",
                'options': [
                    "Analyze all HWMA files (5 geographies)",
                    "Analyze GTMS contracts",
                    "Analyze Expert Care contracts",
                    "Let me select specific files"
                ]
            }
        
        # Simulate analysis
        return {
            'type': 'analysis_complete',
            'message': "✅ Analysis complete! I've processed your contract data.",
            'summary': {
                'total_tcv': 5720000000,
                'contracts': 397860,
                'auto_renewal_rate': 6.6,
                'eos_violations': 28159
            },
            'next_actions': [
                "Show detailed breakdown by geography",
                "Identify top upsell opportunities",
                "Generate executive presentation",
                "Create action plan for EOS violations"
            ]
        }
    
    def handle_show(self, user_input):
        """Handle display requests"""
        if 'opportunity' in user_input.lower() or 'upsell' in user_input.lower():
            return {
                'type': 'opportunities',
                'message': "Here are your top 5 revenue opportunities:",
                'opportunities': [
                    {
                        'rank': 1,
                        'type': 'Auto-Renewal Campaign',
                        'contracts': 371601,
                        'tcv': 5400000000,
                        'action': 'Launch 90-day adoption campaign',
                        'priority': 'CRITICAL'
                    },
                    {
                        'rank': 2,
                        'type': 'CMSL Upsell',
                        'contracts': 340569,
                        'tcv': 800000000,
                        'action': 'Target high-value accounts',
                        'priority': 'HIGH'
                    },
                    {
                        'rank': 3,
                        'type': 'EOS Migration',
                        'contracts': 28159,
                        'tcv': 215000000,
                        'action': 'Proactive customer engagement',
                        'priority': 'CRITICAL'
                    }
                ]
            }
        elif 'geography' in user_input.lower() or 'geo' in user_input.lower():
            return {
                'type': 'geographic_breakdown',
                'message': "Here's the geographic distribution:",
                'data': [
                    {'geo': 'Europe', 'contracts': 157987, 'tcv': 2653928685, 'pct': 39.7},
                    {'geo': 'NA', 'contracts': 117120, 'tcv': 1833455711, 'pct': 29.4},
                    {'geo': 'APAC', 'contracts': 91255, 'tcv': 553928685, 'pct': 22.9},
                    {'geo': 'LA', 'contracts': 19247, 'tcv': 553789686, 'pct': 4.8},
                    {'geo': 'MEA', 'contracts': 13485, 'tcv': 125874727, 'pct': 3.4}
                ]
            }
        else:
            return {
                'type': 'general_info',
                'message': "I can show you various insights. What would you like to see?",
                'options': [
                    "Top upsell opportunities",
                    "Geographic breakdown",
                    "Service mix analysis",
                    "Quarterly trends",
                    "Risk assessment"
                ]
            }
    
    def handle_compare(self, user_input):
        """Handle comparison requests"""
        return {
            'type': 'comparison',
            'message': "📊 Comparison Analysis:",
            'comparison': {
                'q1_2026': {'contracts': 65739, 'tcv': 164000000},
                'q2_2026': {'contracts': 34892, 'tcv': 87000000},
                'change': {'contracts': -47, 'tcv': -47}
            }
        }
    
    def handle_find(self, user_input):
        """Handle search requests"""
        if 'expiring' in user_input.lower():
            return {
                'type': 'expiring_contracts',
                'message': "🔍 Found contracts expiring in the next 6 months:",
                'data': {
                    'count': 12847,
                    'tcv': 342000000,
                    'breakdown': [
                        {'month': 'July 2026', 'contracts': 2341, 'tcv': 67000000},
                        {'month': 'August 2026', 'contracts': 3156, 'tcv': 89000000},
                        {'month': 'September 2026', 'contracts': 2890, 'tcv': 78000000}
                    ]
                }
            }
        elif 'eos' in user_input.lower():
            return {
                'type': 'eos_violations',
                'message': "⚠️ EOS Violations Found:",
                'data': {
                    'total': 28159,
                    'tcv': 215200000,
                    'by_service': [
                        {'service': 'HWMA Storage', 'count': 15234, 'tcv': 123000000},
                        {'service': 'HWMA Power', 'count': 8765, 'tcv': 67000000},
                        {'service': 'HWMA IBM Z', 'count': 4160, 'tcv': 25200000}
                    ]
                }
            }
        else:
            return {
                'type': 'search_help',
                'message': "I can help you find specific contracts. Try asking:",
                'examples': [
                    "Find contracts expiring in next 6 months",
                    "Find all EOS violations",
                    "Find contracts without auto-renewal",
                    "Find high-value contracts in APAC"
                ]
            }
    
    def handle_calculate(self, user_input):
        """Handle calculation requests"""
        if 'arr' in user_input.lower():
            return {
                'type': 'calculation',
                'message': "💰 ARR Calculation:",
                'calculation': {
                    'total_tcv': 5720000000,
                    'avg_duration': 3,
                    'estimated_arr': 1906666667,
                    'quarterly_revenue': 476666667
                }
            }
        else:
            return {
                'type': 'calculation_help',
                'message': "I can calculate various metrics. What would you like to know?",
                'options': [
                    "Calculate ARR from TCV",
                    "Calculate renewal pipeline value",
                    "Calculate upsell potential",
                    "Calculate revenue at risk"
                ]
            }
    
    def handle_recommend(self, user_input):
        """Handle recommendation requests"""
        return {
            'type': 'recommendations',
            'message': "💡 Strategic Recommendations:",
            'recommendations': [
                {
                    'priority': 'CRITICAL',
                    'title': 'Launch Auto-Renewal Campaign',
                    'reason': 'Only 6.6% adoption rate',
                    'impact': 'Protect $5.4B TCV',
                    'timeline': '90 days',
                    'actions': [
                        'Segment contracts by value and renewal date',
                        'Create targeted outreach programs',
                        'Set up tracking and reporting'
                    ]
                },
                {
                    'priority': 'CRITICAL',
                    'title': 'Address EOS Violations',
                    'reason': '28,159 contracts violating EOS',
                    'impact': 'Protect $215M TCV',
                    'timeline': '60 days',
                    'actions': [
                        'Identify top 100 highest-value violations',
                        'Create immediate action plan',
                        'Engage account teams'
                    ]
                }
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
                    'commands': [
                        'Analyze HWMA contracts',
                        'Analyze contracts for [geography]',
                        'Process all contract files'
                    ]
                },
                {
                    'category': '🔍 Search & Find',
                    'commands': [
                        'Find contracts expiring in [timeframe]',
                        'Find EOS violations',
                        'Find contracts without auto-renewal'
                    ]
                },
                {
                    'category': '💰 Calculations',
                    'commands': [
                        'Calculate ARR',
                        'Calculate renewal pipeline',
                        'What is the total TCV?'
                    ]
                },
                {
                    'category': '💡 Insights',
                    'commands': [
                        'Show upsell opportunities',
                        'Recommend actions',
                        'Compare Q1 vs Q2'
                    ]
                }
            ]
        }
    
    def handle_general(self, user_input):
        """Handle general queries"""
        return {
            'type': 'general',
            'message': "I'm not sure I understood that. Could you rephrase? Or try asking:",
            'suggestions': [
                "Analyze my contracts",
                "Show me opportunities",
                "Find expiring contracts",
                "Help"
            ]
        }

def format_currency(value):
    """Format currency values"""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    else:
        return f"${value:,.0f}"

def render_message(message, is_user=False):
    """Render a chat message"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">👤 You</div>
            <div>{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-header">🤖 Bob</div>
            <div>{render_bot_response(message['content'])}</div>
        </div>
        """, unsafe_allow_html=True)

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
            <span class="metric-inline">💰 TCV: {format_currency(summary['total_tcv'])}</span>
            <span class="metric-inline">📄 Contracts: {summary['contracts']:,}</span>
            <span class="metric-inline">🔄 Auto-Renewal: {summary['auto_renewal_rate']:.1f}%</span>
            <span class="metric-inline">⚠️ EOS Issues: {summary['eos_violations']:,}</span>
        </div>
        <p><strong>What would you like to do next?</strong></p>
        """
        for action in response['next_actions']:
            html += f'<div style="margin: 0.5rem 0;">• {action}</div>'
    
    elif response_type == 'opportunities':
        html += "<div style='margin-top: 1rem;'>"
        for opp in response['opportunities']:
            priority_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}.get(opp['priority'], '🟢')
            html += f"""
            <div style="background-color: #ffffff; color: #161616; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem; border: 1px solid #c6c6c6;">
                <strong>{priority_emoji} {opp['rank']}. {opp['type']}</strong><br>
                <span class="metric-inline">Contracts: {opp['contracts']:,}</span>
                <span class="metric-inline">TCV: {format_currency(opp['tcv'])}</span><br>
                <em>Action: {opp['action']}</em>
            </div>
            """
        html += "</div>"
    
    elif response_type == 'geographic_breakdown':
        html += "<div style='margin-top: 1rem;'>"
        for geo_data in response['data']:
            html += f"""
            <div style="margin: 0.5rem 0;">
                <strong>{geo_data['geo']}</strong>: {geo_data['contracts']:,} contracts | 
                {format_currency(geo_data['tcv'])} | {geo_data['pct']:.1f}%
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
                <strong>Timeline:</strong> {rec['timeline']}<br>
                <strong>Actions:</strong>
                <ul>
            """
            for action in rec['actions']:
                html += f"<li>{action}</li>"
            html += "</ul></div>"
        html += "</div>"
    
    elif response_type == 'help':
        html += "<div style='margin-top: 1rem;'>"
        for cap in response['capabilities']:
            html += f"<div style='margin: 1rem 0;'><strong>{cap['category']}</strong><ul>"
            for cmd in cap['commands']:
                html += f"<li><code>{cmd}</code></li>"
            html += "</ul></div>"
        html += "</div>"
    
    if 'options' in response:
        html += "<p><strong>Choose an option:</strong></p>"
        for option in response['options']:
            html += f'<div style="margin: 0.5rem 0;">• {option}</div>'
    
    return html

def main():
    """Main chatbot interface"""
    
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://www.ibm.com/brand/experience-guides/developer/b1db1ae501d522a1a4b49613fe07c9f1/01_8-bar-positive.svg", width=80)
    with col2:
        st.title("🤖 Bob - Your Contract Analysis Assistant")
        st.caption("Ask me anything about your contracts in natural language")
    
    # Sidebar
    with st.sidebar:
        st.header("💬 Conversation")
        
        if st.button("🔄 New Conversation"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        st.subheader("📁 Available Files")
        files = [
            "Contract Base Reports HWMA NA 02June2026.xlsx",
            "Contract Base Reports HWMA LA 02june2026.xlsx",
            "Contract Base Reports HWMA Europe 02June2026.xlsx",
            "Contract Base Reports HWMA APAC 02June2026.xlsx",
            "Contract Base Reports HWMA MEA 02June2026.xlsx",
            "Contract Base Reports GTMS WW 03June2026.xlsx",
            "Contract Base Reports Expert Care Power Storage 03june2026.xlsx"
        ]
        
        for file in files:
            st.text(f"✅ {file[:30]}...")
        
        st.markdown("---")
        
        st.subheader("💡 Quick Commands")
        quick_commands = [
            "Analyze all contracts",
            "Show opportunities",
            "Find EOS violations",
            "Calculate ARR",
            "Help"
        ]
        
        for cmd in quick_commands:
            if st.button(cmd, key=f"quick_{cmd}"):
                st.session_state.messages.append({
                    'role': 'user',
                    'content': cmd,
                    'timestamp': datetime.now()
                })
                st.rerun()
    
    # Initialize bot
    bot = ContractAnalysisBot()
    
    # Welcome message
    if not st.session_state.messages:
        welcome_response = {
            'type': 'welcome',
            'message': """👋 Hi! I'm Bob, your AI-powered contract analysis assistant. 
            
I can help you analyze contracts, find insights, calculate metrics, and identify opportunities - all through natural conversation!

**Try asking me:**
- "Analyze my HWMA contracts"
- "Show me the top upsell opportunities"
- "Find contracts expiring in the next 6 months"
- "Calculate the ARR"
- "What are the EOS violations?"

What would you like to know?"""
        }
        st.session_state.messages.append({
            'role': 'assistant',
            'content': welcome_response,
            'timestamp': datetime.now()
        })
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            render_message(message, is_user=(message['role'] == 'user'))
    
    # Chat input
    st.markdown("---")
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="Ask me anything about your contracts...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", type="primary", use_container_width=True)
    
    # Process input
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Generate bot response
        bot_response = bot.process_message(user_input)
        
        # Add bot message
        st.session_state.messages.append({
            'role': 'assistant',
            'content': bot_response,
            'timestamp': datetime.now()
        })
        
        # Rerun to update chat
        st.rerun()
    
    # Example queries
    st.markdown("---")
    st.subheader("💭 Example Questions")
    
    examples = [
        "Analyze my HWMA contracts for Q2 2026",
        "Show me the top 5 upsell opportunities",
        "Find all contracts expiring in next 6 months",
        "Calculate ARR assuming 3-year average duration",
        "What are the critical alerts I should know about?",
        "Compare Q1 vs Q2 2026 performance",
        "Recommend actions for EOS violations",
        "Show geographic breakdown"
    ]
    
    cols = st.columns(4)
    for i, example in enumerate(examples):
        with cols[i % 4]:
            if st.button(example, key=f"example_{i}"):
                st.session_state.messages.append({
                    'role': 'user',
                    'content': example,
                    'timestamp': datetime.now()
                })
                st.rerun()

if __name__ == "__main__":
    main()

# Made with Bob
