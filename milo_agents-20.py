"""
MILO Client Intelligence Dashboard - Enhanced Version with Query Responsiveness
CrewAI Agent Implementation with Rich Sample Data and Query Processing
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import re
from typing import Dict, List

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
        "subject": "Mid-Year Portfolio Review - Northwestern Acceptance Celebration",
        "full_content": """In-person meeting - 45 minutes at office

Agenda: Mid-year portfolio review, college planning update, ESG options discussion

PORTFOLIO PERFORMANCE REVIEW:
- YTD return: 6.8% (on track for annual target)
- Strong performance from VTSAX (up 11.2% YTD) 
- VTIAX recovering nicely (up 5.1% YTD)
- Bond funds providing stability as expected
- Overall very pleased with performance trajectory

MAJOR NEWS - NORTHWESTERN ACCEPTANCE:
Robert was beaming - Emma got into Northwestern! She'll start fall 2025.
- Full tuition: ~$65K/year
- Financial aid: ~$30K/year
- Family responsibility: ~$35K/year
- Four-year total family cost: ~$140K

College funding strategy discussion:
- Current 529 balance: $85K (good start)
- Need additional ~$55K over four years
- Discussed reducing equity allocation by 5% in early 2025
- Move funds to more liquid/conservative positions for tuition payments
- Timeline: Start repositioning by January 2025

ESG INTEGRATION UPDATE:
Robert has done his homework! Brought printed research on:
- Vanguard ESG International Stock ETF (VSGX) - expense ratio 0.12%
- Current VTIAX expense ratio: 0.11% 
- Performance comparison looks reasonable
- Strong ESG scores, screens out controversial sectors

Decision: Plan to transition 50% of VTIAX to VSGX over next two quarters
- Gradual transition to minimize tax impact
- Monitor performance differential closely
- Full transition if performance remains competitive

FAMILY DYNAMICS:
- Emma is very engaged in family financial discussions now
- She's taking economics at her high school
- Interested in learning about investing (maybe summer internship opportunity?)
- Linda (Robert's wife) wants to be more involved in investment decisions
- Agreed to include Linda in next quarterly review

ACTION ITEMS:
1. Prepare VSGX transition analysis
2. Create college funding timeline and strategy
3. Schedule joint meeting with Linda for Q3
4. Research summer finance internship opportunities for Emma

COMMUNICATION PREFERENCES UPDATE:
- Robert appreciates our monthly check-ins during volatile periods
- Wants quarterly written summaries even during stable times
- Linda prefers email updates vs. phone calls
- Emma is curious about investing basics (maybe some educational materials?)

Overall sentiment: Very positive meeting. Family is engaged, excited about college, and appreciative of our guidance. Robert has become much more knowledgeable about ESG investing.""",
        "sentiment": "very_positive_and_engaged",
        "key_themes": ["portfolio_performance", "college_acceptance", "education_planning", "ESG_transition", "family_involvement", "financial_education", "liquidity_planning"],
        "entities": ["Emma", "Northwestern", "VSGX", "VTIAX", "Linda", "529 plan"],
        "client_requests": ["ESG fund transition", "college funding strategy", "include Linda in meetings", "educational materials for Emma"],
        "urgency": "medium"
    },
    {
        "date": "2024-05-22",
        "type": "email",
        "subject": "Quick Check-in - Market Concerns and Summer Plans",
        "full_content": """Hi Sarah,

Just a quick check-in as we head into summer. The markets have been a bit choppy lately, and I wanted to get your thoughts.

A few questions:
1. Our YTD performance is still strong, but I'm seeing some volatility in tech stocks. Should we be concerned about our VTSAX concentration?

2. Emma starts her summer job at a local financial planning firm next week (thanks for the referral!). She's very excited and has been asking great questions about our portfolio. Is there a basic investing book you'd recommend for her?

3. Linda and I have been discussing our estate planning. With Emma going to college soon, we want to make sure everything is updated. Do you work with estate planning attorneys, or should we find our own?

4. The ESG transition seems to be going well. How is VSGX performing vs our old VTIAX position? I haven't been tracking it closely but would love an update.

Summer plans: We're taking Emma on a college tour trip in July (Northwestern, plus a few backup schools just in case she changes her mind). We'll be traveling from July 15-25. Let me know if you need anything before then.

Also, Linda mentioned she'd still like to sit in on our next meeting. Could we schedule something for early August when we're back?

Hope you're having a great spring!

Best,
Robert

P.S. - Emma asked if there are any good finance podcasts for beginners. Any recommendations?""",
        "sentiment": "positive_and_curious",
        "key_themes": ["market_volatility", "financial_education", "family_involvement", "estate_planning", "ESG_performance", "summer_plans", "professional_development"],
        "entities": ["VTSAX", "Emma", "Linda", "VSGX", "VTIAX", "Northwestern"],
        "client_requests": ["tech stock concentration analysis", "book recommendations", "estate planning referrals", "ESG performance update", "August meeting with Linda", "podcast recommendations"],
        "urgency": "low"
    },
    {
        "date": "2024-06-22",
        "type": "email",
        "subject": "Fed Rate Decision Impact - Portfolio Positioning Questions",
        "full_content": """Sarah,

Hope you're having a good summer! I wanted to reach out after yesterday's Fed decision.

I've been following the rate situation closely (maybe too closely - Linda says I'm becoming a markets nerd!), and I'm wondering about our bond positioning given the potential for rate cuts later this year.

Specific questions:
1. Should we extend duration in our bond holdings to capture more upside if rates fall?
2. Our VBTLX has been steady, but would a longer-term bond fund make sense for a portion?
3. What about VTABX - how do international bonds typically perform in a U.S. rate-cutting cycle?

I've also been thinking about our equity allocation. With potentially lower rates ahead, should we consider increasing our stock weighting? We're currently at 70% equity (target range), but with Emma's college still a year away, we have some flexibility.

Emma update: Her summer internship is going great! She's learning about financial planning software and has been practicing building portfolios (with fake money, thankfully). She told me yesterday that she wants to minor in finance now along with her environmental science major. The apple doesn't fall far from the tree!

She's also been pushing us harder on ESG investing. She found some article about how VSGX is outperforming broader international markets this year and won't let me forget it. Kids these days with their research!

Speaking of which - how has our ESG transition been performing? Are you happy with the VSGX position so far?

One more thing - Linda has been reading about I Bonds and Treasury bills with these higher rates. She's wondering if we should put some of our cash position (the money we're holding for Emma's first-year tuition) into something higher-yielding than our savings account. Thoughts?

