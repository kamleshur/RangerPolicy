import json
import time
import datetime
import requests
import os
import zipfile
import shutil
import re
import sys
import math
import platform
from pytz import timezone
import logging
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

starttime=datetime.datetime.now()

ConfigFileName=os.getenv('CONFIG_FILE_NAME')

#ConFileChnageTime=os.stat(ConfigFileName).st_mtime
#print(ConFileChnageTime)
#print(os.getcwd()+"//..")

### Uncomment if this needed

# with open("Application.properties") as app_file:
    # appProperty=app_file.readlines()
    # for confdata in appProperty:
        # if "CONFIGFILE" ==(confdata.split("=")[0].strip()).upper():
            # print(confdata.split("=")[1].strip())

with open(ConfigFileName) as json_file:
	configdata=json.load(json_file)

if os.name=='nt':
	configdata['OSTypePath']="\\"
	#configdata['SYSTEM_PARAMETERS']['LOCAL_FILE_PATH']=configdata['LOCAL_FILE_PATH_WINDOW']
elif os.name=='posix':
	configdata['OSTypePath']="/"
	### Get Kerberos Ticket To Secure Login
	os.system("echo "+configdata['Password']+"|kinit "+configdata['Username'].split('\\')[1])

if configdata['SYSTEM_PARAMETERS']['LOCAL_FILE_PATH'][0:2]=="//": 
	configdata['OSTypePath']="/"

EntityName=configdata['SYSTEM_PARAMETERS']['ENTITY_NAME']

def EpochTimeConversion(Time,Format):
	utc_time = datetime.datetime.strptime(Time, Format)
	epoch_time = (utc_time - datetime.datetime(1970, 1, 1)).total_seconds()
	#print(epoch_time)
	return int(epoch_time)
	


### Print Log Message	
def LogMessageInProcessLog(LogMessage):	
	
	if configdata['PROCESS_LOG']['ENABLE_FILE_LOGGING'].upper()=='YES':
		logging.error(LogMessage)
	if configdata['PROCESS_LOG']['PRINT_LOG_MESSGAE_ON_CONSOLE'].upper()=='YES':
		print(LogMessage)
	#	print("calll insid..",LogMessage)

### Log Configuration 

def SetProcessLogConfiguration():
	LogFilePath=configdata['SYSTEM_PARAMETERS']['LOCAL_FILE_PATH']+configdata['OSTypePath']+"Logs"+configdata['OSTypePath']
		
	LogLevel=configdata['PROCESS_LOG']['LOG_LEVEL'].upper().replace("ERROR","40").replace("WARNING","30").replace("INFO","20").replace("DEBUG","10") ##ERROR 40|WARNING	30|INFO	20|DEBUG 10
	
	if not os.path.exists(LogFilePath):
		os.makedirs(LogFilePath)	
		
	for file in os.listdir(LogFilePath):
		LogFileName=LogFilePath+file	
		CurrentLogFileSize=os.stat(LogFileName).st_size
		FileCreatedDaysBack= (EpochTimeConversion(str(datetime.datetime.now().astimezone(timezone(configdata['SYSTEM_PARAMETERS']['TIMEZONE']))).split('.')[0],'%Y-%m-%d %H:%M:%S')- os.stat(LogFileName).st_ctime) //86400
		#print(FileCreatedDaysBack)
		if (FileCreatedDaysBack  >=configdata['PROCESS_LOG']['LOG_FILE_RETENTION_PERIOD'] or CurrentLogFileSize >= configdata['PROCESS_LOG']['LOG_FILE_MAX_FILE_SIZE']):
			print("\nLog File <{}> Is Deleted Current File Size <{}> Has Crossed The Permiiited Limit <{}>Big Or Its <{}> Days Old In System -Created Date <{}>\n".format(LogFileName,CurrentLogFileSize,configdata['PROCESS_LOG']['LOG_FILE_MAX_FILE_SIZE'],FileCreatedDaysBack,time.ctime(os.stat(LogFileName).st_ctime)))
			try:
				os.remove(LogFileName)
			except Exception as e:
				print(e)
		
	LogFileName=LogFilePath+configdata['PROCESS_LOG']['LOG_FILE_NAME']+starttime.strftime('%Y%m%d')+".txt"
	logging.basicConfig(filename=LogFileName,format='%(asctime)s %(message)s', filemode='a',level=int(LogLevel))


def GetItemIndex(IndexForItem):	
	for k,v in configdata.items():	
		if isinstance(v,dict):
			#print(v,type(v))
			for k1,v1 in v.items():
				if isinstance(v1,list):	
					idx=0
					for litem in v1:					
						#print(litem)
						if isinstance(litem,dict):
							#print(litem)
							for k2,v2 in litem.items():
								#print(litem[k2])
								if IndexForItem in litem[k2]:
									print(litem[k2])
									return idx 
						idx+=1
		
		
		if isinstance(v,list):	
			idx=0
			for litem in v:					
				#print(litem)
				if isinstance(litem,dict):
					#print(litem)
					for k2,v2 in litem.items():
						#print(litem[k2])
						if IndexForItem in litem[k2]:
							print(litem[k2])
							return idx 
				idx+=1
		


### Remove Escape Character
def RemoveEscapeAnsi(line):
	return re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('', line).replace('\\','\\\\')
#print(RemoveEscapeAnsi('\t\u001b[0;35mSome\n\rText\u001b[0m\u001b[0;36m172.18.0.2\u001b[0m'))
						
#print(GetItemIndex('SnowflakeDSIIDriver'))
#print(GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['MYSQL1']))	

def GetEnvironment():
    Environment=""
    if platform.node() in configdata['SYSTEM_PARAMETERS']['HOSTNAME']['DEV']:
        Environment="DEV"
    elif platform.node() in configdata['SYSTEM_PARAMETERS']['HOSTNAME']['UAT']:
        Environment="UAT"
    elif platform.node() in configdata['SYSTEM_PARAMETERS']['HOSTNAME']['COB']:
        Environment="COB"
    elif platform.node() in configdata['SYSTEM_PARAMETERS']['HOSTNAME']['PROD']:
        Environment="PROD"
    return Environment

def encrypt_password(password):
    encrypted_password = ""
    for char in password:
        encrypted_password += chr(ord(char) +10)  # Increment ASCII value of each character
    return encrypted_password

def decrypt_password(encrypted_password):
    decrypted_password = ""
    for char in encrypted_password:
        decrypted_password += chr(ord(char) -10)  # Decrement ASCII value of each character
    return decrypted_password
    
environment=GetEnvironment() 
SetProcessLogConfiguration()