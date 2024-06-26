import openai
import pandas as pd

# openai.api_key = "API key"

questions = [
    "肩周炎发病的原因是什么",
    "什么是外伤性肩周炎",
    "肩周炎怎么得的",
    "肩周炎会传染吗",
    "肩周炎看可以看骨科吗",
    "长期抱小孩会肩周炎吗",
    "什么是五十肩",
    "肩周炎挂哪个科",
    "检查肩周炎挂什么科室",
    "肩周炎检查什么科",
    "肩周炎挂什么科室",
    "肩周炎属于什么科室",
    "轻微肩周炎的症状"
]

system_prompt = '假如现在由你来扮演一个健康助手，我会向你提出具体问题，你给我一个专业易懂的答案。答案的字数要求在80-100字符之间，一定不要超过100个字。'

responses = []

for question in questions:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'答案分两个部分，一部分是最直接的，针对这个问题的结论性回答，让我知道该怎么做，多少钱，分几类，能不能做，对不对等。然后换行，输出第二部分内容，第二部分内容是针对第一部分结论性回答的解释，说明和延展。比如能解释为什么，相关背景，作为健康助手你的建议等等。\n我的问题是###{question}###'}
        ],
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response = completion.choices[0].message.content.strip()
    responses.append({
        "Question": question,
        "Response": response,
        "Character Count": len(response)
    })

df = pd.DataFrame(responses)
df.to_excel("result.xlsx", index=False)
