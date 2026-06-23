# 🏋️ FitPlan AI

## 📌 Project Overview

FitPlan AI is an AI-powered fitness planning application that generates personalized workout and diet plans based on user demographics, fitness goals, and activity levels. The platform combines artificial intelligence, secure authentication, progress tracking, and automated reminders to help users maintain consistency throughout their fitness journey.

Designed with a modular architecture, FitPlan AI offers a seamless experience for creating customized fitness plans, monitoring progress, and receiving intelligent recommendations through an interactive dashboard.

---

## ✨ Features

* 🤖 AI-generated personalized workout plans
* 🥗 Customized diet recommendations
* 🔐 Secure user authentication with OTP verification
* 📊 Progress and streak tracking
* 📅 Daily fitness reminders
* 📧 Weekly email summaries and notifications
* 👤 User profile management
* 🎯 Goal-oriented fitness planning
* ⚠️ Input validation and error handling
* 📱 Responsive and user-friendly interface

---

## 🛠️ Tech Stack

| Category       | Technology                   |
| -------------- | ---------------------------- |
| Frontend       | Streamlit                    |
| Backend        | Python                       |
| Database       | SQLite                       |
| AI Model       | Gemini API                   |
| Authentication | OTP-based Email Verification |
| Deployment     | Docker, Hugging Face Spaces  |

---

## 📂 Project Structure

```bash
FitPlan-AI/
│
├── pages/                  # Multi-page application modules
├── utils/                  # Utility functions and database operations
│
├── app.py                  # Main application entry point
├── auth_token.py           # Authentication and OTP management
├── model_api.py            # AI model integration
├── prompt_builder.py       # Prompt engineering
├── daily_reminder.py       # Daily reminder service
├── weekly_email.py         # Weekly email notifications
├── nav_component.py        # Navigation components
├── bg_utils.py             # UI utility functions
├── Dockerfile              # Docker configuration
├── requirements.txt        # Project dependencies
└── README.md
```

---

## 🚀 Application Workflow

1. User signs up and verifies their email using OTP authentication.
2. User enters demographic and fitness-related information.
3. AI processes the user profile and fitness goals.
4. Personalized workout and diet plans are generated.
5. Progress and streaks are tracked over time.
6. Daily reminders and weekly emails help maintain consistency.

---

## 🚀 Live Demo

🔗 **Hugging Face Spaces:**
(https://huggingface.co/spaces/Sreehitha-V/FitPlan_AI_APersonalizedFitnessPlanGenerator)
---

## ⚙️ Installation

```bash
git clone <repository-url>
cd FitPlan-AI

pip install -r requirements.txt

streamlit run app.py
```

---

## 🎯 Future Enhancements

* Real-time AI fitness coaching
* Exercise video recommendations
* Advanced analytics dashboard
* Wearable device integration
* Community challenges and leaderboards

---

### FitPlan AI — Your Personalized Fitness Journey by AI 💪
