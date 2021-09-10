from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages #傳提示框訊息用
import MySQLdb
from django.http import JsonResponse

#---------------------------------------
#connect() 方法用於建立資料庫的連線，裡面可以指定引數：使用者名稱，密碼，主機等資訊。
#這只是連線到了資料庫，要想操作資料庫需要建立遊標。
#會員資料的DB
# mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')


#通過獲取到的資料庫連線conn下的cursor()方法來建立遊標。
# cursor = mysqldb.cursor()



#-------------------------------------------------------------------
# Create your views here.
    
# 傳訊息
# def sayhellosomebody(req,username):
#     return HttpResponse('Hello World!'+username)

#傳網址連上登入頁面
def login(req):
    if req.method=='POST':
        mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
        cursor = mysqldb.cursor()
        print("執行登入")
        username=req.POST['username1']
        password=req.POST['password1']
        cursor.execute("SELECT count(*) FROM user where username=%s and password=%s",[(username),(password)])
        result = cursor.fetchall()  
        cursor.close()
        for row in result:
            # print(row[0])
            if row[0]>0:
                # print('有此帳號')
                req.session['is_login']=True
                req.session['username']=username
                stock_id='2330'
                return HttpResponseRedirect('/main/?stock_id='+stock_id) 
            else:
                # print('無此帳號')
                return HttpResponseRedirect('/login/')
    else:
        return render(req,'login.html')
    #也可寫return render(req,'index.html',locals()) 傳遞所有區域變數

from django.contrib.sessions.models import Session
def logout(req):
    if 'username' in req.session:
        # Session.objects.all().delete()
        req.session['is_login']=False
        req.session['username']=None
        return HttpResponseRedirect('/login/')


def main(req):
    if req.session['username']!=None:
        req.session['is_login']=True
        req.session['username']=req.session['username']
        stock_id=req.GET['stock_id']
        return render(req,'main.html',locals())
    else:
        req.session['is_login']=False
        return HttpResponseRedirect('/login/')
    
# 模擬下單頁
def stockPlay(req):
    
    if req.session['username']!=None:
        req.session['is_login']=True
        req.session['username']=req.session['username']

        mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
        cursor = mysqldb.cursor()
        cursor.execute("SELECT deposit FROM income where username=%s",[(req.session['username'])])
        result = cursor.fetchall()
        cursor.close()
        
        # print(result)
        #存款
        deposit=result[0][0]
        stock_id=req.GET['stock_id']
        return render(req,'stockPlay.html',locals())
    else:
        req.session['is_login']=False
        return HttpResponseRedirect('/login/')

# GET方法 網址輸入http://localhost:8000/djget/?name=陳宥維&city=彰化縣
# def djget(req):
#     name=req.GET['name']
#     city=req.GET['city']
#     return render(req,'djget.html',locals())

#POST方法 提交會員註冊表
def signup(req):
    if req.method=='POST':
        username=req.POST['username2']
        password=req.POST['password2']
        email=req.POST['email']
        # 存資料進去
        #初始化user表
        mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
        cursor = mysqldb.cursor()
        sqlStuff = "INSERT INTO `user` (`username`, `password` ,`email`) VALUES (%s,%s,%s)" 
        records = [(username, password,email)]
        cursor.executemany(sqlStuff, records)
        # cursor.execute("SELECT count(*) FROM user where username =%s",[(username)])
        mysqldb.commit() #提交 此行一定要寫
        #初始化warehouse表
        sqlStuff="INSERT INTO `warehouse`(`username`) VALUES (%s)"
        records=[(username)]
        cursor.executemany(sqlStuff, records)
        mysqldb.commit() #提交 此行一定要寫
        #初始化income表
        sqlStuff="INSERT INTO `income`(`username`) VALUES (%s)"
        records=[(username)]
        cursor.executemany(sqlStuff, records)
        mysqldb.commit() #提交 此行一定要寫
        cursor.close()
        messages.info(req, '註冊成功')
        # return HttpResponse('您輸入的帳號是:{}\n您輸入的密碼是:{}\n您輸入的信箱是:{}'.format(username,password,email))
        return render(req,'login.html', {'massage': True})
