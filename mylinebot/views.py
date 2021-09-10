from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent,TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage
import MySQLdb
import os
import speech_recognition as sr # 語音辨識 套件
import pyimgur
import datetime
# 獲取今天日期
today = datetime.date.today()

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# Create your views here.

mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')

# 股票ID
stock_ids=['1301','1303','2303','2308','2317','2330','2412','2454','2881','2882',]

# LINEBOT 的 views
@csrf_exempt
def callback(request):

    try:
        cursor = mysqldb.cursor()
    except Exception as ex:
        print(ex)
    
    if request.method == 'POST':
        #先設定一個要回傳的message空集合
        message=[]
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        #在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        # message.append(TextSendMessage(text=str(body)))

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            #如果事件為訊息
            if isinstance(event, MessageEvent):
                print(event.message.type)
                if event.message.type=='text':
                    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
                    if event.message.text in stock_ids: 
                        # 連資料庫獲取未來股價
                        stock_id=event.message.text
                        day=[1,2,3,4,5,6,7,8,9,10]
                        future=''
                        for i in day:
                            # print("有進for") 
                            cursor.execute("SELECT `day_%s_predict` FROM future where stock_id =%s",[(i),(stock_id)])
                            result_count = cursor.fetchall()
                            future= future+'\n'+future_day(i)+' : '+str(result_count[0][0])+'元'  
                        # print(future)  
                        
                        # 抓圖片的url
                        img_url=pngToURL(stock_id)
                        
                        reply_arr=[]
                        # reply_arr.append( TextSendMessage(text='2330即時股價 : 580.00元'))
                        reply_arr.append( TextSendMessage(text=stock_id+'即時股價 : '+now_price(stock_id)+'元\n為您預測'+event.message.text+'未來十天的股價\n======================='+future) )
                        reply_arr.append(ImageSendMessage(original_content_url=img_url,preview_image_url=img_url))
                        line_bot_api.reply_message( event.reply_token, reply_arr )
                    elif event.message.text=='？' or event.message.text=='?':
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='使用說明 :\n\n輸入或說出「股票代碼」\n即會顯示當前「股票」的即時價格\n及「未來10天的股價預測值」\n\n有提供服務的股票:\n「2330」 : 台積電\n「2454」 : 聯發科\n「2317」 : 鴻海\n「2303」 : 聯電\n「2308」 : 台達電\n「2881」 : 富邦金\n「1303」 : 南亞\n「1301」 : 台塑\n「2882」 : 國泰金\n「2412」 : 中華電'))
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="很抱歉，我們沒有提供此個股的資料"))

                elif event.message.type=='audio':
                    # message.append(TextSendMessage(text='聲音訊息'))
                    audio_content = line_bot_api.get_message_content(event.message.id)
                    path='./static/speech/sound2.m4a'
                    name_m4a = './static/speech/sound2.m4a'
                    name_wav = './static/speech/sound2.wav'
                    with open(path, 'wb') as fd:
                        for chunk in audio_content.iter_content():
                            fd.write(chunk)
                    os.system('ffmpeg -y -i ' + name_m4a + ' ' + name_wav + ' -loglevel quiet')
                    trans_text = transcribe(name_wav)
                    if trans_text in stock_ids:  
                           # 連資料庫獲取未來股價
                        stock_id=trans_text
                        day=[1,2,3,4,5,6,7,8,9,10]
                        future=''
                        for i in day:
                            # print("有進for") 
                            cursor.execute("SELECT `day_%s_predict` FROM future where stock_id =%s",[(i),(stock_id)])
                            result_count = cursor.fetchall()
                            future= future+'\n'+future_day(i)+' : '+str(result_count[0][0])+'元'  
                        # print(future) 
                        
                        # 抓圖片的url
                        img_url=pngToURL(stock_id)
                        
                        reply_arr=[]
                        reply_arr.append( TextSendMessage(text=stock_id+'即時股價 : '+now_price(stock_id)+'元\n為您預測'+trans_text+'未來十天的股價\n======================='+future) )
                        reply_arr.append(ImageSendMessage(original_content_url=img_url,preview_image_url=img_url))
                        line_bot_api.reply_message( event.reply_token, reply_arr )
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="很抱歉，我們沒有提供此個股的資料"))

                cursor.close()#關閉資料庫連線
                return HttpResponse()

                # elif event.message.type=='image':
                #     message.append(TextSendMessage(text='圖片訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='location':
                #     message.append(TextSendMessage(text='位置訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='video':
                #     message.append(TextSendMessage(text='影片訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='sticker':
                #     message.append(TextSendMessage(text='貼圖訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='file':
                #     message.append(TextSendMessage(text='檔案訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)



# 語音辨識函數
def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''
    
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None


# png轉URL
def pngToURL(stock_id):
    CLIENT_ID = "a43a6159850e6e2"
    PATH = "./static/img/img_prophet/prophet_"+stock_id+'.png'
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=stock_id+"未來股價圖")
    return uploaded_image.link 
# 抓未來日期
def future_day(days):
    today = datetime.date.today()
    tomorrow=today + datetime.timedelta(days=days)
    return tomorrow.strftime('%m/%d')

#抓及時股價
def now_price(stock_id):
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
    return match.group(1)