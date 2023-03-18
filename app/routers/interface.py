"""
File: interface.py
Path: /app/routers/interface.py
Description: Definition of routes
CreatedAt: 01/03/2023
"""

# # Installed # #
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# # Package # #
from ..models.interface import Interface
from ..database import ethernet
from ..utils import get_time, get_uuid

router = APIRouter()

 
""" Create a new interface profile in the database."""
@router.post('/Ethernet/interface', status_code=status.HTTP_201_CREATED, summary="Create an interface", response_description="Create an interface with all the information")
async def create(interface:Interface):
    try:
        if(ethernet.find_one({"nativeVlanId":interface.nativeVlanId})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder({"detail":"nativeVlanId already exists"}))
        
        interface = interface.dict()
        interface["created"] = interface["updated"] = get_time()
        interface["_id"] = get_uuid()
        try:
            result = ethernet.insert_one(interface)
            if result.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"Interface has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Retrive all interface profiles in the database."""
@router.get('/Ethernet/interface', status_code=status.HTTP_200_OK, summary="Get all interface")
async def get_all(page:int=1, limit:int=10):
    try:
        if not list(ethernet.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"No Data Found", "interface":list(ethernet.find())}))
        
        page = (page - 1) * limit
        interface = list(ethernet.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total":ethernet.count_documents({}), "interface":interface}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(({"detail":str(e)})))
    

""" Retrieve a interface profile with a matching ID. """     
@router.get('/Ethernet/{interfaceId}', status_code=status.HTTP_200_OK)
async def get_an_interface(interfaceId: str):
    try:
        if (interfaceId := ethernet.find_one({"_id":interfaceId})) is not None:
            return JSONResponse(content=jsonable_encoder({"interface":interfaceId}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Interface with Id ({interfaceId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
"""Update a person by giving only the fields to update"""
@router.put("/Ethernet/{interfaceId}", status_code=status.HTTP_200_OK)
async def update_user(interface:Interface, interfaceId: str):
    try:
        
        interface = interface.dict()
        interface["updated"] = get_time()
        if len(interface) >= 1:
            update_result = ethernet.update_one({"_id": interfaceId}, {"$set": interface})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Interface with ID ({interfaceId}) not found"}))

        if (
            existing_interface := ethernet.find_one({"_id": interfaceId})
        ) is not None:
            
            return JSONResponse(content=jsonable_encoder({"interface": existing_interface}))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Interface with ID ({interfaceId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Delete a interface given its a interfaceId """
@router.delete("/Ethernet/{interfaceId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interface(interfaceId: str, response:Response):
    try:
        interface = ethernet.delete_one({"_id":interfaceId})
        if interface.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"Interface has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Interface with ID ({interfaceId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))