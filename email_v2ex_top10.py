#!/usr/bin/env python
# coding = utf-8

import os
import sys
import smtplib
from email.mime.text import MIMEText
import urllib2
import json
import time
import codecs

url = "https://www.v2ex.com/api/topics/hot.json"
user_name = "xxxxx@xxx.com"
passwd = "xxxxxx"
smtp_serv = "smtp@xxx.com"

class SendMail:
    
    def __init__(self,username,passwd,serv_addr):
        self.__username = username
        self.__passwd = passwd
        self.__serv = smtplib.SMTP(serv_addr)
    
    def __login(self):
        self.__serv.login(self.__username,self.__passwd)
    
    def sendmsg(self,mail_to,subject,content):
        
        self.__login()
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.__username
        msg['To'] = mail_to
        self.__serv.sendmail(self.__username,mail_to,msg.as_string())
        self.__serv.quit()


def build_msg():
    res = urllib2.urlopen(url).read()
    json_res = json.loads(res)
    msg = []
    id = 0
    for top in json_res:
        id = id + 1
        msg.append(str(id)+": ")
        msg.append(top['url'].encode('utf-8'))
        msg.append("\r\n\r\n")
        msg.append("Title:  ")
        msg.append(top['title'].encode('utf-8'))
        msg.append("\r\n\r\n")
        msg.append("Content:  ")
        msg.append(top['content'].encode('utf-8'))
        msg.append("\r\n\r\n")
    return msg

if __name__ == "__main__":
    send = SendMail(user_name,passwd,smtp_serv)
    today = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    title = "v2ex top 10  " + today
    #print title
    msg = build_msg()
    #print msg
    #with codecs.open(r"d:/msg.txt","w+",'utf-8') as f:
    #with open(r"d:/msg.txt","w+") as f:
    #    f.writelines(msg)
    str_msg = ''.join(msg)
    send.sendmsg("xxxx@xxx.com",title,str_msg)

