# https://deepnote.com/project/54315573-60bb-43bb-9a5d-2cab4c2aa649

import requests
import time, datetime


API_Base_URL = "https://rt.data.gov.hk"

API_PATH = "/v1/transport/citybus-nwfb"

API_New_World_First_Bus_Service_Limited = "/NWFB"
API_Citybus_Limited = "/CTB"

API_Direction_INBOUND = "/inbound"
API_Direction_OUTBOUND = "/outbound"

def getRouteStop(API_CompanyID, Route, API_Direction):
    URL = API_Base_URL+API_PATH+"/route-stop"+API_CompanyID+"/"+Route+API_Direction
    return requests.get(url = URL).json() 

def getCompany(API_CompanyID):
    URL = API_Base_URL+API_PATH+"/company"+API_CompanyID
    return requests.get(url = URL).json() 

def getStop(stop_id):
    """
    6-digit representation of a bus stop
    (Remark: To find the corresponding bus stop ID, user can query the "Route-Stop API") 
    """
    URL = API_Base_URL+API_PATH+"/stop"+"/"+stop_id
    return requests.get(url = URL).json() 

def getRoute(API_CompanyID, route=""):
    URL = API_Base_URL+API_PATH+"/route"+API_CompanyID+"/"+route
    return requests.get(url = URL).json() 

def getETA(API_CompanyID, stop_id, route):
    URL = API_Base_URL+API_PATH+"/eta"+API_CompanyID+"/"+stop_id+"/"+route
    return requests.get(url = URL).json() 


def toDatetime(str_datetime):
    """
    '2021-02-04T17:25:00+08:00'
    r['data'][2]["eta"].replace("T"," ")
    %Y-%m-%d %H:%M:%S%z
    datetime.datetime(2021, 2, 4, 17, 25, tzinfo=datetime.timezone(datetime.timedelta(seconds=28800)))
    """
    return datetime.datetime.strptime(str_datetime.replace("T"," "),"%Y-%m-%d %H:%M:%S%z")

def ETA(strTime):
    """
    This will return the expect time in second. Divide 60 sec by your own
    """
    temp =  toDatetime(strTime) - datetime.datetime.now(datetime.timezone.utc)
    return temp.total_seconds()
  
  
  
# Find the Time that from Cyberport 
data = getETA(API_New_World_First_Bus_Service_Limited, "002392", "30X")
f = []
for dataa in data["data"]:
    if dataa["dir"] == "O":
        f.append(dataa)
print(ETA(f[0]["eta"])/60, ETA(f[1]["eta"])/60)
