import urllib.request
import os
import re
import sys

def url_open(url):  
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()

    return html
    

def find_imgs(url):
    html = url_open(url).decode('gbk')
    img_addres = []

    reg = r'http://ymz.qqwmb.com/allimg/c.*\.gif'
    for each in re.findall(reg,html):
        url = each
        img_addres.append(url)
    return img_addres
    

def save_imgs(folder,img_addres):
    for each in img_addres:
        filename = each.split('/')[5]
        with open(filename,'wb') as f:
            img = url_open(each)
            f.write(img)
            
def download_mm(folder='xxoo'):
    try:
        os.mkdir(folder)
        os.chdir(folder)
    except:
        os.chdir(folder)
    url = 'http://www.youmzi.com/meinvgif.html'
    reg = 'meinvgif_[0-9][0-9]?.html' ##找到最后一页的网址的正则
    pages = re.findall(reg, url_open(url).decode('gbk'))
  
    reg ='[0-9]+'
    lastpage = re.findall(reg,pages[-1])[0]

    for page in range(5,int(lastpage)):
        print('正在下载第%d页...'%(page+1))
        url = "http://www.youmzi.com/meinvgif_"+str(page+1)+".html"
        img_adress = find_imgs(url)
        save_imgs(folder,img_adress)
    
if __name__ == "__main__":
    download_mm()
