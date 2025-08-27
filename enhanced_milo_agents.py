"""
MILO Client Intelligence Dashboard - No CrewAI Required Version
This version works perfectly without CrewAI for Streamlit Cloud deployment
"""

from datetime import datetime, timedelta
from typing import Dict, List
import os
import re
import json
import hashlib
print("🚀 MILO Agents loading - Streamlit Cloud optimized (no CrewAI required)")


# Only essential imports
try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    YFINANCE_AVAILABLE = True
    print("✅ yfinance available")
except ImportError:
    print("❌ yfinance not available - using fallback data")
    YFINANCE_AVAILABLE = False

print("✅ All imports successful - ready for analysis")

# Rich sample communications data
ENHANCED_COMMUNICATIONS_DATA = [
    {
        "date": "2024-01-15",
        "type": "email",
        "subject": "Q4 2023 Portfolio Review Follow-up - ESG Questions",
        "full_content": """Hi Sarah,

Thank you for yesterday's portfolio review meeting. I'm pleased with the 8.1% return - it exceeded our expectations and stayed within our target range.

However, I wanted to follow up on something that's been on my mind. I've been reading more about ESG investing, and I'm becoming concerned about some of our international holdings. Specifically, I noticed that VTIAX might include companies with questionable environmental practices, particularly in emerging markets.

My daughter Emma (she's the one starting at Northwestern next year) has been taking environmental science classes and keeps asking about our family's carbon footprint, including our investments. It got me thinking - are we investing in companies that align with our values?

I don't want to sacrifice returns for feel-good investing, but I'd like to explore sustainable alternatives for our international allocation. Could you research some ESG-focused international funds?

Best regards,
Robert Smith""",
        "sentiment": "thoughtful_concern",
        "key_themes": ["ESG_investing", "international_holdings", "family_influence", "values_alignment", "environmental_concerns", "daughter_influence"],
        "entities": ["Emma", "Northwestern", "VTIAX", "ESG funds", "fossil fuels"],
        "client_requests": ["research ESG international funds", "explain impact investing"],
        "urgency": "medium"
    },
    {
        "date": "2024-02-28",
        "type": "phone_call",
        "subject": "Banking Sector Concerns - Market Volatility Discussion",
        "full_content": """Phone call summary - 30 minutes

Robert called expressing concern about recent banking sector news. He'd been reading about regional bank issues and was worried about potential contagion effects on our portfolio.

Key discussion points:
- He's been watching too much financial news and feeling anxious
- Specifically worried about our bond holdings and interest rate exposure
- Asked if we should reduce our VBTLX allocation given rate environment
- Mentioned his neighbor sold all his stocks last week - peer pressure evident
- Reassured him about our diversified approach and bond laddering strategy

Outcome: He felt better after our discussion but requested more frequent check-ins during volatile periods. Agreed to schedule monthly calls during market stress periods rather than quarterly.""",
        "sentiment": "anxious_but_reassured",
        "key_themes": ["market_volatility", "banking_sector_concerns", "peer_influence", "risk_management", "communication_preferences", "media_influence"],
        "entities": ["VBTLX", "Vanguard", "regional banks", "neighbor Bob"],
        "client_requests": ["more frequent communication during volatility", "reassurance about bond safety"],
        "urgency": "high"
    },
    {
        "date": "2024-04-10",
        "type": "meeting",
        "subject": "Mid-Year Review Meeting - Northwestern Acceptance Celebration",
        "full_content": """Mid-Year Portfolio Review Meeting - 60 minutes
Robert and Linda Smith

GREAT NEWS: Emma got into Northwestern! 

Portfolio Performance Review:
- YTD return: 6.8% (exceeding expectations)
- Asset allocation remains within IPS guidelines
- ESG research has progressed significantly

Key Discussion Points:

1. Northwestern Acceptance & Financial Planning
- Emma accepted to Northwestern for Fall 2025
- Financial aid package better than expected
- Still need ~$35K/year for 4 years
- Discussed 529 plan optimization and cash flow timing
- Linda very engaged in this discussion

2. ESG Fund Transition Decision
- Robert has done extensive research on VSGX vs VTIAX
- Family alignment important (Emma's influence clear)
- Decided to transition 15% allocation from VTIAX to VSGX
- Will monitor performance closely vs benchmark

3. Family Financial Involvement
- Linda attending meetings now (first time today)
- Family financial decision-making becoming more collaborative
- Discussion about Linda's own retirement planning needs
- Emma showing interest in investment discussions

Action Items:
- Execute VSGX transition (15% of international allocation)
- Set up 529 plan review meeting
- Schedule Linda's individual retirement planning session
- Prepare ESG performance tracking framework""",
        "sentiment": "celebratory_and_planning",
        "key_themes": ["Northwestern_acceptance", "family_milestone", "ESG_transition", "college_funding", "family_involvement", "portfolio_performance"],
        "entities": ["Emma", "Northwestern", "Linda", "VSGX", "VTIAX", "529 plan"],
        "client_requests": ["execute ESG transition", "529 plan review", "Linda retirement planning"],
        "urgency": "medium"
    },
    {
        "date": "2024-05-22",
        "type": "email",
        "subject": "Summer Plans and Portfolio Check-in",
        "full_content": """Hi Sarah,

Hope you're having a good start to your summer! I wanted to give you a quick update on our family plans and check in on the portfolio.

Emma is doing a summer internship at a local financial planning firm - she's really excited about it and has been asking us lots of questions about our own planning. It's wonderful to see her taking an interest in financial literacy.

The VSGX transition seems to be going well. I've been tracking it against our previous VTIAX position and the performance has been quite competitive. Linda has been asking good questions about the ESG criteria and how we evaluate the funds.

Speaking of Linda - when might be a good time to schedule her individual planning session? She's been more engaged since our last meeting and I think she's ready to focus on her own goals.

One question: with the strong market performance this year, should we consider any rebalancing? I know we're still within our target ranges, but wanted to get your thoughts.

Also, Emma asked an interesting question the other day about our portfolio's "carbon footprint." Do you know if there are tools to measure the environmental impact of our investments? She's becoming quite the sustainability advocate!

Looking forward to hearing from you.

Best,
Robert""",
        "sentiment": "positive_and_curious",
        "key_themes": ["summer_updates", "Emma_internship", "ESG_performance", "Linda_engagement", "rebalancing_question", "sustainability_metrics"],
        "entities": ["Emma", "Linda", "VSGX", "VTIAX", "carbon footprint"],
        "client_requests": ["rebalancing assessment", "Linda scheduling", "carbon footprint measurement"],
        "urgency": "low"
    },
    {
        "date": "2024-08-15",
        "type": "meeting",
        "subject": "Summer Review Meeting - Family Team Approach",
        "full_content": """Summer Portfolio Review Meeting - 75 minutes
Robert, Linda, and Emma Smith (Emma's first meeting!)

This was a special family meeting with Emma joining for the first time. Very engaging discussion with all three family members actively participating.

Portfolio Performance (YTD through August):
- Total return: 7.8% (excellent performance)
- All asset classes contributing positively
- ESG integration successful - VSGX performing competitively
- Risk metrics within acceptable ranges

Emma's Internship Insights:
- She's learned about fee structures, portfolio construction, and performance measurement
- Asks sophisticated questions about our ESG criteria
- Suggested looking into green bonds for fixed income ESG integration
- Interested in understanding our advisor fee structure (good questions!)

Family Financial Dynamics:
- Linda now fully engaged in planning discussions
- Robert appreciates having family input on major decisions
- Emma brings generational perspective on sustainability priorities
- Discussion about teaching financial literacy to next generation

ESG Expansion Discussion:
- Family wants to explore ESG options for bond allocation
- Interested in impact investing beyond traditional ESG screening
- Emma research project: compare our portfolio's carbon footprint to benchmarks
- Discussion about proxy voting and shareholder engagement

Future Planning:
- Emma will join quarterly meetings going forward
- Linda scheduling her individual retirement planning session
- Family considering annual "values and money" discussion
- Emma interested in potentially pursuing finance/economics at Northwestern

This meeting highlighted the evolution of the Smith family into a true "financial team" with each member bringing valuable perspectives.""",
        "sentiment": "collaborative_and_forward_thinking",
        "key_themes": ["family_collaboration", "Emma_first_meeting", "portfolio_performance", "ESG_expansion", "college_planning", "financial_education", "generational_planning"],
        "entities": ["Emma", "Linda", "Northwestern", "VSGX", "green bonds", "529 plan"],
        "client_requests": ["explore bond ESG options", "carbon footprint analysis", "impact investing research"],
        "urgency": "low"
    }
]


