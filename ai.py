from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def generate_truth():
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Give 1 fun truth question"}]
    )
    return res.choices[0].message.content

def generate_dare():
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Give 1 fun dare"}]
    )
    return res.choices[0].message.content