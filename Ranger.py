from Utilities import *

def GetAuthAccessPassword():
# Get Authorization Password for Basic Auth
    try:
        #print(os.getenv('RANGER_PASSWORD_SYSTEM'))
        if configdata['SYSTEM_PARAMETERS']['CREDENTIAL']=='SYSTEM_ENVIRONMENT':
            configdata['RANGER']['AUTHENTICATION']['Password']= decrypt_password(os.getenv('RANGER_PASSWORD'))  #from system env
            #configdata['RANGER']['AUTHENTICATION']['Password']= decrypt_password(os.getenv('RANGER_PASSWORD'))  ##from .env file
            
        LogMessageInProcessLog('Access Authentication Details...')
        return configdata['RANGER']['AUTHENTICATION']['Password']
    except Exception as e:
        LogMessageInProcessLog("Exception Raiased in "+sys._getframe().f_code.co_name +"...."+str(e))
        raise Exception(str(response_dict))

#print(GetAuthAccessToken()
def GetFromRanger(UrlEndPoint):
    responseGet=""
    try:
        responseRequest = requests.get(UrlEndPoint, auth = (configdata['RANGER']['AUTHENTICATION']['UserName'],GetAuthAccessPassword()),headers = {"Content-Type" : "application/json"})
        #print(UrlEndPoint, type(responseRequest.text))
        LogMessageInProcessLog(UrlEndPoint)
        if responseRequest.text[0]=='[':
            responseRequest=responseRequest.json()
        else:    
            responseRequest=dict(responseRequest.json())
        return responseRequest
    except Exception as e:
        LogMessageInProcessLog("Exception Raiased in "+sys._getframe().f_code.co_name +"...."+str(e))
        raise Exception(str(responseRequest))#exit(0)


def PostToRanger(UrlEndPoint,BodyPayLoad):
    try:
        BodyPayLoad=json.dumps(BodyPayLoad)  ## convert from josn to string  ==>false==>Flase
        LogMessageInProcessLog(UrlEndPoint+"\n BodyPayload...."+BodyPayLoad)
        responseRequest=requests.post(UrlEndPoint,data=BodyPayLoad,auth = (configdata['RANGER']['AUTHENTICATION']['UserName'],GetAuthAccessPassword()),headers = {"Content-Type" : "application/json"})
        responseRequest=dict(responseRequest.json())
        return responseRequest
    except Exception as e:
        LogMessageInProcessLog("Exception Raiased in "+sys._getframe().f_code.co_name +"...."+str(e))
        raise Exception(str(responseRequest))#exit(0)

def PutToRangerById(UrlEndPoint,BodyPayLoad,rangerPolicyID):
    try:
        BodyPayLoad["id"]=rangerPolicyID
        BodyPayLoad=json.dumps(BodyPayLoad)  ## convert from josn to string  ==>false==>Flase
        LogMessageInProcessLog(UrlEndPoint+"\n BodyPayload ...."+BodyPayLoad)
        UrlEndPoint=UrlEndPoint+"/"+str(rangerPolicyID)
        responseRequest=requests.put(UrlEndPoint,data=BodyPayLoad,auth = (configdata['RANGER']['AUTHENTICATION']['UserName'],GetAuthAccessPassword()),headers = {"Content-Type" : "application/json"})
        responseRequest=dict(responseRequest.json())
        return responseRequest
    except Exception as e:
        LogMessageInProcessLog("Exception Raiased in "+sys._getframe().f_code.co_name +"...."+str(e))
        raise Exception(str(responseRequest))#exit(0)


def DeleteFromRangerById(UrlEndPoint,rangerPolicyID):
    try:
        UrlEndPoint=UrlEndPoint+"/"+str(rangerPolicyID)
        LogMessageInProcessLog("\nDeleting Rest API...."+UrlEndPoint)
        responseRequest=requests.delete(UrlEndPoint,auth = (configdata['RANGER']['AUTHENTICATION']['UserName'],GetAuthAccessPassword()),headers = {"Content-Type" : "application/json"})
        if responseRequest.status_code==204:
            LogMessageInProcessLog("\nPolicy ID {"+str(rangerPolicyID)+"} Deleted Successfully....")
            return responseRequest.text
        else:
            responseRequest=responseRequest.json()
            return responseRequest

    except Exception as e:
        LogMessageInProcessLog("Exception Raiased in "+sys._getframe().f_code.co_name +"...."+str(e))
        raise Exception(str(responseRequest))#exit(0)


defaultPolicy={}
def GetDefualtPolicy():
    defaultPolicy=configdata['RANGER']['POLICIES']['POSTAPI']['BodyParameters']
    return basePolicy
    
def SetDefualtPolicy():
   configdata['RANGER']['POLICIES']['POSTAPI']['BodyParameters']=defaultPolicy

