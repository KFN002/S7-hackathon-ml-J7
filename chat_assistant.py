import openai

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

def get_checklist_advice(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Ты помощник для авиационных инженеров."},
                  {"role": "user", "content": question}]
    )
    return response["choices"][0]["message"]["content"]
