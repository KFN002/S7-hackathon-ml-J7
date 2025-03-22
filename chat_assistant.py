import openai
from credentials import chatgpt_token
from document_parser import processor


OPENAI_API_KEY = chatgpt_token

def get_advice_from_docs(question):
    full_text = "\n".join(processor.documents.values())
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помощник, анализирующий документы."},
            {"role": "user", "content": f"Документы: {full_text}"},
            {"role": "user", "content": f"Вопрос: {question}"}
        ]
    )
    return response["choices"][0]["message"]["content"]