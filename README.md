


# 🚀 VenturePilot

## Overview
**VenturePilot** is an AI-powered platform designed to help entrepreneurs streamline their startup journey. It automates critical business processes, from idea validation and financial forecasting to investor matching and pitch deck analysis. Additionally, it includes **email and calendar automation** to enhance business communications.

## 🌟 Features

### 🔍 **Idea Validation and Research**
- Enter key details (Startup Name, Problem Statement, Target Audience, Business Model).
- AI generates:
  - **Viability Score** – A feasibility rating of the idea.
  - **Market & Competitor Analysis** – Industry trends and competitor insights.
  - **Business Recommendations** – Actionable strategy tips.
  - **SWOT Analysis** – Strengths, Weaknesses, Opportunities, and Threats.

### 📊 **Financial Projection & Expense Breakdown**
- Generate **automated financial forecasts** including:
  - Revenue projections with growth analysis.
  - Expense breakdowns by category.
  - Essential financial documents required at each stage.
- Helps founders plan finances efficiently and mitigate risks.

### 🤝 **Investor-Founder Matching**
- Uses **Crunchbase API** to:
  - Identify investors who have previously funded startups in the same industry.
  - Display investment history and amounts raised.
  - Prioritize investors most likely to be interested in the startup.

### 📑 **Pitch Deck Generator**
- Automatically generates a structured **pitch deck** with:
  - Key business highlights.
  - Market insights and revenue projections.
  - Competitive analysis and financial forecasts.

### 🎤 **Voice-to-Text Pitch Deck Analysis**
- Uses AI-powered **speech analysis** to:
  - Convert speech to text during a pitch.
  - Perform **sentiment analysis** on tone and confidence.
  - Provide actionable feedback on how to **improve pitch delivery**.

### 📬 **Email and Calendar Automation**
- **Email Automation**:
  - Send emails instantly from the platform.
  - Create and save reusable email templates.
- **Meeting Scheduling**:
  - Sync with calendars, set availability, and automate reminders.

---

## 🚀 Getting Started
### **1️⃣ Installation**
Ensure you have **Node.js**, **Python**, and **Streamlit** installed.
```bash
npm install
pip install -r requirements.txt
```

### **2️⃣ Running the Application**
To start the full platform, open **multiple terminals** and run:

#### **Frontend (Next.js Application)**
```bash
npm run dev
```

#### **Backend Processes**
Run these commands in **separate terminals**:
```bash
streamlit run app.py  # Pitch Deck Generation
python investor.py    # Investor-Founder Matching
streamlit run pitchsound.py  # Voice-to-Text Pitch Deck Analysis
```

---