# 檢查用戶是否註冊過
def CheckSignUp(req):
    if req.method=='POST':
        username=req.POST['username']
        mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
        cursor = mysqldb.cursor()
        cursor.execute("SELECT count(*) FROM user where username =%s",[(username)])
        result = cursor.fetchall()
        cursor.close()
        
        for row in result:
            # print(row[0])
            if row[0]>0:
                # print('此帳號已被註冊過')
                return HttpResponse('此帳號已被註冊過')
            else:
                # print('此帳號允許註冊')
                return HttpResponse('此帳號允許註冊')
# 庫存 接收ajax
def warehouse_table(req):
    if req.method=='POST':
        username=req.POST['username']
        taiwan10=[2330, 2454, 2317, 2303, 2308, 2881, 1303, 1301, 2882, 2412]
        message={}
        for i in taiwan10:
            mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
            cursor = mysqldb.cursor()
            cursor.execute("SELECT `%s`  FROM warehouse where username =%s",[(i),(username)])
            result_count = cursor.fetchall()
            # print(result_count[0][0])
            if result_count[0][0]>0:
                cursor.execute("SELECT `buy_%s_price` FROM income where username =%s",[(i),(username)])
                result_price = cursor.fetchall()
                # print(result_price[0][0])
                message[i] = result_count[0][0]
                message['buy_'+str(i)+'_price'] = result_price[0][0]
        # print(message) 
        cursor.close()
        return JsonResponse(message)

#收益 接收ajax
def income_table(req):
    print("income_table有接收到")
    if req.method=='POST':
        username=req.POST['username']
        print(username)
        taiwan10=['2330', '2454', '2317', '2303', '2308', '2881', '1303', '1301', '2882', '2412']
        message={} 
        # print(message)
        
        for i in taiwan10:
            # print('sell_'+i+'_gain')
            # column='sell_'+i+'_gain'
            print(type(i),i)
            mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
            cursor = mysqldb.cursor()
            #這裡破例用字串連接的方式(sell_"+i+"_gain) 寫mysql語法，標準寫法有BUG
            cursor.execute("SELECT sell_"+i+"_gain FROM income where username =%s",[(username)])
            result_gain = cursor.fetchall()
            cursor.close()
            print('資料庫回傳 : ',result_gain[0][0])
            if result_gain[0][0]!=0:
                message[i] = result_gain[0][0] 
        
        return JsonResponse(message)

# 下單 接受表單
def buy(req):
    if req.method=='POST':
        # print("下單開始")
        username=str(req.session['username'])
        # print(username)
        # 接到 股票ID
        stock_id=int(req.POST['stock_id'])
        # print(stock_id)
        # 接到 股數
        count=int(req.POST['one_or_all'])*int(req.POST['quantity'])
        # print("count",count)
        # 接到 買進還是賣出
        trade=req.POST['trade']
        # print(trade)
        # 接到 當時價格
        now_price=float(req.POST['now_price'])
        # print(now_price)
        mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
        cursor = mysqldb.cursor()
        # 獲取存款
        cursor.execute("SELECT deposit FROM income where username =%s",[(username)])
        deposit = float(cursor.fetchall()[0][0])
        # print("現在存款",deposit)
        #獲取現在這支股票的持有股數
        cursor.execute("SELECT `%s` FROM `warehouse` WHERE `username` = %s",[(stock_id),(username)])
        old_count = int(cursor.fetchall()[0][0])
        # print("舊的股數",old_count)
        #獲取之前買進的價格
        cursor.execute("SELECT `buy_%s_price` FROM `income` WHERE `username` = %s",[(stock_id),(username)])
        old_price = float(cursor.fetchall()[0][0])
        #獲取目前這支股票讓你賺了多少元
        cursor.execute("SELECT `sell_%s_gain` FROM `income` WHERE `username` = %s",[(stock_id),(username)])
        old_gain = float(cursor.fetchall()[0][0])

        if trade=="buy":
            deposit=deposit-(now_price*count)
            # print('買完後的存款',deposit)
            new_count=old_count+count
            # print("現在的股數",new_count)
            new_price=((old_price*old_count)+(now_price*count))/new_count
            cursor.execute("UPDATE `income` SET `buy_%s_price`= %s WHERE `username`=%s",[(stock_id),(new_price),(username)])
            mysqldb.commit() #提交 此行一定要寫
        else:#賣掉
            deposit=deposit+(now_price*count)
            # print('賣完後的存款',deposit)
            new_count=old_count-count
            # print("現在的股數",new_count)
            if new_count==0: #賣光的時候
                cursor.execute("UPDATE `income` SET `buy_%s_price`= 0.00  WHERE `username`=%s",[(stock_id),(username)])
                mysqldb.commit() #提交 此行一定要寫
            else:
                new_price=((old_price*old_count)-(now_price*count))/new_count
                cursor.execute("UPDATE `income` SET `buy_%s_price`= %s WHERE `username`=%s",[(stock_id),(new_price),(username)])
                mysqldb.commit() #提交 此行一定要寫
            new_gain=old_gain+((now_price*count)-(old_price*count))
            cursor.execute("UPDATE `income` SET `sell_%s_gain`= %s WHERE `username`=%s",[(stock_id),(new_gain),(username)])
            mysqldb.commit() #提交 此行一定要寫
            
        # 更新數據
        cursor.execute("UPDATE `warehouse` SET `%s`=%s WHERE `username`=%s",[(stock_id),(new_count),(username)])
        mysqldb.commit() #提交 此行一定要寫
        cursor.execute("UPDATE `income` SET `deposit`= %s WHERE `username`=%s",[(deposit),(username)])
        mysqldb.commit() #提交 此行一定要寫
        cursor.close()
        
        return HttpResponseRedirect('/stockPlay/?stock_id='+str(stock_id))