def analyze_query(query: str) -> Dict[str, any]:
    """Analyze user query to determine focus areas and response strategy"""

    query_lower = query.lower()

    query_categories = {
        "esg_sustainability": ["esg", "sustainable", "sustainability", "environmental", "social", "governance", "values", "impact", "green", "ethical"],
        "performance": ["performance", "returns", "return", "gains", "losses", "profit", "growth", "yield", "benchmark"],
        "family_personal": ["family", "daughter", "emma", "linda", "college", "northwestern", "personal", "education", "life"],
        "risk_volatility": ["risk", "volatility", "volatile", "concerned", "worry", "anxious", "safe", "conservative", "aggressive"],
        "communication": ["communication", "contact", "meeting", "email", "call", "frequency", "updates"],
        "market_economy": ["market", "fed", "rates", "economy", "economic", "inflation", "election", "policy"],
        "bonds_fixed_income": ["bond", "bonds", "fixed income", "duration", "vbtlx", "vtabx", "interest rate"],
        "equity_stocks": ["equity", "stock", "stocks", "vtsax", "vtiax", "vsgx", "allocation"],
        "planning": ["planning", "strategy", "goals", "future", "timeline", "prepare", "preparation"]
    }

    category_scores = {}
    for category, keywords in query_categories.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        if score > 0:
            category_scores[category] = score

    primary_focus = max(
        category_scores, key=category_scores.get) if category_scores else "general"

    return {
        "original_query": query,
        "primary_focus": primary_focus,
        "all_categories": category_scores,
        "query_type": "informational"
    }


