"""
MILO Client Intelligence Dashboard - Enhanced Demo Interface
Streamlit application with query-responsive CrewAI agents
"""

import streamlit as st
import time
import json
from datetime import datetime
import pandas as pd

# Import the enhanced MILO crew
from enhanced_milo_agents import execute_enhanced_milo_analysis, analyze_query

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

        # Query examples
        st.write("**Try these example queries:**")

        example_queries = [
            "What are the client's ESG concerns?",
            "How has the portfolio performed this year?",
            "What family changes should I know about?",
            "Are there any risk management issues?",
            "What communication preferences does the client have?",
            "What has happened with this account over the past year?"
        ]

        # Create clickable example queries
        selected_query = None
        for i, example in enumerate(example_queries):
            if st.button(f"💭 {example}", key=f"example_{i}", use_container_width=True):
                selected_query = example

        # Query text area
        if selected_query:
            query = st.text_area(
                "Your question about the client:",
                value=selected_query,
                height=100,
                help="MILO will analyze communications, performance, and generate meeting prep focused on your specific question."
            )
        else:
            query = st.text_area(
                "Your question about the client:",
                value="What are the client's ESG concerns?",
                height=100,
                help="MILO will analyze communications, performance, and generate meeting prep focused on your specific question."
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


def analyze_query_preview(query: str) -> dict:
    """Preview what the query analysis will focus on"""

    query_lower = query.lower()

    focus_keywords = {
        "ESG/Sustainability": ["esg", "sustainable", "environmental", "values", "green", "ethical"],
        "Performance": ["performance", "returns", "gains", "profit", "growth"],
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


def run_enhanced_milo_analysis(client_name: str, query: str):
    """Execute the enhanced MILO analysis with query responsiveness"""

    st.markdown("---")
    st.header("🤖 MILO Query-Focused Analysis")

    # Show query processing
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
    agent_results = {}

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

        # Generate enhanced results based on query focus
        if "Communications" in agent_info['name']:
            agent_results["communications"] = generate_enhanced_communications_results(
                query_analysis['focus'])
        elif "Performance" in agent_info['name']:
            agent_results["performance"] = generate_enhanced_performance_results(
                query_analysis['focus'])
        elif "Meeting" in agent_info['name']:
            agent_results["meeting_prep"] = generate_enhanced_meeting_prep_results(
                query_analysis['focus'], query)

    progress_bar.progress(1.0)
    status_text.markdown(
        "**✅ Query-Focused Analysis Complete!** All agents have processed your specific question.")

    # Display enhanced results
    display_enhanced_milo_results(
        agent_results, client_name, query, query_analysis)


def generate_enhanced_communications_results(focus: str):
    """Generate communications results focused on specific query type"""

    base_results = {
        "total_interactions": 8,
        "analysis_approach": f"Filtered and prioritized communications based on {focus} themes"
    }

    if focus == "ESG/Sustainability":
        base_results.update({
            "focused_timeline": [
                {"date": "Aug 15, 2024", "type": "Meeting",
                    "summary": "ESG expansion discussion - family values alignment", "relevance": 10},
                {"date": "Jun 22, 2024", "type": "Email",
                    "summary": "Emma's environmental influence on investment decisions", "relevance": 9},
                {"date": "Apr 10, 2024", "type": "Meeting",
                    "summary": "VSGX transition planning - competitive performance", "relevance": 10},
                {"date": "Mar 20, 2024", "type": "Email",
                    "summary": "ESG fund research - client doing homework", "relevance": 8},
                {"date": "Jan 15, 2024", "type": "Email",
                    "summary": "Initial ESG concerns about VTIAX holdings", "relevance": 9}
            ],
            "key_themes": [
                "Strong family commitment to ESG investing driven by Emma's environmental interests",
                "Successful VSGX transition with competitive performance vs VTIAX",
                "Client has become highly knowledgeable about ESG options through research",
                "Values alignment now as important as return optimization",
                "Interest in expanding ESG beyond equities to bonds and impact investing"
            ],
            "esg_evolution": "Evolved from initial concerns to sophisticated ESG integration strategy",
            "family_driver": "Emma's environmental science studies and internship driving family ESG commitment"
        })

    elif focus == "Performance":
        base_results.update({
            "focused_timeline": [
                {"date": "Aug 15, 2024", "type": "Meeting",
                    "summary": "YTD 7.8% performance review - on track for goals", "relevance": 10},
                {"date": "Jun 22, 2024", "type": "Email",
                    "summary": "Questions about optimizing returns with rate environment", "relevance": 8},
                {"date": "May 22, 2024", "type": "Email",
                    "summary": "Tech stock concentration concerns in VTSAX", "relevance": 7},
                {"date": "Apr 10, 2024", "type": "Meeting",
                    "summary": "Strong YTD 6.8% performance discussion", "relevance": 9},
                {"date": "Feb 28, 2024", "type": "Phone Call",
                    "summary": "Banking sector concerns but reassured by diversification", "relevance": 8}
            ],
            "key_themes": [
                "Consistent satisfaction with risk-adjusted portfolio performance",
                "Growing sophistication in performance evaluation and market analysis",
                "ESG integration achieved without performance sacrifice",
                "Performance discussions now include family goals and values context",
                "Proactive questions about optimizing returns in changing market environment"
            ],
            "performance_satisfaction": "High - client appreciates both absolute and risk-adjusted returns",
            "sophistication_growth": "Client financial knowledge and analysis skills have increased significantly"
        })

    elif focus == "Family/Personal":
        base_results.update({
            "focused_timeline": [
                {"date": "Aug 15, 2024", "type": "Meeting",
                    "summary": "Linda's first joint meeting - family team strengthened", "relevance": 10},
                {"date": "Jul 18, 2024", "type": "Phone Call",
                    "summary": "Northwestern campus visit - Emma's excitement", "relevance": 9},
                {"date": "May 22, 2024", "type": "Email",
                    "summary": "Emma's summer finance internship success", "relevance": 8},
                {"date": "Apr 10, 2024", "type": "Meeting",
                    "summary": "Northwestern acceptance celebration!", "relevance": 10},
                {"date": "Mar 20, 2024", "type": "Email",
                    "summary": "College funding strategy and financial aid package", "relevance": 9}
            ],
            "key_themes": [
                "Northwestern acceptance represents successful long-term planning milestone",
                "Linda's involvement has created powerful family financial planning dynamic",
                "Emma's financial education accelerating through internship and coursework",
                "Family approaching investments as multi-generational strategy",
                "College funding strategy well-positioned for $35K annual payments"
            ],
            "family_evolution": "Evolved from individual planning to comprehensive family financial team",
            "education_success": "Emma's financial sophistication growing rapidly through real-world experience"
        })

    else:  # General focus
        base_results.update({
            "focused_timeline": [
                {"date": "Aug 15, 2024", "type": "Meeting",
                    "summary": "Comprehensive family review - all stakeholders engaged", "relevance": 8},
                {"date": "Jun 22, 2024", "type": "Email",
                    "summary": "Fed rate decision analysis and positioning questions", "relevance": 7},
                {"date": "Apr 10, 2024", "type": "Meeting",
                    "summary": "Northwestern acceptance and ESG transition success", "relevance": 9},
                {"date": "Mar 20, 2024", "type": "Email",
                    "summary": "Multi-topic planning discussion", "relevance": 7},
                {"date": "Jan 15, 2024", "type": "Email",
                    "summary": "ESG interests and performance satisfaction", "relevance": 8}
            ],
            "key_themes": [
                "Highly engaged client family with sophisticated financial discussions",
                "Successful integration of performance goals with values alignment",
                "Proactive communication and planning for major life milestones",
                "Growing family financial education and involvement"
            ]
        })

    return base_results


def generate_enhanced_performance_results(focus: str):
    """Generate performance results focused on specific query type"""

    base_performance = {
        "portfolio_return": 8.2,
        "analysis_approach": f"Performance analysis emphasized {focus} metrics"
    }

    if focus == "ESG/Sustainability":
        base_performance.update({
            "esg_performance": {
                "VSGX": {"return": 5.8, "allocation": 15, "vs_benchmark": "Competitive"},
                "VTIAX_comparison": {"previous_return": 6.2, "transition_impact": "Minimal"},
                "esg_cost": "0.4% performance difference - within acceptable range"
            },
            "sustainability_metrics": {
                "esg_allocation": "15% of portfolio in dedicated ESG funds",
                "values_alignment": "High - screens out fossil fuels and controversial sectors",
                "impact_potential": "Ready for impact investing expansion"
            },
            "esg_recommendations": [
                "ESG transition successful - consider expansion to other asset classes",
                "Research green bonds for fixed income ESG integration",
                "Explore impact investing for 2-3% allocation"
            ]
        })

    elif focus == "Performance":
        base_performance.update({
            "detailed_performance": {
                "vs_ips": {"current": 8.2, "target": "7-9%", "status": "Exceeding midpoint"},
                "risk_adjusted": {"sharpe_ratio": 0.89, "status": "Excellent"},
                "benchmark": {"excess_return": "+0.8%", "status": "Outperforming"}
            },
            "fund_leaders": {
                "top_performer": {"fund": "VGSLX", "return": 15.3, "impact": "Significant positive contribution"},
                "steady_performers": ["VTSAX (12.1%)", "VTIAX (6.2%)", "VSGX (5.8%)"],
                "defensive_anchors": ["VBTLX (2.1%)", "VTABX (1.8%)"]
            },
            "performance_drivers": [
                "Equity allocation benefiting from market strength",
                "Real estate (VGSLX) exceptional outperformance",
                "ESG integration not hindering returns",
                "Bond allocation providing stability and income"
            ]
        })

    elif focus == "Risk/Volatility":
        base_performance.update({
            "risk_analysis": {
                "portfolio_volatility": 12.8,
                "risk_budget": "Appropriate for moderate risk tolerance",
                "downside_protection": {"max_drawdown": -8.2, "status": "Well controlled"},
                "diversification": {"correlation_benefit": "Strong", "asset_class_spread": "Effective"}
            },
            "risk_recommendations": [
                "Current risk level appropriate for client profile",
                "Consider reducing equity allocation as college approaches",
                "Maintain diversification during market uncertainty"
            ]
        })

    else:  # General performance
        base_performance.update({
            "overall_metrics": {
                "annual_return": 8.2,
                "volatility": 12.8,
                "sharpe_ratio": 0.89,
                "max_drawdown": -8.2
            },
            "fund_performance": {
                "VTSAX": {"return": 12.1, "allocation": 40},
                "VSGX": {"return": 5.8, "allocation": 15},
                "VTIAX": {"return": 6.2, "allocation": 15},
                "VBTLX": {"return": 2.1, "allocation": 20},
                "VGSLX": {"return": 15.3, "allocation": 5},
                "VTABX": {"return": 1.8, "allocation": 5}
            }
        })

    return base_performance


def generate_enhanced_meeting_prep_results(focus: str, original_query: str):
    """Generate meeting prep results focused on specific query type"""

    base_prep = {
        "query_addressed": original_query,
        "focus_area": focus,
        "response_approach": "Targeted analysis with comprehensive context"
    }

    if focus == "ESG/Sustainability":
        base_prep.update({
            "executive_summary": f"ESG Query Response: Client's ESG integration has been highly successful with VSGX performing competitively (5.8% vs 6.2% for replaced VTIAX). Emma's environmental interests are driving strong family commitment to sustainable investing. Client has become highly knowledgeable through research and ready for expanded ESG options including green bonds and impact investing.",

            "targeted_talking_points": [
                {"priority": 1, "topic": "ESG Success Story",
                    "point": "VSGX transition performing within 0.4% of previous VTIAX - values achieved without return sacrifice"},
                {"priority": 2, "topic": "Family Values Driver",
                    "point": "Emma's environmental studies creating meaningful family investment alignment"},
                {"priority": 3, "topic": "Expansion Opportunities",
                    "point": "Ready to explore green bonds and impact investing for further ESG integration"},
                {"priority": 4, "topic": "Knowledge Evolution",
                    "point": "Client ESG research sophistication has increased dramatically"}
            ],

            "esg_action_items": [
                "Research green bond options for fixed income ESG integration",
                "Prepare impact investing proposal for 2-3% allocation",
                "Schedule ESG-focused review with Emma included",
                "Monitor VSGX performance vs international benchmarks"
            ],

            "conversation_starters": [
                "Emma must be proud that your investments now reflect your family's environmental values...",
                "Your ESG research has been impressive - you've become quite the expert...",
                "The VSGX transition proves you don't have to choose between values and returns..."
            ]
        })

    elif focus == "Performance":
        base_prep.update({
            "executive_summary": f"Performance Query Response: Portfolio delivering exceptional 8.2% annual return, exceeding IPS midpoint by 0.2%. Risk-adjusted performance excellent with 0.89 Sharpe ratio. All asset classes contributing positively with VGSLX leading at 15.3%. ESG integration achieved without performance penalty, proving values and returns can align.",

            "targeted_talking_points": [
                {"priority": 1, "topic": "Outstanding Returns",
                    "point": "8.2% annual return exceeds IPS midpoint target - strategy working perfectly"},
                {"priority": 2, "topic": "Risk-Adjusted Excellence",
                    "point": "0.89 Sharpe ratio demonstrates efficient risk-taking and strong risk management"},
                {"priority": 3, "topic": "Diversification Success",
                    "point": "All asset classes contributing - VGSLX standout at 15.3%, bonds providing stability"},
                {"priority": 4, "topic": "Values Integration",
                    "point": "ESG transition achieved competitive performance - no return sacrifice for values"}
            ],

            "performance_action_items": [
                "Continue monitoring risk-adjusted returns quarterly",
                "Consider slight VGSLX allocation increase given strong performance",
                "Maintain discipline during market volatility periods",
                "Prepare performance attribution analysis for family education"
            ]
        })

    elif focus == "Family/Personal":
        base_prep.update({
            "executive_summary": f"Family Query Response: Northwestern acceptance represents successful long-term planning with college funding well-positioned. Linda's involvement has strengthened family financial decision-making significantly. Emma's financial education accelerating through internship. Family evolved from individual planning to comprehensive multi-generational strategy with strong values alignment.",

            "targeted_talking_points": [
                {"priority": 1, "topic": "Northwestern Achievement",
                    "point": "Emma's acceptance represents successful planning - college funding strategy ready"},
                {"priority": 2, "topic": "Family Team Strength",
                    "point": "Linda's analytical involvement creating powerful planning dynamic"},
                {"priority": 3, "topic": "Emma's Growth",
                    "point": "Summer internship developing impressive financial sophistication"},
                {"priority": 4, "topic": "Multi-Generational Approach",
                    "point": "Family approaching investments with long-term perspective and shared values"}
            ],

            "family_action_items": [
                "Finalize college funding automation timeline",
                "Create educational materials for Emma's continued learning",
                "Plan Linda's retirement projection scenarios",
                "Schedule family financial goal-setting session"
            ]
        })

    else:  # General comprehensive response
        base_prep.update({
            "executive_summary": f"Comprehensive Query Response: Smith Family Trust experiencing exceptional year with 8.2% portfolio return, Northwestern acceptance milestone, successful ESG integration, and strengthened family financial planning approach. All metrics indicating successful strategy execution and high client satisfaction.",

            "targeted_talking_points": [
                {"priority": 1, "topic": "Overall Success",
                    "point": "8.2% return exceeding targets while achieving family values alignment"},
                {"priority": 2, "topic": "Major Milestones",
                    "point": "Northwestern acceptance and college funding preparation on track"},
                {"priority": 3, "topic": "Family Evolution",
                    "point": "Linda's involvement and Emma's education creating strong financial team"},
                {"priority": 4, "topic": "Strategic Integration",
                    "point": "ESG implementation without performance sacrifice proves strategy effectiveness"}
            ]
        })

    return base_prep


def display_enhanced_milo_results(results: dict, client_name: str, query: str, query_analysis: dict):
    """Display enhanced MILO results with query focus"""

    st.markdown("---")
    st.header(f"📊 Query-Focused Analysis Results - {client_name}")

    # Query response header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
        <h3 style="margin: 0; color: white;">🎯 Response to: "{query}"</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Analysis Focus: {query_analysis['focus']} | Response Type: {query_analysis['type']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Executive summary
    if "meeting_prep" in results:
        st.subheader("📋 Executive Summary")
        st.info(results["meeting_prep"]["executive_summary"])

    # Create enhanced tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Query Response", "📞 Communications", "📈 Performance", "💬 Talking Points", "✅ Actions"])

    with tab1:
        st.subheader("Direct Response to Your Query")

        focus = query_analysis['focus']

        if focus == "ESG/Sustainability" and "communications" in results:
            st.write("**🌱 ESG Integration Status:**")
            for theme in results["communications"].get("key_themes", []):
                st.markdown(f"• {theme}")

            if "performance" in results and "esg_performance" in results["performance"]:
                st.write("**📊 ESG Performance Impact:**")
                esg_perf = results["performance"]["esg_performance"]
                st.success(
                    f"VSGX: {esg_perf['VSGX']['return']}% return - {esg_perf['esg_cost']}")

        elif focus == "Performance" and "performance" in results:
            st.write("**📈 Performance Highlights:**")
            if "detailed_performance" in results["performance"]:
                perf = results["performance"]["detailed_performance"]
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Annual Return", f"{results['performance']['portfolio_return']}%", "+0.2% vs target")
                with col2:
                    st.metric(
                        "Sharpe Ratio", perf["risk_adjusted"]["sharpe_ratio"], "Excellent")
                with col3:
                    st.metric(
                        "vs Benchmark", perf["benchmark"]["excess_return"], "Outperforming")

        elif focus == "Family/Personal" and "communications" in results:
            st.write("**👨‍👩‍👧 Family Developments:**")
            if "focused_timeline" in results["communications"]:
                # Top 4 most relevant
                for event in results["communications"]["focused_timeline"][:4]:
                    relevance_color = "🔥" if event["relevance"] >= 9 else "⭐" if event["relevance"] >= 8 else "📌"
                    st.markdown(
                        f"**{event['date']}** {relevance_color} {event['summary']}")

        else:
            st.write("**📊 Comprehensive Overview:**")
            st.markdown(f"""
            - **Portfolio Return:** {results.get('performance', {}).get('portfolio_return', 8.2)}% annually
            - **Total Communications:** {results.get('communications', {}).get('total_interactions', 8)} interactions analyzed  
            - **Analysis Focus:** Customized for {focus} topics
            - **Meeting Readiness:** Complete preparation materials generated
            """)

    with tab2:
        st.subheader(f"Communications Analysis - {focus} Focus")

        if "communications" in results:
            comm_data = results["communications"]

            if "focused_timeline" in comm_data:
                st.write("**📅 Most Relevant Communications:**")
                for item in comm_data["focused_timeline"]:
                    relevance_stars = "⭐" * \
                        min(int(item.get("relevance", 5) / 2), 5)
                    st.markdown(f"""
                    <div style="padding: 0.75rem; margin: 0.5rem 0; border-left: 3px solid #007bff; background-color: #f8f9fa;">
                        <strong>{item['date']}</strong> - {item['type']} {relevance_stars}<br>
                        {item['summary']}
                    </div>
                    """, unsafe_allow_html=True)

            st.write("**🎯 Key Themes Identified:**")
            for theme in comm_data.get("key_themes", []):
                st.markdown(f"• {theme}")

            if focus == "ESG/Sustainability" and "esg_evolution" in comm_data:
                st.success(f"**ESG Evolution:** {comm_data['esg_evolution']}")
            elif focus == "Family/Personal" and "family_evolution" in comm_data:
                st.success(
                    f"**Family Evolution:** {comm_data['family_evolution']}")

    with tab3:
        st.subheader(f"Performance Analysis - {focus} Focus")

        if "performance" in results:
            perf_data = results["performance"]

            # Key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Portfolio Return",
                          f"{perf_data['portfolio_return']}%", "+0.2% vs IPS")
            with col2:
                if focus == "ESG/Sustainability" and "esg_performance" in perf_data:
                    esg = perf_data["esg_performance"]["VSGX"]
                    st.metric(
                        "ESG Fund (VSGX)", f"{esg['return']}%", f"{esg['allocation']}% allocation")
                else:
                    st.metric("Risk Level", "12.8%", "Moderate")
            with col3:
                if focus == "Performance" and "detailed_performance" in perf_data:
                    st.metric(
                        "Sharpe Ratio", perf_data["detailed_performance"]["risk_adjusted"]["sharpe_ratio"], "Excellent")
                else:
                    st.metric("IPS Compliance", "✅", "Fully compliant")

            # Focus-specific analysis
            if focus == "ESG/Sustainability" and "esg_performance" in perf_data:
                st.write("**🌱 ESG Performance Details:**")
                esg_perf = perf_data["esg_performance"]
                st.write(
                    f"• **VSGX Performance:** {esg_perf['VSGX']['return']}% ({esg_perf['VSGX']['vs_benchmark']})")
                st.write(f"• **Transition Impact:** {esg_perf['esg_cost']}")
                st.write(
                    f"• **ESG Allocation:** {perf_data['sustainability_metrics']['esg_allocation']}")

            elif focus == "Performance" and "performance_drivers" in perf_data:
                st.write("**🚀 Performance Drivers:**")
                for driver in perf_data["performance_drivers"]:
                    st.markdown(f"• {driver}")

    with tab4:
        st.subheader(f"Meeting Talking Points - {focus} Focused")

        if "meeting_prep" in results:
            meeting_data = results["meeting_prep"]

            if "targeted_talking_points" in meeting_data:
                st.write("**🎯 Prioritized Discussion Topics:**")

                for point in meeting_data["targeted_talking_points"]:
                    priority_color = "🔴" if point["priority"] == 1 else "🟡" if point["priority"] == 2 else "🟢"
                    st.markdown(f"""
                    <div class="talking-point">
                        {priority_color} <strong>Priority {point['priority']}: {point['topic']}</strong><br>
                        {point['point']}
                    </div>
                    """, unsafe_allow_html=True)

            if "conversation_starters" in meeting_data:
                st.write("**💬 Conversation Starters:**")
                for starter in meeting_data["conversation_starters"]:
                    st.markdown(f"• *\"{starter}\"*")

    with tab5:
        st.subheader(f"Action Items - {focus} Focused")

        if "meeting_prep" in results:
            meeting_data = results["meeting_prep"]

            # Focus-specific action items
            action_key = f"{focus.lower().replace('/', '_')}_action_items"
            if action_key in meeting_data:
                st.write(f"**📝 {focus}-Specific Actions:**")
                for item in meeting_data[action_key]:
                    if isinstance(item, dict):
                        priority_color = "🔴" if item.get("priority") == "High" else "🟡" if item.get(
                            "priority") == "Medium" else "🟢"
                        st.markdown(
                            f"{priority_color} **{item.get('action', item)}** ({item.get('timeline', 'TBD')})")
                    else:
                        st.checkbox(item, value=False)
            else:
                # General action items
                general_actions = [
                    "Continue monitoring portfolio performance quarterly",
                    "Schedule follow-up discussion on query-specific topics",
                    "Prepare additional analysis based on client interests",
                    "Plan next review meeting with targeted agenda"
                ]

                for action in general_actions:
                    st.checkbox(action, value=False)

            # Export options
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📄 Download Report", use_container_width=True):
                    st.success(
                        "Query-focused report downloaded! (Demo - would generate PDF)")

            with col2:
                if st.button("📧 Email Summary", use_container_width=True):
                    st.success(
                        "Targeted summary emailed! (Demo - would send to advisor)")

            with col3:
                if st.button("🔄 Ask Follow-up", use_container_width=True):
                    st.info("Ready for your next query about this client!")


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

    # Portfolio composition chart
    chart_data = pd.DataFrame({
        'Fund': ['VTSAX', 'VSGX', 'VTIAX', 'VBTLX', 'VGSLX', 'VTABX'],
        'Return': [12.1, 5.8, 6.2, 2.1, 15.3, 1.8],
        'Allocation': [40, 15, 15, 20, 5, 5]
    })

    st.bar_chart(chart_data.set_index('Fund')['Return'])


def show_communications_focus():
    """Show communications-focused quick analysis"""
    st.markdown("---")
    st.subheader("💬 Communications Focus View")

    recent_communications = [
        {"date": "Aug 15", "type": "Meeting", "topic": "Family Review", "sentiment": "Very Positive",
            "themes": ["Linda involvement", "Emma education", "ESG expansion"]},
        {"date": "Jul 18", "type": "Call", "topic": "College Tour", "sentiment": "Excited",
            "themes": ["Northwestern excitement", "Family bonding", "Financial planning"]},
        {"date": "Jun 22", "type": "Email", "topic": "Fed Rates", "sentiment": "Analytical",
            "themes": ["Market analysis", "Bond strategy", "Emma pride"]}
    ]

    for comm in recent_communications:
        with st.expander(f"{comm['date']} - {comm['type']}: {comm['topic']} ({comm['sentiment']})"):
            st.write("**Key Themes:**")
            for theme in comm['themes']:
                st.write(f"• {theme}")


if __name__ == "__main__":
    main()
