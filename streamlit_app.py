import streamlit as st
import time
from datetime import datetime
import json

# Import your MILO crew (assuming the previous code is in milo_crew.py)
# from milo_crew import execute_annual_review_prep

st.set_page_config(
    page_title="MILO Client Intelligence Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 2rem;
}
.client-info {
    background-color: #f0f8ff;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #1f4e79;
}
.agent-status {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border-radius: 5px;
    font-weight: bold;
}
.agent-working {
    background-color: #fff3cd;
    color: #856404;
}
.agent-complete {
    background-color: #d4edda;
    color: #155724;
}
.talking-point {
    background-color: #f8f9fa;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #007bff;
    border-radius: 0 5px 5px 0;
}
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">🤖 MILO Client Intelligence Dashboard</h1>',
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Embedded AI Assistant for Crescent Grove Advisors</p>', unsafe_allow_html=True)

    # Sidebar for client selection and parameters
    with st.sidebar:
        st.header("Client Selection")
        client_name = st.selectbox(
            "Select Client",
            ["Smith Family Trust", "Johnson Portfolio", "Williams Estate"]
        )

        st.header("Analysis Parameters")
        time_period = st.selectbox(
            "Review Period",
            ["Past Year", "Past 6 Months", "Past Quarter"]
        )

        include_performance = st.checkbox(
            "Include Performance Analysis", value=True)
        include_communications = st.checkbox(
            "Include Communications Review", value=True)

        st.header("Client Overview")
        st.markdown(f"""
        **{client_name}**
        - Portfolio Value: $2.5M
        - Risk Tolerance: Moderate
        - Last Review: Jan 2024
        - Advisor: Sarah Johnson
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Annual Review Preparation")

        # Query input
        st.subheader("What would you like to know?")
        query = st.text_area(
            "Enter your question about the client:",
            value="What has happened with this account over the past year?",
            height=100
        )

        # Execute button
        if st.button("🚀 Generate Annual Review Materials", type="primary"):
            execute_milo_analysis(client_name, query)

    with col2:
        st.header("Quick Stats")

        # Mock quick stats
        st.metric("YTD Return", "8.2%", "1.2%")
        st.metric("Portfolio Value", "$2.5M", "$180K")
        st.metric("Last Contact", "Sep 15", "-30 days")

        st.header("Portfolio Allocation")
        portfolio_data = {
            "US Equity": 40,
            "Intl Equity": 30,
            "Bonds": 25,
            "Alternatives": 5
        }

        for asset, allocation in portfolio_data.items():
            st.write(f"**{asset}:** {allocation}%")
            st.progress(allocation / 100)


def execute_milo_analysis(client_name, query):
    """Execute the MILO crew analysis and display results"""

    st.markdown("---")
    st.header("🤖 MILO Analysis in Progress")

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Agent status containers
    agent_containers = {
        "communications": st.empty(),
        "performance": st.empty(),
        "meeting_prep": st.empty()
    }

    # Simulate the three-agent workflow
    agents = [
        ("Communications Analyst", "Analyzing client emails and meeting transcripts..."),
        ("Portfolio Performance Analyst",
         "Calculating returns and comparing to IPS..."),
        ("Meeting Preparation Specialist",
         "Generating talking points and recommendations...")
    ]

    results = {}

    for i, (agent_name, task_description) in enumerate(agents):

        # Update progress
        progress = (i + 1) / len(agents)
        progress_bar.progress(progress)
        status_text.text(f"Agent {i+1}/3: {agent_name}")

        # Show agent working status
        agent_key = list(agent_containers.keys())[i]
        agent_containers[agent_key].markdown(
            f'<div class="agent-status agent-working">🔄 {agent_name}: {task_description}</div>',
            unsafe_allow_html=True
        )

        # Simulate processing time
        time.sleep(2)

        # Show completion and results
        agent_containers[agent_key].markdown(
            f'<div class="agent-status agent-complete">✅ {agent_name}: Complete</div>',
            unsafe_allow_html=True
        )

        # Generate mock results for each agent
        if "Communications" in agent_name:
            results["communications"] = generate_mock_communications_analysis()
        elif "Performance" in agent_name:
            results["performance"] = generate_mock_performance_analysis()
        elif "Meeting" in agent_name:
            results["meeting_prep"] = generate_mock_meeting_prep()

    progress_bar.progress(1.0)
    status_text.text("✅ Analysis Complete!")

    # Display results
    display_analysis_results(results)


def generate_mock_communications_analysis():
    """Generate mock communications analysis results"""
    return {
        "timeline": [
            {"date": "Jan 15, 2024", "type": "Email",
                "summary": "Q4 review follow-up - ESG concerns discussed"},
            {"date": "Mar 20, 2024", "type": "Email",
                "summary": "Banking sector anxiety - reassurance requested"},
            {"date": "Jun 10, 2024", "type": "Meeting",
                "summary": "Mid-year review - college planning discussed"},
            {"date": "Sep 15, 2024", "type": "Email",
                "summary": "Fed rate decision impact on bonds"}
        ],
        "key_themes": [
            "ESG investment preferences",
            "Market volatility concerns",
            "College funding planning (2025)",
            "Interest rate sensitivity"
        ],
        "client_sentiment": "Generally satisfied but seeks more communication during market stress"
    }


def generate_mock_performance_analysis():
    """Generate mock performance analysis results"""
    return {
        "portfolio_return": 8.2,
        "ips_target": "7-9%",
        "benchmark_comparison": "Outperformed by 0.8%",
        "individual_funds": {
            "VTSAX": {"return": 12.1, "allocation": 40},
            "VTIAX": {"return": 6.2, "allocation": 30},
            "VBTLX": {"return": 2.1, "allocation": 20},
            "VGSLX": {"return": 15.3, "allocation": 5},
            "VTABX": {"return": 1.8, "allocation": 5}
        },
        "needs_rebalancing": False,
        "risk_metrics": {"volatility": "12.3%", "sharpe_ratio": "0.85"}
    }


def generate_mock_meeting_prep():
    """Generate mock meeting preparation materials"""
    return {
        "executive_summary": "Smith Family Trust portfolio performed well in 2024 with 8.2% return, meeting IPS objectives. Key focus areas: ESG alignment, college planning, and market communication preferences.",
        "talking_points": [
            "Celebrate strong 8.2% portfolio performance - exceeded midpoint of 7-9% IPS target",
            "Address ESG concerns in international holdings - explore ESG fund alternatives",
            "College planning update: daughter starting fall 2025, review 529 funding strategy",
            "Discuss communication preferences during market volatility periods",
            "REIT allocation (VGSLX) strong performer at 15.3% - consider slight increase",
            "Bond portfolio positioning ahead of potential rate environment changes",
            "Review and update risk tolerance given strong market performance",
            "Plan next rebalancing date and triggers"
        ],
        "action_items": [
            "Research ESG international equity alternatives",
            "Schedule 529 plan funding review",
            "Set up quarterly market update emails",
            "Review beneficiary designations"
        ],
        "conversation_starters": [
            "How are you feeling about the college timeline approaching?",
            "What are your thoughts on the current ESG landscape?",
            "Any changes in your financial situation we should discuss?"
        ]
    }


def display_analysis_results(results):
    """Display the comprehensive analysis results"""

    st.markdown("---")
    st.header("📊 Annual Review Analysis Results")

    # Executive Summary
    st.subheader("Executive Summary")
    st.info(results["meeting_prep"]["executive_summary"])

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📞 Communications", "📈 Performance", "💬 Talking Points", "✅ Action Items"])

    with tab1:
        st.subheader("Communications Timeline")
        for item in results["communications"]["timeline"]:
            st.markdown(f"""
            **{item['date']}** - {item['type']}  
            {item['summary']}
            """)

        st.subheader("Key Themes Identified")
        for theme in results["communications"]["key_themes"]:
            st.markdown(f"• {theme}")

        st.subheader("Client Sentiment")
        st.write(results["communications"]["client_sentiment"])

    with tab2:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Portfolio Return",
                      f"{results['performance']['portfolio_return']}%", "Above Target")
        with col2:
            st.metric("vs Benchmark",
                      results['performance']['benchmark_comparison'])
        with col3:
            st.metric("Sharpe Ratio",
                      results['performance']['risk_metrics']['sharpe_ratio'])

        st.subheader("Individual Fund Performance")
        for fund, data in results['performance']['individual_funds'].items():
            st.write(
                f"**{fund}**: {data['return']}% (Allocation: {data['allocation']}%)")

        rebalancing_status = "✅ No rebalancing needed" if not results[
            'performance']['needs_rebalancing'] else "⚠️ Rebalancing recommended"
        st.write(f"**Rebalancing Status**: {rebalancing_status}")

    with tab3:
        st.subheader("Meeting Talking Points")
        for i, point in enumerate(results["meeting_prep"]["talking_points"], 1):
            st.markdown(f"""
            <div class="talking-point">
            <strong>{i}.</strong> {point}
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Conversation Starters")
        for starter in results["meeting_prep"]["conversation_starters"]:
            st.markdown(f"💬 *{starter}*")

    with tab4:
        st.subheader("Recommended Action Items")
        for item in results["meeting_prep"]["action_items"]:
            st.checkbox(item, value=False)

        st.subheader("Follow-up Schedule")
        st.write("📅 Next Review: January 2025")
        st.write("📧 Quarterly Updates: March, June, September 2025")
        st.write("📞 Check-in Call: After Q1 2025 performance")

    # Download button for the report
    st.markdown("---")
    if st.button("📄 Download Full Report"):
        st.success(
            "Report downloaded! (This would generate a PDF in the full implementation)")


if __name__ == "__main__":
    main()
