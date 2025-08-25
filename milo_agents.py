from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from typing import List, Dict
import json
from datetime import datetime, timedelta

# Custom tools for the agents


class EmailAnalysisTool(BaseTool):
    name: str = "Email Analysis Tool"
    description: str = "Analyzes client emails and meeting transcripts for key themes and chronological patterns"

    def _run(self, client_data: str) -> str:
        # In real implementation, this would connect to Gmail API or SharePoint
        # For demo, we'll use mock data
        mock_communications = [
            {
                "date": "2024-01-15",
                "type": "email",
                "subject": "Q4 2023 Portfolio Review Follow-up",
                "summary": "Client confirmed satisfaction with portfolio performance but raised concerns about ESG alignment in international holdings."
            },
            {
                "date": "2024-03-20",
                "type": "email",
                "subject": "Market Volatility Concerns",
                "summary": "Client expressed anxiety about banking sector issues and requested reassurance about portfolio exposure."
            },
            {
                "date": "2024-06-10",
                "type": "meeting",
                "subject": "Mid-Year Portfolio Review",
                "summary": "45-minute meeting. Discussed rebalancing strategy and client's daughter starting college in 2025. Need to plan for tuition payments."
            },
            {
                "date": "2024-09-15",
                "type": "email",
                "subject": "Fed Rate Decision Discussion",
                "summary": "Client asked about impact of rate cuts on bond portfolio. Expressed interest in increasing equity allocation."
            }
        ]

        return json.dumps(mock_communications, indent=2)


class PerformanceAnalysisTool(BaseTool):
    name: str = "Portfolio Performance Analysis Tool"
    description: str = "Analyzes portfolio performance against IPS benchmarks using real market data"

    def _run(self, portfolio_data: str) -> str:
        # This would integrate with the PortfolioAnalyzer class we created above
        from portfolio_analyzer import PortfolioAnalyzer

        # Mock portfolio and IPS data for demo
        sample_portfolio = {
            "allocation": {
                "VTIAX": {"allocation": 30, "name": "Vanguard Total International Stock Index"},
                "VTSAX": {"allocation": 40, "name": "Vanguard Total Stock Market Index"},
                "VBTLX": {"allocation": 20, "name": "Vanguard Total Bond Market Index"},
                "VTABX": {"allocation": 5, "name": "Vanguard Total International Bond Index"},
                "VGSLX": {"allocation": 5, "name": "Vanguard Real Estate Index Fund"}
            }
        }

        sample_ips = {
            "return_objective": "7-9%",
            "asset_allocation_targets": {
                "equity": {"target": 70},
                "fixed_income": {"target": 25},
                "alternatives": {"target": 5}
            },
            "rebalancing_threshold": 5
        }

        # In real implementation, this would call the actual analyzer
        mock_performance = {
            "portfolio_return": 0.08,  # 8% return
            "ips_comparison": "Within Range",
            "individual_funds": {
                "VTSAX": {"return": 0.12, "allocation": 40},
                "VTIAX": {"return": 0.06, "allocation": 30},
                "VBTLX": {"return": 0.02, "allocation": 20},
                "VTABX": {"return": 0.01, "allocation": 5},
                "VGSLX": {"return": 0.15, "allocation": 5}
            },
            "needs_rebalancing": False
        }

        return json.dumps(mock_performance, indent=2)


class ReportGenerationTool(BaseTool):
    name: str = "Meeting Report Generation Tool"
    description: str = "Combines communications and performance data into structured meeting preparation materials"

    def _run(self, combined_data: str) -> str:
        # This tool formats the final report
        return "Report generation tool ready to compile final meeting materials"

# Define the three core agents


def create_milo_agents():

    communications_analyst = Agent(
        role='Client Communications Analyst',
        goal='Analyze the past year of client communications to identify key themes, concerns, and relationship developments in chronological order',
        backstory="""You are an expert at parsing through client emails, meeting notes, and phone call summaries to understand the full context of the advisor-client relationship. You excel at identifying patterns, recurring concerns, and important life events that impact financial planning decisions.""",
        tools=[EmailAnalysisTool()],
        verbose=True,
        allow_delegation=False
    )

    portfolio_analyst = Agent(
        role='Portfolio Performance Analyst',
        goal='Calculate portfolio returns, compare against IPS objectives, and assess whether rebalancing is needed',
        backstory="""You are a quantitative analyst specializing in portfolio performance evaluation. You have deep expertise in mutual fund analysis, benchmark comparison, and Investment Policy Statement compliance. You provide clear, data-driven assessments of portfolio performance.""",
        tools=[PerformanceAnalysisTool()],
        verbose=True,
        allow_delegation=False
    )

    meeting_prep_specialist = Agent(
        role='Meeting Preparation Specialist',
        goal='Synthesize communications history and performance analysis into actionable talking points for client meetings',
        backstory="""You are an experienced advisor support specialist who creates compelling meeting preparation materials. You excel at connecting client concerns with portfolio performance to create meaningful conversation topics and actionable recommendations.""",
        tools=[ReportGenerationTool()],
        verbose=True,
        allow_delegation=False
    )

    return communications_analyst, portfolio_analyst, meeting_prep_specialist