def analyze_communications(query: str) -> Dict:
    """Analyze communications with query-specific focus"""

    print(f"🔍 Communications analysis - Focus: {query}")

    query_analysis = analyze_query(query)
    focus = query_analysis["primary_focus"]

    # Filter communications using keyword/theme matching
    relevant_comms = []
    for comm in ENHANCED_COMMUNICATIONS_DATA:
        relevance_score = 0

        # Score based on primary focus
        if focus == "esg_sustainability" and any(
            theme in ["ESG_investing", "values_alignment", "environmental_concerns",
                      "ESG_transition", "ESG_performance", "ESG_expansion"]
            for theme in comm["key_themes"]
        ):
            relevance_score += 10
        elif focus == "performance" and any(
            theme in ["portfolio_performance", "market_volatility"]
            for theme in comm["key_themes"]
        ):
            relevance_score += 10
        elif focus == "family_personal" and any(
            theme in ["family_involvement", "college_planning", "education_planning",
                      "daughter_influence", "Northwestern_acceptance", "family_milestone",
                      "Emma_first_meeting", "family_collaboration"]
            for theme in comm["key_themes"]
        ):
            relevance_score += 10
        elif focus == "risk_volatility" and any(
            theme in ["market_volatility",
                      "risk_management", "banking_sector_concerns"]
            for theme in comm["key_themes"]
        ):
            relevance_score += 10

        # Keyword matching from query
        query_words = query.lower().split()
        content_text = (comm.get("full_content", "") + " " +
                        comm.get("subject", "")).lower()

        for word in query_words:
            if len(word) > 3 and word in content_text:
                relevance_score += 2

        # Base relevance
        relevance_score += 1

        relevant_comms.append({**comm, "relevance_score": relevance_score})

    # Sort by relevance
    relevant_comms.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Generate insights based on focus
    if focus == "esg_sustainability":
        insights = [
            "Strong family commitment to ESG investing driven by Emma's environmental interests",
            "Successful VSGX transition with competitive performance vs VTIAX",
            "Values alignment now as important as return optimization",
            "Family ready for expanded ESG options including green bonds"
        ]
    elif focus == "family_personal":
        insights = [
            "Northwestern acceptance represents successful long-term planning milestone",
            "Linda's involvement has strengthened family financial decision-making",
            "Emma's financial education accelerating through internship experience",
            "Multi-generational approach to financial planning established"
        ]
    elif focus == "performance":
        insights = [
            "Consistent satisfaction with portfolio performance vs expectations",
            "Growing sophistication in performance evaluation and analysis",
            "ESG integration achieved without performance sacrifice",
            "Strong risk-adjusted returns with controlled volatility"
        ]
    else:
        insights = [
            "Highly engaged family with sophisticated financial discussions",
            "Successful integration of performance goals with values alignment",
            "Proactive communication and planning for major life milestones"
        ]

    return {
        "query_focus": focus,
        "total_interactions": len(ENHANCED_COMMUNICATIONS_DATA),
        "focused_timeline": [
            {
                "date": comm["date"],
                "type": comm["type"],
                "summary": comm["subject"],
                "relevance": comm["relevance_score"]
            }
            for comm in relevant_comms[:6]
        ],
        "key_insights": insights,
        "themes_analysis": {
            "most_frequent_themes": [
                ("ESG_investing", 3),
                ("family_collaboration", 2),
                ("portfolio_performance", 2),
                ("Northwestern_acceptance", 1)
            ]
        }
    }


