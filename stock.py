import requests #step1
from requests_html import HTML #step2


def fetch(url): #step1
    response = requests.get(url)
    return response

def parse_article_entries(doc): #step2
    html = HTML(html=doc)
    post_entries = html.find('table')
    return post_entries


def parse_article_meta(entry): #step3
    return {
    	'stocknum': entry.find('tr > th'), #find the stock number and name
        'datatype': entry.find('thead tr td'), #find the datatype in the table
        'data': entry.find('tbody tr td'), #find the data in the table
    }

def print_stockinfo(day,post_entries):
    if len(post_entries)==0:
        print('There isn\'t existing this stock')
    for entry in post_entries: 
        meta = parse_article_meta(entry)
        print('This is '+meta['stocknum'][0].text[8:16]) #print STOCK NO. and name 
        datatype=(meta['datatype'][0].text,meta['datatype'][3].text,meta['datatype'][4].text,meta['datatype'][5].text,meta['datatype'][6].text)
        datalist=[]
        i=0
        while i<len(meta['data']):  #make data be a list cataloged by date, and store in datalist
            tmplist=[]
            tmplist.append(meta['data'][i].text)
            j=1            
            while j<9:
                tmplist.append(meta['data'][i+j].text)                
                j=j+1        
            datalist.append(tmplist)
            i=i+j               
        datalist.reverse()  #make the latest data in the beginning of the datalist
        i=0
        while i<day:  #make the two row's data combine
            if i==10:
                print('The system is just storing the information of the stock in 10 days,\nso it\'s just shown the information in 10 days here')
                break
            print(meta['datatype'][0].text+' : '+datalist[i][0])
            print(meta['datatype'][1].text+' : '+datalist[i][1])
            print(meta['datatype'][3].text+' : '+datalist[i][3])
            print(meta['datatype'][4].text+' : '+datalist[i][4])
            print(meta['datatype'][5].text+' : '+datalist[i][5])
            i=i+1
while 1:
    stocknum=input('please input the number of the stock :')
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20180715&stockNo='+stocknum
    day=input('please input the number of day :')
    resp = fetch(url)  # step-1
    post_entries = parse_article_entries(resp.text)  # step-2
    print_stockinfo(int(day),post_entries)
    check=input('Do you want to get another information of stock? Y/n: ')
    if(check!='Y' and check!='y'):
        break



    
