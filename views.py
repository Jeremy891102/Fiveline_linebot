from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, PostbackEvent, PostbackTemplateAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate,ImageSendMessage
from . import drawline,basic_information,recommend_ETF

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
yourID = 'U0f46bcfb6e02517edca32cf7987f02ac'

@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent): # 如果有訊息事件

                if event.message.text == "主選單":
                #if "Help" in event.message.text:
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text = 'Help Buttons Template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://storage.googleapis.com/www-cw-com-tw/article/202112/article-61b108fd8f600.jpg',
                                title='主選單',
                                text='請選擇你需要的功能',
                                actions=[
                                    MessageAction(
                                        label='Using Instructions',
                                        text='輸入 "ETF____" 搜尋該檔基本資訊或策略圖形\n（ETF清單可在 ETF List Link 中找到）'
                                    ),
                                    URIAction(
                                        label='ETF List Link',
                                        uri='https://docs.google.com/spreadsheets/d/16DFZGhIjmhFuQRnz9xc7pD8sFn92Ljzd/edit?usp=share_link&ouid=103564067831742851998&rtpof=true&sd=true'
                                    ),    
                                    URIAction(
                                        label='Yahoo Finance Link',
                                        uri='https://tw.stock.yahoo.com/fund/'
                                    )
                                ]
                            )
                        )
                    )
 
                elif "ETF" in event.message.text:
                    msg = event.message.text[4:]
                    #msg = event.message.text.strip("ETF ")
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text = 'Buttons Template',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://cimg.cnyes.cool/prod/news/3946641/l/872d56244d0152ebe4b4ca9221dd2c35.jpg',
                                title= event.message.text + ' Visualization',
                                text='請選擇想查看的即時資訊或輸入"fl或bb+基金代碼"查看五線譜和布林通道策略圖形',
                                actions=[
                                    MessageAction(
                                        label='Basic Information',
                                        text= basic_information.basic_information(msg)
                    
                                    ),
                                    MessageAction(
                                        label='即時價格',
                                        text= recommend_ETF.stock_price(msg)
                                    ),
                                ]
                            )
                        )
                    )
                
                elif event.message.text == "Chosen":
                    pass
                
                elif "recommend" in event.message.text:
                    #etf_id = int(event.message.text)
                    count = event.message.text[10:]
                    #print(count)
                    reply= recommend_ETF.recommend(int(count))
                    #print(reply)
                    #print(chosen)
                    line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(
                        text=reply
                    )
                )
                        
                elif "fl" in event.message.text:
                    msg = event.message.text[3:]
                    img_url = drawline.linebot_draw_fiveline(msg)
                    
                    line_bot_api.reply_message(  
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    )
                )
                elif "bb" in event.message.text:
                    msg = event.message.text[3:]
                    img_url = drawline.linebot_draw_fivelinebb(msg)
                    
                    line_bot_api.reply_message(  
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=img_url,
                        preview_image_url=img_url
                    )
                )


                else:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text= '• 輸入 "主選單" 可搜尋ETF清單以及相關網站連結\n• 輸入 "ETF___" 搜尋該檔最新交易日基本資訊或策略圖形，清單可在主選單中的ETF List中找到\n• 輸入 "recommend+數量" 可得最新交易日所推薦的ETF\n• 輸入 "fl +基金代碼" 可得最新該基金五線譜圖\n• 輸入 "bb +基金代碼" 可得最新該基金布林通道圖')
                )

            
            if not isinstance(event, MessageEvent):
                pass

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# Create your views here.
