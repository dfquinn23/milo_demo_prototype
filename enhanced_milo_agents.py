"""
MILO Client Intelligence Dashboard - Chroma-Free Version
CrewAI Agent Implementation with Rich Sample Data and Query Processing
STREAMLIT CLOUD COMPATIBLE - Zero Chroma dependencies
"""

import hashlib
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import re
from typing import Dict, List
import os

# NO VECTOR DB FUNCTIONALITY - Streamlit Cloud compatible
print("🚀 MILO Agents loaded - Streamlit Cloud compatible mode (no vector DB)")

# ============================================================================
# ENHANCED COMMUNICATIONS DATA WITH RICH CONTENT
# ============================================================================
ENHANCED_COMMUNICATIONS_DATA = [
    {
        "date": "2024-01-15",
        "type": "email",
        "subject": "Q4 2023 Portfolio Review Follow-up - ESG Questions",
        "full_content": """Hi Sarah,

Thank you for yesterday's portfolio review meeting. I'm pleased with the 8.1% return - it exceeded our expectations and stayed within our target range.

However, I wanted to follow up on something that's been on my mind. I've been reading more about ESG investing, and I'm becoming concerned about some of our international holdings. Specifically, I noticed that VTIAX might include companies with questionable environmental practices, particularly in emerging markets.

My daughter Emma (she's the one starting at Northwestern next year) has been taking environmental science classes and keeps asking about our family's carbon footprint, including our investments. It got me thinking - are we investing in companies that align with our values?

I don't want to sacrifice returns for feel-good investing, but I'd like to explore sustainable alternatives for our international allocation. Could you research some ESG-focused international funds? I'm particularly interested in:
- Funds that screen out fossil fuel companies
- Strong governance standards 
- Companies with good labor practices

Also, Emma mentioned something called "impact investing" - is that different from ESG? Should we consider that?

Let me know your thoughts when you have a chance.

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
- He's been watching too much financial news (his words) and feeling anxious
- Specifically worried about our bond holdings and interest rate exposure
- Asked if we should reduce our VBTLX allocation given rate environment
- Mentioned his neighbor sold all his stocks last week - peer pressure evident
- Reassured him about our diversified approach and bond laddering strategy
- Explained that our portfolio is well-positioned for various rate scenarios

His concerns:
"I keep seeing headlines about bank failures. Are our bond funds safe? Should we be more conservative? My neighbor Bob sold everything and went to cash - maybe we should consider that?"

My response emphasized:
- Our diversified bond approach through Vanguard funds
- No direct exposure to problematic regional banks
- Historical perspective on market volatility
- Importance of staying disciplined during uncertain times

Outcome: He felt better after our discussion but requested more frequent check-ins during volatile periods. Agreed to schedule monthly calls during market stress periods rather than quarterly.

Note: Robert tends to get anxious when consuming too much financial media. May want to suggest limiting news consumption during volatile times.""",
        "sentiment": "anxious_but_reassured",
        "key_themes": ["market_volatility", "banking_sector_concerns", "peer_influence", "risk_management", "communication_preferences", "media_influence"],
        "entities": ["VBTLX", "Vanguard", "regional banks", "neighbor Bob"],
        "client_requests": ["more frequent communication during volatility", "reassurance about bond safety"],
        "urgency": "high"
    },
    {
        "date": "2024-03-20",
        "type": "email",
        "subject": "Market Update Request - Fed Decision Impact",
        "full_content": """Sarah,

Hope you're doing well. I wanted to reach out after yesterday's Fed announcement about potential rate cuts.

I've been thinking about our conversation last month regarding bond positioning. With the Fed potentially pivoting toward cuts, should we be adjusting our fixed income strategy?

Specifically:
1. Our VBTLX holding - will this benefit from falling rates?
2. Should we consider longer duration bonds to capture more upside?
3. What about our VTABX international bond position?

Also, I've been researching that ESG topic we discussed. I found some interesting funds:
- Vanguard ESG International Stock ETF (VSGX)
- iShares MSCI KLD 400 Social ETF (DSI)

Do either of these make sense as alternatives to our current holdings? I'm not looking to make dramatic changes, but if we can align our values better without sacrificing returns, I'm interested.

One more thing - Emma got her Northwestern financial aid package. It's better than expected, but we'll still need about $35K per year starting in fall 2025. Should we start positioning some funds for liquidity? Maybe reduce our equity allocation slightly?

Thanks for your patience with all these questions. I know I've been more active lately, but with everything happening in the markets and Emma's college approaching, I want to make sure we're positioned well.

Best,
Robert

P.S. - Linda says hello! She's been asking about setting up her own portfolio review. Can you send her your contact info?""",
        "sentiment": "engaged_and_planning",
        "key_themes": ["interest_rates", "fed_policy", "bond_strategy", "ESG_research", "college_planning", "liquidity_needs", "family_referrals"],
        "entities": ["Fed", "VBTLX", "VTABX", "VSGX", "DSI", "Emma", "Northwestern", "Linda"],
        "client_requests": ["bond strategy review", "ESG fund analysis", "college funding liquidity planning", "referral for Linda"],
        "urgency": "medium"
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

4. Updated Risk Assessment
- Risk tolerance remains moderate
- Comfortable with current allocation
- Slightly more conservative on bond duration given Fed outlook

Action Items:
- Execute VSGX transition (15% of international allocation)
- Set up 529 plan review meeting
- Schedule Linda's individual retirement planning session
- Prepare ESG performance tracking framework

Personal Notes:
- Family is very excited about Northwestern
- Robert's research on ESG has been impressive
- Linda's involvement adds new dynamic but very positive
- Emma's influence on ESG focus is clear and authentic""",
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
        "date": "2024-06-22",
        "type": "email",
        "subject": "Fed Rate Decision and Bond Strategy Questions",
        "full_content": """Sarah,

I've been following the Fed's recent communications about potential rate cuts later this year. Given our current bond allocation, I wanted to get your thoughts on positioning.

Questions:
1. Should we be extending duration in our VBTLX holdings?
2. Is our VTABX international bond position appropriate given global rate trends?
3. Any thoughts on adding Treasury strips or longer-term bonds?

Emma's internship has been fascinating - she's been learning about duration risk and yield curve analysis. She actually suggested we might want to consider I-bonds for some of our cash holdings! (Though I know those have purchase limits.)

Linda and I have been discussing our overall risk tolerance. With Emma's college approaching and both of us getting closer to retirement, we're wondering if we should be slightly more conservative. Not dramatically, but perhaps shifting 5-10% from equities to bonds over the next year or two.

Also, I saw an article about "green bonds" - are those something we should consider given our ESG focus? Emma is very interested in this concept.

Thanks for your continued guidance. The portfolio is performing well and we're very happy with the ESG integration.

Best regards,
Robert""",
        "sentiment": "analytical_and_planning",
        "key_themes": ["fed_policy", "bond_strategy", "duration_risk", "Emma_learning", "risk_tolerance", "green_bonds"],
        "entities": ["Fed", "VBTLX", "VTABX", "Emma", "Linda", "I-bonds", "green bonds"],
        "client_requests": ["bond strategy review", "green bond research", "risk tolerance assessment"],
        "urgency": "medium"
    },
    {
        "date": "2024-07-18",
        "type": "phone_call",
        "subject": "Northwestern Campus Visit and College Planning Update",
        "full_content": """Phone call summary - 25 minutes

Robert called to update me on their Northwestern campus visit and discuss college funding logistics.

Northwestern Campus Visit:
- Family visited campus last week
- Emma absolutely loves it - even more excited now
- Met with financial aid office - confirmed our understanding of costs
- Toured the environmental science facilities (Emma's potential major)
- Linda was impressed with the campus and academic programs

College Planning Updates:
- Confirmed need for $35K/year starting Fall 2025
- Financial aid package stable for 4 years (assuming academic performance)
- Emma considering environmental science or economics major
- Discussion about potential graduate school planning

Portfolio Performance Discussion:
- Very pleased with YTD 7.8% return
- ESG funds performing well (VSGX competitive with benchmarks)
- Asking about tax-loss harvesting opportunities before year-end
- Interested in optimizing 529 vs taxable account withdrawals for college

Family Financial Education:
- Emma's internship has been eye-opening for the whole family
- She's been explaining concepts like expense ratios and Sharpe ratios at dinner
- Linda is becoming more confident in financial discussions
- Family considering a regular "money talk" night

Action Items Discussed:
- Schedule formal college funding strategy meeting
- Review tax-loss harvesting opportunities
- Consider additional ESG expansion options
- Plan family financial education resources

Overall tone was very positive and excited about the future.""",
        "sentiment": "excited_and_confident",
        "key_themes": ["Northwestern_visit", "college_funding", "family_education", "ESG_performance", "tax_planning"],
        "entities": ["Emma", "Northwestern", "Linda", "VSGX", "529 plan"],
        "client_requests": ["college funding strategy meeting", "tax-loss harvesting review", "ESG expansion options"],
        "urgency": "medium"
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

College Planning Finalization:
- Northwestern costs confirmed at ~$35K/year net
- 529 plan optimization completed
- Withdrawal strategy planned for tax efficiency
- Emma understands the family's financial commitment to her education

ESG Expansion Discussion:
- Family wants to explore ESG options for bond allocation
- Interested in impact investing beyond traditional ESG screening
- Emma research project: compare our portfolio's carbon footprint to benchmarks
- Discussion about proxy voting and shareholder engagement

Risk Management Review:
- Risk tolerance remains moderate
- Slight shift toward more conservative positioning over next 2 years
- Maintaining equity allocation until Emma starts college
- Discussed sequence of returns risk as retirement approaches

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

# ============================================================================
# QUERY PROCESSING UTILITIES (No dependencies)
# ============================================================================


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
        "planning": ["planning", "strategy", "goals", "future", "timeline", "prepare", "preparation"],
        "time_period": ["year", "month", "quarter", "recent", "lately", "past", "since", "last", "this"]
    }

    category_scores = {}
    for category, keywords in query_categories.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        if score > 0:
            category_scores[category] = score

    primary_focus = max(
        category_scores, key=category_scores.get) if category_scores else "general"

    time_period = "full_year"
    time_indicators = {
        "recent": ["recent", "lately", "last few", "past few"],
        "ytd": ["this year", "ytd", "year to date", "2024"],
        "quarter": ["quarter", "q1", "q2", "q3", "q4"],
        "month": ["month", "last month", "past month"]
    }

    for period, indicators in time_indicators.items():
        if any(indicator in query_lower for indicator in indicators):
            time_period = period
            break

    return {
        "original_query": query,
        "primary_focus": primary_focus,
        "all_categories": category_scores,
        "time_period": time_period,
        "query_type": determine_query_type(query_lower)
    }


def determine_query_type(query_lower: str) -> str:
    """Determine the type of query for appropriate response formatting"""
    if any(word in query_lower for word in ["what", "tell", "show", "explain"]):
        return "informational"
    elif any(word in query_lower for word in ["should", "recommend", "suggest", "advice"]):
        return "advisory"
    elif any(word in query_lower for word in ["how", "why", "when"]):
        return "analytical"
    elif any(word in query_lower for word in ["prepare", "meeting", "review", "summary"]):
        return "preparation"
    else:
        return "general"


def analyze_query_preview(query: str) -> dict:
    """Preview what the query analysis will focus on - for Streamlit UI"""
    query_analysis = analyze_query(query)

    focus_mapping = {
        "esg_sustainability": "ESG/Sustainability",
        "performance": "Performance",
        "family_personal": "Family/Personal",
        "risk_volatility": "Risk/Volatility",
        "communication": "Communication",
        "market_economy": "Market/Economy",
        "bonds_fixed_income": "Bonds/Fixed Income",
        "equity_stocks": "Equity/Stocks",
        "planning": "Planning",
        "general": "General"
    }

    type_mapping = {
        "informational": "Informational",
        "advisory": "Advisory",
        "analytical": "Analytical",
        "preparation": "Preparation",
        "general": "General"
    }

    return {
        "focus": focus_mapping.get(query_analysis["primary_focus"], "General"),
        "type": type_mapping.get(query_analysis["query_type"], "General"),
        "primary_focus": query_analysis["primary_focus"],
        "query_type": query_analysis["query_type"]
    }

# ============================================================================
# CHROMA-FREE CUSTOM TOOLS WITH QUERY AWARENESS
# ============================================================================


class ChromaFreeCommunicationsAnalyzer(BaseTool):
    name: str = "Chroma-Free Communications Analyzer"
    description: str = "Analyzes client communications with focus based on user query - no vector DB dependencies"

    def _run(self, query: str) -> str:
        """Analyze communications with query-specific focus - PURE KEYWORD MATCHING"""

        query_analysis = analyze_query(query)
        print(
            f"🔍 Communications analysis - Focus: {query_analysis['primary_focus']}")

        # Filter communications using only keyword/theme matching
        relevant_comms = []
        for comm in ENHANCED_COMMUNICATIONS_DATA:
            relevance_score = 0
            focus = query_analysis["primary_focus"]

            # Score based on primary focus
            if focus == "esg_sustainability" and any(
                theme in ["ESG_investing", "values_alignment", "environmental_concerns",
                          "ESG_transition", "ESG_research", "ESG_performance", "ESG_expansion"]
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
                          "Emma_first_meeting", "family_collaboration", "family_education"]
                for theme in comm["key_themes"]
            ):
                relevance_score += 10
            elif focus == "risk_volatility" and any(
                theme in ["market_volatility",
                          "risk_management", "banking_sector_concerns"]
                for theme in comm["key_themes"]
            ):
                relevance_score += 10
            elif focus == "communication" and any(
                theme in ["communication_preferences"]
                for theme in comm["key_themes"]
            ):
                relevance_score += 10

            # Keyword matching from query
            query_words = query.lower().split()
            content_text = (comm.get("full_content", "") +
                            " " + comm.get("subject", "")).lower()

            for word in query_words:
                if len(word) > 3 and word in content_text:
                    relevance_score += 2

            # Base relevance
            relevance_score += 1

            relevant_comms.append({**comm, "relevance_score": relevance_score})

        # Sort by relevance
        relevant_comms.sort(key=lambda x: x["relevance_score"], reverse=True)

        # Create analysis result
        analysis_result = {
            "query_analysis": {
                "original_query": query,
                "interpreted_focus": query_analysis["primary_focus"],
                "query_type": query_analysis["query_type"]
            },
            "total_interactions": len(ENHANCED_COMMUNICATIONS_DATA),
            "focused_communications": [],
            "focused_timeline": [],
            "key_insights": [],
            "themes_analysis": {}
        }

        # Process top 6 most relevant communications
        for comm in relevant_comms[:6]:
            focused_comm = {
                "date": comm["date"],
                "type": comm["type"],
                "subject": comm["subject"],
                "summary": self._extract_focused_summary(comm, query_analysis),
                "sentiment": comm["sentiment"],
                "relevance_score": comm["relevance_score"]
            }
            analysis_result["focused_communications"].append(focused_comm)
            analysis_result["focused_timeline"].append({
                "date": comm["date"],
                "type": comm["type"],
                "summary": focused_comm["summary"],
                "relevance": comm["relevance_score"]
            })

        analysis_result["key_insights"] = self._generate_focused_insights(
            relevant_comms[:6], query_analysis)
        analysis_result["themes_analysis"] = self._analyze_themes_focused(
            relevant_comms[:6], query_analysis)

        return json.dumps(analysis_result, indent=2)

    def _extract_focused_summary(self, comm: Dict, query_analysis: Dict) -> str:
        """Extract summary focused on query"""
        focus = query_analysis["primary_focus"]

        text = comm.get("full_content", "") or ""
        subj = comm.get("subject", "Client communication")

        if focus == "esg_sustainability":
            if "ESG" in text or "values" in text or "sustainab" in text.lower():
                return "ESG/sustainability focus - family values alignment and implementation progress"
        elif focus == "family_personal":
            if "Northwestern" in text or "Linda" in text or "Emma" in text:
                return "Family milestone and involvement - Northwestern planning and engagement"
        elif focus == "performance":
            if "performance" in text.lower() or "return" in text.lower():
                return "Portfolio performance discussion and satisfaction with results"

        # Extract relevant sentence based on focus
        sentences = text.split('. ')
        for sentence in sentences:
            if focus == "esg_sustainability" and any(word in sentence.lower() for word in ["esg", "environmental", "sustainable", "values"]):
                return sentence.strip()[:100] + "..." if len(sentence) > 100 else sentence.strip()
            elif focus == "family_personal" and any(word in sentence for word in ["Emma", "Linda", "Northwestern", "family"]):
                return sentence.strip()[:100] + "..." if len(sentence) > 100 else sentence.strip()
            elif focus == "performance" and any(word in sentence.lower() for word in ["return", "performance", "portfolio"]):
                return sentence.strip()[:100] + "..." if len(sentence) > 100 else sentence.strip()

        return subj

    def _generate_focused_insights(self, communications: List[Dict], query_analysis: Dict) -> List[str]:
        """Generate insights focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Strong family commitment to ESG investing driven by Emma's environmental interests",
                "Successful VSGX transition with competitive performance vs VTIAX",
                "Client has become highly knowledgeable about ESG options through research",
                "Values alignment now as important as return optimization",
                "Family ready for expanded ESG options including green bonds"
            ]
        elif focus == "family_personal":
            return [
                "Northwestern acceptance represents successful long-term planning milestone",
                "Linda's involvement has strengthened family financial decision-making",
                "Emma's financial education accelerating through internship and coursework",
                "Family approaching investments as multi-generational strategy",
                "Strong collaborative approach to financial planning emerging"
            ]
        elif focus == "performance":
            return [
                "Consistent satisfaction with portfolio performance vs expectations",
                "Growing sophistication in performance evaluation and market analysis",
                "ESG integration achieved without performance sacrifice",
                "Performance discussions now include family goals context",
                "Strong risk-adjusted returns with controlled volatility"
            ]

        return [
            "Highly engaged client family with sophisticated financial discussions",
            "Successful integration of performance goals with values alignment",
            "Proactive communication and planning for major life milestones"
        ]

    def _analyze_themes_focused(self, communications: List[Dict], query_analysis: Dict) -> Dict:
        """Analyze themes with query focus"""
        theme_frequency = {}
        for comm in communications:
            for theme in comm["key_themes"]:
                theme_frequency[theme] = theme_frequency.get(theme, 0) + 1

        return {
            "most_frequent_themes": sorted(theme_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
            "sentiment_evolution": "Increasingly positive and engaged over time",
            "communication_pattern": "Regular proactive outreach with sophisticated questions"
        }


class ChromaFreePortfolioAnalyzer(BaseTool):
    name: str = "Chroma-Free Portfolio Performance Analyzer"
    description: str = "Analyzes portfolio performance with focus based on user query - no dependencies"

    def _run(self, query: str) -> str:
        """Analyze portfolio with query-specific focus"""

        query_analysis = analyze_query(query)
        print(
            f"📊 Portfolio analysis - Focus: {query_analysis['primary_focus']}")

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

        performance_data = self._get_performance_data(portfolio)

        focused_analysis = {
            "query_context": {
                "original_query": query,
                "analysis_focus": query_analysis["primary_focus"],
                "query_type": query_analysis["query_type"]
            },
            "portfolio_summary": {
                "total_return": performance_data["total_return"],
                "focused_metrics": self._get_focused_metrics(performance_data, query_analysis)
            },
            "fund_analysis": performance_data["fund_performance"],
            "ips_compliance": self._analyze_ips_compliance(performance_data),
            "recommendations": self._get_focused_recommendations(performance_data, query_analysis)
        }

        return json.dumps(focused_analysis, indent=2)

    def _get_performance_data(self, portfolio: Dict) -> Dict:
        """Get performance data with real Yahoo Finance calls and comprehensive fallbacks"""

        performance_data = {"fund_performance": {}, "total_return": 0}
        total_weighted_return = 0

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

        for ticker, details in portfolio["allocations"].items():
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
                else:
                    raise Exception("Insufficient data")

            except Exception as e:
                annual_return = fallback_data[ticker]["return"]
                volatility = fallback_data[ticker]["volatility"]
                print(
                    f"📋 Using fallback for {ticker}: {annual_return*100:.1f}%")

            weight = details["allocation"] / 100
            weighted_return = annual_return * weight
            total_weighted_return += weighted_return

            performance_data["fund_performance"][ticker] = {
                "name": details["name"],
                "allocation": details["allocation"],
                "annual_return": round(annual_return * 100, 2),
                "volatility": round(volatility * 100, 2),
                "weighted_contribution": round(weighted_return * 100, 2)
            }

        performance_data["total_return"] = round(
            total_weighted_return * 100, 2)
        return performance_data

    def _get_focused_metrics(self, performance_data: Dict, query_analysis: Dict) -> Dict:
        """Get metrics focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return {
                "esg_fund_performance": f"{performance_data['fund_performance']['VSGX']['annual_return']}% (VSGX)",
                "esg_allocation": "15% of portfolio in ESG funds",
                "transition_impact": "Minimal performance difference vs previous VTIAX allocation"
            }
        elif focus == "performance":
            return {
                "annual_return": f"{performance_data['total_return']}%",
                "vs_ips_target": "Within 7-9% target range" if 7 <= performance_data['total_return'] <= 9 else "Exceeding target range",
                "top_performer": "VGSLX at 15.3% return"
            }

        return {
            "annual_return": f"{performance_data['total_return']}%",
            "ips_status": "Compliant"
        }

    def _analyze_ips_compliance(self, performance_data: Dict) -> Dict:
        """Basic IPS compliance check"""
        total_return = performance_data["total_return"] / 100

        return {
            "return_compliance": {
                "current_return": f"{performance_data['total_return']}%",
                "ips_target": "7-9% annually",
                "status": "Compliant" if 0.07 <= total_return <= 0.09 else ("Exceeding" if total_return > 0.09 else "Below target")
            },
            "allocation_compliance": "Within IPS guidelines"
        }

    def _get_focused_recommendations(self, performance_data: Dict, query_analysis: Dict) -> List[str]:
        """Get recommendations based on query focus"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "ESG transition successful - VSGX performing competitively with VTIAX",
                "Consider expanding ESG integration to fixed income allocation with green bonds",
                "Monitor ESG fund performance vs benchmarks quarterly",
                "Explore impact investing opportunities beyond traditional ESG screening"
            ]
        elif focus == "performance":
            return [
                f"Outstanding {performance_data['total_return']}% return exceeding IPS targets",
                "All asset classes contributing positively to portfolio performance",
                "Maintain current allocation and rebalancing strategy",
                "Consider tax-loss harvesting opportunities as year-end approaches"
            ]

        return [
            "Portfolio performing well within IPS guidelines",
            "Continue current strategy and monitoring approach"
        ]


class ChromaFreeMeetingPrep(BaseTool):
    name: str = "Chroma-Free Meeting Preparation Generator"
    description: str = "Creates meeting materials focused on specific query topics - no dependencies"

    def _run(self, combined_data: str) -> str:
        """Generate meeting prep materials based on query focus"""

        # Extract query from task context
        try:
            query_match = re.search(
                r'The user has asked: "([^"]*)"', combined_data)
            query = query_match.group(
                1) if query_match else "What has happened with this account over the past year?"
        except:
            query = "What has happened with this account over the past year?"

        query_analysis = analyze_query(query)
        print(f"📋 Meeting prep - Focus: {query_analysis['primary_focus']}")

        meeting_prep = {
            "query_response": {
                "original_question": query,
                "query_focus": query_analysis["primary_focus"],
                "response_approach": query_analysis["query_type"]
            },
            "executive_summary": self._generate_focused_summary(query_analysis),
            "targeted_talking_points": self._generate_focused_talking_points(query_analysis),
            "action_items": self._generate_focused_actions(query_analysis),
            "conversation_starters": self._generate_conversation_starters(query_analysis)
        }

        return json.dumps(meeting_prep, indent=2)

    def _generate_focused_summary(self, query_analysis: Dict) -> str:
        """Generate summary focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return "ESG Integration Success Story: Smith Family Trust has successfully implemented ESG investing with VSGX performing competitively against traditional benchmarks. Emma's environmental interests are driving authentic family values alignment. The family has become sophisticated ESG researchers and are ready for expanded sustainable investing options including green bonds."
        elif focus == "family_personal":
            return "Family Milestone Achievement: Northwestern acceptance represents successful 18-year planning milestone. College funding secured and on track. Linda's engagement has strengthened family financial decision-making. Emma's financial education through internship has elevated family discussions. Multi-generational approach to planning established."
        elif focus == "performance":
            return "Outstanding Performance Results: Portfolio delivering 8.2% annual return, exceeding IPS targets and client expectations. ESG integration achieved without performance penalty. All asset classes contributing positively with excellent risk management. Strong foundation for continued success."

        return "Comprehensive Planning Success: Portfolio performing excellently with successful ESG integration and strong family engagement. All planning objectives being met or exceeded with clear path forward."

    def _generate_focused_talking_points(self, query_analysis: Dict) -> List[Dict]:
        """Generate talking points focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                {"priority": 1, "topic": "ESG Success Story",
                 "point": "VSGX performing at 5.8% - values achieved without return sacrifice"},
                {"priority": 2, "topic": "Family Leadership in Sustainability",
                 "point": "Emma's influence creating authentic investment alignment with environmental values"},
                {"priority": 3, "topic": "Expansion Opportunities",
                 "point": "Ready for green bonds and expanded ESG options based on family research"},
                {"priority": 4, "topic": "Impact Measurement",
                 "point": "Consider carbon footprint analysis and ESG impact reporting"}
            ]
        elif focus == "family_personal":
            return [
                {"priority": 1, "topic": "Northwestern Achievement",
                 "point": "Emma's acceptance represents successful 18-year planning milestone"},
                {"priority": 2, "topic": "Family Financial Team",
                 "point": "Linda's involvement has strengthened family decision-making process"},
                {"priority": 3, "topic": "Next Generation Education",
                 "point": "Emma's internship developing sophisticated financial understanding"},
                {"priority": 4, "topic": "Future Planning",
                 "point": "Multi-generational approach with quarterly family meetings established"}
            ]
        elif focus == "performance":
            return [
                {"priority": 1, "topic": "Exceptional Returns",
                 "point": "8.2% return significantly exceeding IPS midpoint target of 8%"},
                {"priority": 2, "topic": "Risk Management Excellence",
                 "point": "Strong performance achieved with well-controlled volatility at 12.8%"},
                {"priority": 3, "topic": "Diversification Success",
                 "point": "Every asset class adding positive value - no weak performers"},
                {"priority": 4, "topic": "ESG Integration Success",
                 "point": "Values alignment achieved without performance compromise"}
            ]

        return [
            {"priority": 1, "topic": "Overall Success",
             "point": "Portfolio and planning objectives being exceeded across all areas"},
            {"priority": 2, "topic": "Family Engagement",
             "point": "Strong multi-generational involvement in financial decisions"},
            {"priority": 3, "topic": "Future Positioning",
             "point": "Well positioned for all upcoming milestones and opportunities"}
        ]

    def _generate_focused_actions(self, query_analysis: Dict) -> List[str]:
        """Generate action items based on query focus"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Research green bond options for fixed income ESG integration",
                "Explore impact investing opportunities beyond traditional ESG screening",
                "Schedule ESG-focused family discussion with carbon footprint analysis",
                "Investigate proxy voting and shareholder engagement options"
            ]
        elif focus == "family_personal":
            return [
                "Finalize Northwestern college funding timeline and withdrawal strategy",
                "Schedule Linda's individual retirement planning session",
                "Create family financial education plan and regular meeting schedule",
                "Plan Emma's continued involvement in quarterly reviews"
            ]
        elif focus == "performance":
            return [
                "Continue quarterly performance monitoring vs benchmarks and IPS",
                "Maintain current allocation strategy with disciplined rebalancing",
                "Prepare detailed performance attribution analysis",
                "Review tax-loss harvesting opportunities before year-end"
            ]

        return [
            "Continue current successful strategy and monitoring approach",
            "Schedule next quarterly review meeting",
            "Prepare follow-up materials based on meeting discussion",
            "Monitor ongoing performance and market conditions"
        ]

    def _generate_conversation_starters(self, query_analysis: Dict) -> List[str]:
        """Generate conversation starters based on query focus"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Emma must be proud that your investments now reflect your family's environmental values...",
                "Your ESG research has been impressive - you've become quite the sustainability expert...",
                "How does it feel to have achieved values alignment without sacrificing returns?",
                "What are your thoughts on expanding ESG to your bond allocation with green bonds?"
            ]
        elif focus == "family_personal":
            return [
                "How are you feeling about Emma starting at Northwestern this fall?",
                "Linda, how has being more involved in the planning process felt for you?",
                "What has Emma learned from her internship that surprised you the most?",
                "How do you see your family's approach to financial planning evolving?"
            ]
        elif focus == "performance":
            return [
                "I'm excited to share your exceptional performance results - you've exceeded every target...",
                "How do you feel about the 8.2% return compared to your expectations?",
                "What aspects of this performance are you most pleased with?",
                "How comfortable are you with the current risk level given these strong returns?"
            ]

        return [
            "What aspects of this year's progress are you most proud of?",
            "How has your family's approach to financial planning evolved this year?",
            "What questions do you have about our strategy going forward?",
            "What are your priorities for the upcoming year?"
        ]

# ============================================================================
# CHROMA-FREE CREWAI AGENT DEFINITIONS
# ============================================================================


def create_chroma_free_milo_agents():
    """Create the chroma-free query-aware MILO agents"""

    communications_analyst = Agent(
        role='Chroma-Free Communications Analyst',
        goal='Analyze client communications with specific focus based on user queries using keyword matching',
        backstory="""You are an expert at analyzing client communications and adapting your analysis based on specific questions. You use sophisticated keyword matching and theme analysis to focus on what matters most. When asked about ESG concerns, you focus on sustainability themes. When asked about family matters, you highlight personal relationships and milestones.""",
        tools=[ChromaFreeCommunicationsAnalyzer()],
        verbose=True,
        allow_delegation=False
    )

    portfolio_analyst = Agent(
        role='Chroma-Free Portfolio Performance Analyst',
        goal='Provide portfolio analysis focused on specific aspects requested in queries',
        backstory="""You are a quantitative analyst who adapts analysis based on what's being asked. You focus on ESG performance when asked about sustainability, risk metrics when asked about volatility, and returns when asked about performance. You provide targeted insights using real market data when available.""",
        tools=[ChromaFreePortfolioAnalyzer()],
        verbose=True,
        allow_delegation=False
    )

    meeting_prep_specialist = Agent(
        role='Chroma-Free Meeting Preparation Specialist',
        goal='Create meeting materials that directly address specific questions raised in queries',
        backstory="""You create targeted meeting materials based on what advisors need to discuss. When they ask about ESG, you prepare ESG-focused talking points. When they ask about family matters, you emphasize personal milestones. You ensure materials directly respond to the specific question asked.""",
        tools=[ChromaFreeMeetingPrep()],
        verbose=True,
        allow_delegation=False
    )

    return communications_analyst, portfolio_analyst, meeting_prep_specialist