# Define the tasks for each agent


def create_milo_tasks(communications_analyst, portfolio_analyst, meeting_prep_specialist):

    communications_task = Task(
        description="""
        Analyze the Smith Family Trust's communications over the past year. Your analysis should include:
        
        1. A chronological timeline of all client interactions (emails, meetings, calls)
        2. Key themes and concerns raised by the client
        3. Any changes in client circumstances (family, career, financial goals)
        4. Recurring topics that may need addressing
        5. Client sentiment and satisfaction indicators
        
        Focus on extracting actionable insights that will help the advisor prepare for the annual review meeting.
        """,
        agent=communications_analyst,
        expected_output="A structured chronological summary of client communications with key themes and concerns highlighted"
    )

    performance_task = Task(
        description="""
        Conduct a comprehensive analysis of the Smith Family Trust portfolio performance:
        
        1. Calculate the weighted portfolio return for the past year
        2. Compare returns to the Investment Policy Statement objectives (7-9% target)
        3. Analyze individual fund performance within the portfolio
        4. Assess current asset allocation vs. IPS targets (70% equity, 25% fixed income, 5% alternatives)
        5. Determine if rebalancing is needed based on the 5% threshold
        6. Identify any performance outliers or concerns
        
        Provide specific data points and clear assessment of IPS compliance.
        """,
        agent=portfolio_analyst,
        expected_output="Detailed portfolio performance report with IPS compliance assessment and rebalancing recommendations"
    )

    meeting_prep_task = Task(
        description="""
        Create comprehensive meeting preparation materials by combining the communications analysis and portfolio performance data:
        
        1. Executive summary connecting client concerns with portfolio performance
        2. Address any specific client questions or concerns from communications
        3. Highlight portfolio performance relative to client expectations
        4. Generate 4-8 specific talking points for the annual review meeting
        5. Identify action items and recommendations
        6. Suggest conversation starters based on client interests and concerns
        
        The output should be advisor-ready material that can be used directly in the client meeting.
        """,
        agent=meeting_prep_specialist,
        expected_output="Complete meeting preparation package with executive summary, talking points, and recommended actions",
        # This task depends on the previous two
        context=[communications_task, performance_task]
    )

    return communications_task, performance_task, meeting_prep_task

# Create the MILO crew


def create_milo_crew():

    # Create agents
    communications_analyst, portfolio_analyst, meeting_prep_specialist = create_milo_agents()

    # Create tasks
    communications_task, performance_task, meeting_prep_task = create_milo_tasks(
        communications_analyst, portfolio_analyst, meeting_prep_specialist
    )

    # Create the crew
    milo_crew = Crew(
        agents=[communications_analyst,
                portfolio_analyst, meeting_prep_specialist],
        tasks=[communications_task, performance_task, meeting_prep_task],
        process=Process.sequential,  # Tasks run in sequence
        verbose=2
    )

    return milo_crew

# Main execution function for Streamlit integration


def execute_annual_review_prep(client_name: str = "Smith Family Trust"):
    """
    Main function to execute the annual review preparation workflow
    """
    print(f"🤖 MILO: Preparing annual review materials for {client_name}")
    print("=" * 60)

    # Create and execute the crew
    crew = create_milo_crew()

    # The crew will execute all tasks in sequence
    result = crew.kickoff(inputs={
        'client_name': client_name,
        'review_type': 'annual',
        'query': 'What has happened with this account over the past year?'
    })

    return result


if __name__ == "__main__":
    # Test the crew execution
    result = execute_annual_review_prep()
    print("\n" + "=" * 60)
    print("🎯 MILO ANNUAL REVIEW PREPARATION COMPLETE")
    print("=" * 60)
    print(result)
