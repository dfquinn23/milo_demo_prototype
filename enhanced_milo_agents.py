"""
MILO Client Intelligence Dashboard - Enhanced Version with Query Responsiveness
CrewAI Agent Implementation with Rich Sample Data and Query Processing
"""

import hashlib  # for stable doc IDs when indexing comms
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
import tempfile

# ── Feature flag: keep vector DB OFF by default ──────────────────────────────
USE_VECTOR_DB = os.getenv("USE_VECTOR_DB", "0") == "1"

# If vector DB will be used, set Chroma backend away from SQLite (Cloud-safe)
if USE_VECTOR_DB:
    os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
    os.environ["PERSIST_DIRECTORY"] = os.path.join(
        tempfile.gettempdir(), "chroma_db")


# ── Lazy Chroma accessor (only imported/created if USE_VECTOR_DB is true) ────
def get_chroma_collection():
    """
    Create or return a Chroma collection only when vector DB is enabled.
    This avoids ONNX/SQLite issues when you don't need retrieval.
    """
    # Local imports (prevent crashing at module import time)
    from chromadb.utils import embedding_functions
    import chromadb

    # Explicitly use sentence-transformers instead of ONNX
    sentence_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.Client()
    return client.get_or_create_collection(
        name="milo",
        embedding_function=sentence_embedder
    )


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
# ENHANCED CUSTOM TOOLS WITH QUERY AWARENESS
# ============================================================================


