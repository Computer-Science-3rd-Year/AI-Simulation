# pip install --upgrade openai
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

def classif_review(user_content):
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

# user_content_ = """ I recently had the pleasure of staying at the Hotel Riviera, and while my overall experience was quite enjoyable, there was one aspect that left me feeling a bit disappointed. I was excited to try their special energy drink, which they claim is a unique blend of local ingredients and flavors. Unfortunately, the energy drink was nohe energy drink was not to my liking. The taste was unpleasantly sweet and the aftertaste lingered for too long.

# Other than the energy drink, my stay at the Hotel Riviera was excellent. The staff was friendly and attentive, the rooms were clean and comfortable, and the location was perfect for exploring the city. The breakfast buffet was also impressive, with a wide variety of delicious options to choose from.

# I would recommend the Hotel Riviera to anyone looking for a convenient and comfortable place to stay in the city. Just be sure to avoid the energy drink, and you'll be all set for a wonderful trip!

# Positives: Friendly staff, comfortable rooms, great location, excellent breakfast buffet

# Negatives: Energy drink was not good """

# print(classif_review(user_content_))