"""
MILO Client Intelligence Dashboard - Enhanced Demo Interface
Streamlit application with query-responsive CrewAI agents
"""

import streamlit as st
import time
import json
from datetime import datetime
import pandas as pd

# Force Chroma to use sentence-transformers instead of ONNX
# from chromadb.utils import embedding_functions


# Import the enhanced MILO functions - MAKE SURE THESE MATCH YOUR FILE NAMES
# If you saved the enhanced agents as 'enhanced_milo_agents.py', use:
# from enhanced_milo_agents import execute_enhanced_milo_analysis, analyze_query_preview

st.set_page_config(
    page_title="MILO Client Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (enhanced version)
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

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOCAL QUERY PREVIEW FUNCTION (since we can't always import)
# ============================================================================


def analyze_query_preview(query: str) -> dict:
    """Local query preview function with debug info"""

    query_lower = query.lower()
    st.write(f"🔍 **ANALYZING:** '{query_lower}'")

    focus_keywords = {
        "ESG/Sustainability": ["esg", "sustainable", "environmental", "values", "green", "ethical"],
        "Performance": ["performance", "returns", "gains", "profit", "growth", "return"],
        "Family/Personal": ["family", "daughter", "college", "personal", "emma", "linda"],
        "Risk/Volatility": ["risk", "volatility", "concerned", "safe", "conservative"],
        "Communication": ["communication", "contact", "meeting", "updates"],
        "Portfolio": ["portfolio", "allocation", "funds", "holdings"]
    }

    # Find best match with debug info
    best_focus = "General"
    max_matches = 0
    match_details = {}

    for focus, keywords in focus_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in query_lower)
        match_details[focus] = matches
        if matches > max_matches:
            max_matches = matches
            best_focus = focus

    # DEBUG: Show all matches
    st.write("🎯 **KEYWORD MATCHES:**")
    for focus, count in match_details.items():
        st.write(f"  - {focus}: {count} matches")
    st.write(f"**WINNER: {best_focus}** ({max_matches} matches)")

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
# MOCK RESULTS GENERATION (for when agents aren't available)
# ============================================================================


def generate_mock_enhanced_results(query: str, focus: str):
    """Generate mock results for demo when agents aren't available"""

    # DEBUG: Show what we're generating
    st.write(f"🔧 **GENERATING MOCK RESULTS FOR:** {focus}")

    if focus == "ESG/Sustainability":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "ESG expansion discussion - family values alignment", "relevance": 10},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "VSGX transition planning", "relevance": 10},
                    {"date": "Jan 15, 2024", "type": "Email",
                        "summary": "Initial ESG concerns about VTIAX", "relevance": 9}
                ],
                "key_themes": [
                    "Strong family commitment to ESG investing driven by Emma's interests",
                    "Successful VSGX transition with competitive performance",
                    "Values alignment now as important as returns"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "esg_performance": {
                    "VSGX": {"return": 5.8, "allocation": 15},
                    "transition_impact": "Minimal performance difference"
                }
            },
            "meeting_prep": {
                "executive_summary": "ESG Integration Success: VSGX performing competitively while achieving family values alignment. Emma's environmental interests driving strong commitment to sustainable investing.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "ESG Success",
                        "point": "VSGX performing competitively - values achieved without return sacrifice"},
                    {"priority": 2, "topic": "Family Values",
                        "point": "Emma's influence creating meaningful investment alignment"}
                ],
                "action_items": ["Research additional ESG options", "Explore green bonds", "Schedule ESG family discussion"],
                "conversation_starters": ["Emma must be proud that your investments reflect your values..."]
            }
        }

    elif focus == "Performance":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "YTD 7.8% performance review - exceeding targets", "relevance": 10},
                    {"date": "Jun 22, 2024", "type": "Email",
                        "summary": "Rate environment optimization questions", "relevance": 8},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "Strong YTD 6.8% performance celebration", "relevance": 9}
                ],
                "key_themes": [
                    "Consistent satisfaction with risk-adjusted returns",
                    "Growing sophistication in performance analysis",
                    "ESG integration without performance sacrifice",
                    "All asset classes contributing positively"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "detailed_performance": {
                    "vs_ips": "Exceeding midpoint target",
                    "sharpe_ratio": 0.89,
                    "top_performer": "VGSLX at 15.3%"
                }
            },
            "meeting_prep": {
                "executive_summary": "Strong Performance: Portfolio delivering 8.2% return, exceeding IPS targets. All asset classes contributing positively with excellent risk management.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Exceptional Returns",
                        "point": "8.2% return exceeding IPS midpoint target"},
                    {"priority": 2, "topic": "Risk Management",
                        "point": "Strong performance with controlled volatility"},
                    {"priority": 3, "topic": "Diversification Success",
                        "point": "Every asset class adding value to portfolio"}
                ],
                "action_items": ["Continue quarterly monitoring", "Maintain allocation strategy", "Prepare attribution analysis"],
                "conversation_starters": ["I'm excited to share your exceptional performance results..."]
            }
        }

    elif focus == "Family/Personal":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "Linda's first joint meeting - family team strengthened", "relevance": 10},
                    {"date": "Jul 18, 2024", "type": "Call",
                        "summary": "Northwestern campus visit - Emma's excitement", "relevance": 9},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "Northwestern acceptance celebration!", "relevance": 10}
                ],
                "key_themes": [
                    "Northwestern acceptance - successful planning milestone",
                    "Linda's involvement strengthening family decisions",
                    "Emma's financial education accelerating through internship",
                    "Multi-generational approach to financial planning"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "college_funding": {
                    "annual_need": "$35K",
                    "funding_status": "On track"
                }
            },
            "meeting_prep": {
                "executive_summary": "Family Milestone Year: Northwestern acceptance represents successful planning. College funding on track. Strong family engagement in financial decisions.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Northwestern Achievement",
                        "point": "Emma's acceptance represents successful long-term planning"},
                    {"priority": 2, "topic": "Family Team",
                        "point": "Linda's involvement strengthening financial decisions"},
                    {"priority": 3, "topic": "Emma's Growth",
                        "point": "Summer internship developing financial sophistication"}
                ],
                "action_items": ["Finalize college funding timeline", "Plan Linda's retirement projections", "Create family education materials"],
                "conversation_starters": ["How are the Northwestern preparations going?"]
            }
        }

    elif focus == "Risk/Volatility":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Feb 28, 2024", "type": "Call",
                        "summary": "Banking sector concerns - reassurance provided", "relevance": 10},
                    {"date": "Jun 22, 2024", "type": "Email",
                        "summary": "Market volatility questions about positioning", "relevance": 8}
                ],
                "key_themes": [
                    "Periodic anxiety during market stress periods",
                    "Strong confidence in diversification approach",
                    "Preference for more communication during volatility"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "risk_metrics": {
                    "volatility": "12.8%",
                    "max_drawdown": "-8.2%",
                    "sharpe_ratio": "0.89"
                }
            },
            "meeting_prep": {
                "executive_summary": "Risk Management Success: Portfolio volatility well-controlled at moderate levels. Client comfort maintained through market stress periods.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Risk Control",
                        "point": "Portfolio volatility maintained at appropriate 12.8% level"},
                    {"priority": 2, "topic": "Downside Protection",
                        "point": "Maximum drawdown limited to -8.2%"}
                ],
                "action_items": ["Continue risk monitoring", "Maintain diversification", "Plan volatility communication"],
                "conversation_starters": ["How comfortable are you with the current risk level?"]
            }
        }

    # Default general response
    st.write("🔧 **USING DEFAULT/GENERAL RESULTS**")
    return {
        "communications": {
            "total_interactions": 8,
            "key_themes": [
                "Highly engaged family with sophisticated discussions",
                "Successful ESG integration with performance goals",
                "Proactive planning for life milestones"
            ]
        },
        "performance": {
            "portfolio_return": 8.2,
            "ips_compliance": "Fully compliant"
        },
        "meeting_prep": {
            "executive_summary": "Comprehensive success across all planning objectives with strong family engagement and values alignment.",
            "targeted_talking_points": [
                {"priority": 1, "topic": "Overall Success",
                    "point": "Portfolio and planning objectives being met"},
                {"priority": 2, "topic": "Family Engagement",
                    "point": "Strong involvement in financial decisions"}
            ],
            "action_items": ["Continue current strategy", "Schedule next review", "Monitor performance"],
            "conversation_starters": ["What aspects of this year's progress are you most proud of?"]
        }
    }