class QueryAwareCommunicationsAnalyzer(BaseTool):
    name: str = "Query-Aware Communications Analyzer"
    description: str = "Analyzes client communications with focus based on user query"

 # --- NEW: helpers for optional vector DB indexing/querying ---
    def _comm_doc_text(self, comm: Dict) -> str:
        """Serialize a communication to a plain-text blob for embedding."""
        parts = [
            f"Date: {comm.get('date','')}",
            f"Type: {comm.get('type','')}",
            f"Subject: {comm.get('subject','')}",
            f"Sentiment: {comm.get('sentiment','')}",
            f"Key Themes: {', '.join(comm.get('key_themes', []))}",
            "",
            comm.get("full_content", comm.get("subject", "")),
        ]
        return "\n".join(parts)

    def _comm_doc_id(self, comm: Dict) -> str:
        """Stable deterministic ID for a comm (prevents duplicate adds)."""
        raw = f"{comm.get('date','')}|{comm.get('type','')}|{comm.get('subject','')}"
        return "comm_" + hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def _run(self, query: str) -> str:
        """Analyze communications with query-specific focus"""

        query_analysis = analyze_query(query)
        # --- NEW: optional vector retrieval to guide relevance ---
        retrieved_ids = set()
        if USE_VECTOR_DB:
            collection = get_chroma_collection()

            # Index (idempotent adds: Chroma will ignore dup IDs)
            docs, ids, metas = [], [], []
            for comm in ENHANCED_COMMUNICATIONS_DATA:
                ids.append(self._comm_doc_id(comm))
                docs.append(self._comm_doc_text(comm))
                metas.append({
                    "date": comm.get("date"),
                    "type": comm.get("type"),
                    "subject": comm.get("subject"),
                    "sentiment": comm.get("sentiment", ""),
                    "themes": ",".join(comm.get("key_themes", [])),
                })
            # Add in manageable batches to avoid timeouts on Cloud
            B = 32
            for i in range(0, len(ids), B):
                try:
                    collection.add(
                        ids=ids[i:i+B],
                        documents=docs[i:i+B],
                        metadatas=metas[i:i+B],
                    )
                except Exception:
                    # safe to ignore duplicate ID errors
                    pass

            # Query top hits to bias/boost our relevance scoring
            try:
                q = collection.query(query_texts=[query], n_results=6)
                for hit_id in q.get("ids", [[]])[0]:
                    retrieved_ids.add(hit_id)
            except Exception:
                # Retrieval is optional; proceed without it if it fails
                retrieved_ids = set()

        # Filter communications based on query focus
        relevant_comms = []
        for comm in ENHANCED_COMMUNICATIONS_DATA:
            relevance_score = 0
            focus = query_analysis["primary_focus"]

            # Score based on primary focus
            if focus == "esg_sustainability" and any(theme in ["ESG_investing", "values_alignment", "environmental_concerns", "ESG_transition"] for theme in comm["key_themes"]):
                relevance_score += 10
            elif focus == "performance" and any(theme in ["portfolio_performance", "market_volatility"] for theme in comm["key_themes"]):
                relevance_score += 10
            elif focus == "family_personal" and any(theme in ["family_involvement", "college_planning", "education_planning", "daughter_influence"] for theme in comm["key_themes"]):
                relevance_score += 10
            elif focus == "risk_volatility" and any(theme in ["market_volatility", "risk_management", "banking_sector_concerns"] for theme in comm["key_themes"]):
                relevance_score += 10
            elif focus == "communication" and any(theme in ["communication_preferences"] for theme in comm["key_themes"]):
                relevance_score += 10

            # Add base relevance
            relevance_score += 1

            relevant_comms.append({
                **comm,
                "relevance_score": relevance_score
            })

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

        # Generate focused insights
        analysis_result["key_insights"] = self._generate_focused_insights(
            relevant_comms[:6], query_analysis)
        analysis_result["themes_analysis"] = self._analyze_themes_focused(
            relevant_comms[:6], query_analysis)

        return json.dumps(analysis_result, indent=2)

    def _extract_focused_summary(self, comm: Dict, query_analysis: Dict) -> str:
        """Extract summary focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            if "ESG" in comm.get("full_content", ""):
                return "Client expressing strong interest in ESG investing, driven by Emma's environmental concerns"
            elif "values" in comm.get("full_content", ""):
                return "Family values alignment becoming important factor in investment decisions"
        elif focus == "family_personal":
            if "Northwestern" in comm.get("full_content", ""):
                return "Northwestern acceptance milestone and college planning developments"
            elif "Linda" in comm.get("full_content", ""):
                return "Linda becoming more involved in family financial planning decisions"
        elif focus == "performance":
            if "performance" in comm.get("full_content", "") or "return" in comm.get("full_content", ""):
                return "Portfolio performance discussion and satisfaction with results"

        # Default summary
        return comm.get("subject", "Client communication")

    def _generate_focused_insights(self, communications: List[Dict], query_analysis: Dict) -> List[str]:
        """Generate insights focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Strong family commitment to ESG investing driven by Emma's environmental interests",
                "Successful VSGX transition with competitive performance vs VTIAX",
                "Client has become highly knowledgeable about ESG options through research",
                "Values alignment now as important as return optimization"
            ]
        elif focus == "family_personal":
            return [
                "Northwestern acceptance represents successful long-term planning milestone",
                "Linda's involvement has strengthened family financial decision-making",
                "Emma's financial education accelerating through internship and coursework",
                "Family approaching investments as multi-generational strategy"
            ]
        elif focus == "performance":
            return [
                "Consistent satisfaction with portfolio performance vs expectations",
                "Growing sophistication in performance evaluation and market analysis",
                "ESG integration achieved without performance sacrifice",
                "Performance discussions now include family goals context"
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


class QueryAwarePortfolioAnalyzer(BaseTool):
    name: str = "Query-Aware Portfolio Performance Analyzer"
    description: str = "Analyzes portfolio performance with focus based on user query"

    def _run(self, query: str) -> str:
        """Analyze portfolio with query-specific focus"""

        query_analysis = analyze_query(query)

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

        # Get performance data
        performance_data = self._get_performance_data(portfolio)

        # Create focused analysis
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
        """Get performance data with real Yahoo Finance calls and fallbacks"""

        performance_data = {
            "fund_performance": {},
            "total_return": 0
        }

        total_weighted_return = 0

        # Fallback data
        fallback_data = {
            "VTSAX": {"return": 0.121, "volatility": 0.135},
            "VTIAX": {"return": 0.062, "volatility": 0.142},
            "VSGX": {"return": 0.058, "volatility": 0.138},
            "VBTLX": {"return": 0.021, "volatility": 0.045},
            "VGSLX": {"return": 0.153, "volatility": 0.218},
            "VTABX": {"return": 0.018, "volatility": 0.055}
        }

        for ticker, details in portfolio["allocations"].items():
            try:
                # Try Yahoo Finance
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1y")

                if not hist.empty and len(hist) > 20:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    annual_return = (end_price - start_price) / start_price

                    daily_returns = hist['Close'].pct_change().dropna()
                    volatility = daily_returns.std() * np.sqrt(252)
                else:
                    raise Exception("Insufficient data")

            except:
                # Use fallback
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
        return performance_data

    def _get_focused_metrics(self, performance_data: Dict, query_analysis: Dict) -> Dict:
        """Get metrics focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return {
                "esg_fund_performance": f"{performance_data['fund_performance']['VSGX']['annual_return']}% (VSGX)",
                "esg_allocation": "15% of portfolio in ESG funds",
                "transition_impact": "Minimal performance difference vs previous VTIAX"
            }
        elif focus == "performance":
            return {
                "annual_return": f"{performance_data['total_return']}%",
                "vs_ips_target": "Within 7-9% target range",
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
                "status": "Compliant" if 0.07 <= total_return <= 0.09 else "Review needed"
            },
            "allocation_compliance": "Within IPS guidelines"
        }

    def _get_focused_recommendations(self, performance_data: Dict, query_analysis: Dict) -> List[str]:
        """Get recommendations based on query focus"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "ESG transition successful - VSGX performing competitively",
                "Consider expanding ESG integration to other asset classes",
                "Monitor ESG fund performance vs benchmarks quarterly"
            ]
        elif focus == "performance":
            return [
                f"Strong {performance_data['total_return']}% return exceeding IPS targets",
                "All asset classes contributing positively",
                "Maintain current allocation and strategy"
            ]

        return [
            "Portfolio performing well within IPS guidelines",
            "Continue current strategy and monitoring"
        ]


