import requests
import json
'''
一、‘过渡句大全’查询‘模块’、‘1/2’接口（python dataframe、jason）
type：区分开头编码还是收尾模块结束模块  1代表开头  2代表收尾
nameCode：延展模块类型比如：ZZ、WH、BY、YY、CB、JC等 示例如下
'''
url = "http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-type-list?type=1&nameCode=ZZ"

payload={}
response = requests.request("GET", url, data=payload)
data = json.loads(response.text)
print(data['data'])



'''
二、查询‘病种-模块’接口（python dataframe、jason）
参数放在接口url的最后一位上‘病种-模块’ 示例如下
'''

# url = "http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-list/BDF-YY"
# url = "http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-list/JQY-ZZ"
url = "http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-list/BJXQGY-YF"
response = requests.request("GET", url, data=payload)
data = json.loads(response.text)
print(data['data'])

'''
带过渡句的接口
'''
url = "http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-list-transition/AZB-WH"
response = requests.request("GET", url, data=payload)
data = json.loads(response.text)
print("测试")
print(data['data'])

'''
三、查询所有疾病模块接口
'''
url = "http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-list-all"
response = requests.request("GET", url, data=payload)
data = json.loads(response.text)
print(data['data'])