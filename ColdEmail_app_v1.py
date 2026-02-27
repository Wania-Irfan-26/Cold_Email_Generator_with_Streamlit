import streamlit as st
from crewai import LLM, Task, Agent, Crew, Process
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv
import os

load_dotenv()

# Page config
st.set_page_config(page_title="Cold Email Generator", page_icon="📧", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📧 Cold Email Generator")
st.markdown("Generate personalized cold emails using AI agents")
st.divider()

# Agency services
agency_services = """
1. SEO Optimization Service: Best for companies with good products but low traffic. We increase organic reach.
2. Custom Web Development: Best for companies with outdated, ugly, or slow websites. We build modern React/Python sites.
3. AI Automation: Best for companies with manual, repetitive tasks. We build agents to save time.
"""

# Input form
with st.form("email_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        user_name = st.text_input("Your Name", placeholder="John Doe")
        user_company = st.text_input("Your Company", placeholder="Tech Solutions Inc.")
    
    with col2:
        target_company = st.text_input("Target Company", placeholder="Acme Corp")
        target_url = st.text_input("Target Company URL", placeholder="https://example.com")
    
    submit = st.form_submit_button("Generate Email")

# Process when form is submitted
if submit:
    if not all([user_name, user_company, target_company, target_url]):
        st.error("Please fill in all fields")
    else:
        with st.spinner("🤖 AI agents are working..."):
            try:
                # Initialize LLM
                my_llm = LLM(
                    model="groq/llama-3.3-70b-versatile",
                    api_key=os.getenv("GROQ_API_KEY")
                )
                
                scrape_tool = ScrapeWebsiteTool()
                
                # Create agents
                researcher = Agent(
                    role='Business Intelligence Analyst',
                    goal='Analyze the target company website and identify their core business and potential weaknesses.',
                    backstory="You are an expert at analyzing businesses just by looking at their landing page.",
                    tools=[scrape_tool],
                    verbose=False,
                    allow_delegation=True,
                    memory=True,
                    llm=my_llm
                )
                
                strategist = Agent(
                    role='Agency Strategist',
                    goal='Match the target company needs with ONE of our agency services.',
                    backstory=f"""You work for a top-tier digital agency.
                    OUR SERVICES KNOWLEDGE BASE:
                    {agency_services}
                    You must pick the SINGLE best service for this specific client and explain why.""",
                    verbose=False,
                    memory=True,
                    llm=my_llm
                )
                
                writer = Agent(
                    role='Senior Sales Copywriter',
                    goal='Write a personalized cold email that sounds human and professional.',
                    backstory="You write emails that get replies. You never sound robotic.",
                    verbose=False,
                    llm=my_llm
                )
                
                # Create tasks
                task_analyze = Task(
                    description=f"Scrape the website {target_company} from given url {target_url}. Summarize what the company does and identify 1 key area where they could improve.",
                    expected_output="A brief summary of the company and their potential pain points.",
                    agent=researcher
                )
                
                task_strategize = Task(
                    description="Based on the analysis, pick ONE service from our Agency Knowledge Base that solves their problem.",
                    expected_output="The selected service and the reasoning for the match.",
                    agent=strategist
                )
                
                task_write = Task(
                    description=f"Draft a cold email to the CEO of {target_company}. Pitch the selected service. Keep it under 150 words. Sign it from {user_name} at {user_company}.",
                    expected_output="A professional cold email ready to send.",
                    agent=writer
                )
                
                # Create and run crew
                sales_crew = Crew(
                    agents=[researcher, strategist, writer],
                    tasks=[task_analyze, task_strategize, task_write],
                    process=Process.sequential,
                    verbose=False
                )
                
                result = sales_crew.kickoff()
                
                # Display result
                st.success("✅ Email generated successfully!")
                st.divider()
                
                st.subheader("📨 Your Cold Email")
                st.text_area("", value=str(result), height=300, label_visibility="collapsed")
                
                # Download button
                st.download_button(
                    label="📥 Download Email",
                    data=str(result),
                    file_name=f"cold_email_{target_company.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