class QueryAwareMeetingPrep(BaseTool):
    name: str = "Query-Aware Meeting Preparation Generator"
    description: str = "Creates meeting materials focused on specific query topics"

    def _run(self, combined_data: str) -> str:
        """Generate meeting prep materials based on query focus"""

        # Extract query from task context
        try:
            # The query should be passed through the task context
            import re
            query_match = re.search(
                r'The user has asked: "([^"]*)"', combined_data)
            if query_match:
                query = query_match.group(1)
            else:
                query = "What has happened with this account over the past year?"
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
            "targeted_talking_points": self._generate_focused_talking_points(query_analysis),
            "action_items": self._generate_focused_actions(query_analysis),
            "conversation_starters": self._generate_conversation_starters(query_analysis)
        }

        return json.dumps(meeting_prep, indent=2)

    def _generate_focused_summary(self, query_analysis: Dict) -> str:
        """Generate summary focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return "ESG Integration Success: Smith Family Trust has successfully implemented ESG investing with VSGX performing competitively. Emma's environmental interests are driving strong family values alignment. Client research sophistication has increased significantly. Ready for expanded ESG options."
        elif focus == "family_personal":
            return "Family Milestone Year: Northwestern acceptance represents planning success. College funding on track. Linda's involvement strengthening decision-making. Emma's financial education accelerating. Multi-generational strategy with values alignment."
        elif focus == "performance":
            return "Strong Performance: Portfolio delivering 8.2% annual return, exceeding IPS targets. ESG integration without performance penalty. All asset classes contributing positively. Risk management effective."

        return "Comprehensive Analysis: Portfolio performing well with successful ESG integration and strong family engagement. All objectives being met."

    def _generate_focused_talking_points(self, query_analysis: Dict) -> List[Dict]:
        """Generate talking points focused on query"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                {"priority": 1, "topic": "ESG Success",
                    "point": "VSGX performing competitively - values achieved without return sacrifice"},
                {"priority": 2, "topic": "Family Values",
                    "point": "Emma's influence creating meaningful investment alignment"},
                {"priority": 3, "topic": "Expansion Ready",
                    "point": "Client research shows readiness for additional ESG options"}
            ]
        elif focus == "family_personal":
            return [
                {"priority": 1, "topic": "Northwestern Achievement",
                    "point": "Emma's acceptance represents successful planning milestone"},
                {"priority": 2, "topic": "Family Team",
                    "point": "Linda's involvement strengthening financial decisions"},
                {"priority": 3, "topic": "Education Success",
                    "point": "Emma's internship developing financial sophistication"}
            ]
        elif focus == "performance":
            return [
                {"priority": 1, "topic": "Exceptional Returns",
                    "point": "8.2% return exceeding IPS midpoint target"},
                {"priority": 2, "topic": "Risk Management",
                    "point": "Strong performance with controlled volatility"},
                {"priority": 3, "topic": "All Contributors",
                    "point": "Every asset class adding value to portfolio"}
            ]

        return [
            {"priority": 1, "topic": "Overall Success",
                "point": "Portfolio and planning objectives being met"},
            {"priority": 2, "topic": "Family Engagement",
                "point": "Strong family involvement in financial decisions"},
            {"priority": 3, "topic": "Future Ready",
                "point": "Well positioned for upcoming milestones"}
        ]

    def _generate_focused_actions(self, query_analysis: Dict) -> List[str]:
        """Generate action items based on query focus"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Research additional ESG fund options",
                "Explore green bonds for fixed income ESG",
                "Schedule ESG-focused family discussion"
            ]
        elif focus == "family_personal":
            return [
                "Finalize college funding timeline",
                "Plan Linda's retirement projections",
                "Create family financial education materials"
            ]
        elif focus == "performance":
            return [
                "Continue monitoring quarterly performance",
                "Maintain current allocation strategy",
                "Prepare performance attribution analysis"
            ]

        return [
            "Continue current strategy and monitoring",
            "Schedule next review meeting",
            "Prepare follow-up materials"
        ]

    def _generate_conversation_starters(self, query_analysis: Dict) -> List[str]:
        """Generate conversation starters based on query focus"""
        focus = query_analysis["primary_focus"]

        if focus == "esg_sustainability":
            return [
                "Emma must be proud that your investments reflect your family's values...",
                "Your ESG research has been impressive - you've become quite the expert...",
                "How do you feel about expanding ESG to other parts of your portfolio?"
            ]
        elif focus == "family_personal":
            return [
                "How are the Northwestern preparations going?",
                "Linda, how has being more involved in the planning felt?",
                "What has Emma learned from her internship that surprised you?"
            ]
        elif focus == "performance":
            return [
                "I'm excited to share your exceptional performance results...",
                "How do you feel about exceeding your target returns?",
                "What aspects of this performance are you most pleased with?"
            ]

        return [
            "What aspects of this year's progress are you most proud of?",
            "How has your family's financial planning evolved?",
            "What questions do you have about our strategy?"
        ]

# ============================================================================
# ENHANCED CREWAI AGENT DEFINITIONS
# ============================================================================


def create_enhanced_milo_agents():
    """Create the enhanced query-aware MILO agents"""

    communications_analyst = Agent(
        role='Query-Aware Communications Analyst',
        goal='Analyze client communications with specific focus based on user queries',
        backstory="""You are an expert at analyzing client communications and adapting your analysis based on specific questions. When asked about ESG concerns, you focus on sustainability themes. When asked about family matters, you highlight personal relationships and milestones. You always provide targeted, relevant insights.""",
        tools=[QueryAwareCommunicationsAnalyzer()],
        verbose=True,
        allow_delegation=False
    )

    portfolio_analyst = Agent(
        role='Query-Aware Portfolio Performance Analyst',
        goal='Provide portfolio analysis focused on specific aspects requested in queries',
        backstory="""You are a quantitative analyst who adapts analysis based on what's being asked. You focus on ESG performance when asked about sustainability, risk metrics when asked about volatility, and returns when asked about performance. You provide targeted insights rather than generic reports.""",
        tools=[QueryAwarePortfolioAnalyzer()],
        verbose=True,
        allow_delegation=False
    )

    meeting_prep_specialist = Agent(
        role='Query-Aware Meeting Preparation Specialist',
        goal='Create meeting materials that directly address specific questions raised in queries',
        backstory="""You create targeted meeting materials based on what advisors need to discuss. When they ask about ESG, you prepare ESG-focused talking points. When they ask about family matters, you emphasize personal milestones. You ensure materials directly respond to the specific question asked.""",
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
        
        Analyze Smith Family Trust communications to specifically address this question. Focus on communications most relevant to the query topic and provide targeted insights that will help answer what was asked.
        """,
        agent=communications_analyst,
        expected_output=f"Targeted communications analysis focused on: '{user_query}'"
    )

    portfolio_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Analyze portfolio performance with specific focus on answering this question. Adapt your analysis based on whether the query relates to ESG, performance, risk, or other topics.
        """,
        agent=portfolio_analyst,
        expected_output=f"Focused portfolio analysis addressing: '{user_query}'"
    )

    meeting_prep_task = Task(
        description=f"""
        The user has asked: "{user_query}"
        
        Create meeting preparation materials that directly respond to this question. Generate talking points and action items focused on the query topic while maintaining comprehensive coverage.
        """,
        agent=meeting_prep_specialist,
        expected_output=f"Meeting prep package designed to address: '{user_query}'",
        context=[communications_task, portfolio_task]
    )

    return communications_task, portfolio_task, meeting_prep_task