def create_chroma_free_milo_tasks(communications_analyst, portfolio_analyst, meeting_prep_specialist, user_query: str):
    """Create enhanced tasks that incorporate user query"""

    communications_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Analyze Smith Family Trust communications to specifically address this question. Focus on communications most relevant to the query topic using keyword matching and theme analysis.
        """,
        agent=communications_analyst,
        expected_output=f"Targeted communications analysis focused on: '{user_query}'"
    )

    portfolio_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Analyze portfolio performance with specific focus on answering this question. Use real market data when available and adapt analysis based on query focus.
        """,
        agent=portfolio_analyst,
        expected_output=f"Focused portfolio analysis addressing: '{user_query}'"
    )

    meeting_prep_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Create meeting preparation materials that directly respond to this question. Generate talking points and action items focused on the query topic.
        """,
        agent=meeting_prep_specialist,
        expected_output=f"Meeting prep package designed to address: '{user_query}'",
        context=[communications_task, portfolio_task]
    )

    return communications_task, portfolio_task, meeting_prep_task


def create_chroma_free_milo_crew(user_query: str):
    """Create chroma-free MILO crew with query awareness"""

    communications_analyst, portfolio_analyst, meeting_prep_specialist = create_chroma_free_milo_agents()

    communications_task, portfolio_task, meeting_prep_task = create_chroma_free_milo_tasks(
        communications_analyst, portfolio_analyst, meeting_prep_specialist, user_query
    )

    milo_crew = Crew(
        agents=[communications_analyst,
                portfolio_analyst, meeting_prep_specialist],
        tasks=[communications_task, portfolio_task, meeting_prep_task],
        process=Process.sequential,
        verbose=2
    )

    return milo_crew

# ============================================================================
# MAIN EXECUTION FUNCTIONS
# ============================================================================


def execute_chroma_free_milo_analysis(
    client_name: str = "Smith Family Trust",
    user_query: str = "What has happened with this account over the past year?"
):
    """Main function to execute chroma-free query-aware MILO analysis"""

    print(f"🤖 MILO: Chroma-free analysis for {client_name}")
    print(f"📋 Query: {user_query}")

    query_analysis = analyze_query(user_query)
    print(f"🎯 Query Focus: {query_analysis['primary_focus']}")
    print("=" * 80)

    try:
        crew = create_chroma_free_milo_crew(user_query)

        result = crew.kickoff(inputs={
            'client_name': client_name,
            'query': user_query,
            'query_focus': query_analysis['primary_focus']
        })

        print("\n" + "=" * 80)
        print("🎯 MILO CHROMA-FREE ANALYSIS COMPLETE")
        print("=" * 80)

        return result

    except Exception as e:
        print(f"❌ Error in chroma-free MILO analysis: {str(e)}")
        return None


# Alias for compatibility
execute_enhanced_milo_analysis = execute_chroma_free_milo_analysis

if __name__ == "__main__":
    test_queries = [
        "What are the client's ESG concerns?",
        "How has the portfolio performed this year?",
        "What family changes should I know about?",
        "What has happened with this account over the past year?"
    ]

    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        result = execute_chroma_free_milo_analysis(user_query=query)
        if result:
            print("✅ Success!")
        print("-" * 40)
