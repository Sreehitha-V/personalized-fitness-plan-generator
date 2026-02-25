# Milestone 2: Core AI Model Integration 🤖

## Objective
The objective of this milestone is to integrate a Large Language Model (LLM) into the FitPlan AI application. This transformation moves the project from a static data collection form to an intelligent system capable of generating dynamic, personalized workout routines based on specific user health metrics and fitness goals.

## Model Name Used
* **Model:** `HuggingFaceH4/zephyr-7b-beta` (or insert your specific model name here)
* **Framework:** Hugging Face Inference API / Transformers

## Prompt Design Explanation
The core of this milestone is the "Prompt Builder" logic. To ensure the AI generates high-quality, safe, and relevant fitness plans, a structured prompt template was designed:
* **Role Acted:** Professional Fitness Coach.
* **Input Injection:** Dynamically injects the user's Name, BMI Category, Fitness Goal, Experience Level, and Available Equipment.
* **Constraints:** Specifically instructs the model to only include exercises possible with the user's "Available Equipment" to ensure the plan is actionable.
* **Formatting:** Requests a clear, day-by-day breakdown (e.g., 3-day or 7-day splits).

## Steps Performed
1. **Model Loading**: Configured the application to connect to the Hugging Face Hub, ensuring secure authentication via API tokens stored in Streamlit secrets.
2. **Prompt Creation**: Developed `prompt_builder.py` to handle the logic of turning raw user inputs (like "Dumbbells" and "Weight Loss") into a detailed natural language instruction for the AI.
3. **Inference Testing**: Conducted rigorous testing across multiple user scenarios (e.g., Beginner with no equipment vs. Advanced with a full gym) to ensure the model produces consistent results.
4. **Error Handling**: Implemented "Graceful Failure" logic to notify the user if the model is currently loading or if the API limit has been reached.
5. **Deployment**: Deployed the updated AI-powered engine to Hugging Face Spaces.

## Sample Generated Output
**User Scenario:** Beginner, Goal: Build Muscle, Equipment: Dumbbells.
> "Day 1: Upper Body - Dumbbell Bench Press: 3 sets of 8-10 reps. Dumbbell Rows: 3 sets of 10-12 reps. Overhead Press: 3 sets of 8-10 reps. Ensure 60s rest between sets..."

## Application Link
[[Live Hugging Face Space Link](https://huggingface.co/spaces/Sreehitha-V/FitPlan_1)]
## Screenshots
### 1. Core AI Inference Module
![AI Logic](Milestone 2/screenshots/User Profile.png)

### 2. Personalized Plan Result
![Plan Output](Milestone2/screenshots/result_screenshot.png)
