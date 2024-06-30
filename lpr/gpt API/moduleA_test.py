import openai
import pandas as pd

openai.api_key = "API KEY"

questions = [
    "引起颈椎病发作的原因有哪些",
    "颈椎病的背部疼痛特点是什么",
    "颈椎病手术后的注意事项",
    "为何一喝酒颈椎病就疼",
    "不枕枕头睡觉对颈椎病有没有好处吗",
    "男性慢性尿道炎症状表现有哪些",
    "甲硝唑可以治疗尿道炎吗",
    "尿道炎不治疗会怎么样",
    "尿道炎常用的药物治疗有什么",
    "急性尿道炎饮食提醒事项有哪些",
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
    "轻微肩周炎的症状",
    "针灸治疗前列腺炎效果如何",
    "前列腺炎打什么点滴",
    "得了前列腺炎还可以自慰吗",
    "温水坐浴治疗前列腺炎需要多长时间",
    "前列腺炎与手淫有啥关系",
    "前列腺炎去医院怎么查",
    "跑步能治疗前列腺炎",
    "前列腺炎哪科看好",
    "如何区分膀胱炎和前列腺炎",
    "前列腺炎是哪个部位疼"
]

system_prompt = '假如你来扮演健康专家，针对问题给出答案。'

responses = []

for question in questions:
    completion = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0125:personal:morethan95chars:9fppAyW7",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'1、答案第一句话要求直接回答问题，最好能将答案带入到问题中，完整的表达出来。针对需要多少时间，大概多少费用这类疑问句问题，也要直接回答问题。\
                2、第二句话要求对答案第一句话进行详细说明，说明这么回答的原因，理论基础等，比如能解释为什么，相关背景，背后的逻辑等。\
                3、答案的第一句话和第二句话之间加换行。\
                4、回答问题最好条理清楚，逻辑严谨，用词简洁，符合医学专业性，不能违背医学伦理。\
                5、对整个回答要求语言通顺，没有语病，标点符号规范，少用生僻字。\
                6、整个答案字数在90-110中文字之间，一定不要超过110个字。\
                问题是###{question}###'}
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response = completion.choices[0].message["content"].strip()
    responses.append({
        "Question": question,
        "Response": response,
        "Character Count": len(response)
    })

df = pd.DataFrame(responses)
df.to_excel("result.xlsx", index=False)

print("Responses have been saved to 'result.xlsx'")