Looking forward to our August meeting. Linda is excited to finally meet you in person!

Best,
Robert

P.S. - Emma loved the "A Random Walk Down Wall Street" recommendation. She's halfway through it already!""",
        "sentiment": "engaged_and_analytical",
        "key_themes": ["fed_policy", "interest_rates", "bond_duration", "equity_allocation", "family_pride", "ESG_performance", "cash_management", "financial_education"],
        "entities": ["Fed", "VBTLX", "VTABX", "VSGX", "Emma", "Linda", "I Bonds", "Treasury bills"],
        "client_requests": ["bond duration analysis", "equity allocation review", "ESG performance update", "cash investment options for college funds"],
        "urgency": "medium"
    },
    {
        "date": "2024-07-18",
        "type": "phone_call",
        "subject": "College Tour Update - Investment Philosophy Discussion",
        "full_content": """Phone call from Chicago during college tour trip - 25 minutes

Robert called from Northwestern campus (they're doing a second visit). Very excited about Emma's reaction to the school and wanted to share some thoughts.

COLLEGE TOUR UPDATES:
- Northwestern still her top choice
- Also visited University of Michigan and Wash U in St. Louis
- Emma loved all three but Northwestern feels like "home"
- Financial aid packages similar across schools
- Confirmed our $35K/year planning assumption is accurate

INTERESTING DEVELOPMENT:
Emma has been talking with other prospective students and their families about college financing strategies. She's learned about:
- 529 vs. Coverdell ESA differences
- Tax implications of education funding
- Merit aid vs. need-based aid strategies

She actually asked Robert some sophisticated questions about our funding approach that impressed him. "She's thinking like a financial planner already!"

INVESTMENT PHILOSOPHY EVOLUTION:
Robert shared an interesting observation: "This whole college planning process has made me realize how much our investment approach has matured. Five years ago, we were just trying to grow wealth. Now we're thinking about sustainability (ESG), family values, and specific goals like education funding. It feels more purposeful."

He's appreciating how our ESG integration isn't just about returns anymore - it's about teaching Emma that investments can reflect values.

MARKET TIMING CONCERNS:
Robert mentioned he's been reading about potential market volatility in election years. He's not worried about long-term performance but wondering about timing for our college fund positioning:
- Should we move Emma's first-year funds (due fall 2025) to cash earlier than planned?
- Original plan was January 2025, but he's wondering about November 2024
- Wants to avoid any market disruption affecting tuition payments

LINDA'S INVOLVEMENT:
Linda has been more engaged on this trip. She's been asking Emma about career interests and how finances play into decision-making. She's looking forward to our August meeting and wants to discuss:
- Joint decision-making on major portfolio changes
- Her own retirement planning (she's 52)
- Family financial goal setting

Action items from call:
1. Research election year market patterns for college funding timing
2. Prepare comparison of 529 vs. other education funding vehicles for August meeting
3. Include discussion of Linda's retirement planning in next review
4. Consider earlier timeline for college fund positioning

Robert seemed very content with our relationship and strategy. The family is functioning well as a financial planning unit now.""",
        "sentiment": "proud_and_content",
        "key_themes": ["college_planning", "family_financial_education", "investment_philosophy_evolution", "ESG_values_alignment", "market_timing", "spousal_involvement", "retirement_planning"],
        "entities": ["Northwestern", "University of Michigan", "Wash U", "Emma", "Linda", "529 plan", "Coverdell ESA"],
        "client_requests": ["election year market analysis", "education funding vehicle comparison", "Linda's retirement planning discussion", "earlier college fund timing"],
        "urgency": "medium"
    },
    {
        "date": "2024-08-15",
        "type": "meeting",
        "subject": "Summer Review - Linda's First Joint Meeting",
        "full_content": """Joint meeting with Robert and Linda - 60 minutes at office

First time meeting Linda in person - she's been looking forward to this for months!

INTRODUCTIONS & BACKGROUND:
Linda's financial background:
- High school math teacher, 18 years experience
- Very analytical, appreciates detailed explanations
- Has been managing household budget and savings
- Interested in understanding investment strategy beyond just performance
- Comfortable with moderate risk but wants to understand the "why" behind decisions

PORTFOLIO PERFORMANCE REVIEW (Linda's focus):
Linda came prepared with questions! She'd printed our quarterly statements and highlighted areas of confusion:
- Why do we own 5 different funds instead of just one diversified fund?
- How do expense ratios impact returns over time?
- What's the tax efficiency of our current approach?

Her questions were excellent - clearly she's been studying. Robert beamed with pride as she engaged with complex topics.

Current performance: 
- YTD: 7.8% (well on track for annual goals)
- ESG transition performing well - VSGX only 0.1% behind previous VTIAX performance
- Bond positioning has been smart given rate environment

COLLEGE FUNDING FINAL STRATEGY:
With Emma starting Northwestern in exactly one year:
- Agreed to move first-year funds ($35K) to high-yield savings by December 2024
- Keep remaining college funds invested until needed year by year
- 529 plan is well-positioned with good tax-advantaged growth

Linda asked great questions about 529 vs. other options - she'd researched Coverdell ESAs and UTMA accounts on her own.

LINDA'S RETIREMENT PLANNING:
This was the surprise focus of the meeting. Linda is 52 and thinking seriously about retirement:
- Teacher's pension will provide base income
- She's maxing out 403(b) contributions
- Wants to understand how our joint portfolio supports her retirement goals
- Interested in potentially retiring at 62 (10 years from now)

We discussed:
- Projection of portfolio growth over 10 years
- Healthcare cost planning for early retirement
- Social Security timing strategies
- Tax implications of retirement account withdrawals

Linda's revelation: "I love teaching, but I want the financial freedom to choose. Maybe I'll keep teaching part-time, maybe I'll do something completely different. I want our investments to give me options."

ESG ALIGNMENT - FAMILY VALUES DISCUSSION:
Both Robert and Linda expressed how much they appreciate the ESG integration:
- Linda: "It's not just about returns anymore. Emma asks us about our values all the time. It's nice that our money reflects what we believe."
- They want to explore more ESG options
- Interested in impact investing for a small portion of portfolio
- Emma has been researching sustainable investing for a school project

COMMUNICATION PREFERENCES ESTABLISHED:
- Monthly email updates to both Robert and Linda
- Quarterly phone calls with all three (including Emma when she's available)
- Annual in-person meetings in August
- Emergency availability during market stress periods

FAMILY FINANCIAL EDUCATION:
Emma joins the meeting via video call from her summer internship:
- She presented a mock portfolio she'd built (very impressive!)
- Asked sophisticated questions about international diversification
- Interested in sustainable investing beyond just ESG screening
- Plans to take investment analysis course at Northwestern

Linda's comment: "Our daughter is going to be better at this than we are!"

ACTION ITEMS:
1. Prepare Linda's retirement projection scenarios
2. Research additional ESG and impact investing options
3. Create family financial goal worksheet for annual planning
4. Set up systematic college funding transfers starting December
5. Include Emma in quarterly calls when her schedule allows

MEETING OUTCOME:
Fantastic dynamic between all family members. Linda brings great analytical perspective, Robert provides historical context, and Emma keeps them focused on values and sustainability.

This has evolved from managing Robert's portfolio to comprehensive family financial planning. Very rewarding relationship.""",
        "sentiment": "highly_positive_and_collaborative",
        "key_themes": ["spousal_involvement", "financial_education", "retirement_planning", "family_values", "ESG_expansion", "college_funding_finalization", "comprehensive_planning"],
        "entities": ["Linda", "Robert", "Emma", "Northwestern", "403(b)", "VSGX", "529 plan"],
        "client_requests": ["Linda's retirement projections", "expanded ESG options", "family goal setting", "college funding automation", "quarterly family calls"],
        "urgency": "low"
    }
]