def create_enhanced_milo_crew(user_query: str):
    """Create enhanced MILO crew with query awareness"""

    communications_analyst, portfolio_analyst, meeting_prep_specialist = create_enhanced_milo_agents()

    communications_task, portfolio_task, meeting_prep_task = create_enhanced_milo_tasks(
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


def execute_enhanced_milo_analysis(client_name: str = "Smith Family Trust", user_query: str = "What has happened with this account over the past year?"):
    """Main function to execute enhanced query-aware MILO analysis"""

    print(f"🤖 MILO: Analyzing query for {client_name}")
    print(f"📋 Query: {user_query}")

    query_analysis = analyze_query(user_query)
    print(f"🎯 Query Focus: {query_analysis['primary_focus']}")
    print("=" * 80)

    try:
        crew = create_enhanced_milo_crew(user_query)

        result = crew.kickoff(inputs={
            'client_name': client_name,
            'query': user_query,
            'query_focus': query_analysis['primary_focus']
        })

        print("\n" + "=" * 80)
        print("🎯 MILO ENHANCED ANALYSIS COMPLETE")
        print("=" * 80)

        return result

    except Exception as e:
        print(f"❌ Error in enhanced MILO analysis: {str(e)}")
        return None


if __name__ == "__main__":
    # Test with different queries
    test_queries = [
        "What are the client's ESG concerns?",
        "How has the portfolio performed this year?",
        "What family changes should I know about?",
        "What has happened with this account over the past year?"
    ]

    for query in test_queries:
        print(f"\nTesting: {query}")
        result = execute_enhanced_milo_analysis(user_query=query)
        if result:
            print("✅ Success!")
