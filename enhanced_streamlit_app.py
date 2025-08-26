"""
MILO Client Intelligence Dashboard - Enhanced Demo Interface
Streamlit application with query-responsive CrewAI agents
STREAMLIT CLOUD COMPATIBLE VERSION - No Chroma dependencies
"""

import streamlit as st
import time
import json
from datetime import datetime
import pandas as pd
import os
import tempfile

# ── Feature flag: FORCE OFF for Streamlit Cloud ──────────────────────────────
# IMPORTANT: Keep this OFF ("0") for Streamlit Cloud deployment due to SQLite version issues
USE_VECTOR_DB = os.getenv("USE_VECTOR_DB", "0") == "1"

# Only set environment variables if vector DB is actually enabled (which it shouldn't be on Cloud)
if USE_VECTOR_DB:
    st.warning(
        "⚠️ Vector DB is enabled - this may cause SQLite errors on Streamlit Cloud!")
    os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
    os.environ["PERSIST_DIRECTORY"] = os.path.join(
        tempfile.gettempdir(), "chroma_db")
else:
    st.info("✅ Vector DB disabled - using keyword-based analysis for Streamlit Cloud compatibility")

st.set_page_config(
    page_title="MILO Client Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 2rem;
}

.query-focus-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: bold;
    margin: 0.5rem 0;
}

.client-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.agent-working {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    animation: pulse 2s infinite;
}

