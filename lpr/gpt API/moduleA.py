import openai
openai.api_key = "YOUR API KEY"

if __name__ == '__main__':
    question = '低钾血症会导致房颤吗'
    prompt = f'''
    回答问题：{question} \n
    答案的要求如下：
    1、答案第一句话要求直接回答问题，是或者不是，可以或者不可以，等判断类的问题，要直接给出判断。针对需要多少时间，大概多少费用这类疑问句问题，也要直接回答问题。
    2、第二句话，希望能够详细展开这个答案的原因，帮助理解答案。第一句话和第二句话之间加换行。
    3、回答问题最好条理清楚，有层次，逻辑严谨，用词简洁。整个答案字数在90-100字之间。
    '''

    # gpt-4 is not available for current version
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "user", "content": prompt}])
    print(completion.choices[0].message.content)

