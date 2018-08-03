import time
import datetime
import requests
import json
import os
import logging

url = 'http://free_bus_ticket.fyxmt.com/interface/grabTicket'
logging.basicConfig(filename=os.path.join(os.getcwd(), 'grabticket.log'),
                    level=logging.DEBUG, format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',)

# 抢早上8:10票 3号车 8:10开往产业园停车场
def grabMorningTicket():
    grabticketHour = 21
    grabticketMinute = 3
    grabticketSecond = 0
    getTicketUrl = 'http://free_bus_ticket.fyxmt.com/interface/ticketList?queryDate={0}'.format(
        (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    sendData = getSendData(getTicketUrl, False)
    return grabticketHour, grabticketMinute, grabticketSecond, sendData


# 抢晚上18:10票 1号车 18:10开往金尚路
def grabNightTicket():
    grabticketHour = 12
    grabticketMinute = 29
    grabticketSecond = 29
    getTicketUrl = 'http://free_bus_ticket.fyxmt.com/interface/ticketList?queryDate={0}%20{1}'.format(
        datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'))
    sendData = getSendData(getTicketUrl, True)
    return grabticketHour, grabticketMinute, grabticketSecond, sendData


def getSendData(url, isNight):
    r = requests.get(url)
    result = json.loads(r.text)
    if result['success']:
        if isNight:
            id = result['obj']['busTrips'][0]['trips'][1]['id']
        else:
            id = result['obj']['busTrips'][2]['trips'][0]['id']
        sendData = {'wechatNo': 'ofqo-uJLT6jux0jk8vm4vlPLIDCE',
                    'id': id}
    return sendData


# 优化点
# 1.时间比较
if __name__ == '__main__':
    try:
        if datetime.datetime.now().hour > 9 and datetime.datetime.now().hour < 13:
            grabticketHour, grabticketMinute, grabticketSecond, sendData = grabNightTicket()
        elif datetime.datetime.now().hour > 18 and datetime.datetime.now().hour < 23:
            grabticketHour, grabticketMinute, grabticketSecond, sendData = grabMorningTicket()
        else:
            logging.debug('非抢票时间段')
            exit(0)
        while True:
            nowDateTime = datetime.datetime.now().time()
            if abs(nowDateTime.hour-grabticketHour) > 0 or abs(grabticketMinute-nowDateTime.minute) > 5:
                logging.debug(nowDateTime)
                time.sleep(60)
            else:
                if nowDateTime.hour == grabticketHour and nowDateTime.minute == grabticketMinute and nowDateTime.second >= grabticketSecond:
                    r = requests.post(url, data=json.dumps(sendData))
                    result = json.loads(r.text)
                    logging.debug(result)
                    if not result['success']:
                        continue
                    else:
                        break
                else:
                    time.sleep(1)
                    logging.debug(nowDateTime)
    except:
        logging.debug('程序异常')
    