# 及時股價回傳
def now_price(req):
    stock_id=str(req.POST['stock_id'])
    import re 
    import urllib.request as ur
    url = "https://invest.cnyes.com/twstock/TWS/"+stock_id 
    content = ur.urlopen(url).read().decode("utf-8")
    # print(content)
    match=re.search('<div class="jsx-2941083017 info-lp">(.*?)</div>',content)
    # print(match.group(1))
    match=re.search('>(.*?)</span>',match.group(1))
    # print(match.group(1))
    print('個股{}即時股價為{}元'.format(stock_id,match.group(1)))
    return HttpResponse(match.group(1))


# 搜尋框 GET 表單出去
def search(req):
    stock_id=req.GET['search']
    # print(stock_id)
    return HttpResponseRedirect('/stockPlay/?stock_id='+str(stock_id))


def main_search(req):
    stock_id=req.GET['search']
    # print(stock_id)
    return HttpResponseRedirect('/main/?stock_id='+str(stock_id))


# 獲取預測模型的個股價格 接收ajax
def future_table(req):
    print("future_table有接收到")
    if req.method=='POST':
        stock_id=req.POST['stock_id']
        day=[1,2,3,4,5,6,7,8,9,10]
        message={}
        
        for i in day:
            mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
            cursor = mysqldb.cursor()
            cursor.execute("SELECT `day_%s_predict` FROM future where stock_id =%s",[(i),(stock_id)])
            result_count = cursor.fetchall()
            message[str(i)]= str(result_count[0][0])
            cursor.close()
        # print(message) 
        return JsonResponse(message, safe=False) 

def future_range_lower(req):
    print("lower_range有接收到")
    if req.method=='POST':
        stock_id=req.POST['stock_id']
        day=[1,2,3,4,5,6,7,8,9,10]
        lower={}
        for i in day:
            mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
            cursor = mysqldb.cursor()
            cursor.execute("SELECT `day_%s_lower` FROM future where stock_id =%s",[(i),(stock_id)])
            result_count = cursor.fetchall()
            lower[str(i)]=str(result_count[0][0])
            cursor.close()
        # print(lower)
        return JsonResponse(lower, safe=False)


def future_range_upper(req):
    print("upper_range有接收到")
    if req.method=='POST':
        stock_id=req.POST['stock_id']
        day=[1,2,3,4,5,6,7,8,9,10]
        upper={}
        # lower={}
        for i in day:
            mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
            cursor = mysqldb.cursor()
            cursor.execute("SELECT `day_%s_upper` FROM future where stock_id =%s",[(i),(stock_id)])
            result_count = cursor.fetchall()
            upper[str(i)]=str(result_count[0][0])
            cursor.close()
        # print(upper)
        return JsonResponse(upper, safe=False)







    
   