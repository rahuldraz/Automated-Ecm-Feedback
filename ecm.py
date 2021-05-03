#!/usr/bin/python3
#Author Shashwat Kumar
#Github https://github.com/rahudraz

import requests
from bs4 import BeautifulSoup
import re
import sys

print ('''
 _____                 _____             _ _                _    
| ____|___ _ __ ___   |  ___|__  ___  __| | |__   __ _  ___| | __
|  _| / __| '_ ` _ \  | |_ / _ \/ _ \/ _` | '_ \ / _` |/ __| |/ /
| |__| (__| | | | | | |  _|  __/  __/ (_| | |_) | (_| | (__|   < 
|_____\___|_| |_| |_| |_|  \___|\___|\__,_|_.__/ \__,_|\___|_|\_\
                                                                 
						-By Shashwat
''')


ecm_url="https://ecm.smtech.in/ecm/"
if(len(sys.argv)!=4):
	print("Usage ./ecm.py Your_REG_NO ECM_PASSWORD FEEDBACK_SCORE(1-5)")
	print("Example ./ecm.py 201800149 demo 5")
	exit()

reg_no=sys.argv[1]
passwd=sys.argv[2]
point=sys.argv[3]

VIEWSTATE=""
VIEWSTATEGENERATOR=""
EVENTVALIDATION=""

def sanitize_url(url: str) -> str:
    return re.sub(r"([^:]/)(/)+", r"\1", url)


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
"Content-Type": "application/x-www-form-urlencoded","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}


session = requests.session()

index=session.get(ecm_url+"login.aspx",headers=headers)

def get_State(index):
	global VIEWSTATE,VIEWSTATEGENERATOR,EVENTVALIDATION
	soup=BeautifulSoup(index.content, "html.parser")
	VIEWSTATE=requests.utils.quote(soup.find(id="__VIEWSTATE")['value'])
	VIEWSTATEGENERATOR=requests.utils.quote(soup.find(id="__VIEWSTATEGENERATOR")['value'])
	EVENTVALIDATION=requests.utils.quote(soup.find(id="__EVENTVALIDATION")['value'])

get_State(index)

data = "__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE="+VIEWSTATE+"&__VIEWSTATEGENERATOR="+VIEWSTATEGENERATOR+"&__EVENTVALIDATION="+EVENTVALIDATION+"&tbEmail=&TxtUserName="+reg_no+"&TxtPassword="+passwd+"&btnLogin=Sign+in"

login=session.post(ecm_url+"login.aspx",data=data,headers=headers,allow_redirects=False)

if(login.status_code==302):
	print("[+] Login Success!")
	login=session.post(ecm_url+"login.aspx",data=data,headers=headers)

	get_State(login)
else:
	print("[-] Login Failed!")
	exit()

try:

	data= "ctl00%24ScriptManager1=ctl00%24UpdatePanel1%7Cctl00%24ContentPlaceHolder1%24Button1&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE="+VIEWSTATE+"&__VIEWSTATEGENERATOR="+VIEWSTATEGENERATOR+"&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION="+EVENTVALIDATION+"&ctl00%24ContentPlaceHolder1%24hfCourse=3&__ASYNCPOST=true&ctl00%24ContentPlaceHolder1%24Button1=Close"

	index=session.post(ecm_url+"Students/index.aspx",data=data,headers=headers)


	all_link=re.findall("<a id=\"ctl00_ContentPlaceHolder1_gvFB_ctl(.*?)_LinkButton1", index.text)

	print("[+] ",str(len(all_link))," Feedback to Submit!")
	#print(all_link)
except:
	print("[-] No Feeback to Submit!")
	exit()
try:
	VIEWSTATE_L=re.findall("__VIEWSTATE[|](.*?)[|]",index.text)
	VIEWSTATEGENERATOR_L=re.findall("__VIEWSTATEGENERATOR[|](.*?)[|]",index.text)
	EVENTVALIDATION_L=re.findall("__EVENTVALIDATION[|](.*?)[|]",index.text)
	j=1
	for i in all_link:
		data="ctl00%24ScriptManager1=ctl00%24UpdatePanel1%7Cctl00%24ContentPlaceHolder1%24gvFB%24ctl"+str(i)+"%24LinkButton1&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24gvFB%24ctl"+str(i)+"%24LinkButton1&__EVENTARGUMENT=&__VIEWSTATE="+requests.utils.quote(VIEWSTATE_L[0])+"&__VIEWSTATEGENERATOR="+requests.utils.quote(VIEWSTATEGENERATOR_L[0])+"&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION="+requests.utils.quote(EVENTVALIDATION_L[0])+"&__ASYNCPOST=true&"
		lenk=session.post(ecm_url+"Students/index.aspx",data=data,headers=headers)
		fb_link=re.findall("pageRedirect[|][|](.*?)[|]",lenk.text)
		fb_link[0]=requests.utils.unquote(fb_link[0])
		new_link=sanitize_url(ecm_url+"../"+fb_link[0])
		f_page=session.get(new_link,headers=headers)
		soup=BeautifulSoup(f_page.content, "html.parser")
		eVIEWSTATE=requests.utils.quote(soup.find(id="__VIEWSTATE")['value'])
		eVIEWSTATEGENERATOR=requests.utils.quote(soup.find(id="__VIEWSTATEGENERATOR")['value'])
		eEVENTVALIDATION=requests.utils.quote(soup.find(id="__EVENTVALIDATION")['value'])
		data="ctl00%24ScriptManager1=ctl00%24UpdatePanel1%7Cctl00%24ContentPlaceHolder1%24btnSubmit&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE="+eVIEWSTATE+"&__VIEWSTATEGENERATOR="+eVIEWSTATEGENERATOR+"&__EVENTVALIDATION="+eEVENTVALIDATION+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl02%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl03%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl04%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl05%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl06%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl07%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl08%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl09%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl10%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl11%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl12%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl13%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl14%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl15%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24gvFeedback%24ctl16%24rblVal="+str(point)+"&ctl00%24ContentPlaceHolder1%24tbComment=&__ASYNCPOST=true&ctl00%24ContentPlaceHolder1%24btnSubmit=Submit"
		session.post(new_link,data=data,headers=headers)
		print("[+] ",str(j)," Feedback Submitted!")
		j+=1

except:
	print("[-] Some Error Occured!")
print("[+] All Feedback Has been given!")
