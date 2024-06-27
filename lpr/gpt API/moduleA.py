import openai
openai.api_key = "API KEY"


if __name__ == '__main__':
    # 5.24 VERSION
    # question = '腰椎间盘突出压迫神经手术大吗'
    # prompt = f'''
    # 回答问题：{question} \n
    # 答案的要求如下：
    # 1、答案第一句话要求直接回答问题，是或者不是，可以或者不可以，等判断类的问题，要直接给出判断。针对需要多少时间，大概多少费用这类疑问句问题，也要直接回答问题。
    # 2、第二句话，希望能够详细展开这个答案的原因，帮助理解答案。第一句话和第二句话之间加换行。
    # 3、回答问题最好条理清楚，有层次，逻辑严谨，用词简洁。整个答案字数在90-100中文字符之间，不能超过100个中文字符。


    # 6.15 VERSION
    question = '腰椎间盘突出压迫神经手术大吗'
    system_prompt = '假如你来扮演健康专家，针对问题给出答案。'
    
    # gpt-4 is not available for current version
    completion = openai.ChatCompletion.create(model="gpt-4",
                                              messages=[
                                                  {"role": "system", "content": system_prompt},
                                                  {"role": "user", "content": f'''1、答案第一句话要求直接回答问题，最好能将答案带入到问题中，完整的表达出来。针对需要多少时间，大概多少费用这类疑问句问题，也要直接回答问题。
2、第二句话要求对答案第一句话进行详细说明，说明这么回答的原因，理论基础等，比如能解释为什么，相关背景，背后的逻辑等。
3、答案的第一句话和第二句话之间加换行。
4、回答问题最好条理清楚，逻辑严谨，用词简洁，符合医学专业性，不能违背医学伦理。
5、对整个回答要求语言通顺，没有语病，标点符号规范，少用生僻字。
5、整个答案字数在90-110字符之间，一定不要超过110个字。
问题是###{question}###'''}
                                              ],
                                              temperature=1,
                                              max_tokens=150,
                                              top_p=1,
                                              frequency_penalty=0,
                                              presence_penalty=0
                                              )
                                              
    print(completion.choices[0].message.content)

