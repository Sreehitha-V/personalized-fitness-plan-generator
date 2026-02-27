from huggingface_hub import InferenceClient
import os

def query_model(prompt):
    try:
        HF_TOKEN = os.getenv("HF_TOKEN")

        client = InferenceClient(
            model="Qwen/Qwen2.5-7B-Instruct",
            token=HF_TOKEN
        )

        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a certified professional fitness trainer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2400,      # increase slightly
            temperature=0.6,      # lower randomness
            top_p=0.9
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
