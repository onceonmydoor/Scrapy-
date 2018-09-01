from urllib import request
from base64 import b64encode
import requests
captcha_url='https://www.douban.com/misc/captcha?id=Ukb5u5EUMiMEcTARld2p4sH2:en&size=s'

regonize_url = 'https://302307.market.alicloudapi.com/ocr/captcha'

request.urlretrieve(captcha_url,'captcha.png')

formdata={}
with open('captcha.png','rb')as fp:
    data =fp.read()
    pic =b64encode(data)
    formdata['image']=pic
    formdata['type']= 1001
appcode ='8e3f46a30db9467c82e0cb1b40a008aa'

headers ={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Authorization':'APPCODE ' + appcode
}
response =requests.post(regonize_url,data=formdata,headers=headers)
print(response.json())
