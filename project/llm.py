from openai import OpenAI

def generate_review(user_content):
    client = OpenAI(
           api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiY2U4MGY4NzgtMzJlMy00OTgzLWJmYTMtOWQxZjVmNDg4YTViIiwiZXhwIjoyNTM0MDIzMDA3OTl9.0xN8acFvMbKKs9IiTMziS7PwWCRX09WMJzn7ch0kgko",
           base_url="https://apigateway.avangenio.net",
         )

    completion = client.chat.completions.create(
           messages=[
             { "role": "system", "content": "You are a Tourist writing a review about the Hotel Banana" },
             { "role": "user", "content": f'{user_content}' }
           ],
           model="spark",
         )
     
    return completion.choices[0].message.content



#print(generate_review(user_content))

def classify_review(user_content):
    client = OpenAI(
           api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiY2U4MGY4NzgtMzJlMy00OTgzLWJmYTMtOWQxZjVmNDg4YTViIiwiZXhwIjoyNTM0MDIzMDA3OTl9.0xN8acFvMbKKs9IiTMziS7PwWCRX09WMJzn7ch0kgko",
           base_url="https://apigateway.avangenio.net",
         )

    completion = client.chat.completions.create(
           messages=[
             { "role": "system", "content": "You can classify a tourist's experience into 'very good', 'good', 'fair', 'bad' or 'very bad' (without giving explanations, only the classification) based on their review" },
             { "role": "user", "content": f'{user_content}' }
           ],
           model="spark",
         )
     
    return completion.choices[0].message.content




# from transformers import pipeline
# from transformers import BertTokenizerFast, BertConfig, BertForSequenceClassification
# import torch

# generator = pipeline('text-generation', model='gpt2')

# def generate_review(experience):
#     prompt = f"Based on the following experience of tourist at hotel, write a review: {experience}"
#     result = generator(prompt, max_length=100, num_return_sequences=1)
#     review = result[0]['generated_text']
#     return review

# #experience = "The hotel was clean and the staff was friendly. The food was excellent, but the pool was a bit small."
# #review = generate_review(experience)
# #print(review)

# # Cargar el tokenizador
# tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

# # Crear una configuración personalizada para el modelo
# config = BertConfig.from_pretrained('bert-base-uncased', num_labels=5)  # Especificar el número de clases

# # Cargar el modelo con la nueva configuración
# model = BertForSequenceClassification._from_config(config)

# def classify_review(review):
#     inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
#     outputs = model(**inputs)
#     _, predicted = torch.max(outputs.logits, dim=1)
    
#     # Mapeo de los índices de predicción a las etiquetas correspondientes
#     labels = ["very bad", "bad", "improvable", "good", "very good"]  # Definir tus propias etiquetas
#     return labels[predicted.item()]

# #review = "The food was delicious and the service was excellent."

# #print(classify_experience(review))




























# #from transformers import pipeline
# from transformers import BertTokenizerFast, BertConfig, BertForSequenceClassification
# import torch

# #generator = pipeline('text-generation', model='gpt-3')
# # Cargar el tokenizador
# tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

# # Crear una configuración personalizada para el modelo
# config = BertConfig.from_pretrained('bert-base-uncased', num_labels=5)  # Especificar el número de clases

# # Cargar el modelo con la nueva configuración
# model = BertForSequenceClassification._from_config(config)

# # def generate_review(experience):
# #     result = generator(experience, max_length=100, num_return_sequences=1)
# #     review = result[0]['generated_text']
# #     return review

# def classify_experience(review):
#     inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
#     outputs = model(**inputs)
#     _, predicted = torch.max(outputs.logits, dim=1)
    
#     # Mapeo de los índices de predicción a las etiquetas correspondientes
#     labels = ["very bad", "bad", "improvable", "good", "very good"]  # Definir tus propias etiquetas
#     return labels[predicted.item()]

# review = "The food was delicious and the service was excellent."

# print(classify_experience(review))






# survey_eng = """How would you rate the booking process? 
#                 Was the check-in process efficient? / Are you satisfied with the features of your room?
#                 Do you feel satisfied with the cleanliness and maintenance of your room?
#                 How would you rate the quality of service in general?
#                 Did you use the additional facilities such as the restaurant or spa?
#                 How would you rate the variety of amenities offered?
#                 Were the staff friendly and helpful during your stay?
#                 Were there any issues that were not satisfactorily resolved?
#                 Do you think that the price paid was fair for the experience received?
#                 Would you recommend our hotel to others based on your experience?"""

# survey_esp = """¿Cómo calificarías el proceso de reserva? 
#                 ¿Fue eficiente el proceso de check-in? / ¿Está satisfecho con las características de su habitación?
#                 ¿Te sientes satisfecho con la limpieza y el mantenimiento de tu habitación?
#                 ¿Cómo calificarías la calidad del servicio en general?
#                 ¿Utilizaste las instalaciones adicionales como el restaurante o el spa?
#                 ¿Cómo calificarías la variedad de comodidades ofrecidas?
#                 ¿El personal fue amable y servicial durante tu estancia?
#                 ¿Hubo algún problema que no se resolvió satisfactoriamente?
#                 ¿Consideras que el precio pagado fue justo por la experiencia recibida?
#                 ¿Recomendarías nuestro hotel a otros basándote en tu experiencia?"""
