"""
File: templete.py
Path: /app/routers/templete.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 03/03/2023
"""

from fastapi import APIRouter, status, Response
from ..database import templete
from ..models.templete import Templete
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid


router = APIRouter()

""" Create a new templete profile in the database."""
@router.post('/Templete', status_code=status.HTTP_201_CREATED, summary="Create an templete", response_description="Create an templete with all the information")
def create(templetes:Templete):
    try:

        templetes = templetes.dict()
        templetes["created"] = templetes["updated"] = get_time()
        templetes["_id"] = get_uuid()
        
        if (templete.find_one({"tempId":templetes["tempId"]})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Temp Id already exists"}))
        
        """ WanInterface with data """
        wan_interface = []
        for wanVal in templetes["wanInterface"]:
            wan_interface.append(wanVal["interface"])
    
        wan_unitId = []
        wan_network = []
                        
        for Interface in templetes["wanInterface"]:
            # print(Interface["interface"].split('/')[1])
            for unitInfo in Interface["unitInfo"]:
                wan_unitId.append(unitInfo["unitId"])
                
            for wannetwork in Interface["unitInfo"]:
                wan_network.append(wannetwork["wannetwork"])
                
        """ split tunnel """
        for val_split in templetes["splitTunnel"]:
            if val_split["wanNetwork"] not in wan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch splitTunnel(wannetwork) and Waninterface(wannetwork) - ({wannetwork["wannetwork"]})'}))
        
        """ inboundNat """
        for val_inbound in templetes["inboundNat"]:
            if val_inbound["wanNetwork"] not in wan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch inboundNat(wannetwork) and Waninterface(wannetwork) - ({wannetwork["wannetwork"]})'}))
       
            if len(wan_network) != len(set(wan_network)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface WanNetwork - ({Interface["interface"]})'}))
               
            if len(wan_unitId) != len(set(wan_unitId)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface unitId - ({Interface["interface"]})'}))
            
            if int(Interface["interface"].split('/')[1]) != Interface["portNumber"]:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Portnumber and WANinterface - ({Interface["portNumber"]})'}))
            
            if len(wan_interface) != len(set(wan_interface)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Invalid WANinterface({wanVal["interface"]}) name Types'}))
        
        """ LanInterface with data """
        lan_interface = []
        for lanVal in templetes["lanInterface"]:
            lan_interface.append(lanVal["interface"]) 
        
        lan_unitId = []
        lan_organization = []
        lan_route = []
        lan_network = []
        instance = [] 
        for Interface_name in templetes["lanInterface"]:
            for unit_lan in Interface_name["unitInfo"]:
                lan_unitId.append(unit_lan["unitId"])
            
            for organization_name in Interface_name["unitInfo"]:
                lan_organization.append(organization_name["organization"])
            
            for route in Interface_name["unitInfo"]:
                lan_route.append(route["routingInstance"])

            for lannet_works in Interface_name["unitInfo"]:
                lan_network.append(lannet_works["lannetwork"])
        
            for routinginstance in Interface_name["unitInfo"]:
                instance.append(routinginstance["routingInstance"])
                
        """ split tunnel """
        for splitval in templetes["splitTunnel"]:
            if splitval["vrfName"] not in instance:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch split vrfname laninterface routinginstance - ({routinginstance["routingInstance"]})'}))
        
        """ inboundNat """
        for inbound in templetes["inboundNat"]:
            if inbound["lanRoutingInstance"] not in instance:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch inboundNat lanroutinginstance laninterface routinginstance - ({routinginstance["routingInstance"]})'}))
    
        """ ntp server """
        ntp_server = []   
        for ntpVal in templetes["ntpServer"]:
            ntp_server.append(ntpVal["interface"]) 
            if ntpVal["interface"] not in lan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Laninterface(network) and ntpserver(interface) -({ntpVal["interface"]})'}))
        
        if len(ntp_server) != len(set(ntp_server)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch ntpserver interface - ({ntpVal["interface"]})'}))
        
        """ syslog server """              
        syslog_server = []
        for syslogVal in templetes["syslogServer"]:
            syslog_server.append(syslogVal["interface"]) 
            if syslogVal["interface"] not in lan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Laninterface(network) and syslogserver(interface) -({syslogVal["interface"]})'}))
        
        if len(syslog_server) != len(set(syslog_server)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch syslogserver interface - ({syslogVal["interface"]})'}))
        
        """ ldap server """
        ldap_server = []
        for ldapval in templetes["ldapServer"]:
            ldap_server.append(ldapval["interface"])
            if ldapval["interface"] not in lan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Laninterface(network) and ldapserver(interface) -({ldapval["interface"]})'}))
        
        if len(ldap_server) != len(set(ldap_server)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch ldapserver interface - ({ldapval["interface"]})'}))
        
        """ organization """
        for laninterface in lan_organization:
            if templetes["Organization"] != laninterface:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Organization and Lan_organization -({Interface_name["interface"]})'}))
        
        """ laninterface """
        if len(lan_network) != len(set(lan_network)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LANInterface LanNetwork - ({Interface_name["interface"]})'}))
                
        if len(lan_unitId) != len(set(lan_unitId)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LANInterface unitId - ({Interface_name["interface"]})'}))
                
        if int(Interface_name["interface"].split('/')[1]) != Interface_name["portNumber"]:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch portnumber and LANinterface - ({Interface_name["interface"]})'}))

        if len(lan_interface) != len(set(lan_interface)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Invalid LANinterface ({lanVal["interface"]}) name Types'}))
        
        """ Port type and numberofport """       
        if templetes["portType"]["wan"] != len(templetes["wanInterface"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WAN interface and WAN - ({templetes["portType"]["wan"]}) values'}))
        
        if templetes["portType"]["lan"] != len(templetes["lanInterface"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LAN interface and LAN - ({templetes["portType"]["lan"]}) values'}))
        
        if templetes["numberOfPort"] != (sum(templetes["portType"].values())):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Numberofport and PortType - ({templetes["numberOfPort"]}) values'}))

        if templetes["portType"]["wifi"] != len(templetes["wifiConfig"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch wifiConfig and wifi - ({templetes["portType"]["wifi"]}) values'}))
        
        
        try:
            results = templete.insert_one(templetes)
            if results.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"templete has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Retrieve all templete profiles in the database """    
@router.get('/Templete/templete', status_code=status.HTTP_200_OK, summary= "Get all templete")
def read_all(page:int=1, limit:int=25):
    try:
        
        if not list(templete.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"NO DATA FOUND", "templete":list(templete.find())}))
        
        page = (page - 1) * limit
        getTemplete = list(templete.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total": templete.count_documents({}), "templete":getTemplete}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
""" Retrieve a templete profile with a matching ID """
@router.get('/Templete/{templeteId}', status_code=status.HTTP_200_OK, summary="Get an templete")
def get_an_templete(templeteId: str):
    try:
        
        if (templeteId := templete.find_one({"_id":templeteId})) is not None:
            return JSONResponse(content=jsonable_encoder({'templete':templeteId}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Templete with Id ({templeteId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
"""Update a person by giving only the fields to update"""
@router.put('/Templete/{templeteId}', status_code=status.HTTP_200_OK, summary="Update an templete")
def update_an(templetes:Templete, tempId: str):
    try:

        temp = templetes.dict()
        temp["updated"] = get_time()
        
        """ WanInterface with data """
        wan_interface = []
        for wanVal in templetes["wanInterface"]:
            wan_interface.append(wanVal["interface"])
    
        wan_unitId = []
        wan_network = []
                        
        for Interface in templetes["wanInterface"]:
            # print(Interface["interface"].split('/')[1])
            for unitInfo in Interface["unitInfo"]:
                wan_unitId.append(unitInfo["unitId"])
                
            for wannetwork in Interface["unitInfo"]:
                wan_network.append(wannetwork["wannetwork"])
                
        """ split tunnel """
        for val_split in templetes["splitTunnel"]:
            if val_split["wanNetwork"] not in wan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch splitTunnel(wannetwork) and Waninterface(wannetwork) - ({wannetwork["wannetwork"]})'}))
        
        """ inboundNat """
        for val_inbound in templetes["inboundNat"]:
            if val_inbound["wanNetwork"] not in wan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch inboundNat(wannetwork) and Waninterface(wannetwork) - ({wannetwork["wannetwork"]})'}))
       
            if len(wan_network) != len(set(wan_network)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface WanNetwork - ({Interface["interface"]})'}))
               
            if len(wan_unitId) != len(set(wan_unitId)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WANInterface unitId - ({Interface["interface"]})'}))
            
            if int(Interface["interface"].split('/')[1]) != Interface["portNumber"]:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Portnumber and WANinterface - ({Interface["portNumber"]})'}))
            
            if len(wan_interface) != len(set(wan_interface)):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Invalid WANinterface({wanVal["interface"]}) name Types'}))
        
        """ LanInterface with data """
        lan_interface = []
        for lanVal in templetes["lanInterface"]:
            lan_interface.append(lanVal["interface"]) 
        
        lan_unitId = []
        lan_organization = []
        lan_route = []
        lan_network = []
        instance = [] 
        for Interface_name in templetes["lanInterface"]:
            for unit_lan in Interface_name["unitInfo"]:
                lan_unitId.append(unit_lan["unitId"])
            
            for organization_name in Interface_name["unitInfo"]:
                lan_organization.append(organization_name["organization"])
            
            for route in Interface_name["unitInfo"]:
                lan_route.append(route["routingInstance"])

            for lannet_works in Interface_name["unitInfo"]:
                lan_network.append(lannet_works["lannetwork"])
        
            for routinginstance in Interface_name["unitInfo"]:
                instance.append(routinginstance["routingInstance"])
                
        """ split tunnel """
        for splitval in templetes["splitTunnel"]:
            if splitval["vrfName"] not in instance:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch split vrfname laninterface routinginstance - ({routinginstance["routingInstance"]})'}))
        
        """ inboundNat """
        for inbound in templetes["inboundNat"]:
            if inbound["lanRoutingInstance"] not in instance:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch inboundNat lanroutinginstance laninterface routinginstance - ({routinginstance["routingInstance"]})'}))
    
        """ ntp server """
        ntp_server = []   
        for ntpVal in templetes["ntpServer"]:
            ntp_server.append(ntpVal["interface"]) 
            if ntpVal["interface"] not in lan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Laninterface(network) and ntpserver(interface) -({ntpVal["interface"]})'}))
        
        if len(ntp_server) != len(set(ntp_server)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch ntpserver interface - ({ntpVal["interface"]})'}))
        
        """ syslog server """              
        syslog_server = []
        for syslogVal in templetes["syslogServer"]:
            syslog_server.append(syslogVal["interface"]) 
            if syslogVal["interface"] not in lan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Laninterface(network) and syslogserver(interface) -({syslogVal["interface"]})'}))
        
        if len(syslog_server) != len(set(syslog_server)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch syslogserver interface - ({syslogVal["interface"]})'}))
        
        """ ldap server """
        ldap_server = []
        for ldapval in templetes["ldapServer"]:
            ldap_server.append(ldapval["interface"])
            if ldapval["interface"] not in lan_network:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Laninterface(network) and ldapserver(interface) -({ldapval["interface"]})'}))
        
        if len(ldap_server) != len(set(ldap_server)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch ldapserver interface - ({ldapval["interface"]})'}))
        
        """ organization """
        for laninterface in lan_organization:
            if templetes["Organization"] != laninterface:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Organization and Lan_organization -({Interface_name["interface"]})'}))
        
        """ laninterface """
        if len(lan_network) != len(set(lan_network)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LANInterface LanNetwork - ({Interface_name["interface"]})'}))
                
        if len(lan_unitId) != len(set(lan_unitId)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LANInterface unitId - ({Interface_name["interface"]})'}))
                
        if int(Interface_name["interface"].split('/')[1]) != Interface_name["portNumber"]:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch portnumber and LANinterface - ({Interface_name["interface"]})'}))

        if len(lan_interface) != len(set(lan_interface)):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Invalid LANinterface ({lanVal["interface"]}) name Types'}))
        
        """ Port type and numberofport """       
        if templetes["portType"]["wan"] != len(templetes["wanInterface"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch WAN interface and WAN - ({templetes["portType"]["wan"]}) values'}))
        
        if templetes["portType"]["lan"] != len(templetes["lanInterface"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch LAN interface and LAN - ({templetes["portType"]["lan"]}) values'}))
        
        if templetes["numberOfPort"] != (sum(templetes["portType"].values())):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch Numberofport and PortType - ({templetes["numberOfPort"]}) values'}))

        if templetes["portType"]["wifi"] != len(templetes["wifiConfig"]):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch wifiConfig and wifi - ({templetes["portType"]["wifi"]}) values'}))
        
        
        if (
            existing_templete := templete.find_one({"_id": tempId})
        ) is not None:
            return JSONResponse(content=jsonable_encoder({"templates": existing_templete}))

        if len(temp) >= 1:
            update_result = templete.update_one({"_id": tempId}, {"$set": temp})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Template with ID ({tempId}) not found"}))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Template with ID ({tempId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Delete a interface given its a templeteId """
@router.delete("/Templete/{templeteId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interface(templeteId: str, response:Response):
    try:
        templete = templete.delete_one({"_id":templeteId})
        
        if templete.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"Templete has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Templete with ID ({templeteId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))  


            