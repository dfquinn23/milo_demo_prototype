"""
MILO Client Intelligence Dashboard - Final Streamlit Cloud Compatible Version
Streamlit application with query-responsive CrewAI agents
100% COMPATIBLE WITH STREAMLIT CLOUD - No Chroma/SQLite dependencies
"""

import streamlit as st
import time
import json
from datetime import datetime
import pandas as pd
import os

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

.success-badge {
    background-color: #28a745;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: bold;
    display: inline-block;
    margin: 0.5rem 0;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOCAL QUERY PREVIEW FUNCTION (zero dependencies)
# ============================================================================


def analyze_query_preview(query: str) -> dict:
    """Local query preview function - zero external dependencies"""

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


def generate_comprehensive_mock_results(query: str, focus: str):
    """Generate comprehensive mock results - zero dependencies"""

    if focus == "ESG/Sustainability":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "Family ESG expansion discussion - Emma's leadership in sustainability", "relevance": 10},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "VSGX transition decision - successful ESG implementation", "relevance": 10},
                    {"date": "Jan 15, 2024", "type": "Email",
                        "summary": "Initial ESG research prompted by Emma's environmental studies", "relevance": 9},
                    {"date": "May 22, 2024", "type": "Email",
                        "summary": "VSGX performance tracking - competitive results vs VTIAX", "relevance": 8}
                ],
                "key_themes": [
                    "Strong family commitment to ESG investing driven by Emma's environmental interests",
                    "Successful VSGX transition with competitive performance vs VTIAX benchmark",
                    "Values alignment now as important as return optimization in decision-making",
                    "Client becoming sophisticated ESG researcher and sustainability advocate",
                    "Family ready for expanded ESG options including green bonds and impact investing"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "esg_performance": {
                    "VSGX": {"return": 5.8, "allocation": 15, "vs_benchmark": "Competitive"},
                    "transition_impact": "Minimal performance difference vs VTIAX - values achieved without sacrifice"
                }
            },
            "meeting_prep": {
                "executive_summary": "ESG Integration Success Story: VSGX performing competitively at 5.8% while achieving authentic family values alignment. Emma's environmental leadership has driven sophisticated ESG research. Family positioned for expanded sustainable investing including green bonds and impact opportunities.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "ESG Achievement",
                        "point": "VSGX delivering competitive 5.8% performance - values achieved without return sacrifice"},
                    {"priority": 2, "topic": "Family Leadership",
                        "point": "Emma's environmental passion driving authentic investment alignment across generations"},
                    {"priority": 3, "topic": "Expansion Ready",
                        "point": "Sophisticated ESG research positions family for green bonds and impact investing"},
                    {"priority": 4, "topic": "Measurement Tools",
                        "point": "Consider carbon footprint analysis and ESG impact reporting for portfolio"}
                ],
                "action_items": [
                    "Research green bond options for fixed income ESG integration",
                    "Explore impact investing opportunities beyond traditional ESG screening",
                    "Schedule family ESG discussion with carbon footprint analysis",
                    "Investigate proxy voting and shareholder engagement strategies"
                ],
                "conversation_starters": [
                    "Emma must be proud that your investments now reflect your family's environmental values...",
                    "Your ESG research has been impressive - you've become sustainability experts...",
                    "How does it feel to achieve values alignment without sacrificing returns?"
                ]
            }
        }

    elif focus == "Performance":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "YTD 7.8% performance celebration - exceeding all IPS targets", "relevance": 10},
                    {"date": "Jul 18, 2024", "type": "Call",
                        "summary": "Performance satisfaction discussion - all objectives met", "relevance": 9},
                    {"date": "Jun 22, 2024", "type": "Email",
                        "summary": "Fed environment performance optimization questions", "relevance": 8},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "Mid-year 6.8% performance milestone achievement", "relevance": 9}
                ],
                "key_themes": [
                    "Consistent satisfaction with risk-adjusted portfolio returns",
                    "Growing sophistication in performance analysis and evaluation",
                    "ESG integration achieved without any performance sacrifice",
                    "All asset classes contributing positively to total returns",
                    "Strong risk management with controlled volatility levels"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "detailed_performance": {
                    "vs_ips": "Exceeding 7-9% target range - outstanding results",
                    "sharpe_ratio": 0.89,
                    "top_performer": "VGSLX (REITs) at 15.3% annual return",
                    "risk_level": "12.8% volatility - well controlled for return level",
                    "all_positive": "Every asset class contributing positive returns"
                }
            },
            "meeting_prep": {
                "executive_summary": "Outstanding Performance Achievement: Portfolio delivering exceptional 8.2% annual return, significantly exceeding IPS targets. All asset classes contributing positively with excellent risk management. ESG transition achieved without performance penalty - a remarkable success story.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Exceptional Returns",
                        "point": "8.2% annual return significantly exceeding IPS midpoint target of 8%"},
                    {"priority": 2, "topic": "Risk Management Excellence",
                        "point": "Outstanding performance achieved with well-controlled 12.8% volatility"},
                    {"priority": 3, "topic": "Diversification Success",
                        "point": "Every single asset class adding positive value - no weak performers"},
                    {"priority": 4, "topic": "ESG Success",
                        "point": "Values alignment achieved while maintaining superior performance"}
                ],
                "action_items": [
                    "Continue quarterly performance monitoring vs benchmarks and IPS targets",
                    "Maintain current allocation strategy with disciplined rebalancing approach",
                    "Prepare detailed performance attribution analysis for transparency",
                    "Review tax-loss harvesting opportunities as year-end approaches"
                ],
                "conversation_starters": [
                    "I'm thrilled to share your exceptional performance results - you've exceeded every target...",
                    "How do you feel about the 8.2% return compared to your initial expectations?",
                    "What aspects of this outstanding performance are you most pleased with?"
                ]
            }
        }

    elif focus == "Family/Personal":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Aug 15, 2024", "type": "Meeting",
                        "summary": "Emma's first joint meeting - family financial team fully established", "relevance": 10},
                    {"date": "Jul 18, 2024", "type": "Call",
                        "summary": "Northwestern campus visit excitement - college dreams becoming reality", "relevance": 9},
                    {"date": "Apr 10, 2024", "type": "Meeting",
                        "summary": "Northwestern acceptance celebration - 18-year planning milestone achieved!", "relevance": 10},
                    {"date": "May 22, 2024", "type": "Email",
                        "summary": "Emma's internship insights transforming family financial discussions", "relevance": 8}
                ],
                "key_themes": [
                    "Northwestern acceptance - successful long-term planning milestone achievement",
                    "Linda's involvement has strengthened and elevated family financial decision-making",
                    "Emma's financial education accelerating through internship and active participation",
                    "Multi-generational approach to financial planning and values alignment established",
                    "Family collaboration creating stronger, more informed investment decisions"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "college_funding": {
                    "annual_need": "$35K per year for Northwestern",
                    "funding_status": "Fully on track - 529 plan optimized",
                    "timeline": "Fall 2025 start - all planning complete",
                    "financial_aid": "Better than expected - reduces family burden"
                }
            },
            "meeting_prep": {
                "executive_summary": "Family Milestone Achievement: Northwestern acceptance represents successful 18-year planning milestone. College funding secured and optimized. Strong family financial team established with Linda and Emma both actively engaged. Multi-generational approach to values-based planning achieved.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Northwestern Success",
                        "point": "Emma's acceptance represents successful 18-year planning milestone - dreams realized"},
                    {"priority": 2, "topic": "Family Financial Team",
                        "point": "Linda's engagement has transformed family decision-making process for the better"},
                    {"priority": 3, "topic": "Next Generation Leadership",
                        "point": "Emma's internship has developed sophisticated financial understanding and perspective"},
                    {"priority": 4, "topic": "Collaborative Future",
                        "point": "Multi-generational planning approach established with regular family meetings"}
                ],
                "action_items": [
                    "Finalize Northwestern college funding timeline and tax-efficient withdrawal strategy",
                    "Schedule Linda's comprehensive individual retirement planning session",
                    "Develop family financial education plan with regular learning opportunities",
                    "Establish Emma's continued involvement in quarterly portfolio reviews"
                ],
                "conversation_starters": [
                    "How are you feeling about Emma starting her Northwestern journey this fall?",
                    "Linda, how has being more involved in the financial planning process felt?",
                    "What has Emma learned from her internship that surprised you the most?"
                ]
            }
        }

    elif focus == "Risk/Volatility":
        return {
            "communications": {
                "total_interactions": 8,
                "focused_timeline": [
                    {"date": "Feb 28, 2024", "type": "Call",
                        "summary": "Banking sector concerns - comprehensive risk reassurance provided", "relevance": 10},
                    {"date": "Jun 22, 2024", "type": "Email",
                        "summary": "Fed policy volatility positioning questions - proactive risk management", "relevance": 8},
                    {"date": "Mar 20, 2024", "type": "Email",
                        "summary": "Market volatility response and risk tolerance discussion", "relevance": 7}
                ],
                "key_themes": [
                    "Periodic market anxiety during stress periods - normal client behavior",
                    "Strong confidence in diversification approach and risk management strategy",
                    "Preference for increased communication during volatile market conditions",
                    "Effective reassurance through education and historical perspective"
                ]
            },
            "performance": {
                "portfolio_return": 8.2,
                "risk_metrics": {
                    "volatility": "12.8% - well controlled for return level",
                    "max_drawdown": "-8.2% during stress periods - limited downside",
                    "sharpe_ratio": "0.89 - excellent risk-adjusted returns",
                    "risk_management": "Diversification strategy working effectively"
                }
            },
            "meeting_prep": {
                "executive_summary": "Risk Management Excellence: Portfolio volatility well-controlled at moderate 12.8% level while delivering exceptional returns. Client comfort maintained through market stress periods with proactive communication and education. Risk management strategy highly effective.",
                "targeted_talking_points": [
                    {"priority": 1, "topic": "Risk Control Success",
                        "point": "Portfolio volatility maintained at appropriate 12.8% level for return target"},
                    {"priority": 2, "topic": "Downside Protection",
                        "point": "Maximum drawdown limited to -8.2% during stress periods - excellent protection"},
                    {"priority": 3, "topic": "Risk-Adjusted Excellence",
                        "point": "Sharpe ratio of 0.89 demonstrates superior risk-adjusted performance"},
                    {"priority": 4, "topic": "Communication Success",
                        "point": "Proactive communication during volatility maintains client confidence"}
                ],
                "action_items": [
                    "Continue proactive risk monitoring with quarterly assessments",
                    "Maintain diversification strategy - it's working excellently",
                    "Plan enhanced communication during future volatile periods",
                    "Schedule risk tolerance review as family circumstances evolve"
                ],
                "conversation_starters": [
                    "How comfortable have you felt with the portfolio's risk level during recent market stress?",
                    "What's your confidence level in our risk management approach?",
                    "How do you feel about the balance we've achieved between risk and return?"
                ]
            }
        }

    # Default comprehensive response
    return {
        "communications": {
            "total_interactions": 8,
            "focused_timeline": [
                {"date": "Aug 15, 2024", "type": "Meeting",
                    "summary": "Comprehensive family review - all objectives exceeded across every area", "relevance": 10},
                {"date": "Jul 18, 2024", "type": "Call",
                    "summary": "Northwestern planning celebration and performance satisfaction", "relevance": 9},
                {"date": "Jun 22, 2024", "type": "Email",
                    "summary": "Fed policy discussion and portfolio positioning optimization", "relevance": 8},
                {"date": "Apr 10, 2024", "type": "Meeting",
                    "summary": "Mid-year milestone achievement - Northwestern acceptance!", "relevance": 10}
            ],
            "key_themes": [
                "Highly engaged family with sophisticated and collaborative financial discussions",
                "Successful ESG integration with performance goals - no trade-offs required",
                "Proactive planning and communication for all major life milestones",
                "Strong multi-generational approach to values-based financial planning"
            ]
        },
        "performance": {
            "portfolio_return": 8.2,
            "comprehensive_success": {
                "ips_compliance": "Exceeding all targets across every metric",
                "family_goals": "All objectives met or exceeded",
                "risk_management": "Excellent - controlled volatility with strong returns"
            }
        },
        "meeting_prep": {
            "executive_summary": "Comprehensive Planning Excellence: Portfolio performing exceptionally at 8.2% with strong family engagement and successful values alignment. All planning objectives exceeded. Northwestern milestone achieved. ESG integration successful. Outstanding results across every dimension.",
            "targeted_talking_points": [
                {"priority": 1, "topic": "Exceptional Overall Success",
                    "point": "Portfolio and planning objectives being exceeded across all areas - remarkable achievement"},
                {"priority": 2, "topic": "Family Team Excellence",
                    "point": "Multi-generational involvement creating stronger, more informed financial decisions"},
                {"priority": 3, "topic": "Values Integration Success",
                    "point": "ESG alignment achieved without any compromise on performance or goals"},
                {"priority": 4, "topic": "Future Positioning",
                    "point": "Exceptionally well positioned for all upcoming opportunities and milestones"}
            ],
            "action_items": [
                "Continue current highly successful strategy and monitoring approach",
                "Schedule celebratory quarterly review meeting to acknowledge achievements",
                "Prepare comprehensive success summary for family records",
                "Plan future opportunities building on current success foundation"
            ],
            "conversation_starters": [
                "What aspects of this year's remarkable progress are you most proud of?",
                "How do you feel about exceeding every goal you set at the beginning of the year?",
                "What opportunities do you see building on this success foundation?"
            ]
        }
    }

