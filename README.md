# Cold Email Generator with Streamlit

An AI-powered cold email generator that uses CrewAI agents to analyze target companies and create personalized outreach emails.

## Features

- 🤖 AI-powered analysis using multiple specialized agents
- 🎨 Beautiful purple-themed UI
- 📊 Real-time progress tracking
- 📥 Download generated emails
- 🔍 Automatic company website analysis
- ✉️ Personalized email generation

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

4. Run the app:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push this repository to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your API keys in the Secrets section:
   - GROQ_API_KEY
   - SERPER_API_KEY
   - HUGGINGFACE_API_KEY
5. Deploy!

## Technologies Used

- Streamlit
- CrewAI
- Groq LLM
- Python