.agent-complete {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.talking-point {
    background-color: #f8f9fa;
    border-left: 4px solid #007bff;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 0 5px 5px 0;
}

.metric-card {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #e9ecef;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.success-metric {
    color: #28a745;
    font-size: 1.5rem;
    font-weight: bold;
}

.warning-metric {
    color: #ffc107;
    font-size: 1.5rem;
    font-weight: bold;
}

.query-example {
    background-color: #e3f2fd;
    border: 1px solid #bbdefb;
    padding: 0.75rem;
    border-radius: 8px;
    margin: 0.25rem 0;
    cursor: pointer;
    transition: background-color 0.2s;
}

.query-example:hover {
    background-color: #bbdefb;
}

.compatibility-notice {
    background-color: #e8f5e8;
    border: 1px solid #4caf50;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOCAL QUERY PREVIEW FUNCTION (Streamlit Cloud compatible)
# ============================================================================


def analyze_query_preview(query: str) -> dict:
    """Local query preview function - no external dependencies"""

    query_lower = query.lower()

    focus_keywords = {
        "ESG/Sustainability": ["esg", "sustainable", "environmental", "values", "green", "ethical"],
        "Performance": ["performance", "returns", "gains", "profit", "growth", "return"],
        "Family/Personal": ["family", "daughter", "college", "personal", "emma", "linda"],
        "Risk/Volatility": ["risk", "volatility", "concerned", "safe", "conservative"],
        "Communication": ["communication", "contact", "meeting", "updates"],
        "Portfolio": ["portfolio", "allocation", "funds", "holdings"]
    }

    # Find best match
    best_focus = "General"
    max_matches = 0

    for focus, keywords in focus_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in query_lower)
        if matches > max_matches:
            max_matches = matches
            best_focus = focus

    # Determine query type
    if any(word in query_lower for word in ["what", "tell", "show"]):
        query_type = "Informational"
    elif any(word in query_lower for word in ["should", "recommend"]):
        query_type = "Advisory"
    elif any(word in query_lower for word in ["how", "why", "when"]):
        query_type = "Analytical"
    else:
        query_type = "General"

    return {"focus": best_focus, "type": query_type}

# ============================================================================
# ENHANCED MOCK RESULTS GENERATION (Streamlit Cloud compatible)
# ============================================================================


def generate_mock_enhanced_results(query: str, focus: str):
    """Generate comprehensive mock results for demo - no external dependencies"""

    if focus == "ESG/Sustainability":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "ESG expansion discussion - family values alignment with Emma's environmental interests", "relevance": 10},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "VSGX transition planning - successful implementation", "relevance": 10},
                    {"date": "Jan 15, 2024", "type": "Email",
                        "summary": "Initial ESG concerns about VTIAX holdings", "relevance": 9},
                    {"date": "May 22, 2024", "type": "Email",
                        "summary": "VSGX performance tracking vs VTIAX", "relevance": 8}
                ],
                "key_themes": [
                    "Strong family commitment to ESG investing driven by Emma's environmental interests",
                    "Successful VSGX transition with competitive performance vs VTIAX",
                    "Values alignment now as important as return optimization",
                    "Client becoming sophisticated ESG researcher and advocate"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "esg_performance": {
                    "VSGX": {"return": 5.8, "allocation": 15},
                    "transition_impact": "Minimal performance difference vs VTIAX"
                }
            },
            "meeting_prep": {
                "executive_summary": "ESG Integration Success: VSGX performing competitively while achieving family values alignment. Emma's environmental interests driving strong commitment to sustainable investing. Family ready for expanded ESG options including green bonds.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "ESG Success Story",
                        "point": "VSGX performing at 5.8% - values achieved without return sacrifice"},
                    {"priority": 2, "topic": "Family Leadership",
                        "point": "Emma's influence creating authentic investment alignment"},
                    {"priority": 3, "topic": "Expansion Opportunity",
                        "point": "Client research shows readiness for green bonds and expanded ESG"}
                ],
                "action_items": ["Research green bond options for fixed income", "Explore impact investing opportunities", "Schedule ESG-focused family discussion"],
                "conversation_starters": ["Emma must be proud that your investments reflect your family's environmental values..."]
            }
        }

    elif focus == "Performance":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "YTD 7.8% performance review - exceeding IPS targets", "relevance": 10},
                    {"date": "Jun 22, 2024", "type": "Email",
                        "summary": "Fed rate environment performance optimization", "relevance": 8},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "Mid-year 6.8% performance celebration", "relevance": 9},
                    {"date": "May 22, 2024", "type": "Email",
                        "summary": "Strong market performance rebalancing questions", "relevance": 7}
                ],
                "key_themes": [
                    "Consistent satisfaction with risk-adjusted returns",
                    "Growing sophistication in performance analysis and evaluation",
                    "ESG integration achieved without performance sacrifice",
                    "All asset classes contributing positively to returns"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "detailed_performance": {
                    "vs_ips": "Exceeding 7-9% target range",
                    "sharpe_ratio": 0.89,
                    "top_performer": "VGSLX at 15.3% (REITs)",
                    "risk_level": "12.8% volatility - well controlled"
                }
            },
            "meeting_prep": {
                "executive_summary": "Outstanding Performance: Portfolio delivering 8.2% annual return, exceeding IPS targets. All asset classes contributing positively with excellent risk management. ESG transition achieved without performance penalty.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Exceptional Returns",
                        "point": "8.2% return exceeding IPS midpoint of 8% target"},
                    {"priority": 2, "topic": "Risk Management Excellence",
                        "point": "Strong performance with controlled 12.8% volatility"},
                    {"priority": 3, "topic": "Diversification Success",
                        "point": "Every asset class adding value - no weak performers"}
                ],
                "action_items": ["Continue quarterly performance monitoring", "Maintain current allocation strategy", "Prepare detailed attribution analysis"],
                "conversation_starters": ["I'm excited to share your exceptional performance results - you've exceeded every target..."]
            }
        }

    elif focus == "Family/Personal":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "Emma's first joint meeting - family financial team strengthened", "relevance": 10},
                    {"date": "Jul 18, 2024", "type": "Call",
                        "summary": "Northwestern campus visit excitement and planning", "relevance": 9},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "Northwestern acceptance celebration - planning milestone!", "relevance": 10},
                    {"date": "May 22, 2024", "type": "Email",
                        "summary": "Emma's internship insights and financial learning", "relevance": 8}
                ],
                "key_themes": [
                    "Northwestern acceptance - successful long-term planning milestone",
                    "Linda's involvement has strengthened family financial decision-making",
                    "Emma's financial education accelerating through internship experience",
                    "Multi-generational approach to financial planning and values"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "college_funding": {
                    "annual_need": "$35K per year",
                    "funding_status": "On track - 529 plan optimized",
                    "timeline": "Fall 2025 start"
                }
            },
            "meeting_prep": {
                "executive_summary": "Family Milestone Achievement: Northwestern acceptance represents successful long-term planning. College funding secured. Strong family engagement with Linda and Emma both actively involved in financial decisions and learning.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Northwestern Success",
                        "point": "Emma's acceptance represents successful 18-year planning milestone"},
                    {"priority": 2, "topic": "Family Financial Team",
                        "point": "Linda's involvement has strengthened family decision-making process"},
                    {"priority": 3, "topic": "Next Generation Learning",
                        "point": "Emma's internship developing sophisticated financial understanding"}
                ],
                "action_items": ["Finalize Northwestern funding timeline", "Schedule Linda's retirement planning session", "Create family financial education plan"],
                "conversation_starters": ["How are you feeling about Emma starting at Northwestern this fall?"]
            }
        }

    elif focus == "Risk/Volatility":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Feb 28, 2024", "type": "Call",
                        "summary": "Banking sector concerns - reassurance and risk management", "relevance": 10},
                    {"date": "Jun 22, 2024", "type": "Email",
                        "summary": "Fed policy volatility questions and positioning", "relevance": 8},
                    {"date": "Mar 20, 2024", "type": "Email",
                        "summary": "Market volatility and risk tolerance discussion", "relevance": 7}
                ],
                "key_themes": [
                    "Periodic anxiety during market stress periods",
                    "Strong confidence in diversification approach and risk management",
                    "Preference for increased communication during volatile markets"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "risk_metrics": {
                    "volatility": "12.8% - well controlled",
                    "max_drawdown": "-8.2% during stress periods",
                    "sharpe_ratio": "0.89 - excellent risk-adjusted returns"
                }
            },
            "meeting_prep": {
                "executive_summary": "Risk Management Excellence: Portfolio volatility well-controlled at moderate levels. Client comfort maintained through market stress periods with proactive communication and education.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Risk Control Success",
                        "point": "Portfolio volatility maintained at appropriate 12.8% level"},
                    {"priority": 2, "topic": "Downside Protection",
                        "point": "Maximum drawdown limited to -8.2% during stress periods"}
                ],
                "action_items": ["Continue proactive risk monitoring", "Maintain diversification strategy", "Plan communication during volatile periods"],
                "conversation_starters": ["How comfortable have you felt with the portfolio's risk level during recent market stress?"]
            }
        }

    # Default comprehensive response
    return {
        "communications": {
            "total_interactions": 8,
            "focused_timeline": [
                {"date": "Aug 15, 2024", "type": "Meeting",
                    "summary": "Comprehensive family review - all objectives met", "relevance": 9},
                {"date": "Jul 18, 2024", "type": "Call",
                    "summary": "Northwestern planning and performance update", "relevance": 8},
                {"date": "Jun 22, 2024", "type": "Email",
                    "summary": "Fed policy and portfolio positioning questions", "relevance": 7}
            ],
            "key_themes": [
                "Highly engaged family with sophisticated financial discussions",
                "Successful ESG integration with performance goals achievement",
                "Proactive planning and communication for major life milestones"
            ]
        },
        "performance": {
            "portfolio_return": 8.2,
            "ips_compliance": "Fully compliant with all targets"
        },
        "meeting_prep": {
            "executive_summary": "Comprehensive Success: Portfolio performing excellently with strong family engagement and successful values alignment. All planning objectives on track.",
            "targeted_talking_points": [
                {"priority": 1, "topic": "Overall Excellence",
                    "point": "Portfolio and planning objectives being exceeded across all areas"},
                {"priority": 2, "topic": "Family Engagement",
                    "point": "Strong multi-generational involvement in financial decisions"}
            ],
            "action_items": ["Continue current successful strategy", "Schedule next quarterly review", "Monitor ongoing performance"],
            "conversation_starters": ["What aspects of this year's progress are you most proud of?"]
        }
    }

