import requests
import pymysql,re,time


db = pymysql.connect(
            #host='98.142.140.54',
            host='127.0.0.1',
            port = 3306,
            user='root',
            #passwd='APTX4369',
            passwd='',
            db ='test',
            charset='utf8'
            )
cursor=db.cursor()
cookies={
        'bid':'zmrKGEvLMkw',
        'gr_user_id':'0a7afdfd - 1b63 - 4899 - abe6 - 771b2c3674fc',
        'll':"108289",
        'viewed':"4828875_3288908_24703171",
        'ps':'y',
        'ap' : 1,
        'ue' : "48450976@qq.com",
        'dbcl2' : "159444618:vzET3x2tiaE",
        'ck' : 'CMVL_pk_ref.100001.8cb4 = % 5B % 22 % 22 % 2C % 22 % 22 % 2C1490260693 % 2C % 22https % 3\
        A % 2F % 2Faccounts.douban.com % 2Flogin % 22 % 5D',
        'push_noty_num' : 0,
        'push_doumail_num' :0,
        '_pk_id.100001.8cb4' : '4615bb76fa621e32.1478607450.7.1490261182.1490258760.',
        '_pk_ses.100001.8cb4' : '*',
        '__utma' : '30149280.1261062391.1478527591.1490258505.1490258583.18',
        '__utmb' : '30149280.6.10.1490258583',
        '__utmc' : '30149280',
        '__utmz' : '30149280.1490258583.18.10.utmcsr = baidu | utmccn = (organic) | utmcmd = organic',
        '__utmv' : '30149280.15944',
        '_vwo_uuid_v2' : '61DCE5169C3BD469097D2632928009A0 | 7d3c0bee4ff6dd33cbd594f0f69f5c5b'
    }
def getData():
    sql='select id,douId from movie where img_url is null'
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def updateMov(id,img):
    sql='update movie set img_url="%s" where id=%s'%(img,id)
    return cursor.execute(sql)

def getImgUrl(douId):
    url='https://movie.douban.com/subject/'+str(douId)
    r=requests.get(url)
    content=r.text
    pattern=re.compile(r'id="mainpic"[\s\S]*?src\s?=\s?"(.*?)"')
    imgs=pattern.findall(content)
    if imgs:
        return imgs[0]

if __name__=='__main__':
  #  while True:
        data=getData()
        for item in data:
            res=getImgUrl(item[1])
            if res:
                updateMov(item[0],res)
            else:
                updateMov(item[0], '')
                print(item[0])
            db.commit()
            time.sleep(2)