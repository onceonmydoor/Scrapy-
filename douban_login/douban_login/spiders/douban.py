# -*- coding: utf-8 -*-
# source: index_nav
# redir: https://www.douban.com/
# form_email: 15958036201
# form_password: 12
# captcha-solution: argument
# captcha-id: cFtKj3ltWDZrbyGYjl8kroj2:en
# login: 登录
import scrapy
from urllib import request
from PIL import Image
import urllib,urllib3, sys
import ssl
from base64 import b64encode
import requests
import json

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login']
    login_url ='https://accounts.douban.com/login'
    profile_url = 'https://www.douban.com/people/155728538/'
    editsign_url = 'https://www.douban.com/j/people/155728538/edit_signature'

    def parse(self, response):
        formdata={
            'source':'None',
            'redir':'https://www.douban.com/',
            'form_email':'15958036201',
            'form_password':'huangzhanjie.',
            'remember':'on',
            'login':'登录'
        }
        captcha_img =response.xpath("//img[@id='captcha_image']/@src").get()
        if captcha_img :
            captcha =self.regonize_captcha(captcha_img)
            formdata['captcha-solution']=captcha
            id =response.xpath("//div[@class='captcha_block']//input[@type='hidden']/@value").get()
            formdata['captcha-id']=id
        yield scrapy.FormRequest(url=self.login_url,formdata=formdata,callback=self.parse_after_login)
    def parse_after_login(self,response):
        if response.url == 'https://www.douban.com/':
            yield scrapy.Request(self.profile_url,callback=self.parse_profile)
            print("登录成功")
        else:
            print("登录失败")
    def parse_profile(self,response):
        print(response.url)
        if response.url == self.profile_url:
            print("已经进入个人中心")
            ck =response.xpath("//div[@style='display:none;']/input[@name='ck']/@value").get()
            formdate ={
                'ck':ck
            }
            signature = input("请输入想要修改的签名：")
            formdate['signature'] =signature
            yield  scrapy.FormRequest(url=self.editsign_url,formdata=formdate,callback=self.parse_none)

        else:
            print('X'*40)
            print("没有进入个人中心")
    def parse_none(self):
        pass


    def regonize_captcha(self,img_url):
        request.urlretrieve(img_url,'captcha.png')
        form ={}
        with open('captcha.png','rb')as fp:
            data =fp.read()
            v_pic = b64encode(data)
            form['v_pic']=v_pic
            form['v_type']='cn'

        appcode ='8e3f46a30db9467c82e0cb1b40a008aa'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'APPCODE ' + appcode
        }
        regonize_url = 'http://yzmplus.market.alicloudapi.com/fzyzm'
        res =requests.post(regonize_url,data=form,headers=headers)
        result = res.json()
        print(result)

        code =result['v_code']
        print("="*40)
        print(code)
        print("=" * 40)
        return code
        # image =Image.open('captcha.png')
        # image.show()
        # capt =input("请输入验证码：")
        # return capt