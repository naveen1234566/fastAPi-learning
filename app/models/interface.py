"""
File: interface.py
Path: /app/models/interface.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 01/03/2023
"""

from pydantic import BaseModel, validator
from typing import Optional, List
import re

class ReachabilityMonitor(BaseModel):
    icmp: bool
    interval: int
    thershold: int
    
    @validator('icmp')
    def icmp_check(cls, v):
        if v == None:
            raise ValueError("None is not allowed value")
        return v
    
    @validator('interval')
    def interval_check(cls, v):
        if not v > 0 or v > 60:
            raise ValueError("Interval  vlaue is required")
        return v
    
    @validator('thershold')
    def thershold_check(cls, v):
        if not v > 0 or v > 60:
            raise ValueError("Thershold value is required")
        return v 

class DHCPAddress(BaseModel):
    routePreference: int
    vendorClassIdentifier: str
    reachabilityMonitor: Optional[ReachabilityMonitor]
    
    @validator('routePreference')
    def routePreference_check(cls, v):
        if not v > 0 or v > 255:
            raise ValueError("routepreference is invalid requirement")
        return v
    
    @validator('vendorClassIdentifier')
    def vendorClass_check(cls, v):
        if not re.match("^\w[a-z 0-9]{0,255}$", v):
            raise ValueError("ClassIdentifier is must cotain space")
        return v

class StaticArp(BaseModel):
    sunnetAddressMask: str
    macAddress: str
    
    @validator('sunnetAddressMask')
    def sunnetAddress_check(cls, v):
        if not re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/([0-2]{1}|0[0-9]|1[0-9]|2[0-4]{0,1})$", v):
                raise ValueError("Invalid IpAddress".format(v))
        return v
    
    @validator('macAddress')
    def macAddress_check(cls, v):
        if not re.match("((([0-9a-fA-F]){2})\\:){5}"\
             "([0-9a-fA-F]){2}", v):
            raise ValueError("Invalid Mac_Address".format(v))
        return v

class StaticAddress(BaseModel):
    ipAddressMask: List[str]
    staticArp:Optional[List[StaticArp]]
    
    @validator('ipAddressMask')
    def validate_ipAddressMask(cls, v):
        if not re.sub("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/([0-2]{1}|0[0-9]|1[0-9]|2[0-4]|2[0-4]{0,1})$", "", str(v)):
                raise ValueError("Invalid IpAddress".format(v))
        return v

class Ipv4(BaseModel):
    addressType: str
    staticAddress: Optional[StaticAddress]
    
    @validator('addressType')
    def addressType_check(cls, v):
        value = ["Static", "DHCP"]
        if not v in value:
            raise ValueError("Address only given a list")
        return v

class Bandwith2(BaseModel):
    uplink: int
    downlink: int
    
    @validator('uplink')
    def uplink_check(cls, v):
        if not v > 0 or v > 10000000:
            raise ValueError("Uplink value is invalid")
        return v
    
    @validator('downlink')
    def downlink_check(cls, v):
        if not v > 0 or v > 10000000:
            raise ValueError("Downlink value is invalid")
        return v

class SubInterface(BaseModel):
    unitId: int
    description: str
    vlanId: int
    networkType: str
    networkName: str
    mtu: int
    bandwith: Optional[Bandwith2]
    ipv4: Optional[Ipv4]
    dhcpAddress: Optional[DHCPAddress]
    
    @validator('unitId')
    def unitId_check(cls, v):
        if not v > 0 or v > 4095:
            raise ValueError("Unitid value is required")
        return v
    
    @validator('description')
    def description_check(cls, v):
        if not re.match("^\w[a-zA-Z_\.-]{2,33}$", v):
            raise ValueError("Description is required")
        return v
    
    @validator('vlanId')
    def vlanId_check(cls, v):
        if not v > 0 or v > 4095:
            raise ValueError("Unitid value is required")
        return v
    
    @validator('networkType')
    def networkType_check(cls, v):
        value = ["WAN", "LAN"]
        if not v in value:
            raise ValueError("NetworkType only given a list")
        return v
    
    @validator('networkName')
    def networkName_check(cls, v):
        if not re.match("^\w[a-z A-Z\.-]{2,33}$", v):
            raise ValueError("NetworkName is must cotain unique.")
        return v
    
    @validator('mtu')
    def validate_mtu(cls, v):
        if not v > 71 or v > 9000:
            raise ValueError('mtu is invalid requirement')
        return v

class Bandwith(BaseModel):
    uplink: int
    downlink: int
    
    @validator('uplink')
    def uplink_check(cls, v):
        if not v > 0 or v > 10000000:
            raise ValueError("Uplink value is invalid")
        return v
    
    @validator('downlink')
    def downlink_check(cls, v):
        if not v > 0 or v > 10000000:
            raise ValueError("Downlink value is invalid")
        return v

class Interface(BaseModel):
    _id: str
    name: str
    admin: bool
    description: str
    nativeVlanId: int
    mtu: int
    bandwith:Optional[Bandwith]
    subInterface: Optional[List[SubInterface]]
    
    @validator('name')
    def name_check(cls, v):
        if not re.match("^pni-([0-9]{1}|0[0-9]|1[0-2]{1})/([0-3]{1}|0[0-9]|1[0-9]|2[0-9]|3[0-2]{0,1})$", v):
            raise ValueError("Invalid name".format(v))
        return v
    
    @validator('admin')
    def admin_check(cls ,v):
        if v == None:
            raise ValueError("None value is not allowed")
        return v
    
    @validator('description')
    def description_check(cls, v):
        if not re.match("^\w[a-zA-Z_\.-]{2,33}$", v):
            raise ValueError("Description is required")
        return v
    
    @validator('nativeVlanId')
    def validate_nativeVlanId(cls, v):
        if not v > 0 or v > 4094:
            raise ValueError('VlandId is invalid')
        return v
    
    @validator('mtu')
    def validate_mtu(cls, v):
        if not v > 71 or v > 9000:
            raise ValueError('mtu is invalid')
        return v

    
    class Config:
        schema_extra = {
            "example": {
            "name": "pni-1/2",
            "admin": "true",
            "description": "Ethernet-interface",
            "nativeVlanId": 1,
            "mtu": 80,
            "bandwidth": {
                "uplink": 10,
                "downlink": 20
            },
            "subInterface": [
                {
                "unitId": 1,
                "description": "Sub-interface",
                "vlanId": 22,
                "networkType": "WAN",
                "networkName": "WAN networks",
                "mtu": 72,
                "bandwidth": {
                    "uplink": 800,
                    "downlink": 900
                },
                "ipv4": {
                    "addressType": "Static",
                    "staticAddress": {
                    "ipAddressMask": [
                        "1.2.3.4/24"
                    ],
                    "staticArp": [
                        {
                        "subnetAddressMask": "1.2.3.4/24",
                        "macAddress": "aa:bb:cc:34:e5:44"
                        }
                    ]
                    }
                },
                "dhcpAddress": {
                    "routePreference": 3,
                    "vendorClassIdentifier": "aaa 1212 bbbb",
                    "reachabilityMonitor": {
                    "icmp": "True",
                    "interval": 1,
                    "threshold": 2
                    }
                    
                }
                }
        ]
        }
}
        
    