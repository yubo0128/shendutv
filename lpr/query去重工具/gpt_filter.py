import requests
import json
import openai
# openai.api_key = "API KEY"
if __name__ == '__main__':
    url = "http://online-hc.shendutv.com/prod-api/sdgather/douyinDistinct/list-title?title=推拿&pageNum=1&pageSize=100"
    payload ={}
    response = requests.request("GET", url, data=payload)
    data = json.loads(response.text)
    arr = []
    for item in data['rows']:
        if '颈椎病' in item['title']:
            arr.append(item['title'])
    print(arr)

    '''
        提取出下列问题中，除“{diease}”外，一个跟医学科普最相关的关键词，每行一个词，不需要写序号：
        {question}
        
        下列问题中，是否有与‘{question}’语义重复的问题。如果没有，返回否。如果有，返回是和所有语义重复的问题。
        {filtered_question list}  
    '''
