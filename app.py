import streamlit as st
import os
from dotenv import load_dotenv

# 1. COMPATIBILITY IMPORTS
# Use langchain_classic to ensure the AgentExecutor works in 2026
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_react_agent

# 2. CORE INTEGRATIONS
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import get_weather, search_travel_info

# Load environment variables from .env
load_dotenv()

# UI Config
st.set_page_config(page_title="MCP Travel Agent", page_icon="✈️")
st.title("🌍 AI Travel Planner (MCP)")

# 3. INITIALIZE LLM (Cleaned up)
# We use gemini-2.5-flash with retries to manage Free Tier quota limits
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0
).with_retry(stop_after_attempt=6)

# 4. TOOLS SETUP
tools = [get_weather, search_travel_info]

# 5. PULL PROMPT
try:
    prompt = hub.pull("hwchase17/react")
except Exception as e:
    st.error(f"Hub Error: {e}. Check your internet connection.")

# 6. AGENT & EXECUTOR
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)

# 7. UI INPUT & EXECUTION
user_prompt = st.text_input("Where do you want to go?", placeholder="Plan a 3-day trip to Tokyo in May")

if st.button("Generate Trip Plan"):
    if user_prompt:
        with st.spinner("Agent is reasoning and calling MCP tools..."):
            try:
                # Execution with the specific Lab requirements
                input_query = f"""
                Analyze the user request: '{user_prompt}'
                Provide the following in your final answer:
                1. One paragraph of the city's cultural & historic significance.
                2. Current weather and a forecast for the trip dates.
                3. Flight & Hotel options based on real-time data.
                4. A detailed 3-part itinerary (Day 1, Day 2, Day 3).
                """
                
                response = agent_executor.invoke({"input": input_query})
                
                # Display Output
                st.markdown("---")
                st.markdown("### 📋 Your Itinerary")
                st.write(response["output"])
                
            except Exception as e:
                # If you see 429 here, it means the 6 retries also failed.
                st.error(f"Execution Error: {e}")
    else:
        st.warning("Please enter a destination!")