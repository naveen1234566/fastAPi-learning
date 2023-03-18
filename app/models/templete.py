"""
File: templete.py
Path: /app/models/templete.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 02/03/2023
"""
import re
from pydantic import BaseModel, validator
from typing import Optional, List, Any

class SSID(BaseModel):
    port: int
    networkname: str
    name: str
    broadcastSSID: bool
    frequency: str
    securityMode: str
    password: str
    
    @validator('port')
    def port_check(cls, v):
        if not v > 0 or v > 200:
            raise ValueError("Port value must contain 0 to 200 range.")
        return v
    
    @validator('networkname')
    def networkName(cls, v):
        if not re.match("^\w[a-z]{3,15}$", v):
            raise ValueError("Network must contain 3 to 15 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("networkname first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("networkname last one is not coming for (- or _)")
        return v
    
    @validator('broadcastSSID')
    def broadcastssid_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('frequency')
    def frequency_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Frequency first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Frequency last one is not coming for (- or _)")
        return v
    
    @validator('securityMode')
    def securitymode_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("securityMode first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("securityMode last one is not coming for (- or _)")
        return v
    
    @validator('password')
    def bindPassword_check(cls, v):
        if not re.match("^\w[a-z]{3,15}$", v):
            raise ValueError("Passowrd must contain 3 to 15 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Password first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Password last one is not coming for (- or _)")
        return v

class Ghz5(BaseModel):
    protocol: str
    channel: str
    country: str
    
    @validator('protocol')
    def protocol_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("protocol first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("protocol last one is not coming for (- or _)")
        return v
    
    @validator('channel')
    def channel_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("channel first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("channel last one is not coming for (- or _)")
        return v
    
    @validator('country')
    def country_check(cls, v):
        if not re.match("^\w[a-zA-Z\-]{3,15}$", v):
            raise ValueError("Country must contain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Country first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Country last one is not coming for (- or _)")
        return v 

class Ghz24(BaseModel):
    country: str
    protocol: str
    channel: str
    channelWidth: str
    
    @validator('country')
    def country_check(cls, v):
        if not re.match("^\w[a-zA-Z\-]{3,15}$", v):
            raise ValueError("Country must contain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Country first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Country last one is not coming for (- or _)")
        return v
    
    @validator('protocol')
    def protocol_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("protocol first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("protocol last one is not coming for (- or _)")
        return v
    
    @validator('channel')
    def channel_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("channel first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("channel last one is not coming for (- or _)")
        return v
    
    @validator('channelWidth')
    def channelwidth_check(cls, v):
        if v[0] == "-" or v[0] == "_":
            raise ValueError("channelWidth first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("channelWidth last one is not coming for (- or _)")
        return v
        
class WifiConfig(BaseModel):
    ghz24: Optional[Ghz24]
    ghz5: Optional[Ghz5]
    ssid: List[Optional[SSID]]

class LdapServer(BaseModel):
    interface: str
    ipAddress: str
    domain: str
    base: str
    bindDn: str
    bindPassword: str
    
    @validator('interface')
    def chech_interface(cls, v):
        if not re.match("^\w[a-z0-9]{2,32}$", v):
            raise ValueError("Lannetwork must contain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Lannetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Lannetwork last one is not coming for (- or _)")
        return v
    
    @validator('ipAddress')
    def ipaddress_check(cls, v):
        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", v):
            raise ValueError("IpAddress is required")
        return v
    
    @validator('domain')
    def domain_check(cls, v):
        if not re.match("^\w[a-z]+[.]+\w[a-z]+[.]+\w[a-z]{2,6}$", v):
            raise ValueError("Domain is required")
        return v
    
    @validator('base')
    def base_check(cls, v):
        if not re.match("^\w[a-z\-]{3,15}$", v):
            raise ValueError("Base must cotain 3 to 15 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Base first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Base last one is not coming for (- or _)")
        return v
    
    @validator('bindDn')
    def bindDn_check(cls, v):
        if not re.match("^\w[a-z\-]{3,15}$", v):
            raise ValueError("BindDn must cotain 3 to 15 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("BindDn first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("BindDn last one is not coming for (- or _)")
        return v
    
    @validator('bindPassword')
    def bindPassword_check(cls, v):
        if not re.match("^(?=.*[a-z])(?=.*[@$!%*#?&])[a-z\d@$!#%*?&]{5,12}$", v):
            raise ValueError("BindDn Password is required")
        return v

class SyslogServer(BaseModel):
    interface: str
    ipAddrFqdn: str
    
    @validator('interface')
    def chech_interface(cls, v):
        if not re.match("^\w[a-z0-9]{2,32}$", v):
            raise ValueError("Lannetwork must contain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Lannetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Lannetwork last one is not coming for (- or _)")
        return v
    
    @validator('ipAddrFqdn')
    def ipAddFqdn(cls, v):
        if not re.match("^(\d{1,1}\.\d{1,1}\.\d{1,1}\.\d{1,1})$", v):
            raise ValueError("ipAddFqdn is required")
        return v
    
class NtpServer(BaseModel):
    interface: str
    ipAddrFqdn: str
    
    @validator('interface')
    def chech_interface(cls, v):
        if not re.match("^\w[a-z0-9]{2,32}$", v):
            raise ValueError("Lannetwork must contain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Lannetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Lannetwork last one is not coming for (- or _)")
        return v
    
    @validator('ipAddrFqdn')
    def ipAddFqdn(cls, v):
        if not re.match("^(\d{1,1}\.\d{1,1}\.\d{1,1}\.\d{1,1})$", v):
            raise ValueError("IpAddfqdn is required")
        return v


class InboundNat(BaseModel):
    externalAddress: str
    externalPort: str
    internalAddress: str
    internalPort: str
    lanRoutingInstance: str
    name: str
    protocol: str
    wanNetwork: str
    
    @validator('externalAddress')
    def externalAddress_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('externalPort')
    def externalPort_check(cls, v):
        if not re.match("^\w[0-9\-]{3,15}$", v):
            raise ValueError("externalPort  must cotain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("externalPort first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("externalPort last one is not coming for (- or _)")
        return v
    
    @validator('internalAddress')
    def internalAddress_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('internalPort')
    def internalPort_check(cls, v):
        if not re.match("^\w[0-9\-]{3,15}$", v):
            raise ValueError("internalPort  must cotain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("internalPort first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("internalPort last one is not coming for (- or _)")
        return v
    
    @validator('lanRoutingInstance')
    def lanRoutingInstance_check(cls, v):
        if not re.match("^\w[a-zA-Z-]{3,15}$", v):
            raise ValueError("lanRoutingInstance  must cotain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("lanRoutingInstance first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("lanRoutingInstance last one is not coming for (- or _)")
        return v
    
    @validator('name')
    def name_check(cls, v):
        if not re.match("^\w[a-z0-9]{3,15}$", v):
            raise ValueError("Name value  must cotain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Name first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Name last one is not coming for (- or _)")
        return v
    
    @validator('protocol')
    def protocal_check(cls, v):
        if not re.match("^\w[A-Z]{2,15}$", v):
            raise ValueError("protocol must cotain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("protocol first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("protocol last one is not coming for (- or _)")
        return v
    
    @validator('wanNetwork')
    def wanNetwork_check(cls, v):
        if not re.match("^\w[a-z_\-]{3,15}$", v):
            raise ValueError("wanNetwork must cotain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("wanNetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("wanNetwork last one is not coming for (- or _)")
        return v
            

class SplitTunnel(BaseModel):
    vrfName: str
    wanNetwork: str
    diaEnabled: str
    gatwayEnabled: str
    
    @validator('vrfName')
    def vrfname_check(cls, v):
        if not re.match("^\w[a-zA-Z\-]{3,15}$", v):
            raise ValueError("vrfName must cotain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("vrfName first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("vrfName last one is not coming for (- or _)")
        return v
    
    @validator('wanNetwork')
    def wanNetwork_check(cls, v):
        if not re.match("^\w[a-z_\-]{3,15}$", v):
            raise ValueError("wanNetwork must cotain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("wanNetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("wanNetwork last one is not coming for (- or _)")
        return v
    
    @validator('diaEnabled')
    def diaEnabled_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('gatwayEnabled')
    def gatwayEnabled_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    

class LANInterfaceUnitInfo(BaseModel):
    unitId: int
    vlanId: str
    lannetwork: str
    organization: str
    ipv4AssignmentMethod: str
    ipv6AssignmentMethod: str
    routingInstance: str
    
    @validator('unitId')
    def unitId_check(cls, v):
        if not v > 0 or v > 4095:
            raise ValueError("UnitId must contain 0 to 4095 range ")
        return v
    
    @validator('vlanId')
    def vlanId_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('lannetwork')
    def lannetwork_check(cls, v):
        if not re.match("^\w[a-z0-9]{2,32}$", v):
            raise ValueError("Lannetwork must contain 3 to 32 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Lannetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Lannetwork last one is not coming for (- or _)")
        return v
    
    @validator('organization')
    def organization_check(cls, v):
        if not re.match("^\w[a-zA-Z-]{3,14}$", v):
            raise ValueError("Organization must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Organization first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Organization last one is not coming for (- or _)")
        return v
    
    @validator('ipv4AssignmentMethod')
    def ipv4Method_check(cls, v):
        value = ["Static", "DHCP"]
        if not v in value:
            raise ValueError("Ipv4 method is only for requirement")
        return v
    
    @validator('ipv6AssignmentMethod')
    def ipv6Method_check(cls, v):
        value = ["Static", "DHCP"]
        if not v in value:
            raise ValueError("Ipv6 method is only for requirement")
        return v
    
    @validator('routingInstance')
    def routing_check(cls, v):
        if not re.match("^\w[a-zA-Z_\-]{3,15}$", v):
            raise ValueError("Routing must cotain 3 to 15 chars")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Routing first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Routing last one is not coming for (- or _)")
        return v
        

class LANInterface(BaseModel):
    interface: str
    portNumber: int
    unitInfo: List[Optional[LANInterfaceUnitInfo]]
    
    @validator('interface')
    def interface_check(cls, v):
        if not re.match("^pni-([0-0]{1})/([0-9]{1,3})$", v):
            raise ValueError("Invalid interface".format(v))
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Interface first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Interface last one is not coming for (- or _)")
        return v
    
    @validator('portNumber')
    def portnumber_check(cls, v):
        if not v >= 0 or v > 200:
            raise ValueError("NumberOfPort must cotain 0 to 200 range.")
        return v
    

class WANInterfaceUnitInfo(BaseModel):
    unitId: int
    vlanId: str
    wannetwork: str
    ipv4AssignmentMethod: str
    ipv6AssignmentMethod: str
    monitorIp: str
    priority: int
    
    @validator('unitId')
    def unitId_check(cls, v):
        if not v > 0 or v > 4095:
            raise ValueError("Unitid must contain 0 to 4095 range.")
        return v
    
    @validator('vlanId')
    def vlanId_check(cls, v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('wannetwork')
    def wannetwork_check(cls, v):
        if not re.match("^\w[a-zA-Z\-]{3,15}$", v):
            raise ValueError("Wannetwork must cotain 3 to 15 chars.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Wannetwork first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Wannetwork last one is not coming for (- or _)")
        return v
    
    @validator('ipv4AssignmentMethod')
    def ipv4Method_check(cls, v):
        value = ["Static", "DHCP"]
        if not v in value:
            raise ValueError("Ipv4 method is only for requirement")
        return v
    
    @validator('ipv6AssignmentMethod')
    def ipv6Method_check(cls, v):
        value = ["Static", "DHCP"]
        if not v in value:
            raise ValueError("Ipv6 method is only for requirement")
        return v
    
    @validator('monitorIp')
    def monitorip_check(cls, v):
        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", v):
            raise ValueError("MonitorIp is required")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Interface first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Interface last one is not coming for (- or _)")
        return v
    
    @validator('priority')
    def priority_check(cls, v):
        if not v > 0 or v >= 200:
            raise ValueError("Priority must contain 0 to 200 range.")
        return v
    
    
class WANInterface(BaseModel):
    interface: str
    portNumber: int
    unitInfo: List[Optional[WANInterfaceUnitInfo]]
    
    @validator('interface')
    def interface_check(cls, v):
        if not re.match("^pni-([0-0]{1})/([0-9]{1,3})$", v):
            raise ValueError("Invalid interface".format(v))
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Interface first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Interface last one is not coming for (- or _)")
        return v
    
    @validator('portNumber')
    def portnumber_check(cls, v):
        if not v >= 0 or v > 200:
            raise ValueError("NumberOfPort must contain 0 to 200 range.")
        return v


class PortType(BaseModel):
    wan: int
    lan: int
    wanLan: int
    lte: int
    wifi: int
    
    
    @validator('wan')
    def wan_check(cls, v):
        if not v >= 0 or v > 8:
            raise ValueError("WAN must contain 0 to 8 values.")
        return v
    
    @validator('lan')
    def lan_check(cls, v):
        if not v >= 0 or v > 8:
            raise ValueError("LAN must contain 0 to 8 values.")
        return v
    
    @validator('wanLan')
    def wanlan_check(cls, v):
        if not v >= 0 or v > 6:
            raise ValueError("WanLan must contain 0 to 6 values.")
        return v
    
    @validator('lte')
    def lte_check(cls, v):
        if not v >= 0 or v > 6:
            raise ValueError("Lte must contain 0 to 6 values.")
        return v
    
    @validator('wifi')
    def wifi_check(cls, v):
        if not v >= 0 or v > 4:
            raise ValueError("Wifi must contain 0 to 4 values.")
        return v

class Templete(BaseModel):
    _id: str
    name: str
    tempId: int
    Organization: str
    subOrganization: List[Any]
    deviceType: str
    ireach: List[str]
    analytics: str
    numberOfPort: int
    portType: Optional[Optional[PortType]]
    status: str
    wanInterface: List[Optional[WANInterface]]
    lanInterface: List[Optional[LANInterface]]
    splitTunnel: List[Optional[SplitTunnel]]
    inboundNat: List[Optional[InboundNat]]
    ntpServer: List[Optional[NtpServer]]
    syslogServer: List[Optional[SyslogServer]]
    ldapServer: List[Optional[LdapServer]]
    wifiConfig: Optional[WifiConfig]
    
    
    @validator('name')
    def name_check(cls, v):
        if not re.match("^\w[a-z0-9-]{3,14}$", v):
            raise ValueError("Name value  must cotain 3 to 15 characters.")
        # print(v[-1])
        # print(v[0])
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Name first one is not coming for (- or _)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Name last one is not coming for (- or _)")
        return v
    
    @validator('tempId')
    def tempId_check(cls, v):
        if not v >= 5000 or v > 10000:
            raise ValueError("TempId is must cotain 5000 to 10000 range.")
        return v
    
    @validator('Organization')
    def organization_check(cls, v):
        if not re.match("^\w[a-zA-Z-]{3,14}$", v):
            raise ValueError("Organization must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Organization first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Organization last one is not coming for (- or _)")
        return v
    
    @validator('subOrganization')
    def suborganization_check(cls, v):
        if not range(len(v) <= 2):
            raise ValueError("Suborganization must contain two values.")
        return v
        
    @validator('deviceType')
    def devicetype_check(cls, v):
        if not re.match("^\w[a-z-]{3,14}$", v):
            raise ValueError("Devicetype must coatain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Devicetype first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Devicetype last one is not coming for (- or _)")
        return v
    
    @validator('ireach')
    def ireach_check(cls, v):
        for item in v:
            if not re.sub("^\w[a-zA-Z]{3,14}$","", str(item)):
                raise ValueError("Ireach is not valid.".format(item))
            return item
    
        
    @validator('analytics')
    def analytics_check(cls, v):
        if not re.match("^\w[a-z]{3,14}$", v):
            raise ValueError("Analytics must contain 3 to 15 characters.")
        if v[0] == "-" or v[0] == "_":
            raise ValueError("Analytics first one is not coming for (_ or -)")
        if v[-1] == "-" or v[-1] == "_":
            raise ValueError("Analytics last one is not coming for (- or _)")
        
        return v
    
    @validator('numberOfPort')
    def numberofport_check(cls, v):
        if not v >= 0 or v > 32:
            raise ValueError("NumberOfPort must contain 3 to 15 chars.")
        return v
    
    class Config:
        schema_extra= {
            "example": {
                "name": "temp-temp-04",
                "tempId": 5000,
                "Organization": "Ticvic",
                "subOrganization": [
                    "tech"
                ],
                "deviceType": "full-mesh",
                "ireach": [
                    "iReach5"
                ],
                "analytics": "cluster",
                "numberOfPort": 2,
                "portType": {
                    "wan": 1,
                    "lan": 1,
                    "wanLan": 0,
                    "lte": 0,
                    "wifi": 0
                },
                "status": "svd",
                "wanInterface": [
                    {
                    "interface": "pni-0/10",
                    "portNumber": 10,
                    "unitInfo": [
                        {
                        "unitId": 10,
                        "vlanId": "{$il_pni-0_0_test__vlanId}",
                        "wannetwork": "test-uv-mpls",
                        "ipv4AssignmentMethod": "Static",
                        "ipv6AssignmentMethod": "DHCP",
                        "monitorIp": "192.168.4.4",
                        "priority": 10
                        }
                    ]
                    }
                ],
                "lanInterface": [
                    {
                    "interface": "pni-0/1",
                    "portNumber": 1,
                    "unitInfo": [
                        {
                        "unitId": 12,
                        "vlanId": "4",
                        "lannetwork": "lan5",
                        "organization": "Ticvic",
                        "ipv4AssignmentMethod": "Static",
                        "ipv6AssignmentMethod": "DHCP",
                        "routingInstance": "Ticvic-LAN-VR"
                        }
                    ]
                    }
                ],
                "splitTunnel": [
                    {
                    "vrfName": "Ticvic-LAN-VR",
                    "wanNetwork": "test-uv-mpls",
                    "diaEnabled": "string",
                    "gatwayEnabled": "string"
                    }
                ],
                "inboundNat": [
                    {
                    "externalAddress": "{$il_One_InboundExternalAddress}",
                    "externalPort": "13-14",
                    "internalAddress": "192.168.5.10-192.168.5.100",
                    "internalPort": "13-14",
                    "lanRoutingInstance": "Ticvic-LAN-VR",
                    "name": "test5",
                    "protocol": "TCP",
                    "wanNetwork": "test-uv-mpls"
                    }
                ],
                "ntpServer": [
                    {
                    "interface": "lan5",
                    "ipAddrFqdn": "4.3.3.3"
                    }
                ],
                "syslogServer": [
                    {
                    "interface": "lan5",
                    "ipAddrFqdn": "4.1.1.1"
                    }
                ],
                "ldapServer": [
                    {
                    "interface": "lan5",
                    "ipAddress": "192.168.5.10",
                    "domain": "testntp.local.com",
                    "base": "testbasedn",
                    "bindDn": "testbase-dn",
                    "bindPassword": "ticvic@1234"
                    }
                ],
                "wifiConfig": {
                    "ghz24": {
                    "country": "AZ-Azerbaijan",
                    "protocol": "b-2.4GHz",
                    "channel": "auto",
                    "channelWidth": "40MHz"
                    },
                    "ghz5": {
                    "protocol": "n-5GHz",
                    "channel": "36",
                    "country": "AZ-Azerbaijan"
                    },
                    "ssid": [
                    {
                        "port": 200,
                        "networkname": "lanwifi",
                        "name": "wifi",
                        "broadcastSSID": "true",
                        "frequency": "2.4-GHz",
                        "securityMode": "wpa2-psk",
                        "password": "wifipassword"
                    }
                    ]
                }
                }
                        }
                    