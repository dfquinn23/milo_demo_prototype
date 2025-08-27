"""
Minimal Test Version - Zero Dependencies
Use this to test if the basic import works without any Chroma issues
"""

from typing import Dict
import json
import os
print("🧪 MINIMAL TEST AGENTS LOADING...")

# Check for any problematic imports

print("✅ Basic imports successful")

# Simple mock function to test the import


def execute_enhanced_milo_analysis(client_name: str, user_query: str):
    """Super simple test function"""
    print(f"🧪 TEST: Analyzing {client_name}")
    print(f"🧪 TEST: Query: {user_query}")

    # Return simple test result
    return {
        "test_status": "SUCCESS",
        "message": "Minimal agents working - no Chroma imports!",
        "client": client_name,
        "query": user_query
    }


# Test CrewAI import specifically
try:
    from crewai import Agent, Task, Crew, Process
    print("✅ CrewAI imports successful")
    CREWAI_AVAILABLE = True
except ImportError as e:
    print(f"❌ CrewAI import failed: {e}")
    CREWAI_AVAILABLE = False

# Test yfinance import
try:
    import yfinance as yf
    print("✅ yfinance import successful")
    YFINANCE_AVAILABLE = True
except ImportError as e:
    print(f"❌ yfinance import failed: {e}")
    YFINANCE_AVAILABLE = False

print("🧪 MINIMAL TEST AGENTS LOADED SUCCESSFULLY")

if __name__ == "__main__":
    print("🧪 Running test...")
    result = execute_enhanced_milo_analysis("Test Client", "Test query")
    print(f"🧪 Result: {result}")
