import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
import streamlit as st
from crewai import LLM, Task, Agent, Crew, Process
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for light mode with purple theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8f7ff 0%, #e9e4f0 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f7ff 0%, #e9e4f0 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(118, 75, 162, 0.15);
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #7c3aed 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #6b21a8;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9d5ff;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s;
        color: #1f2937;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.1);
    }
    
    .stTextInput label {
        color: #6b21a8 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(120deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(120deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    
    .email-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(118, 75, 162, 0.15);
        margin-top: 1.5rem;
    }
    
    .email-container h3 {
        color: #6b21a8;
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e9d5ff;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #1f2937 !important;
        background: white;
    }
    
    .success-box {
        background: linear-gradient(120deg, #f3e8ff 0%, #e9d5ff 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        color: #6b21a8;
        margin-bottom: 1rem;
    }
    
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(118, 75, 162, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .info-card h3 {
        color: #6b21a8;
        margin-top: 0 !important;
    }
    
    .service-badge {
        display: inline-block;
        background: linear-gradient(120deg, #f3e8ff 0%, #e9d5ff 100%);
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #6b21a8;
        font-weight: 500;
        margin: 0.3rem;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(120deg, #7c3aed 0%, #a855f7 100%);
    }
    
    .stExpander summary p {
        color: #6b21a8 !important;
        font-weight: 600 !important;
    }
    
    .stExpander summary svg {
        fill: #7c3aed !important;
        stroke: #7c3aed !important;
    }
    
    .stExpander summary {
        background: linear-gradient(120deg, #f3e8ff 0%, #e9d5ff 100%) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        cursor: pointer !important;
    }
    
    .stExpander summary:hover svg {
        fill: #a855f7 !important;
        stroke: #a855f7 !important;
        transform: scale(1.1);
        transition: all 0.3s;
    }
    
    div[data-testid="stMarkdownContainer"] h3 {
        color: #6b21a8 !important;
    }
    
    hr {
        display: none !important;
    }
    
    .stMarkdown hr {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">Cold Email Generator</div>
        <div class="subtitle">AI-powered personalized outreach in seconds</div>
    </div>
""", unsafe_allow_html=True)

# Agency services
agency_services = """
1. SEO Optimization Service: Best for companies with good products but low traffic. We increase organic reach.
2. Custom Web Development: Best for companies with outdated, ugly, or slow websites. We build modern React/Python sites.
3. AI Automation: Best for companies with manual, repetitive tasks. We build agents to save time.
"""

# Services info card
with st.expander("Our Services", expanded=False):
    st.markdown("""
        <div style='padding: 0.5rem;'>
            <span class='service-badge'>SEO Optimization</span>
            <span class='service-badge'>Web Development</span>
            <span class='service-badge'>AI Automation</span>
        </div>
    """, unsafe_allow_html=True)

# Input form
st.markdown("<div class='info-card'>", unsafe_allow_html=True)
st.markdown("### Enter Details")

with st.form("email_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        user_name = st.text_input("Your Name", placeholder="John Doe")
        user_company = st.text_input("Your Company", placeholder="Tech Solutions Inc.")
    
    with col2:
        target_company = st.text_input("Target Company", placeholder="Acme Corp")
        target_url = st.text_input("Target URL", placeholder="https://example.com")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("Generate Email")

st.markdown("</div>", unsafe_allow_html=True)

# Process when form is submitted
if submit:
    if not all([user_name, user_company, target_company, target_url]):
        st.error("Please fill in all fields")
    else:
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            progress_text.text("Analyzing target company...")
            progress_bar.progress(20)
            
            # Initialize LLM
            my_llm = LLM(
                model="groq/llama-3.3-70b-versatile",
                api_key=os.getenv("GROQ_API_KEY")
            )
            
            scrape_tool = ScrapeWebsiteTool()
            
            progress_text.text("Initializing AI agents...")
            progress_bar.progress(40)
            
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
            
            progress_text.text("Creating strategy...")
            progress_bar.progress(60)
            
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
            
            progress_text.text("Writing your email...")
            progress_bar.progress(80)
            
            # Create and run crew
            sales_crew = Crew(
                agents=[researcher, strategist, writer],
                tasks=[task_analyze, task_strategize, task_write],
                process=Process.sequential,
                verbose=False
            )
            
            result = sales_crew.kickoff()
            
            progress_bar.progress(100)
            progress_text.empty()
            progress_bar.empty()
            
            # Display result
            st.markdown("<div class='success-box'>Email Generated Successfully!</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='email-container'>", unsafe_allow_html=True)
            st.markdown("### Your Personalized Cold Email")
            st.text_area("", value=str(result), height=350, label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Download button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Email",
                    data=str(result),
                    file_name=f"cold_email_{target_company.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            
        except Exception as e:
            progress_text.empty()
            progress_bar.empty()
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>
        Powered by AI Agents • Built with Streamlit
    </div>
""", unsafe_allow_html=True)