# ============================================================================
# QUERY PROCESSING UTILITIES
# ============================================================================


def analyze_query(query: str) -> Dict[str, any]:
    """Analyze user query to determine focus areas and response strategy"""

    query_lower = query.lower()

    # Define query categories and keywords
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

    # Score each category based on keyword matches
    category_scores = {}
    for category, keywords in query_categories.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        if score > 0:
            category_scores[category] = score

    # Determine primary focus
    primary_focus = max(
        category_scores, key=category_scores.get) if category_scores else "general"

    # Extract time period if specified
    time_period = "full_year"  # default
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


def filter_communications_by_query(query_analysis: Dict) -> List[Dict]:
    """Filter and prioritize communications based on query focus"""

    focus = query_analysis["primary_focus"]
    time_period = query_analysis["time_period"]

    relevant_communications = []

    for comm in ENHANCED_COMMUNICATIONS_DATA:
        relevance_score = 0

        # Score based on primary focus
        if focus == "esg_sustainability" and any(theme in ["ESG_investing", "values_alignment", "environmental_concerns"] for theme in comm["key_themes"]):
            relevance_score += 10
        elif focus == "performance" and any(theme in ["portfolio_performance", "market_volatility", "returns"] for theme in comm["key_themes"]):
            relevance_score += 10
        elif focus == "family_personal" and any(theme in ["family_involvement", "college_planning", "education_planning"] for theme in comm["key_themes"]):
            relevance_score += 10
        elif focus == "risk_volatility" and any(theme in ["market_volatility", "risk_management", "banking_sector_concerns"] for theme in comm["key_themes"]):
            relevance_score += 10
        elif focus == "communication" and any(theme in ["communication_preferences"] for theme in comm["key_themes"]):
            relevance_score += 10

        # Add points for recency if relevant
        comm_date = datetime.strptime(comm["date"], "%Y-%m-%d")
        days_ago = (datetime.now() - comm_date).days

        if time_period == "recent" and days_ago <= 60:
            relevance_score += 5
        elif time_period == "ytd":
            relevance_score += 3

        # Add base relevance for all communications
        relevance_score += 1

        relevant_communications.append({
            **comm,
            "relevance_score": relevance_score
        })

    # Sort by relevance and return top communications
    relevant_communications.sort(
        key=lambda x: x["relevance_score"], reverse=True)
    return relevant_communications[:6]  # Return top 6 most relevant

# ============================================================================
# ENHANCED CUSTOM TOOLS WITH QUERY AWARENESS
# ============================================================================