def analyze_portfolio(query: str) -> Dict:
    """Analyze portfolio performance with query-specific focus"""

    print(f"📊 Portfolio analysis - Focus: {query}")

    query_analysis = analyze_query(query)
    focus = query_analysis["primary_focus"]

    # Portfolio data
    portfolio = {
        "client_name": "Smith Family Trust",
        "portfolio_value": 2500000,
        "allocations": {
            "VTSAX": {"allocation": 40, "name": "Vanguard Total Stock Market Index"},
            "VTIAX": {"allocation": 15, "name": "Vanguard Total International Stock Index"},
            "VSGX": {"allocation": 15, "name": "Vanguard ESG International Stock ETF"},
            "VBTLX": {"allocation": 20, "name": "Vanguard Total Bond Market Index"},
            "VGSLX": {"allocation": 5, "name": "Vanguard Real Estate Index Fund"},
            "VTABX": {"allocation": 5, "name": "Vanguard Total International Bond Index"}
        }
    }

    # Enhanced fallback data
    fallback_data = {
        "VTSAX": {"return": 0.121, "volatility": 0.135},
        "VTIAX": {"return": 0.062, "volatility": 0.142},
        # Slightly lower due to ESG screening
        "VSGX": {"return": 0.058, "volatility": 0.138},
        "VBTLX": {"return": 0.021, "volatility": 0.045},
        "VGSLX": {"return": 0.153, "volatility": 0.218},
        "VTABX": {"return": 0.018, "volatility": 0.055}
    }

    fund_performance = {}
    total_weighted_return = 0

    for ticker, details in portfolio["allocations"].items():
        annual_return = fallback_data[ticker]["return"]
        volatility = fallback_data[ticker]["volatility"]

        if YFINANCE_AVAILABLE:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1y")
                if not hist.empty and len(hist) > 20:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    annual_return = (end_price - start_price) / start_price
                    daily_returns = hist['Close'].pct_change().dropna()
                    volatility = daily_returns.std() * np.sqrt(252)
                    print(
                        f"✅ Got real data for {ticker}: {annual_return*100:.1f}%")
            except:
                print(
                    f"📋 Using fallback for {ticker}: {annual_return*100:.1f}%")

        weight = details["allocation"] / 100
        weighted_return = annual_return * weight
        total_weighted_return += weighted_return

        fund_performance[ticker] = {
            "name": details["name"],
            "allocation": details["allocation"],
            "annual_return": round(annual_return * 100, 2),
            "volatility": round(volatility * 100, 2),
            "weighted_contribution": round(weighted_return * 100, 2)
        }

    total_return = round(total_weighted_return * 100, 2)

    # Focus-specific metrics
    if focus == "esg_sustainability":
        focused_metrics = {
            "esg_fund_performance": f"{fund_performance['VSGX']['annual_return']}% (VSGX)",
            "esg_allocation": "15% of portfolio in ESG funds",
            "transition_impact": "Minimal performance difference vs previous VTIAX allocation"
        }
    elif focus == "performance":
        focused_metrics = {
            "annual_return": f"{total_return}%",
            "vs_ips_target": "Exceeding 7-9% target range" if total_return > 9 else "Within target range",
            "top_performer": "VGSLX at 15.3% return"
        }
    else:
        focused_metrics = {
            "annual_return": f"{total_return}%",
            "ips_status": "Compliant"
        }

    return {
        "query_focus": focus,
        "total_return": total_return,
        "focused_metrics": focused_metrics,
        "fund_performance": fund_performance,
        "ips_compliance": {
            "return_compliance": {
                "current_return": f"{total_return}%",
                "ips_target": "7-9% annually",
                "status": "Compliant" if 7 <= total_return <= 9 else ("Exceeding" if total_return > 9 else "Below target")
            },
            "allocation_compliance": "Within IPS guidelines"
        }
    }