def GetDomainURL():
    LogMessageInProcessLog("Environment..."+environment)
    domainURL=""
    if environment=='DEV':
        domainURL=configdata['RANGER']['DomainURL']['DEV'] 
    elif environment=='UAT':
        domainURL=configdata['RANGER']['DomainURL']['UAT']   
    elif environment=='COB':
         domainURL=configdata['RANGER']['DomainURL']['COB']  
    elif environment=='PROD':
       domainURL=configdata['RANGER']['DomainURL']['PROD'] 
    return domainURL
      
def SetPolicy(OptedPolicy):   
    basePolicy=configdata['RANGER']['POLICIES']['POSTAPI']['BodyParameters']
    selectedPolilcy=configdata['RANGER']['POLICIES'][OptedPolicy]
    basePolicy['isEnabled']=selectedPolilcy['isEnabled']
    basePolicy['name']=selectedPolilcy['name']
    basePolicy['description']=selectedPolilcy['description']
    basePolicy['resources']['catalog']['values']=selectedPolilcy['catalogAccess']
    basePolicy['resources']['schema']['values']=selectedPolilcy['schemaAccess']
    basePolicy['resources']['table']['values']=selectedPolilcy['tableAccess']
    basePolicy['resources']['column']['values']=selectedPolilcy['columnAccess']    
####USER GROUP ROLE  

    basePolicy['policyItems'][0]['users']=selectedPolilcy['users']
    
## Group ID As Per Environment    
    if environment=='DEV':
        basePolicy['policyItems'][0]['groups']=selectedPolilcy['groups']['DEV']  
    elif environment=='UAT':
        basePolicy['policyItems'][0]['groups']=selectedPolilcy['groups']['UAT']  
    elif environment=='COB':
            basePolicy['policyItems'][0]['groups']=selectedPolilcy['groups']['COB']  
    elif environment=='PROD':
        basePolicy['policyItems'][0]['groups']=selectedPolilcy['groups']['PROD']          
    
    basePolicy['policyItems'][0]['roles']=selectedPolilcy['roles']
    basePolicy['policyItems'][0]['conditions']=selectedPolilcy['conditions']
    return basePolicy

################################################################ROLE ##############################################################################

#print(GetAuthAccessToken()
def GetRangerRoles(UrlEndPoint):
    responseGet=""
    try:
        responseRequest = requests.get(UrlEndPoint, auth = (configdata['RANGER']['AUTHENTICATION']['UserName'],GetAuthAccessPassword()),headers = {"Content-Type" : "application/json"})
        #print(UrlEndPoint, dict(responseRequest.json())
        responseRequest=responseRequest.json()
        return responseRequest#['mappingId']
    except Exception as e:
        LogMessageInProcessLog("Exception Raiased in "+sys._getframe().f_code.co_name +"...."+str(e))
        raise Exception(str(responseRequest))#exit(0)


def SetRole(OptedRole):   
    baseRole=configdata['RANGER']['ROLES']['POSTAPI']['BodyParameters']
    selectedRole=configdata['RANGER']['ROLES'][OptedRole]
    baseRole['isEnabled']=selectedRole['isEnabled']
    baseRole['name']=selectedRole['name']
    baseRole['description']=selectedRole['description']
    baseRole['roles']=selectedRole['roles']
    baseRole['users']=selectedRole['users']
    baseRole['groups']=selectedRole['groups']
    baseRole['options']=selectedRole['options']
    return baseRole

################################################################ROLE ##############################################################################


#print(environment)   
responseAPI=GetFromRanger(GetDomainURL()+configdata['RANGER']['POLICIES']['GETAPI']['EndPoint'])
#responseAPI=SetPolicy('HiveNAMPolicy')
#responseAPI=PostToRanger(GetDomainURL()+configdata['RANGER']['POLICIES']['POSTAPI']['EndPoint'],configdata['RANGER']['POLICIES']['POSTAPI']['BodyParameters'])
#responseAPI=PutToRangerById(GetDomainURL()+configdata['RANGER']['POLICIES']['PUTAPI']['EndPoint'],configdata['RANGER']['POLICIES']['POSTAPI']['BodyParameters'],28)
#responseAPI=DeleteFromRangerById(GetDomainURL()+configdata['RANGER']['POLICIES']['DELETEAPI']['EndPoint'],28)

#responseAPI=SetRole('TESTROLE')
#responseAPI=PostToRanger(GetDomainURL()+configdata['RANGER']['ROLES']['POSTAPI']['EndPoint'],configdata['RANGER']['ROLES']['POSTAPI']['BodyParameters'])

#responseAPI=GetFromRanger(GetDomainURL()+configdata['RANGER']['ROLES']['GETAPI']['EndPoint'])#,configdata['RANGER']['ROLES']['POSTAPI']['BodyParameters'])
#responseAPI=DeleteFromRangerById(GetDomainURL()+configdata['RANGER']['ROLES']['DELETEAPI']['EndPoint'],"RoleToTestFromWeb")
#enc=encrypt_password("RangerPassword1")
#print(enc)
#print(decrypt_password(enc))
#print(os.getlogin())
LogMessageInProcessLog(json.dumps(responseAPI, indent=4))