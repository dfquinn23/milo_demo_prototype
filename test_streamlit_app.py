"""
Test Streamlit App - Minimal Version
Use this to test if the import issue is in the agents file or elsewhere
"""

import streamlit as st

st.title("🧪 MILO Import Test")

st.write("Testing imports to isolate the Chroma issue...")

# Test 1: Basic import
try:
    st.write("### Test 1: Importing minimal_test_agents...")
    from minimal_test_agents import execute_enhanced_milo_analysis
    st.success("✅ Import successful!")

    # Test 2: Function execution
    st.write("### Test 2: Testing function execution...")
    result = execute_enhanced_milo_analysis(
        "Test Client", "What happened this year?")
    st.success("✅ Function execution successful!")
    st.json(result)

except ImportError as e:
    st.error(f"❌ Import Error: {e}")
except Exception as e:
    st.error(f"❌ Execution Error: {e}")

# Test 3: Try importing your actual file
st.write("### Test 3: Importing enhanced_milo_agents...")
try:
    from enhanced_milo_agents import execute_enhanced_milo_analysis as real_execute
    st.success("✅ Import of enhanced_milo_agents successful!")

    # Try to execute it
    st.write("### Test 4: Testing real function execution...")
    try:
        result = real_execute("Test Client", "What happened this year?")
        st.success("✅ Real function execution successful!")
        st.text(str(result))
    except Exception as e:
        st.error(f"❌ Real function execution failed: {e}")

except ImportError as e:
    st.error(f"❌ Import Error from enhanced_milo_agents: {e}")
except Exception as e:
    st.error(f"❌ Other Error from enhanced_milo_agents: {e}")

st.write("---")
st.write("**Instructions:**")
st.write("1. If Test 1 & 2 work but Test 3 & 4 fail, the issue is in enhanced_milo_agents.py")
st.write("2. If all tests fail, there might be a system-level issue")
st.write("3. Check the console output for detailed error messages")
