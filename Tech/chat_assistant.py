import openai
from credentials import openai_api_key
from document_parser import processor


openai.api_key = openai_api_key

def get_advice_from_docs(question):
    full_text = "\n".join(processor.documents.values())
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты помощник, анализирующий документы и помогающий пилотам и инженерами,"
                                          " не проси больше информации и тд."},
            {"role": "user", "content": f"Документы: {full_text}"},
            {"role": "user", "content": f"Вопрос: {question}"}
        ]
    )
    return response["choices"][0]["message"]["content"]