# ============================================================================
# MAIN STREAMLIT APPLICATION
# ============================================================================


def main():
    """Main Streamlit application"""

    # Header
    st.markdown('<h1 class="main-header">🤖 MILO Client Intelligence Dashboard</h1>',
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">AI-Powered Query-Responsive Meeting Preparation</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🏦 Client Selection")

        client_name = st.selectbox(
            "Select Client",
            ["Smith Family Trust", "Johnson Investment LLC", "Williams Foundation"],
            index=0
        )

        st.header("📊 Portfolio Overview")

        # Mock portfolio data (updated to reflect ESG transition)
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

        # Updated allocation to reflect ESG transition
        allocation_data = {
            "US Equity (VTSAX)": 40,
            "Intl Equity (VTIAX)": 15,  # Reduced
            "ESG Intl (VSGX)": 15,      # New ESG position
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
            "💡 **Enhanced Demo** - Query-responsive agents with rich sample data")

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
                    <strong>ESG Integration:</strong> Active
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Query input section
        st.subheader("❓ Ask MILO Anything About This Client")

        # Query examples with session state management (FIXED - no infinite loop)
        st.write("**Try these example queries:**")

        example_queries = [
            "What are the client's ESG concerns?",
            "How has the portfolio performed this year?",
            "What family changes should I know about?",
            "Are there any risk management issues?",
            "What communication preferences does the client have?",
            "What has happened with this account over the past year?"
        ]

        # Initialize session state for query if it doesn't exist
        if 'selected_query' not in st.session_state:
            st.session_state.selected_query = "What are the client's ESG concerns?"

        # Create columns for example query buttons
        cols = st.columns(2)

        for i, example in enumerate(example_queries):
            with cols[i % 2]:
                if st.button(f"💭 {example}", key=f"example_{i}", use_container_width=True):
                    st.session_state.selected_query = example
                    # REMOVED st.rerun() - this was causing infinite loop!

        # Query text area - always use session state
        query = st.text_area(
            "Your question about the client:",
            value=st.session_state.selected_query,
            height=100,
            help="MILO will analyze communications, performance, and generate meeting prep focused on your specific question.",
            key="query_input"
        )

        # Update session state when user types manually (but don't trigger rerun)
        if query != st.session_state.selected_query:
            st.session_state.selected_query = query

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

        # Recent highlights based on rich data
        st.subheader("🌟 Recent Highlights")

        highlights = [
            {"icon": "🎓", "title": "Northwestern Acceptance",
                "detail": "Emma accepted for Fall 2025"},
            {"icon": "🌱", "title": "ESG Integration",
                "detail": "VSGX transition performing well"},
            {"icon": "👥", "title": "Family Involvement",
                "detail": "Linda actively engaged in planning"},
            {"icon": "📈", "title": "Strong Performance",
                "detail": "8.2% return vs 7-9% target"}
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

        st.subheader("📅 Timeline")

        timeline_items = [
            {"date": "Aug 15", "event": "Summer Review Meeting", "type": "meeting"},
            {"date": "Jul 18", "event": "College Tour Update Call", "type": "call"},
            {"date": "Jun 22", "event": "Fed Rate Decision Email", "type": "email"},
            {"date": "May 22", "event": "Summer Plans Check-in", "type": "email"},
            {"date": "Apr 10", "event": "Mid-Year Review + Northwestern!", "type": "meeting"}
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
    """Execute the enhanced MILO analysis with query responsiveness"""

    st.markdown("---")
    st.header("🤖 MILO Query-Focused Analysis")

    # Show query processing with DEBUG INFO
    query_analysis = analyze_query_preview(query)

    # DEBUG: Show what's actually happening
    st.write("**🐛 DEBUG INFO:**")
    st.write(f"Query received: '{query}'")
    st.write(f"Focus detected: {query_analysis['focus']}")
    st.write(f"Query type: {query_analysis['type']}")

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

    # Enhanced agent workflow
    agents_info = [
        {
            "name": "Communications Analyst",
            "task": f"Filtering communications for {query_analysis['focus'].lower()} themes and analyzing relevant patterns...",
            "description": f"Processing 8 detailed communications, focusing on {query_analysis['focus'].lower()}-related content and themes"
        },
        {
            "name": "Portfolio Performance Analyst",
            "task": f"Calculating {query_analysis['focus'].lower()}-focused performance metrics using real market data...",
            "description": f"Analyzing portfolio with emphasis on {query_analysis['focus'].lower()} aspects, including ESG fund performance"
        },
        {
            "name": "Meeting Preparation Specialist",
            "task": f"Creating {query_analysis['focus'].lower()}-focused talking points and targeted action items...",
            "description": f"Generating meeting materials specifically designed to address {query_analysis['focus'].lower()} concerns"
        }
    ]

    # Execute enhanced agent workflow
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

        # Simulate processing with realistic timing
        # Longer processing for more complex analysis
        time.sleep(2.5 + i * 0.5)

        # Show completion
        agent_containers[i].markdown(f"""
        <div class="agent-complete">
            <strong>✅ {agent_info['name']}</strong><br>
            Query-focused analysis complete<br>
            <small><em>Processed with {query_analysis['focus']} focus • Processing time: {2.5 + i * 0.5:.1f}s</em></small>
        </div>
        """, unsafe_allow_html=True)

    progress_bar.progress(1.0)
    status_text.markdown(
        "**✅ Query-Focused Analysis Complete!** All agents have processed your specific question.")

    # Try to use real agents, fall back to mock data
    try:
        # Attempt to import and use the real enhanced agents
        from enhanced_milo_agents import execute_enhanced_milo_analysis
        result = execute_enhanced_milo_analysis(client_name, query)

        # If we get a result, display it (this would need custom parsing)
        st.success("✅ Real agent analysis completed!")
        st.text("Agent results:")
        st.text(str(result))

    except ImportError:
        st.info("Using demo mode with mock results (enhanced agents not imported)")

        # Generate and display mock results
        agent_results = generate_mock_enhanced_results(
            query, query_analysis['focus'])
        display_enhanced_milo_results(
            agent_results, client_name, query, query_analysis)

    except Exception as e:
        st.warning(f"Agent execution error: {str(e)}")
        st.info("Falling back to demo mode with mock results")

        # Generate and display mock results
        agent_results = generate_mock_enhanced_results(
            query, query_analysis['focus'])
        display_enhanced_milo_results(
            agent_results, client_name, query, query_analysis)


def display_enhanced_milo_results(results: dict, client_name: str, query: str, query_analysis: dict):
    """Display enhanced MILO results with query focus (no nested columns)"""

    st.markdown("---")
    st.header(f"📊 Query-Focused Analysis Results - {client_name}")

    # Safe helpers
    perf = results.get("performance", {}) or {}
    comms = results.get("communications", {}) or {}
    meeting = results.get("meeting_prep", {}) or {}
    focus = query_analysis.get("focus", "General")

    # Query response header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
        <h3 style="margin: 0; color: white;">🎯 Response to: "{query}"</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Analysis Focus: {focus} | Response Type: {query_analysis.get('type','General')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Executive summary
    if meeting:
        st.subheader("📋 Executive Summary")
        st.info(meeting.get("executive_summary", "Summary unavailable."))

    # Tabs (OK to use inside a column; just avoid st.columns within these tabs)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Query Response", "📞 Communications",
            "📈 Performance", "💬 Talking Points", "✅ Actions"]
    )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1 — Direct Response
    # ──────────────────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Direct Response to Your Query")

        if focus == "ESG/Sustainability" and comms:
            st.write("**🌱 ESG Integration Status:**")
            for theme in comms.get("key_themes", []):
                st.markdown(f"• {theme}")

            if "esg_performance" in perf:
                st.write("**📊 ESG Performance Impact:**")
                esg_perf = perf["esg_performance"]
                vsgx = esg_perf.get("VSGX", {})
                transition = esg_perf.get(
                    "transition_impact", "Minimal performance difference")
                st.success(
                    f"VSGX: {vsgx.get('return', 5.8)}% return — {transition}")

        elif focus == "Performance" and "portfolio_return" in perf:
            st.write("**📈 Performance Highlights:**")
            # Stacked metrics (no columns)
            st.metric("Annual Return",
                      f"{perf.get('portfolio_return', 0)}%", "+0.2% vs target")
            if "detailed_performance" in perf:
                dp = perf["detailed_performance"]
                st.metric("Sharpe Ratio", dp.get(
                    "sharpe_ratio", "0.89"), "Excellent")
                st.metric("Top Performer", dp.get(
                    "top_performer", "VGSLX"), "Outstanding")
            else:
                st.metric("IPS Status", "✅", "Compliant")
                st.metric("Risk Level", "Moderate", "12.8%")

        # Family/Personal — NEW independent block (fixes elif-after-else bug)
        if focus == "Family/Personal" and comms:
            st.write("**👨‍👩‍👧 Family Developments:**")
            timeline = comms.get("focused_timeline", [])[:3]
            for event in timeline:
                relevance_color = "🔥" if (
                    event.get("relevance", 5) >= 9) else "⭐"
                st.markdown(
                    f"**{event.get('date','')}** {relevance_color} {event.get('summary','')}")

        # Fallback general overview (shown if none of the above paths wrote details)
        st.write("**📊 Comprehensive Overview:**")
        st.markdown(
            f"- **Portfolio Return:** {perf.get('portfolio_return', 8.2)}% annually\n"
            f"- **Total Communications:** {comms.get('total_interactions', 8)} interactions analyzed\n"
            f"- **Analysis Focus:** Customized for {focus} topics\n"
            f"- **Meeting Readiness:** Complete preparation materials generated"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2 — Communications
    # ──────────────────────────────────────────────────────────────────────────
    with tab2:
        st.subheader(f"Communications Analysis - {focus} Focus")
        if comms:
            if "focused_timeline" in comms:
                st.write("**📅 Most Relevant Communications:**")
                for item in comms.get("focused_timeline", []):
                    relevance_score = item.get("relevance", 5)
                    relevance_stars = "⭐" * min(int(relevance_score / 2), 5)
                    st.markdown(f"""
                    <div style="padding: 0.75rem; margin: 0.5rem 0; border-left: 3px solid #007bff; background-color: #f8f9fa;">
                        <strong>{item.get('date','')}</strong> - {item.get('type','')} {relevance_stars}<br>
                        {item.get('summary','')}
                    </div>
                    """, unsafe_allow_html=True)

            st.write("**🎯 Key Themes Identified:**")
            for theme in comms.get("key_themes", []):
                st.markdown(f"• {theme}")
        else:
            st.info("No communications available for this view.")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3 — Performance
    # ──────────────────────────────────────────────────────────────────────────
    with tab3:
        st.subheader(f"Performance Analysis - {focus} Focus")
        if perf:
            # Key metrics (stacked)
            st.metric("Portfolio Return",
                      f"{perf.get('portfolio_return', 0)}%", "+0.2% vs IPS")

            if focus == "ESG/Sustainability" and "esg_performance" in perf:
                esg = perf["esg_performance"].get("VSGX", {})
                st.metric("ESG Fund (VSGX)", f"{esg.get('return', 5.8)}%",
                          f"{esg.get('allocation', 15)}% allocation")
            else:
                st.metric("Risk Level", "12.8%", "Moderate")

            st.metric("IPS Compliance", "✅", "Fully compliant")

            # Focus-specific detail for ESG
            if focus == "ESG/Sustainability" and "esg_performance" in perf:
                st.write("**🌱 ESG Performance Details:**")
                esg_perf = perf["esg_performance"]
                vsgx = esg_perf.get("VSGX", {})
                st.write(
                    f"• **VSGX Performance:** {vsgx.get('return', 5.8)}% return")
                st.write(
                    f"• **Transition Impact:** {esg_perf.get('transition_impact', 'Minimal performance difference')}")
        else:
            st.info("No performance data available.")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 4 — Talking Points
    # ──────────────────────────────────────────────────────────────────────────
    with tab4:
        st.subheader(f"Meeting Talking Points - {focus} Focused")
        if meeting:
            tps = meeting.get("targeted_talking_points", [])
            if tps:
                st.write("**🎯 Prioritized Discussion Topics:**")
                for point in tps:
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

            starters = meeting.get("conversation_starters", [])
            if starters:
                st.write("**💬 Conversation Starters:**")
                for starter in starters:
                    st.markdown(f"• *\"{starter}\"*")
        else:
            st.info("No meeting prep data available.")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 5 — Actions
    # ──────────────────────────────────────────────────────────────────────────
    with tab5:
        st.subheader(f"Action Items - {focus} Focused")
        if meeting:
            for item in meeting.get("action_items", []):
                st.checkbox(item, value=False)

            st.markdown("---")
            # Stacked buttons (no columns)
            if st.button("📄 Download Report", use_container_width=True):
                st.success(
                    "Query-focused report downloaded! (Demo - would generate PDF)")

            if st.button("📧 Email Summary", use_container_width=True):
                st.success(
                    "Targeted summary emailed! (Demo - would send to advisor)")

            if st.button("🔄 Ask Follow-up", use_container_width=True):
                st.info("Ready for your next query about this client!")
        else:
            st.info("No action items available.")


def show_portfolio_focus():
    """Show portfolio-focused quick analysis"""
    st.markdown("---")
    st.subheader("📈 Portfolio Focus View")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Portfolio Return", "8.2%", "+0.2%")
        st.metric("ESG Integration", "15%", "VSGX Active")
        st.metric("Risk Level", "12.8%", "Moderate")

    with col2:
        st.metric("Sharpe Ratio", "0.89", "Excellent")
        st.metric("Max Drawdown", "-8.2%", "Well controlled")
        st.metric("IPS Compliance", "✅", "Full compliance")


def show_communications_focus():
    """Show communications-focused quick analysis"""
    st.markdown("---")
    st.subheader("💬 Communications Focus View")

    communications = [
        {"date": "Aug 15", "type": "Meeting",
            "topic": "Family Review", "sentiment": "Very Positive"},
        {"date": "Jul 18", "type": "Call",
            "topic": "College Tour", "sentiment": "Excited"},
        {"date": "Jun 22", "type": "Email",
            "topic": "Fed Rates", "sentiment": "Analytical"}
    ]

    for comm in communications:
        with st.expander(f"{comm['date']} - {comm['type']}: {comm['topic']} ({comm['sentiment']})"):
            st.write(
                "Sample communication details would appear here in the full implementation.")


if __name__ == "__main__":
    main()
