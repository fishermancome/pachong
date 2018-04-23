# coding:utf-8

import requests
import re
import time
import os
import pandas as pd  
import csv

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}
def get_html(url):
        res = requests.get(url,headers=headers)
        html = res.text
        #print(html)
        return html
def get_content(html):
        regstr = re.compile('i class="cell date.*?span>(.*?)</span>.*?maincell.*?span>(.*?)'
                +'</span>.*?a href=".*?">(.*?)</a>.*?a href=".*?">(.*?)</a>.*?round.*?gray">'
                +'(.*?)</span>.*?money">(.*?)</i>.*?name.*?investorset">(.*?)</div>',re.S)        
        items = re.findall(regstr,html)
       
        for i in items:
                investment = re.sub('\s+',' ',i[6])
                #print(investment)
                ahref = re.compile('href=".*?">(.*?)</a>',re.S)
                span = re.compile('c-gray">(.*?)</span>',re.S)
                name = []
                a_names = re.findall(ahref,investment)
                span_names = re.findall(span,investment)
                for a_name  in a_names:
                        name.append(a_name)
                for span_name in span_names:
                        name.append(span_name)
                        
                yield {
                "date":i[0],
                "company":i[1],
                "type":i[2],
                "zone":i[3],
                "round":i[4],
                "money":i[5],
                "invesgate":' '.join(name)
                }



if __name__ == '__main__':
        baseurl = "https://www.itjuzi.com/investevents?page="
        date = []
        company = []
        _type = []
        zone= []
        _round =[]
        money = []
        invesgate = []
        for i in range(10,30):
                url = baseurl+str(i)
                html = get_html(url)
                print("页面获取成功")
                items = get_content(html)
               
                for i in items:
                        date.append(i['date'])
                        company.append(i['company'])
                        _type.append(i['type'])
                        zone.append(i['zone'])
                        _round.append(i['round'])
                        money.append(i['money'])
                        invesgate.append(i['invesgate'])
                        list1 = list([i['date'],i['company'],i['type'],i['zone'],i['round'],i['money'],i['invesgate']])
                        
                
                time.sleep(4)
        data = {'date':date,'company':company,'type':_type,'zone':zone,'round':_round,'money':money,'invesgate':invesgate}
        df = pd.DataFrame(data=data)
        df.to_csv('hello.csv',index=False)
        
