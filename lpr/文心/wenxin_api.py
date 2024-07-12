import os
import qianfan

#【推荐】使用安全认证AK/SK鉴权，通过环境变量初始化认证信息
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_AK"] = ""
os.environ["QIANFAN_SK"] = ""

import pandas as pd
import qianfan

# Function to call Wenxin model
def get_wenxin_response(query):
    resp = qianfan.ChatCompletion().do(
        endpoint="completions_pro",
        messages=[{"role": "user", "content": query}],
        temperature=0.95,
        top_p=0.8,
        penalty_score=1,
        disable_search=False,
        enable_citation=False
    )
    return resp.body['result']

# Load the Excel file
file_path = 'GPT生成的A比对-Levenshtein-20240711.xlsx'  # replace with the actual path to your Excel file
df = pd.read_excel(file_path)

# Add a new column for Wenxin model results
df['文心生成的'] = ''

# Get Wenxin responses for each query
for index, row in df.iterrows():
    gpt_prompt = f"""
    假如你来扮演健康专家，针对问题给出答案。
    1、答案第一句话要求直接回答问题，最好能将答案带入到问题中，完整的表达出来。针对需要多少时间，大概多少费用这类疑问句问题，也要直接回答问题。
    2、第二句话要求对答案第一句话进行详细说明，说明这么回答的原因，理论基础等，比如能解释为什么，相关背景，背后的逻辑等。
    3、答案的第一句话和第二句话之间加换行。
    4、回答问题最好条理清楚，逻辑严谨，用词简洁，符合医学专业性，不能违背医学伦理。
    5、对整个回答要求语言通顺，没有语病，标点符号规范，少用生僻字。
    5、整个答案字数在90-110字符之间，一定不要超过110个字。
    问题是###{row['query']}###
    """
    wenxin_response = get_wenxin_response(gpt_prompt)
    print(wenxin_response)
    df.at[index, '文心生成的'] = wenxin_response

# Save the updated dataframe back to Excel
output_file_path = 'updated_GPT生成的A比对-Levenshtein-20240711.xlsx'  # replace with the desired output path
df.to_excel(output_file_path, index=False)