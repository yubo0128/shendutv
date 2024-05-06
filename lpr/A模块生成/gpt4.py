import openai
openai.api_key = "YOUR API KEY"

if __name__ == '__main__':
    question = '低钾血症会导致房颤吗'
    prompt = f'''
    请回答问题，“{question}”
    答案要求：1、第一句话要求直接回答问题，既是回答问题的答案，也能对下面的文字进行概括。2、答案不超过300字。3、答案要求条理清晰，排版最好用一、二、三。
    '''

    # gpt-4 is not available for current version
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "user", "content": prompt}])
    print(completion.choices[0].message.content)