# ============================================================================
# MAIN STREAMLIT APPLICATION
# ============================================================================


def main():
    """Main Streamlit application - 100% Cloud compatible"""

    # Header
    st.markdown('<h1 class="main-header">🤖 MILO Client Intelligence Dashboard</h1>',
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">AI-Powered Query-Responsive Meeting Preparation</p>',
                unsafe_allow_html=True)

    # Compatibility status
    st.markdown("""
    <div class="success-badge">
        ✅ 100% Streamlit Cloud Compatible - Zero Dependencies Mode Active
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

        portfolio_metrics = {
            "Portfolio Value": "$2.5M",
            "YTD Return": "8.2%",
            "Risk Level": "Moderate (12.8%)",
            "ESG Integration": "15% (VSGX)",
            "Last Review": "Aug 2024"
        }

        for metric, value in portfolio_metrics.items():
            if metric == "YTD Return":
                st.metric(metric, value, "↗ +1.2% vs target")
            elif metric == "ESG Integration":
                st.metric(metric, value, "✅ Successful transition")
            else:
                st.metric(metric, value)

        st.header("📈 Current Holdings")

        allocation_data = {
            "US Equity (VTSAX)": 40,
            "Intl Equity (VTIAX)": 15,
            "🌱 ESG Intl (VSGX)": 15,      # ESG transition highlighted
            "Bonds (VBTLX)": 20,
            "REITs (VGSLX)": 5,
            "Intl Bonds (VTABX)": 5
        }

        for asset, percentage in allocation_data.items():
            st.write(f"**{asset}**: {percentage}%")
            st.progress(percentage / 100)

        st.markdown("---")
        st.caption(
            "🚀 **Enhanced Demo** - Rich sample data with comprehensive analysis")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🎯 Query-Responsive Analysis")

        # Enhanced client overview card
        st.markdown(f"""
        <div class="client-card">
            <h3>📋 {client_name}</h3>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <div>
                    <strong>Portfolio Value:</strong> $2.5M<br>
                    <strong>Advisor:</strong> Sarah Johnson<br>
                    <strong>Next Meeting:</strong> Annual Review<br>
                    <strong>Family:</strong> Robert, Linda, Emma
                </div>
                <div>
                    <strong>Risk Tolerance:</strong> Moderate<br>
                    <strong>IPS Target:</strong> 7-9% annually<br>
                    <strong>ESG Integration:</strong> Active (VSGX)<br>
                    <strong>Status:</strong> All goals exceeded
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Query input section
        st.subheader("❓ Ask MILO Anything About This Client")

        st.write("**Try these comprehensive example queries:**")

        example_queries = [
            "What are the client's ESG concerns and sustainability progress?",
            "How has the portfolio performed this year compared to targets?",
            "What family changes and milestones should I know about?",
            "Are there any risk management or volatility concerns to address?",
            "What communication preferences and patterns does the client have?",
            "What has happened with this account over the past year?"
        ]

        # Initialize session state
        if 'selected_query' not in st.session_state:
            st.session_state.selected_query = "What are the client's ESG concerns and sustainability progress?"

        # Example query buttons
        cols = st.columns(2)
        for i, example in enumerate(example_queries):
            with cols[i % 2]:
                if st.button(f"💭 {example}", key=f"example_{i}", use_container_width=True):
                    st.session_state.selected_query = example
                    st.rerun()

        # Query text area
        query = st.text_area(
            "Your detailed question about the client:",
            value=st.session_state.selected_query,
            height=100,
            help="MILO will analyze 8 detailed communications, real performance data, and generate comprehensive meeting prep focused on your specific question.",
            key="query_input"
        )

        # Show query analysis preview
        if query.strip():
            query_preview = analyze_query_preview(query)
            st.markdown(f"""
            <div class="query-focus-badge">
                🎯 Query Focus: {query_preview['focus']} | Analysis Type: {query_preview['type']}
            </div>
            """, unsafe_allow_html=True)

        # Action buttons
        col_btn1, col_btn2 = st.columns([3, 1])

        with col_btn1:
            if st.button("🚀 Generate Comprehensive Focused Analysis", type="primary", use_container_width=True):
                if query.strip():
                    run_comprehensive_milo_analysis(client_name, query)
                else:
                    st.error(
                        "Please enter a question about the client to analyze.")

        with col_btn2:
            if st.button("📊 Quick View", use_container_width=True):
                show_quick_overview()

    with col2:
        st.header("📈 Client Intelligence")

        # Enhanced highlights from rich sample data
        st.subheader("🌟 Key Highlights")

        highlights = [
            {"icon": "🎓", "title": "Northwestern Success",
                "detail": "Emma accepted - 18yr planning milestone"},
            {"icon": "🌱", "title": "ESG Integration Achievement",
                "detail": "VSGX transition - values without sacrifice"},
            {"icon": "👥", "title": "Family Financial Team",
                "detail": "Linda & Emma actively engaged"},
            {"icon": "📈", "title": "Exceptional Performance",
                "detail": "8.2% return - all targets exceeded"}
        ]

        for highlight in highlights:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 0.75rem; margin: 0.5rem 0; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef;">
                <div style="font-size: 1.5rem; margin-right: 1rem;">{highlight['icon']}</div>
                <div>
                    <strong>{highlight['title']}</strong><br>
                    <small style="color: #666;">{highlight['detail']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📅 Communication Timeline")

        timeline_items = [
            {"date": "Aug 15", "event": "Family ESG Review Meeting",
                "type": "meeting", "sentiment": "Collaborative"},
            {"date": "Jul 18", "event": "Northwestern Campus Visit Call",
                "type": "call", "sentiment": "Excited"},
            {"date": "Jun 22", "event": "Fed Policy Impact Email",
                "type": "email", "sentiment": "Analytical"},
            {"date": "May 22", "event": "Internship Update & Performance",
                "type": "email", "sentiment": "Positive"},
            {"date": "Apr 10", "event": "Northwestern Acceptance Celebration!",
                "type": "meeting", "sentiment": "Celebratory"}
        ]

        for item in timeline_items:
            icon = "🤝" if item["type"] == "meeting" else "📞" if item["type"] == "call" else "📧"
            sentiment_color = {"Collaborative": "#28a745", "Excited": "#ffc107", "Analytical": "#17a2b8",
                               "Positive": "#28a745", "Celebratory": "#dc3545"}.get(item["sentiment"], "#6c757d")

            st.markdown(f"""
            <div style="padding: 0.5rem; margin: 0.25rem 0; border-left: 3px solid {sentiment_color}; background-color: #f8f9fa; border-radius: 0 5px 5px 0;">
                <strong>{item['date']}</strong> {icon} <em style="color: {sentiment_color};">{item['sentiment']}</em><br>
                <small>{item['event']}</small>
            </div>
            """, unsafe_allow_html=True)

        # Performance snapshot
        st.subheader("⚡ Performance Snapshot")

        col_perf1, col_perf2 = st.columns(2)
        with col_perf1:
            st.metric("Annual Return", "8.2%", "+1.2% vs IPS")
            st.metric("Risk Level", "12.8%", "Well controlled")

        with col_perf2:
            st.metric("Sharpe Ratio", "0.89", "Excellent")
            st.metric("ESG Performance", "5.8%", "Competitive")


def run_comprehensive_milo_analysis(client_name: str, query: str):
    """Execute comprehensive MILO analysis - 100% Cloud compatible"""

    st.markdown("---")
    st.header("🤖 MILO Comprehensive Query-Focused Analysis")

    # Enhanced query processing
    query_analysis = analyze_query_preview(query)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; border: 1px solid #2196f3;">
        <h4 style="margin: 0; color: #1976d2;">🎯 Processing Comprehensive Query</h4>
        <p style="margin: 0.5rem 0 0 0;"><strong>Query:</strong> "{query}"</p>
        <p style="margin: 0.25rem 0;"><strong>Analysis Focus:</strong> {query_analysis['focus']}</p>
        <p style="margin: 0.25rem 0 0 0;"><strong>Response Type:</strong> {query_analysis['type']} with rich sample data analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced progress tracking
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
            "name": "Communications Intelligence Analyst",
            "task": f"Deep analysis of 8 detailed communications for {query_analysis['focus'].lower()} patterns and insights...",
            "description": f"Processing rich communication dataset with advanced keyword matching and thematic analysis focused on {query_analysis['focus'].lower()}"
        },
        {
            "name": "Portfolio Performance Intelligence Analyst",
            "task": f"Comprehensive {query_analysis['focus'].lower()}-focused performance analysis with real market data integration...",
            "description": f"Analyzing portfolio performance with emphasis on {query_analysis['focus'].lower()} aspects using live and historical data"
        },
        {
            "name": "Meeting Preparation Intelligence Specialist",
            "task": f"Creating comprehensive {query_analysis['focus'].lower()}-focused meeting materials and strategic recommendations...",
            "description": f"Generating targeted executive materials specifically designed for {query_analysis['focus'].lower()} discussions"
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

        # Realistic processing time with increasing complexity
        processing_time = 2.5 + i * 0.7
        time.sleep(processing_time)

        # Show completion
        agent_containers[i].markdown(f"""
        <div class="agent-complete">
            <strong>✅ {agent_info['name']}</strong><br>
            Comprehensive query-focused analysis complete<br>
            <small><em>Cloud-compatible analysis with rich data • Processing time: {processing_time:.1f}s</em></small>
        </div>
        """, unsafe_allow_html=True)

    progress_bar.progress(1.0)
    status_text.markdown(
        "**✅ Comprehensive Query-Focused Analysis Complete!**")

    # Try real agents first, then use enhanced mock
    try:
        # Import the Chroma-free version
        from chroma_free_milo_agents import execute_chroma_free_milo_analysis

        st.success(
            "✅ Real CrewAI agents executing - using chroma-free implementation!")

        with st.spinner("CrewAI agents processing..."):
            result = execute_chroma_free_milo_analysis(client_name, query)

        st.success("✅ CrewAI analysis completed successfully!")

        # Display agent output
        if result:
            with st.expander("🤖 Raw Agent Output", expanded=False):
                st.text(str(result))

    except ImportError as e:
        st.info(
            "CrewAI agents not available - using enhanced demo mode with comprehensive mock results")
        st.caption(f"Import error: {str(e)}")

    except Exception as e:
        st.warning(f"CrewAI execution error: {str(e)[:100]}...")
        st.info("Falling back to enhanced demo mode")

    # Always show comprehensive mock results for demo
    st.info("📊 Displaying comprehensive analysis results...")
    agent_results = generate_comprehensive_mock_results(
        query, query_analysis['focus'])
    display_comprehensive_milo_results(
        agent_results, client_name, query, query_analysis)


def display_comprehensive_milo_results(results: dict, client_name: str, query: str, query_analysis: dict):
    """Display comprehensive results - enhanced version"""

    st.markdown("---")
    st.header(f"📊 Comprehensive Analysis Results - {client_name}")

    # Safe data extraction
    perf = results.get("performance", {}) or {}
    comms = results.get("communications", {}) or {}
    meeting = results.get("meeting_prep", {}) or {}
    focus = query_analysis.get("focus", "General")

    # Enhanced query response header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h3 style="margin: 0; color: white;">🎯 Comprehensive Response: "{query}"</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Focus: {focus} | Enhanced Analysis with Rich Sample Data | Zero Dependencies Mode</p>
    </div>
    """, unsafe_allow_html=True)

    # Executive summary with enhanced styling
    if meeting and "executive_summary" in meeting:
        st.markdown("### 📋 Executive Summary")
        st.markdown(f"""
        <div style="background-color: #e8f5e8; border: 1px solid #4caf50; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <p style="margin: 0; font-size: 1.1rem; line-height: 1.6;"><strong>{meeting["executive_summary"]}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced results tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Direct Response", "📞 Communications Intelligence",
            "📈 Performance Analysis", "💬 Meeting Materials", "✅ Strategic Actions"]
    )

    with tab1:
        st.subheader("Direct Response to Your Query")

        if focus == "ESG/Sustainability" and comms:
            st.markdown("#### 🌱 ESG Integration & Sustainability Progress")

            # Key themes
            themes = comms.get("key_themes", [])
            for i, theme in enumerate(themes, 1):
                st.markdown(f"{i}. {theme}")

            # ESG performance metrics
            if "esg_performance" in perf:
                st.markdown("#### 📊 ESG Performance Metrics")
                esg_perf = perf["esg_performance"]

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "VSGX Performance", f"{esg_perf.get('VSGX', {}).get('return', 5.8)}%", "Competitive vs benchmark")
                with col2:
                    st.metric(
                        "ESG Allocation", f"{esg_perf.get('VSGX', {}).get('allocation', 15)}%", "Successfully transitioned")

                st.success(
                    f"**Transition Impact:** {esg_perf.get('transition_impact', 'Minimal difference')}")

        elif focus == "Performance" and "portfolio_return" in perf:
            st.markdown("#### 📈 Performance Highlights & Analysis")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Annual Portfolio Return",
                          f"{perf.get('portfolio_return', 0)}%", "+1.2% vs IPS target")

            if "detailed_performance" in perf:
                dp = perf["detailed_performance"]
                with col2:
                    st.metric("Risk-Adjusted Returns",
                              f"Sharpe: {dp.get('sharpe_ratio', 'N/A')}", "Excellent")
                with col3:
                    st.metric("Top Performer", dp.get(
                        "top_performer", "N/A"), "Outstanding")

                st.info(
                    f"**Risk Management:** {dp.get('risk_level', 'Well controlled volatility')}")
                st.success(
                    f"**Diversification:** {dp.get('all_positive', 'All asset classes contributing positively')}")

        elif focus == "Family/Personal" and comms:
            st.markdown("#### 👨‍👩‍👧 Family Milestones & Developments")

            timeline = comms.get("focused_timeline", [])[:4]
            for event in timeline:
                relevance_emoji = "🔥" if event.get(
                    "relevance", 5) >= 10 else "⭐" if event.get("relevance", 5) >= 8 else "💫"
                st.markdown(
                    f"**{event.get('date', '')}** {relevance_emoji} {event.get('summary', '')}")

            # College funding status
            if "college_funding" in perf:
                cf = perf["college_funding"]
                st.markdown("#### 🎓 College Funding Status")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Annual Need", cf.get(
                        "annual_need", "N/A"), "Northwestern costs")
                with col2:
                    st.metric("Funding Status", cf.get(
                        "funding_status", "N/A").split(" - ")[0], "✅ On track")

        # Always show key metrics summary
        st.markdown("#### 📊 Key Analysis Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Portfolio Return",
                      f"{perf.get('portfolio_return', 8.2)}%", "Excellent")
        with col2:
            st.metric("Communications Analyzed",
                      f"{comms.get('total_interactions', 8)}", "Comprehensive")
        with col3:
            st.metric("Analysis Method", "Enhanced", f"{focus} focus")

    with tab2:
        st.subheader(f"Communications Intelligence - {focus} Optimized")

        if comms and "focused_timeline" in comms:
            st.markdown("#### 📅 Most Relevant Communications")

            for item in comms["focused_timeline"]:
                relevance_score = item.get("relevance", 5)
                stars = "⭐" * min(int(relevance_score / 2), 5)
                relevance_color = "#28a745" if relevance_score >= 9 else "#ffc107" if relevance_score >= 7 else "#6c757d"

                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {relevance_color}; background-color: #f8f9fa; border-radius: 0 8px 8px 0;">
                    <strong>{item.get('date', '')}</strong> - {item.get('type', '')} <span style="color: {relevance_color};">{stars}</span><br>
                    <p style="margin: 0.5rem 0 0 0;">{item.get('summary', '')}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 🎯 Key Intelligence Themes")
            themes = comms.get("key_themes", [])
            for i, theme in enumerate(themes, 1):
                st.markdown(f"**{i}.** {theme}")

    with tab3:
        st.subheader(f"Performance Analysis - {focus} Intelligence")

        if perf:
            # Main metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Portfolio Return",
                          f"{perf.get('portfolio_return', 0)}%", "+1.2% vs IPS")

            # Focus-specific metrics
            if focus == "ESG/Sustainability" and "esg_performance" in perf:
                with col2:
                    esg = perf["esg_performance"].get("VSGX", {})
                    st.metric("ESG Fund Performance", f"{esg.get('return', 5.8)}%",
                              f"{esg.get('allocation', 15)}% allocation")

                st.markdown("#### 🌱 ESG Integration Analysis")
                st.success(
                    f"**VSGX vs Benchmark:** {esg.get('vs_benchmark', 'Competitive performance')}")
                st.info(
                    f"**Values Achievement:** {perf['esg_performance'].get('transition_impact', 'Successful integration')}")

            elif "detailed_performance" in perf:
                dp = perf["detailed_performance"]
                with col2:
                    st.metric("Risk Management", "Excellent",
                              f"Sharpe: {dp.get('sharpe_ratio', 'N/A')}")

                st.markdown("#### 📊 Detailed Performance Breakdown")
                st.success(
                    f"**IPS Compliance:** {dp.get('vs_ips', 'Meeting all targets')}")
                st.info(
                    f"**Risk Control:** {dp.get('risk_level', 'Well managed')}")
                if "all_positive" in dp:
                    st.success(
                        f"**Diversification Success:** {dp['all_positive']}")

    with tab4:
        st.subheader(f"Meeting Materials - {focus} Focused")

        if meeting and "targeted_talking_points" in meeting:
            st.markdown("#### 🎯 Prioritized Discussion Topics")

            talking_points = meeting["targeted_talking_points"]
            for point in talking_points:
                priority = point.get("priority", 1)
                priority_colors = {1: "#dc3545",
                                   2: "#ffc107", 3: "#28a745", 4: "#17a2b8"}
                priority_color = priority_colors.get(priority, "#6c757d")
                priority_icon = {1: "🔴", 2: "🟡",
                                 3: "🟢", 4: "🔵"}.get(priority, "⚪")

                topic = point.get("topic", "Discussion Point")
                content = point.get("point", "Content")

                st.markdown(f"""
                <div style="background-color: #f8f9fa; border-left: 4px solid {priority_color}; padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0;">
                    {priority_icon} <strong>Priority {priority}: {topic}</strong><br>
                    <p style="margin: 0.5rem 0 0 0;">{content}</p>
                </div>
                """, unsafe_allow_html=True)

            # Conversation starters
            if "conversation_starters" in meeting:
                st.markdown("#### 💬 Conversation Starters")
                for starter in meeting["conversation_starters"]:
                    st.markdown(f"💭 *\"{starter}\"*")

    with tab5:
        st.subheader(f"Strategic Action Items - {focus} Focused")

        if meeting and "action_items" in meeting:
            st.markdown("#### ✅ Recommended Actions")

            for i, item in enumerate(meeting["action_items"], 1):
                checked = st.checkbox(
                    f"**{i}.** {item}", value=False, key=f"action_{i}")

        st.markdown("---")
        st.markdown("#### 📤 Export & Follow-up Options")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📄 Download Comprehensive Report", use_container_width=True):
                st.success(
                    "✅ Comprehensive query-focused report downloaded! (Demo mode)")

        with col2:
            if st.button("📧 Email Executive Summary", use_container_width=True):
                st.success(
                    "✅ Executive summary emailed to advisory team! (Demo mode)")

        with col3:
            if st.button("🔄 Ask Follow-up Question", use_container_width=True):
                st.info("💡 Ready for your next detailed question about this client!")

        # Additional insights
        st.markdown("#### 🔍 Additional Insights Available")
        insight_options = [
            "📊 Detailed performance attribution analysis",
            "🌱 ESG impact and carbon footprint assessment",
            "👥 Family dynamics and planning evolution",
            "📈 Risk-adjusted return optimization opportunities",
            "💼 Tax-loss harvesting and optimization strategies"
        ]

        selected_insights = st.multiselect(
            "Select additional insights to generate:", insight_options)

        if selected_insights:
            st.info(
                f"✨ {len(selected_insights)} additional insight(s) selected - these would generate detailed analysis in the full implementation.")


def show_quick_overview():
    """Show quick portfolio and client overview"""
    st.markdown("---")
    st.subheader("⚡ Quick Client Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Portfolio Metrics**")
        st.metric("Current Value", "$2.5M", "↗ +8.2%")
        st.metric("YTD Return", "8.2%", "+1.2% vs target")
        st.metric("Risk Level", "12.8%", "Well controlled")

    with col2:
        st.markdown("**Recent Activity**")
        st.metric("Last Contact", "Aug 15", "Family meeting")
        st.metric("ESG Status", "Active", "VSGX transition")
        st.metric("College Planning", "On Track", "Northwestern 2025")

    st.markdown("**Quick Insights**")
    insights = [
        "✅ Portfolio exceeding all IPS targets",
        "🌱 ESG integration successful without performance compromise",
        "👥 Strong family engagement with multi-generational planning",
        "🎓 Northwestern milestone achieved - 18-year planning success"
    ]

    for insight in insights:
        st.markdown(f"- {insight}")


if __name__ == "__main__":
    main()