# ============================================================================
# MAIN STREAMLIT APPLICATION
# ============================================================================


def main():
    """Main Streamlit application - Streamlit Cloud compatible"""

    # Header with compatibility notice
    st.markdown('<h1 class="main-header">🤖 MILO Client Intelligence Dashboard</h1>',
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">AI-Powered Query-Responsive Meeting Preparation</p>', unsafe_allow_html=True)

    # Compatibility status
    if not USE_VECTOR_DB:
        st.markdown("""
        <div class="compatibility-notice">
            <strong>✅ Streamlit Cloud Compatible Mode</strong><br>
            Vector database disabled for compatibility. Using enhanced keyword-based analysis with rich sample data.
        </div>
        """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🏦 Client Selection")

        client_name = st.selectbox(
            "Select Client",
            ["Smith Family Trust", "Johnson Investment LLC", "Williams Foundation"],
            index=0
        )

        st.header("📊 Portfolio Overview")

        # Updated portfolio metrics reflecting ESG transition
        portfolio_metrics = {
            "Portfolio Value": "$2.5M",
            "YTD Return": "8.2%",
            "Risk Level": "Moderate",
            "ESG Integration": "15%",
            "Last Review": "Aug 2024"
        }

        for metric, value in portfolio_metrics.items():
            if metric == "YTD Return":
                st.metric(metric, value, "↗ +0.2% vs target")
            elif metric == "ESG Integration":
                st.metric(metric, value, "✅ VSGX Active")
            else:
                st.metric(metric, value)

        st.header("📈 Current Holdings")

        # Updated allocation reflecting ESG transition
        allocation_data = {
            "US Equity (VTSAX)": 40,
            "Intl Equity (VTIAX)": 15,
            "ESG Intl (VSGX)": 15,      # ESG transition
            "Bonds (VBTLX)": 20,
            "REITs (VGSLX)": 5,
            "Intl Bonds (VTABX)": 5
        }

        for asset, percentage in allocation_data.items():
            color = "🌱" if "ESG" in asset else ""
            st.write(f"**{color} {asset}**: {percentage}%")
            st.progress(percentage / 100)

        st.markdown("---")
        st.caption(
            "💡 **Cloud Compatible** - Enhanced keyword analysis with rich sample data")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🎯 Query-Responsive Analysis")

        # Client overview card
        st.markdown(f"""
        <div class="client-card">
            <h3>📋 {client_name}</h3>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <div>
                    <strong>Portfolio Value:</strong> $2.5M<br>
                    <strong>Advisor:</strong> Sarah Johnson<br>
                    <strong>Next Meeting:</strong> Annual Review
                </div>
                <div>
                    <strong>Risk Tolerance:</strong> Moderate<br>
                    <strong>IPS Target:</strong> 7-9% annually<br>
                    <strong>ESG Integration:</strong> Active (VSGX)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Query input section
        st.subheader("❓ Ask MILO Anything About This Client")

        # Enhanced query examples
        st.write("**Try these example queries:**")

        example_queries = [
            "What are the client's ESG concerns and progress?",
            "How has the portfolio performed this year?",
            "What family changes and milestones should I know about?",
            "Are there any risk management or volatility concerns?",
            "What communication preferences does the client have?",
            "What has happened with this account over the past year?"
        ]

        # Initialize session state
        if 'selected_query' not in st.session_state:
            st.session_state.selected_query = "What are the client's ESG concerns and progress?"

        # Create example query buttons
        cols = st.columns(2)
        for i, example in enumerate(example_queries):
            with cols[i % 2]:
                if st.button(f"💭 {example}", key=f"example_{i}", use_container_width=True):
                    st.session_state.selected_query = example
                    st.rerun()

        # Query text area
        query = st.text_area(
            "Your question about the client:",
            value=st.session_state.selected_query,
            height=100,
            help="MILO will analyze communications, performance, and generate meeting prep focused on your specific question.",
            key="query_input"
        )

        # Show query analysis preview
        if query.strip():
            query_preview = analyze_query_preview(query)
            st.markdown(f"""
            <div class="query-focus-badge">
                🎯 Query Focus: {query_preview['focus']} | Type: {query_preview['type']}
            </div>
            """, unsafe_allow_html=True)

        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

        with col_btn1:
            if st.button("🚀 Generate Focused Analysis", type="primary", use_container_width=True):
                if query.strip():
                    run_enhanced_milo_analysis(client_name, query)
                else:
                    st.error("Please enter a question about the client.")

        with col_btn2:
            if st.button("📊 Portfolio View", use_container_width=True):
                show_portfolio_focus()

        with col_btn3:
            if st.button("💬 Communications View", use_container_width=True):
                show_communications_focus()

    with col2:
        st.header("📈 Client Insights")

        # Recent highlights from rich sample data
        st.subheader("🌟 Recent Highlights")

        highlights = [
            {"icon": "🎓", "title": "Northwestern Success",
                "detail": "Emma accepted for Fall 2025"},
            {"icon": "🌱", "title": "ESG Achievement",
                "detail": "VSGX transition successful"},
            {"icon": "👥", "title": "Family Team",
                "detail": "Linda actively engaged"},
            {"icon": "📈", "title": "Strong Performance",
                "detail": "8.2% return exceeding targets"}
        ]

        for highlight in highlights:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 0.75rem; margin: 0.5rem 0; background-color: #f8f9fa; border-radius: 8px;">
                <div style="font-size: 1.5rem; margin-right: 1rem;">{highlight['icon']}</div>
                <div>
                    <strong>{highlight['title']}</strong><br>
                    <small style="color: #666;">{highlight['detail']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📅 Recent Timeline")

        timeline_items = [
            {"date": "Aug 15", "event": "Family Summer Review", "type": "meeting"},
            {"date": "Jul 18", "event": "Northwestern Campus Visit", "type": "call"},
            {"date": "Jun 22", "event": "Fed Policy Discussion", "type": "email"},
            {"date": "May 22", "event": "Summer Internship Update", "type": "email"},
            {"date": "Apr 10", "event": "Mid-Year + Northwestern News!", "type": "meeting"}
        ]

        for item in timeline_items:
            icon = "🤝" if item["type"] == "meeting" else "📞" if item["type"] == "call" else "📧"
            st.markdown(f"""
            <div style="padding: 0.5rem; margin: 0.25rem 0; border-left: 3px solid #007bff; background-color: #f8f9fa;">
                <strong>{item['date']}</strong> {icon}<br>
                <small>{item['event']}</small>
            </div>
            """, unsafe_allow_html=True)


def run_enhanced_milo_analysis(client_name: str, query: str):
    """Execute enhanced MILO analysis - Cloud compatible version"""

    st.markdown("---")
    st.header("🤖 MILO Query-Focused Analysis")

    # Query processing
    query_analysis = analyze_query_preview(query)

    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <strong>🎯 Processing Query:</strong> "{query}"<br>
        <strong>📊 Analysis Focus:</strong> {query_analysis['focus']}<br>
        <strong>🔍 Response Type:</strong> {query_analysis['type']}
    </div>
    """, unsafe_allow_html=True)

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Agent containers
    agent_container1 = st.empty()
    agent_container2 = st.empty()
    agent_container3 = st.empty()
    agent_containers = [agent_container1, agent_container2, agent_container3]

    # Enhanced agent workflow simulation
    agents_info = [
        {
            "name": "Communications Analyst",
            "task": f"Analyzing 8 detailed communications for {query_analysis['focus'].lower()} themes and patterns...",
            "description": f"Processing rich sample data with keyword matching and relevance scoring for {query_analysis['focus'].lower()}"
        },
        {
            "name": "Portfolio Performance Analyst",
            "task": f"Calculating {query_analysis['focus'].lower()}-focused performance metrics with real market data...",
            "description": f"Analyzing portfolio performance with emphasis on {query_analysis['focus'].lower()} aspects"
        },
        {
            "name": "Meeting Preparation Specialist",
            "task": f"Creating {query_analysis['focus'].lower()}-focused talking points and action items...",
            "description": f"Generating targeted meeting materials for {query_analysis['focus'].lower()} discussions"
        }
    ]

    # Execute agent workflow
    for i, agent_info in enumerate(agents_info):
        # Update progress
        progress = (i + 1) / len(agents_info)
        progress_bar.progress(progress)
        status_text.markdown(
            f"**Agent {i+1}/3**: {agent_info['name']} - {query_analysis['focus']} Focus")

        # Show agent working
        agent_containers[i].markdown(f"""
        <div class="agent-working">
            <strong>🔄 {agent_info['name']}</strong><br>
            {agent_info['task']}<br>
            <small><em>{agent_info['description']}</em></small>
        </div>
        """, unsafe_allow_html=True)

        # Realistic processing time
        time.sleep(2.5 + i * 0.5)

        # Show completion
        agent_containers[i].markdown(f"""
        <div class="agent-complete">
            <strong>✅ {agent_info['name']}</strong><br>
            Query-focused analysis complete<br>
            <small><em>Cloud-compatible keyword analysis • Processing time: {2.5 + i * 0.5:.1f}s</em></small>
        </div>
        """, unsafe_allow_html=True)

    progress_bar.progress(1.0)
    status_text.markdown("**✅ Query-Focused Analysis Complete!**")

    # Try real agents first, fall back to enhanced mock
    try:
        # Try to import the fixed agents
        from enhanced_milo_agents import execute_enhanced_milo_analysis
        result = execute_enhanced_milo_analysis(client_name, query)
        st.success("✅ Real agent analysis completed!")

        # Parse and display result if it's structured
        try:
            if isinstance(result, str):
                st.text("Agent Output:")
                st.code(result)
            else:
                st.write("Agent Results:")
                st.write(result)
        except:
            st.text(str(result))

    except ImportError:
        st.info("Using enhanced demo mode with rich sample data")

    except Exception as e:
        st.warning(f"Agent execution error (falling back to demo): {str(e)}")

    # Always show enhanced mock results for demo
    agent_results = generate_mock_enhanced_results(
        query, query_analysis['focus'])
    display_enhanced_milo_results(
        agent_results, client_name, query, query_analysis)


def display_enhanced_milo_results(results: dict, client_name: str, query: str, query_analysis: dict):
    """Display enhanced results - Cloud compatible version"""

    st.markdown("---")
    st.header(f"📊 Query-Focused Analysis Results - {client_name}")

    # Safe data extraction
    perf = results.get("performance", {}) or {}
    comms = results.get("communications", {}) or {}
    meeting = results.get("meeting_prep", {}) or {}
    focus = query_analysis.get("focus", "General")

    # Query response header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
        <h3 style="margin: 0; color: white;">🎯 Response to: "{query}"</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Analysis Focus: {focus} | Enhanced Demo with Rich Sample Data</p>
    </div>
    """, unsafe_allow_html=True)

    # Executive summary
    if meeting and "executive_summary" in meeting:
        st.subheader("📋 Executive Summary")
        st.info(meeting["executive_summary"])

    # Results tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Direct Response", "📞 Communications",
            "📈 Performance", "💬 Talking Points", "✅ Actions"]
    )

    with tab1:
        st.subheader("Direct Response to Your Query")

        if focus == "ESG/Sustainability" and comms:
            st.write("**🌱 ESG Integration Progress:**")
            for theme in comms.get("key_themes", []):
                st.markdown(f"• {theme}")

            if "esg_performance" in perf:
                st.write("**📊 ESG Performance Impact:**")
                esg_perf = perf["esg_performance"]
                st.success(
                    f"VSGX Performance: {esg_perf.get('VSGX', {}).get('return', 5.8)}% annual return")
                st.success(
                    f"Transition Impact: {esg_perf.get('transition_impact', 'Minimal difference')}")

        elif focus == "Performance" and "portfolio_return" in perf:
            st.write("**📈 Performance Highlights:**")
            st.metric("Annual Portfolio Return",
                      f"{perf.get('portfolio_return', 0)}%", "+0.2% vs IPS target")

            if "detailed_performance" in perf:
                dp = perf["detailed_performance"]
                st.metric("Sharpe Ratio", dp.get("sharpe_ratio",
                          "0.89"), "Excellent risk-adjusted returns")
                st.metric("Top Performer", dp.get("top_performer",
                          "VGSLX"), "Outstanding sector performance")

        elif focus == "Family/Personal" and comms:
            st.write("**👨‍👩‍👧 Family Milestones:**")
            timeline = comms.get("focused_timeline", [])[:3]
            for event in timeline:
                relevance_emoji = "🔥" if event.get(
                    "relevance", 5) >= 9 else "⭐"
                st.markdown(
                    f"**{event.get('date', '')}** {relevance_emoji} {event.get('summary', '')}")

        # General overview
        st.write("**📊 Key Metrics:**")
        st.markdown(
            f"- **Portfolio Return:** {perf.get('portfolio_return', 8.2)}% annually\n"
            f"- **Communications Analyzed:** {comms.get('total_interactions', 8)} detailed interactions\n"
            f"- **Analysis Method:** Enhanced keyword matching with relevance scoring\n"
            f"- **Query Focus:** Customized analysis for {focus} topics"
        )

    with tab2:
        st.subheader(f"Communications Analysis - {focus} Focus")
        if comms and "focused_timeline" in comms:
            st.write("**📅 Most Relevant Communications:**")
            for item in comms["focused_timeline"]:
                relevance_score = item.get("relevance", 5)
                stars = "⭐" * min(int(relevance_score / 2), 5)
                st.markdown(f"""
                <div style="padding: 0.75rem; margin: 0.5rem 0; border-left: 3px solid #007bff; background-color: #f8f9fa;">
                    <strong>{item.get('date', '')}</strong> - {item.get('type', '')} {stars}<br>
                    {item.get('summary', '')}
                </div>
                """, unsafe_allow_html=True)

            st.write("**🎯 Key Themes Identified:**")
            for theme in comms.get("key_themes", []):
                st.markdown(f"• {theme}")

    with tab3:
        st.subheader(f"Performance Analysis - {focus} Focus")
        if perf:
            st.metric("Portfolio Return",
                      f"{perf.get('portfolio_return', 0)}%", "+0.2% vs IPS")

            if focus == "ESG/Sustainability" and "esg_performance" in perf:
                esg = perf["esg_performance"].get("VSGX", {})
                st.metric("ESG Fund Performance", f"{esg.get('return', 5.8)}%",
                          f"{esg.get('allocation', 15)}% allocation")
                st.write(
                    f"**Transition Impact:** {perf['esg_performance'].get('transition_impact', 'Minimal difference')}")

            elif "detailed_performance" in perf:
                dp = perf["detailed_performance"]
                st.metric("Risk-Adjusted Returns",
                          f"Sharpe: {dp.get('sharpe_ratio', 0.89)}", "Excellent")
                st.write(
                    f"**Risk Level:** {dp.get('risk_level', '12.8% volatility - well controlled')}")

    with tab4:
        st.subheader(f"Meeting Talking Points - {focus} Focused")
        if meeting and "targeted_talking_points" in meeting:
            st.write("**🎯 Prioritized Discussion Topics:**")
            for point in meeting["targeted_talking_points"]:
                priority = point.get("priority", 1)
                priority_color = "🔴" if priority == 1 else "🟡" if priority == 2 else "🟢"
                topic = point.get("topic", "Discussion Point")
                content = point.get("point", "Talking point content")
                st.markdown(f"""
                <div class="talking-point">
                    {priority_color} <strong>Priority {priority}: {topic}</strong><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)

            if "conversation_starters" in meeting:
                st.write("**💬 Conversation Starters:**")
                for starter in meeting["conversation_starters"]:
                    st.markdown(f"• *\"{starter}\"*")

    with tab5:
        st.subheader(f"Action Items - {focus} Focused")
        if meeting and "action_items" in meeting:
            st.write("**Recommended Actions:**")
            for item in meeting["action_items"]:
                st.checkbox(item, value=False)

        st.markdown("---")

        # Action buttons
        if st.button("📄 Download Analysis Report", use_container_width=True):
            st.success(
                "Query-focused analysis report downloaded! (Demo - would generate PDF)")

        if st.button("📧 Email Summary to Team", use_container_width=True):
            st.success("Targeted summary emailed to advisory team! (Demo)")

        if st.button("🔄 Ask Follow-up Question", use_container_width=True):
            st.info("Ready for your next question about this client!")


def show_portfolio_focus():
    """Portfolio focus view - Cloud compatible"""
    st.markdown("---")
    st.subheader("📈 Portfolio Focus View")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Portfolio Return", "8.2%", "↗ +0.2% vs target")
        st.metric("ESG Integration", "15% (VSGX)", "✅ Active")
        st.metric("Risk Level", "12.8%", "Well controlled")

    with col2:
        st.metric("Sharpe Ratio", "0.89", "Excellent")
        st.metric("IPS Compliance", "✅ Compliant", "All targets met")
        st.metric("Top Performer", "VGSLX", "15.3% return")


def show_communications_focus():
    """Communications focus view - Cloud compatible"""
    st.markdown("---")
    st.subheader("💬 Communications Focus View")

    communications = [
        {"date": "Aug 15", "type": "Meeting",
            "topic": "Family ESG Review", "sentiment": "Collaborative"},
        {"date": "Jul 18", "type": "Call",
            "topic": "Northwestern Visit", "sentiment": "Excited"},
        {"date": "Jun 22", "type": "Email",
            "topic": "Fed Policy Impact", "sentiment": "Analytical"}
    ]

    for comm in communications:
        with st.expander(f"{comm['date']} - {comm['type']}: {comm['topic']} ({comm['sentiment']})"):
            st.write(
                "Rich sample communication data would provide detailed content here.")


if __name__ == "__main__":
    main()
