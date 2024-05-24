import openai
openai.api_key = "YOUR API KEY"

if __name__ == '__main__':
    title = ''
    prompt = f'''
    {title} \n
    这是一个标题，我要给它做一个封面，请帮我完成换行操作。
    换行要求是：1、封面能排列两行内容，每行字数不能超过10个。
    2、换行后，上下两行居中排列，找出排列最好看的一种
    3、不要将固定词语分在上下两行内
    '''

    # gpt-4 is not available for current version
    completion = openai.ChatCompletion.create(model="gpt-4",
                                              messages=[{"role": "user", "content": prompt}])
    print(completion.choices[0].message.content)