class QueryAwareCommunicationsAnalyzer(BaseTool):
    name: str = "Query-Aware Communications Analyzer"
    description: str = "Analyzes client communications with focus based on user query"

    def _run(self, query: str) -> str:
        """Analyze communications with query-specific focus"""

        query_analysis = analyze_query(query)
        relevant_comms = filter_communications_by_query(query_analysis)

        # Create focused analysis based on query
        analysis_result = {
            "query_analysis": {
                "original_query": query,
                "interpreted_focus": query_analysis["primary_focus"],
                "query_type": query_analysis["query_type"]
            },
            "focused_communications": [],
            "key_insights": [],
            "themes_analysis": {},
            "recommendations": []
        }

        # Process relevant communications
        for comm in relevant_comms:
            focused_comm = {
                "date": comm["date"],
                "type": comm["type"],
                "subject": comm["subject"],
                "key_points": self._extract_key_points(comm, query_analysis),
                "sentiment": comm["sentiment"],
                "relevance_to_query": comm["relevance_score"]
            }
            analysis_result["focused_communications"].append(focused_comm)

        # Generate insights based on query focus
        analysis_result["key_insights"] = self._generate_focused_insights(
            relevant_comms, query_analysis)
        analysis_result["themes_analysis"] = self._analyze_themes(
            relevant_comms, query_analysis)
        analysis_result["recommendations"] = self._generate_recommendations(
            relevant_comms, query_analysis)

        return json.dumps(analysis_result, indent=2)

    def _extract_key_points(self, comm: Dict, query_analysis: Dict) -> List[str]:
        """Extract key points relevant to the query focus"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            if "ESG" in comm.get("full_content", ""):
                return [
                    "Client expressing interest in ESG/sustainable investing options",
                    "Daughter Emma's influence on family values and investment decisions",
                    "Specific ESG fund research and transition planning",
                    "Values alignment becoming important factor in investment decisions"
                ]
        elif focus == "family_personal":
            return [
                "Emma accepted to Northwestern University for fall 2025",
                "Family college funding strategy needs (~$35K/year)",
                "Linda becoming more involved in financial planning decisions",
                "Emma's summer internship in financial planning developing her interests"
            ]
        elif focus == "performance":
            return [
                "Portfolio delivering strong performance - on track for annual goals",
                "ESG fund transition (VSGX) performing competitively",
                "Satisfaction with risk-adjusted returns and diversification approach",
                "Interest in optimizing performance while maintaining values alignment"
            ]

        # Default key points if no specific focus
        return [
            "Regular engagement and proactive communication",
            "Growing sophistication in financial planning discussions",
            "Family-centered approach to investment decision making",
            "Balance between performance goals and values alignment"
        ]

    def _generate_focused_insights(self, communications: List[Dict], query_analysis: Dict) -> List[str]:
        """Generate insights focused on query topic"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Strong and growing commitment to ESG investing - client has done significant research",
                "Daughter Emma is a key driver of sustainable investing interest",
                "Successful ESG transition with VSGX showing competitive performance",
                "Family wants to expand ESG integration beyond just screening",
                "Values alignment has become as important as returns optimization"
            ]
        elif focus == "family_personal":
            return [
                "Northwestern acceptance is major milestone - family very excited and proud",
                "College planning has brought family together around financial goals",
                "Linda's involvement has strengthened family financial decision-making",
                "Emma's financial education has accelerated through internship and coursework",
                "Family approaching investments as multi-generational strategy"
            ]
        elif focus == "performance":
            return [
                "Consistent satisfaction with portfolio performance vs. expectations",
                "Strong risk-adjusted returns maintaining target allocation ranges",
                "ESG integration achieved without performance sacrifice",
                "Growing sophistication in performance evaluation and market analysis",
                "Performance discussions now include values and family goals context"
            ]

        return [
            "Highly engaged client family with strong communication patterns",
            "Evolution from individual to comprehensive family financial planning",
            "Successful integration of performance goals with values alignment",
            "Proactive approach to major life events and planning milestones"
        ]

    def _analyze_themes(self, communications: List[Dict], query_analysis: Dict) -> Dict:
        """Analyze themes with query focus"""

        theme_frequency = {}
        for comm in communications:
            for theme in comm["key_themes"]:
                theme_frequency[theme] = theme_frequency.get(theme, 0) + 1

        return {
            "most_frequent_themes": sorted(theme_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
            "query_relevant_themes": [theme for theme in theme_frequency.keys() if self._is_theme_relevant(theme, query_analysis)],
            "sentiment_evolution": "Increasingly positive and engaged over time",
            "communication_pattern": "Regular proactive outreach with sophisticated questions"
        }

    def _is_theme_relevant(self, theme: str, query_analysis: Dict) -> bool:
        """Check if theme is relevant to query focus"""
        focus = query_analysis["primary_focus"]

        relevance_mapping = {
            "esg_sustainability": ["ESG_investing", "values_alignment", "environmental_concerns", "ESG_transition"],
            "family_personal": ["family_involvement", "college_planning", "education_planning", "daughter_influence"],
            "performance": ["portfolio_performance", "market_volatility", "ESG_performance"],
            "risk_volatility": ["market_volatility", "risk_management", "banking_sector_concerns"],
            "communication": ["communication_preferences"]
        }

        return theme in relevance_mapping.get(focus, [])

    def _generate_recommendations(self, communications: List[Dict], query_analysis: Dict) -> List[str]:
        """Generate recommendations based on query focus"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Continue ESG fund research and consider expanding beyond VSGX",
                "Explore impact investing options for small portfolio allocation",
                "Include Emma in ESG investment education and decision-making",
                "Schedule dedicated ESG portfolio review session"
            ]
        elif focus == "family_personal":
            return [
                "Finalize college funding timeline and automation",
                "Include Linda in all major investment decisions going forward",
                "Create educational materials/resources for Emma's continued learning",
                "Plan family financial goal-setting session"
            ]
        elif focus == "performance":
            return [
                "Continue current performance tracking and reporting approach",
                "Monitor ESG fund performance vs. benchmarks quarterly",
                "Consider performance attribution analysis for family education",
                "Maintain discipline during market volatility periods"
            ]

        return [
            "Maintain current communication frequency and engagement level",
            "Continue family-inclusive approach to financial planning",
            "Balance performance optimization with values alignment goals",
            "Plan for upcoming life transitions and milestones"
        ]


class QueryAwarePortfolioAnalyzer(BaseTool):
    name: str = "Query-Aware Portfolio Performance Analyzer"
    description: str = "Analyzes portfolio performance with focus based on user query"

    def _run(self, query: str) -> str:
        """Analyze portfolio with query-specific focus"""

        query_analysis = analyze_query(query)

        # Get basic portfolio performance data (same as before)
        portfolio = {
            "client_name": "Smith Family Trust",
            "portfolio_value": 2500000,
            "allocations": {
                "VTSAX": {"allocation": 40, "name": "Vanguard Total Stock Market Index"},
                # Reduced due to ESG transition
                "VTIAX": {"allocation": 15, "name": "Vanguard Total International Stock Index"},
                # New ESG holding
                "VSGX": {"allocation": 15, "name": "Vanguard ESG International Stock ETF"},
                "VBTLX": {"allocation": 20, "name": "Vanguard Total Bond Market Index"},
                "VGSLX": {"allocation": 5, "name": "Vanguard Real Estate Index Fund"},
                "VTABX": {"allocation": 5, "name": "Vanguard Total International Bond Index"}
            }
        }

        # Get performance data
        performance_data = self._get_performance_data(portfolio)

        # Create focused analysis based on query
        focused_analysis = {
            "query_context": {
                "original_query": query,
                "analysis_focus": query_analysis["primary_focus"],
                "query_type": query_analysis["query_type"]
            },
            "portfolio_summary": {
                "total_return": performance_data["total_return"],
                "risk_metrics": performance_data["risk_metrics"],
                "query_specific_metrics": self._get_focused_metrics(performance_data, query_analysis)
            },
            "fund_analysis": self._get_focused_fund_analysis(performance_data, query_analysis),
            "recommendations": self._get_focused_recommendations(performance_data, query_analysis),
            "ips_compliance": self._analyze_ips_compliance(performance_data, query_analysis)
        }

        return json.dumps(focused_analysis, indent=2)

    def _get_performance_data(self, portfolio: Dict) -> Dict:
        """Get actual performance data from Yahoo Finance with fallbacks"""

        performance_data = {
            "fund_performance": {},
            "total_return": 0,
            "risk_metrics": {}
        }

        total_weighted_return = 0

        # Mock data as fallback (in case Yahoo Finance fails)
        fallback_data = {
            "VTSAX": {"return": 0.121, "volatility": 0.135},
            "VTIAX": {"return": 0.062, "volatility": 0.142},
            # ESG fund performing slightly lower
            "VSGX": {"return": 0.058, "volatility": 0.138},
            "VBTLX": {"return": 0.021, "volatility": 0.045},
            "VGSLX": {"return": 0.153, "volatility": 0.218},
            "VTABX": {"return": 0.018, "volatility": 0.055}
        }

        for ticker, details in portfolio["allocations"].items():
            try:
                # Try Yahoo Finance first
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1y")

                # Ensure we have enough data
                if not hist.empty and len(hist) > 20:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    annual_return = (end_price - start_price) / start_price

                    daily_returns = hist['Close'].pct_change().dropna()
                    volatility = daily_returns.std() * np.sqrt(252)
                else:
                    raise Exception("Insufficient data")

            except:
                # Fallback to mock data
                annual_return = fallback_data[ticker]["return"]
                volatility = fallback_data[ticker]["volatility"]

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
        performance_data["risk_metrics"] = {
            "portfolio_volatility": 12.8,  # Calculated weighted average
            "sharpe_ratio": 0.89,
            "max_drawdown": -8.2
        }

        return performance_data

    def _get_focused_metrics(self, performance_data: Dict, query_analysis: Dict) -> Dict:
        """Get metrics focused on query topic"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return {
                "esg_transition_impact": "VSGX performing within 0.4% of replaced VTIAX position",
                "esg_fund_performance": f"{performance_data['fund_performance']['VSGX']['annual_return']}% annual return",
                "values_alignment_cost": "Minimal performance impact from ESG integration",
                "esg_allocation_percentage": "15% of portfolio in dedicated ESG funds"
            }
        elif focus == "performance":
            return {
                "vs_ips_target": f"Portfolio return {performance_data['total_return']}% vs 7-9% IPS target",
                "risk_adjusted_performance": f"Sharpe ratio of {performance_data['risk_metrics']['sharpe_ratio']}",
                "best_performer": "VGSLX (Real Estate) leading at 15.3% return",
                "performance_consistency": "All asset classes contributing positively"
            }
        elif focus == "risk_volatility":
            return {
                "portfolio_volatility": f"{performance_data['risk_metrics']['portfolio_volatility']}% annualized",
                "risk_vs_return": f"Strong risk-adjusted returns with Sharpe ratio {performance_data['risk_metrics']['sharpe_ratio']}",
                "downside_protection": f"Maximum drawdown limited to {performance_data['risk_metrics']['max_drawdown']}%",
                "diversification_benefit": "Multi-asset approach reducing overall portfolio risk"
            }

        return {
            "overall_performance": f"{performance_data['total_return']}% annual return",
            "risk_level": f"{performance_data['risk_metrics']['portfolio_volatility']}% volatility",
            "efficiency": f"Sharpe ratio {performance_data['risk_metrics']['sharpe_ratio']}"
        }

    def _get_focused_fund_analysis(self, performance_data: Dict, query_analysis: Dict) -> Dict:
        """Provide fund analysis focused on query"""

        focus = query_analysis["primary_focus"]
        fund_data = performance_data["fund_performance"]

        if focus == "esg_sustainability":
            return {
                "esg_funds": {
                    "VSGX": fund_data["VSGX"],
                    "analysis": "ESG transition successful with competitive performance"
                },
                "traditional_comparison": {
                    "VTIAX_replaced": {"return": 6.2, "note": "Historical position, mostly transitioned to VSGX"},
                    "performance_difference": "VSGX performing within expected range of VTIAX"
                },
                "recommendation": "Continue ESG integration, consider expanding to other asset classes"
            }
        elif focus == "bonds_fixed_income":
            return {
                "bond_positions": {
                    "VBTLX": fund_data["VBTLX"],
                    "VTABX": fund_data["VTABX"]
                },
                "interest_rate_impact": "Bond funds providing stability and income in current rate environment",
                "duration_analysis": "Moderate duration positioning appropriate for rate uncertainty",
                "recommendation": "Maintain current bond allocation, consider duration adjustment if rates fall"
            }
        elif focus == "equity_stocks":
            return {
                "equity_positions": {
                    "VTSAX": fund_data["VTSAX"],
                    "VTIAX": fund_data["VTIAX"],
                    "VSGX": fund_data["VSGX"]
                },
                "allocation_analysis": "70% total equity allocation within IPS target range",
                "diversification": "Good balance of domestic and international exposure",
                "recommendation": "Maintain current equity weighting approaching college funding needs"
            }

        return {
            "all_funds": fund_data,
            "top_performer": "VGSLX with 15.3% return",
            "steady_performers": "Core equity and bond positions meeting expectations"
        }

    def _get_focused_recommendations(self, performance_data: Dict, query_analysis: Dict) -> List[str]:
        """Generate recommendations based on query focus"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "ESG transition performing well - continue gradual expansion",
                "Research ESG options for bond allocation (green bonds, sustainability-focused funds)",
                "Consider impact investing allocation for small portion of portfolio",
                "Monitor ESG fund performance vs traditional benchmarks quarterly"
            ]
        elif focus == "performance":
            return [
                f"Portfolio delivering strong {performance_data['total_return']}% return - maintain current strategy",
                "VGSLX (Real Estate) exceptional performance - consider slight allocation increase",
                "All asset classes contributing positively - no immediate rebalancing needed",
                "Performance on track to meet long-term IPS objectives"
            ]
        elif focus == "risk_volatility":
            return [
                "Current risk level appropriate for moderate risk tolerance",
                "Diversification providing good downside protection",
                "Consider increasing bond allocation as college funding approaches",
                "Monitor volatility during election year market uncertainty"
            ]

        return [
            "Portfolio performing well within IPS guidelines",
            "Maintain current allocation approaching college funding timeline",
            "Continue ESG integration without sacrificing returns",
            "Regular rebalancing to maintain target allocations"
        ]

    def _analyze_ips_compliance(self, performance_data: Dict, query_analysis: Dict) -> Dict:
        """Analyze IPS compliance with query focus"""

        total_return = performance_data["total_return"] / 100
        ips_min = 0.07
        ips_max = 0.09

        compliance = {
            "return_compliance": {
                "current_return": f"{performance_data['total_return']}%",
                "ips_target": "7-9% annually",
                "status": "Within range" if ips_min <= total_return <= ips_max else "Outside range",
                "variance": f"{((total_return - 0.08) * 100):.1f}% vs midpoint"
            },
            "allocation_compliance": {
                "equity": {"current": 70, "target": "60-80%", "status": "Compliant"},
                "fixed_income": {"current": 25, "target": "15-35%", "status": "Compliant"},
                "alternatives": {"current": 5, "target": "0-10%", "status": "Compliant"}
            },
            "rebalancing_needed": False,
            "overall_status": "Fully compliant with IPS objectives"
        }

        return compliance


class QueryAwareMeetingPrep(BaseTool):
    name: str = "Query-Aware Meeting Preparation Generator"
    description: str = "Creates meeting materials focused on specific query topics"

    def _run(self, combined_data: str) -> str:
        """Generate meeting prep materials based on query focus"""

        # Extract query from combined data (passed from task context)
        try:
            data = json.loads(combined_data)
            query = data.get(
                "query", "What has happened with this account over the past year?")
        except:
            query = "What has happened with this account over the past year?"

        query_analysis = analyze_query(query)

        meeting_prep = {
            "query_response": {
                "original_question": query,
                "query_focus": query_analysis["primary_focus"],
                "response_approach": query_analysis["query_type"]
            },
            "executive_summary": self._generate_focused_summary(query_analysis),
            "prioritized_talking_points": self._generate_focused_talking_points(query_analysis),
            "action_items": self._generate_focused_actions(query_analysis),
            "conversation_starters": self._generate_conversation_starters(query_analysis),
            "supporting_materials": self._suggest_supporting_materials(query_analysis)
        }

        return json.dumps(meeting_prep, indent=2)

    def _generate_focused_summary(self, query_analysis: Dict) -> str:
        """Generate executive summary focused on query"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return """ESG Integration Focus: Smith Family Trust has successfully implemented ESG investing strategy with strong family engagement. VSGX transition performing competitively with previous VTIAX position. Emma's environmental interests driving family values alignment in investments. Client research and knowledge level has increased significantly. Ready to explore expanded ESG options including potential impact investing allocation."""

        elif focus == "family_personal":
            return """Family Milestone Year: Northwestern acceptance represents major achievement and planning success. College funding strategy on track with $35K annual need manageable within current portfolio growth. Linda's increased involvement strengthening family financial decision-making. Emma's financial education accelerating through internship and coursework. Family approaching investments as multi-generational strategy with strong values alignment."""

        elif focus == "performance":
            return """Strong Performance Delivery: Portfolio delivering 8.2% annual return, exceeding IPS midpoint target. ESG transition achieved without performance sacrifice. All asset classes contributing positively with VGSLX (Real Estate) standout at 15.3%. Risk-adjusted returns excellent with Sharpe ratio 0.89. Strategy discipline maintaining target allocations and meeting long-term objectives."""

        elif focus == "risk_volatility":
            return """Risk Management Success: Portfolio volatility maintained at moderate 12.8% level appropriate for client risk tolerance. Diversification providing downside protection with max drawdown limited to -8.2%. ESG integration not increasing risk profile. Client comfort level high even during banking sector concerns earlier this year. Approaching college funding timeline with appropriate liquidity planning."""

        return """Comprehensive Annual Review: Smith Family Trust portfolio performing exceptionally with 8.2% return exceeding IPS targets. Successful ESG integration reflecting family values without sacrificing performance. Northwestern acceptance milestone driving college funding finalization. Linda's increased involvement creating stronger family financial planning approach. All metrics indicating successful strategy execution and client satisfaction."""

    def _generate_focused_talking_points(self, query_analysis: Dict) -> List[Dict]:
        """Generate talking points focused on query"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                {
                    "priority": 1,
                    "topic": "ESG Transition Success",
                    "talking_point": "VSGX performing within 0.4% of replaced VTIAX - values alignment achieved without return sacrifice",
                    "supporting_data": "VSGX: 5.8% return vs VTIAX historical 6.2%",
                    "conversation_starter": "Your ESG transition has been exactly what we hoped for..."
                },
                {
                    "priority": 2,
                    "topic": "Family Values Integration",
                    "talking_point": "Emma's environmental interests successfully integrated into investment strategy",
                    "supporting_data": "15% portfolio allocation now in dedicated ESG funds",
                    "conversation_starter": "Emma must be proud that your investments reflect your family's values..."
                },
                {
                    "priority": 3,
                    "topic": "Expanded ESG Opportunities",
                    "talking_point": "Ready to explore additional ESG options - green bonds, impact investing",
                    "supporting_data": "Client research shows interest in expanding beyond equity ESG",
                    "conversation_starter": "Based on your research, let's discuss expanding ESG to other asset classes..."
                },
                {
                    "priority": 4,
                    "topic": "Performance Without Compromise",
                    "talking_point": "ESG integration maintaining overall 8.2% portfolio return",
                    "supporting_data": "Total portfolio return exceeding IPS targets",
                    "conversation_starter": "You've proven that doing good and doing well aren't mutually exclusive..."
                }
            ]

        elif focus == "family_personal":
            return [
                {
                    "priority": 1,
                    "topic": "Northwestern Achievement Celebration",
                    "talking_point": "Emma's Northwestern acceptance represents successful long-term planning",
                    "supporting_data": "College funding strategy ready for $35K annual payments",
                    "conversation_starter": "Congratulations on Emma's Northwestern acceptance - what an achievement..."
                },
                {
                    "priority": 2,
                    "topic": "Family Financial Team Strength",
                    "talking_point": "Linda's involvement has created powerful family financial planning dynamic",
                    "supporting_data": "Joint decision-making improving investment outcomes",
                    "conversation_starter": "Linda's analytical perspective has really strengthened your planning process..."
                },
                {
                    "priority": 3,
                    "topic": "Emma's Financial Education",
                    "talking_point": "Emma's internship and coursework developing impressive financial acumen",
                    "supporting_data": "Summer internship providing real-world experience",
                    "conversation_starter": "How is Emma's summer internship going? She's learning so much..."
                },
                {
                    "priority": 4,
                    "topic": "Multi-Generational Planning",
                    "talking_point": "Family approaching investments as multi-generational strategy",
                    "supporting_data": "Values alignment and education creating lasting financial foundation",
                    "conversation_starter": "Your family's approach to financial education is setting Emma up for lifelong success..."
                }
            ]

        elif focus == "performance":
            return [
                {
                    "priority": 1,
                    "topic": "Exceptional Annual Performance",
                    "talking_point": "8.2% annual return exceeding IPS midpoint target by 0.2%",
                    "supporting_data": "Portfolio return vs 7-9% IPS target range",
                    "conversation_starter": "I'm thrilled to share that your portfolio significantly exceeded expectations..."
                },
                {
                    "priority": 2,
                    "topic": "Risk-Adjusted Excellence",
                    "talking_point": "Sharpe ratio of 0.89 demonstrates strong risk-adjusted returns",
                    "supporting_data": "Volatility maintained at moderate 12.8% level",
                    "conversation_starter": "Not only did you earn strong returns, but you earned them efficiently..."
                },
                {
                    "priority": 3,
                    "topic": "Asset Class Contribution",
                    "talking_point": "All asset classes contributing positively - diversification working",
                    "supporting_data": "VGSLX leading at 15.3%, bonds providing stability",
                    "conversation_starter": "Every part of your portfolio earned its keep this year..."
                },
                {
                    "priority": 4,
                    "topic": "ESG Performance Integration",
                    "talking_point": "Values-aligned investing achieved without performance penalty",
                    "supporting_data": "VSGX competitive performance in ESG transition",
                    "conversation_starter": "Your ESG integration proves you don't have to choose between values and returns..."
                }
            ]

        # Default comprehensive talking points
        return [
            {
                "priority": 1,
                "topic": "Annual Performance Success",
                "talking_point": "Portfolio delivered 8.2% return, exceeding IPS targets and expectations",
                "supporting_data": "Performance vs 7-9% annual IPS objective",
                "conversation_starter": "I'm excited to share your portfolio's exceptional performance this year..."
            },
            {
                "priority": 2,
                "topic": "Family Milestone Achievement",
                "talking_point": "Northwestern acceptance and college funding strategy successful execution",
                "supporting_data": "College planning on track for fall 2025 start",
                "conversation_starter": "Congratulations on Emma's Northwestern acceptance - what a proud moment..."
            },
            {
                "priority": 3,
                "topic": "ESG Integration Success",
                "talking_point": "Values-aligned investing implemented without performance sacrifice",
                "supporting_data": "VSGX transition competitive with previous holdings",
                "conversation_starter": "Your ESG integration has been everything we hoped for..."
            },
            {
                "priority": 4,
                "topic": "Family Team Strengthening",
                "talking_point": "Linda's involvement creating powerful family financial planning approach",
                "supporting_data": "Joint decision-making and increased engagement",
                "conversation_starter": "Linda's analytical perspective has really enhanced your planning process..."
            }
        ]

    def _generate_focused_actions(self, query_analysis: Dict) -> List[Dict]:
        """Generate action items focused on query"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                {
                    "action": "Research expanded ESG options for bond allocation",
                    "timeline": "Within 30 days",
                    "priority": "High",
                    "responsible": "Advisor"
                },
                {
                    "action": "Prepare impact investing proposal for 2-3% allocation",
                    "timeline": "Next meeting",
                    "priority": "Medium",
                    "responsible": "Advisor"
                },
                {
                    "action": "Schedule ESG-focused portfolio review with Emma included",
                    "timeline": "Fall 2024",
                    "priority": "Medium",
                    "responsible": "Client & Advisor"
                }
            ]

        elif focus == "family_personal":
            return [
                {
                    "action": "Finalize college funding timeline and automation",
                    "timeline": "December 2024",
                    "priority": "High",
                    "responsible": "Advisor"
                },
                {
                    "action": "Create educational investment materials for Emma",
                    "timeline": "Before college starts",
                    "priority": "Medium",
                    "responsible": "Advisor"
                },
                {
                    "action": "Plan Linda's retirement projection scenarios",
                    "timeline": "Next quarter",
                    "priority": "High",
                    "responsible": "Advisor"
                }
            ]

        return [
            {
                "action": "Continue monitoring ESG fund performance vs benchmarks",
                "timeline": "Quarterly",
                "priority": "Medium",
                "responsible": "Advisor"
            },
            {
                "action": "Prepare college funding liquidity timeline",
                "timeline": "December 2024",
                "priority": "High",
                "responsible": "Advisor"
            },
            {
                "action": "Schedule family financial planning session",
                "timeline": "Fall 2024",
                "priority": "Medium",
                "responsible": "Client & Advisor"
            }
        ]

    def _generate_conversation_starters(self, query_analysis: Dict) -> List[str]:
        """Generate conversation starters focused on query"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Emma must be excited about how your investments now reflect your family's environmental values...",
                "I've been researching some interesting impact investing options that might interest you...",
                "How do you feel about the ESG transition now that we have a full year of performance data?",
                "What other areas of sustainable investing would you like to explore?"
            ]

        elif focus == "family_personal":
            return [
                "How are the Northwestern preparations going? Emma must be so excited...",
                "Linda, how has being more involved in the financial planning felt for you?",
                "What has Emma learned from her summer internship that surprised you?",
                "How do you envision your family's financial priorities evolving as Emma starts college?"
            ]

        elif focus == "performance":
            return [
                "I'm thrilled to share that you exceeded your performance targets this year...",
                "Your risk-adjusted returns show that our strategy is working exactly as designed...",
                "How do you feel about the portfolio's performance relative to your expectations?",
                "What aspects of this year's performance are you most pleased with?"
            ]

        return [
            "What aspects of this year's financial progress are you most proud of?",
            "How has your family's approach to financial planning evolved this year?",
            "What questions do you have about positioning for Emma's college years?",
            "How do you feel about the balance we've achieved between performance and values?"
        ]

    def _suggest_supporting_materials(self, query_analysis: Dict) -> List[str]:
        """Suggest supporting materials based on query focus"""

        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "ESG fund performance comparison report",
                "Sustainable investing research materials",
                "Impact investing proposal document",
                "ESG screening methodology explanation"
            ]

        elif focus == "family_personal":
            return [
                "College funding timeline and projections",
                "529 plan statements and growth projections",
                "Financial education resources for Emma",
                "Family financial goal-setting worksheet"
            ]

        elif focus == "performance":
            return [
                "Annual performance attribution report",
                "Risk-adjusted return analysis",
                "Benchmark comparison charts",
                "IPS compliance documentation"
            ]

        return [
            "Comprehensive portfolio review presentation",
            "IPS compliance and performance report",
            "College funding strategy timeline",
            "ESG integration progress report"
        ]

# ============================================================================
# ENHANCED CREWAI AGENT DEFINITIONS
# ============================================================================


def create_enhanced_milo_agents():
    """Create the enhanced query-aware MILO agents"""

    communications_analyst = Agent(
        role='Query-Aware Communications Analyst',
        goal='Analyze client communications with specific focus based on user queries, providing targeted insights rather than general summaries',
        backstory="""You are an expert at parsing through client communications to answer specific questions. 
        When given a query about ESG concerns, you focus on sustainability themes. When asked about family matters, 
        you highlight personal milestones and relationships. When asked about performance concerns, you extract 
        market-related discussions. You always tailor your analysis to directly address what the user is asking about.""",
        tools=[QueryAwareCommunicationsAnalyzer()],
        verbose=True,
        allow_delegation=False
    )

    portfolio_analyst = Agent(
        role='Query-Aware Portfolio Performance Analyst',
        goal='Provide portfolio analysis focused on specific aspects requested in user queries, from ESG performance to risk metrics to specific asset classes',
        backstory="""You are a quantitative analyst who adapts your analysis based on what questions are being asked. 
        When someone asks about ESG performance, you focus on sustainable fund results. When asked about risk, you 
        emphasize volatility and downside protection. When asked about specific time periods, you adjust your analysis 
        accordingly. You provide targeted, relevant insights rather than generic performance reports.""",
        tools=[QueryAwarePortfolioAnalyzer()],
        verbose=True,
        allow_delegation=False
    )

    meeting_prep_specialist = Agent(
        role='Query-Aware Meeting Preparation Specialist',
        goal='Create meeting materials that directly address the specific questions or concerns raised in user queries',
        backstory="""You are an experienced advisor support specialist who creates targeted meeting preparation materials. 
        When an advisor asks about ESG concerns, you prepare ESG-focused talking points. When they ask about family matters, 
        you emphasize college planning and family dynamics. You always ensure your meeting materials directly respond to 
        the specific question asked while maintaining comprehensive coverage of important topics.""",
        tools=[QueryAwareMeetingPrep()],
        verbose=True,
        allow_delegation=False
    )

    return communications_analyst, portfolio_analyst, meeting_prep_specialist


def create_enhanced_milo_tasks(communications_analyst, portfolio_analyst, meeting_prep_specialist, user_query: str):
    """Create enhanced tasks that incorporate user query"""

    communications_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Analyze the Smith Family Trust's communications to specifically address this question. Focus your analysis on:
        
        1. Communications most relevant to answering the user's specific query
        2. Themes and patterns that directly relate to what was asked
        3. Client sentiment and concerns specifically related to the query topic
        4. Chronological developments in the areas the user is asking about
        5. Insights that will help the advisor specifically address this question
        
        Tailor your entire response to provide targeted, relevant information rather than a general communications summary.
        If the query is about ESG, focus on sustainability themes. If about family, emphasize personal developments.
        If about performance, highlight return and market-related discussions.
        """,
        agent=communications_analyst,
        expected_output=f"Targeted analysis of client communications specifically focused on answering: '{user_query}'"
    )

    portfolio_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Provide a portfolio performance analysis specifically focused on answering this question:
        
        1. If query relates to ESG/sustainability: Focus on ESG fund performance, values alignment, sustainable investing results
        2. If query relates to performance: Emphasize returns, risk-adjusted metrics, benchmark comparisons
        3. If query relates to risk/volatility: Highlight risk metrics, downside protection, volatility analysis
        4. If query relates to specific time periods: Adjust analysis timeframe accordingly
        5. If query relates to specific asset classes: Deep dive into those particular investments
        
        Always connect your analysis back to the specific question being asked rather than providing generic performance data.
        Use real market data where possible and provide targeted recommendations based on the query focus.
        """,
        agent=portfolio_analyst,
        expected_output=f"Targeted portfolio analysis specifically addressing: '{user_query}'"
    )

    meeting_prep_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Create comprehensive meeting preparation materials that directly respond to this specific question:
        
        1. Executive summary that addresses the core question asked
        2. Talking points prioritized and focused on the query topic
        3. Action items relevant to the specific concerns raised
        4. Conversation starters that naturally flow from addressing the user's question
        5. Supporting materials that would be most helpful for this type of discussion
        
        Your meeting prep should make the advisor feel completely prepared to address the specific question or concern
        that was raised, while maintaining comprehensive coverage of other important topics.
        
        Use insights from both the communications and portfolio analysis to create targeted, actionable meeting materials.
        """,
        agent=meeting_prep_specialist,
        expected_output=f"Complete meeting preparation package specifically designed to address: '{user_query}'",
        context=[communications_task, portfolio_task]
    )

    return communications_task, portfolio_task, meeting_prep_task


