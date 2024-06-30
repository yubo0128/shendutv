import pandas as pd
import json
import random

# Load your Excel file
df = pd.read_excel('GPT生成的A-20240629.xlsx')  # Replace with your file path

# Ensure your data is in the correct format
queries = df['query'].tolist()
original_texts = df['Gpt生成的原本的A'].tolist()
desired_outputs = df['修改后的'].tolist()

# Combine queries, original texts, and desired outputs into a list of tuples
data = list(zip(queries, original_texts, desired_outputs))

# Filter the data to include only those samples where '修改后的' has more than 95 characters
filtered_data = [item for item in data if len(item[2]) > 95]

# Randomly select 50 samples from the filtered data
random_samples = random.sample(filtered_data, min(50, len(filtered_data)))

# Define the system and user prompts
system_prompt = '假如你来扮演健康专家，针对问题给出答案。'
user_prompt_template = """1、答案第一句话要求直接回答问题，最好能将答案带入到问题中，完整的表达出来。针对需要多少时间，大概多少费用这类疑问句问题，也要直接回答问题。\
2、第二句话要求对答案第一句话进行详细说明，说明这么回答的原因，理论基础等，比如能解释为什么，相关背景，背后的逻辑等。\
3、答案的第一句话和第二句话之间加换行。\
4、回答问题最好条理清楚，逻辑严谨，用词简洁，符合医学专业性，不能违背医学伦理。\
5、对整个回答要求语言通顺，没有语病，标点符号规范，少用生僻字。\
6、整个答案字数在90-110中文字之间，一定不要超过110个字。\
问题是###{query}###"""

# Create the training data
training_data = []
for query, _, output in random_samples:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_template.replace('{query}', query)},
        {"role": "assistant", "content": output}
    ]
    training_data.append({"messages": messages})

# Save the training data to a JSONL file
with open('chat_training_data.jsonl', 'w', encoding='utf-8') as f:
    for entry in training_data:
        json.dump(entry, f, ensure_ascii=False)
        f.write('\n')

print("Chat-formatted training data with more than 95 characters in '修改后的' has been saved to 'chat_training_data.jsonl'")