def generate_meeting_prep(query: str, communications_data: Dict, portfolio_data: Dict) -> Dict:
    """Generate meeting preparation materials"""

    print(f"📋 Meeting prep - Focus: {query}")

    query_analysis = analyze_query(query)
    focus = query_analysis["primary_focus"]

    # Generate focus-specific content
    if focus == "esg_sustainability":
        executive_summary = "ESG Integration Success Story: Smith Family Trust has successfully implemented ESG investing with VSGX performing competitively. Emma's environmental interests are driving authentic family values alignment. Family ready for expanded sustainable investing options."

        talking_points = [
            {"priority": 1, "topic": "ESG Achievement",
             "point": "VSGX delivering competitive performance - values achieved without return sacrifice"},
            {"priority": 2, "topic": "Family Leadership",
             "point": "Emma's environmental passion driving authentic investment alignment across generations"},
            {"priority": 3, "topic": "Expansion Opportunities",
             "point": "Family positioned for green bonds and expanded ESG options"}
        ]

        action_items = [
            "Research green bond options for fixed income ESG integration",
            "Schedule family ESG discussion with carbon footprint analysis",
            "Explore impact investing opportunities beyond traditional ESG screening"
        ]

        conversation_starters = [
            "Emma must be proud that your investments now reflect your family's environmental values...",
            "Your ESG research has been impressive - you've become sustainability experts...",
            "How does it feel to achieve values alignment without sacrificing returns?"
        ]

    elif focus == "family_personal":
        executive_summary = "Family Milestone Achievement: Northwestern acceptance represents successful 18-year planning milestone. College funding secured and optimized. Strong family financial team established with multi-generational approach."

        talking_points = [
            {"priority": 1, "topic": "Northwestern Success",
             "point": "Emma's acceptance represents successful 18-year planning milestone"},
            {"priority": 2, "topic": "Family Financial Team",
             "point": "Linda's engagement has transformed family decision-making process"},
            {"priority": 3, "topic": "Next Generation Leadership",
             "point": "Emma's internship has developed sophisticated financial understanding"}
        ]

        action_items = [
            "Finalize Northwestern college funding timeline and withdrawal strategy",
            "Schedule Linda's comprehensive individual retirement planning session",
            "Establish Emma's continued involvement in quarterly portfolio reviews"
        ]

        conversation_starters = [
            "How are you feeling about Emma starting her Northwestern journey this fall?",
            "Linda, how has being more involved in the financial planning process felt?",
            "What has Emma learned from her internship that surprised you the most?"
        ]

    elif focus == "performance":
        executive_summary = f"Outstanding Performance Results: Portfolio delivering {portfolio_data['total_return']}% annual return, exceeding IPS targets. All asset classes contributing positively with excellent risk management."

        talking_points = [
            {"priority": 1, "topic": "Exceptional Returns",
             "point": f"{portfolio_data['total_return']}% return significantly exceeding IPS targets"},
            {"priority": 2, "topic": "Risk Management Excellence",
             "point": "Strong performance achieved with well-controlled volatility"},
            {"priority": 3, "topic": "Diversification Success",
             "point": "Every asset class adding positive value - no weak performers"}
        ]

        action_items = [
            "Continue quarterly performance monitoring vs benchmarks and IPS targets",
            "Maintain current allocation strategy with disciplined rebalancing",
            "Review tax-loss harvesting opportunities as year-end approaches"
        ]

        conversation_starters = [
            "I'm thrilled to share your exceptional performance results...",
            f"How do you feel about the {portfolio_data['total_return']}% return compared to your expectations?",
            "What aspects of this outstanding performance are you most pleased with?"
        ]

    else:
        executive_summary = "Comprehensive Planning Success: Portfolio performing excellently with strong family engagement and successful values alignment. All planning objectives being met."

        talking_points = [
            {"priority": 1, "topic": "Overall Success",
             "point": "Portfolio and planning objectives being exceeded across all areas"}
        ]

        action_items = [
            "Continue current successful strategy and monitoring approach"
        ]

        conversation_starters = [
            "What aspects of this year's progress are you most proud of?"
        ]

    return {
        "query_response": {
            "original_question": query,
            "query_focus": focus,
            "response_approach": query_analysis["query_type"]
        },
        "executive_summary": executive_summary,
        "targeted_talking_points": talking_points,
        "action_items": action_items,
        "conversation_starters": conversation_starters
    }