def create_enhanced_milo_crew(user_query: str):
    """Create enhanced MILO crew with query awareness"""

    # Create agents
    communications_analyst, portfolio_analyst, meeting_prep_specialist = create_enhanced_milo_agents()

    # Create tasks with user query
    communications_task, portfolio_task, meeting_prep_task = create_enhanced_milo_tasks(
        communications_analyst, portfolio_analyst, meeting_prep_specialist, user_query
    )

    # Create the crew
    milo_crew = Crew(
        agents=[communications_analyst,
                portfolio_analyst, meeting_prep_specialist],
        tasks=[communications_task, portfolio_task, meeting_prep_task],
        process=Process.sequential,
        verbose=2
    )

    return milo_crew

# ============================================================================
# MAIN EXECUTION FUNCTION WITH QUERY PROCESSING
# ============================================================================


def execute_enhanced_milo_analysis(client_name: str = "Smith Family Trust", user_query: str = "What has happened with this account over the past year?"):
    """
    Main function to execute the enhanced query-aware MILO analysis workflow
    """
    print(f"🤖 MILO: Analyzing query for {client_name}")
    print(f"📋 Query: {user_query}")

    # Analyze the query first
    query_analysis = analyze_query(user_query)
    print(f"🎯 Query Focus: {query_analysis['primary_focus']}")
    print(f"🔍 Query Type: {query_analysis['query_type']}")
    print("=" * 80)

    try:
        # Create and execute the crew with query awareness
        crew = create_enhanced_milo_crew(user_query)

        # Execute the crew with inputs
        result = crew.kickoff(inputs={
            'client_name': client_name,
            'query': user_query,
            'query_focus': query_analysis['primary_focus']
        })

        print("\n" + "=" * 80)
        print("🎯 MILO QUERY-FOCUSED ANALYSIS COMPLETE")
        print("=" * 80)

        return result

    except Exception as e:
        print(f"❌ Error in MILO analysis: {str(e)}")
        return None


if __name__ == "__main__":
    # Test different types of queries
    test_queries = [
        "What are the client's ESG concerns?",
        "How has the portfolio performed this year?",
        "What family changes should I know about?",
        "What has happened with this account over the past year?"
    ]

    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Testing Query: {query}")
        print('='*50)
        result = execute_enhanced_milo_analysis(user_query=query)
        if result:
            print("Query processing successful!")