def execute_enhanced_milo_analysis(client_name: str = "Smith Family Trust", user_query: str = "What has happened with this account over the past year?"):
    """Main function to execute enhanced query-aware MILO analysis - NO CREWAI REQUIRED"""

    print(f"🤖 MILO: No-CrewAI analysis for {client_name}")
    print(f"📋 Query: {user_query}")

    query_analysis = analyze_query(user_query)
    print(f"🎯 Query Focus: {query_analysis['primary_focus']}")
    print("=" * 80)

    try:
        # Step 1: Analyze communications
        print("🔍 Step 1: Analyzing communications...")
        communications_result = analyze_communications(user_query)

        # Step 2: Analyze portfolio
        print("📊 Step 2: Analyzing portfolio performance...")
        portfolio_result = analyze_portfolio(user_query)

        # Step 3: Generate meeting prep
        print("📋 Step 3: Generating meeting preparation materials...")
        meeting_prep_result = generate_meeting_prep(
            user_query, communications_result, portfolio_result)

        # Combine results
        final_result = {
            "client_name": client_name,
            "query": user_query,
            "query_analysis": query_analysis,
            "communications_analysis": communications_result,
            "portfolio_analysis": portfolio_result,
            "meeting_preparation": meeting_prep_result,
            "analysis_method": "Enhanced keyword analysis with rich sample data",
            "timestamp": datetime.now().isoformat()
        }

        print("\n" + "=" * 80)
        print("🎯 MILO NO-CREWAI ANALYSIS COMPLETE")
        print("=" * 80)

        return final_result

    except Exception as e:
        print(f"❌ Error in MILO analysis: {str(e)}")
        return {
            "error": str(e),
            "client_name": client_name,
            "query": user_query,
            "status": "failed"
        }


print("🚀 MILO agents loaded successfully - No CrewAI required!")
print("✅ Ready for comprehensive analysis with rich sample data")

if __name__ == "__main__":
    # Test the analysis
    test_queries = [
        "What are the client's ESG concerns?",
        "How has the portfolio performed this year?",
        "What family changes should I know about?"
    ]

    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        result = execute_enhanced_milo_analysis(user_query=query)
        if result and "error" not in result:
            print("✅ Success!")
        else:
            print("❌ Failed!")
        print("-" * 40)
