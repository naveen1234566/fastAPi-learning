"""
File: notification.py
Path: /app/routers/notification.py
Description: Definition of Fields used on model classes attributes.
CreatedAt: 012/03/2023
"""

from fastapi import APIRouter, status, Response
from ..database import notification
from ..models.notification import Notification
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils import get_time, get_uuid


router = APIRouter()

""" Create a new templete profile in the database."""
@router.post('/Notification', status_code=status.HTTP_201_CREATED, summary="Create an Notifications", response_description="Create an Notifications with all the information")
def create(notifications:Notification):
    try:

        notifications = notifications.dict()
        notifications["created"] = notifications["updated"] = get_time()
        notifications["_id"] = get_uuid()
        
        if (notification.find_one({"rulename":notifications["rulename"]})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":"Notifications name already exists"}))

        # print(notifications["communicationDetails"]["emailConfiguration"]["toAddress"])
        # print(notifications["conditions"][0])
        
        if len(notifications["conditions"][0]) != len(set(notifications["conditions"][0])):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch conditionsName - ({notifications["conditions"][1]})'}))

        if len(notifications["conditions"][0]["conditionName"]) == len(set(notifications["conditions"][0]["conditionName"])):
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"details":f'Mismatch conditionsname - ({notifications["conditions"][0]})'}))
        
        try:
            results = notification.insert_one(notifications)
            if results.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail":"Notifications has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail":str(e)}))
        
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(e)}))
    
""" Retrieve all notification profiles in the database """    
@router.get('/Notification/notification', status_code=status.HTTP_200_OK, summary= "Get all notification")
def read_all(page:int=1, limit:int=25):
    try:
        
        if not list(notification.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"NO DATA FOUND", "notification":list(notification.find())}))
        
        page = (page - 1) * limit
        getnotification = list(notification.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total": notification.count_documents({}), "notification":getnotification}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))
    
""" Retrieve a Notification profile with a matching ID """
@router.get('/Notification/{notificationId}', status_code=status.HTTP_200_OK, summary="Get an Notification")
def get_an_templete(notificationId: str):
    try:
        
        if (notificationId := notification.find_one({"_id":notificationId})) is not None:
            return JSONResponse(content=jsonable_encoder({'notification':notificationId}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Notification with Id ({notificationId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))

"""Update a person by giving only the fields to update"""    
@router.put('/Notification/{notificationId}', status_code=status.HTTP_200_OK)
async def update_user(notifications:Notification, notificationId: str):
    try:
       
        notifications = notifications.dict()
        notifications["updated"] = get_time()
        if len(notifications) >= 1:
            update_result = notification.update_one({"_id": notificationId}, {"$set": notifications})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Notification with ID ({notificationId}) not found"}))

        if (
            existing_notification := notification.find_one({"_id": notificationId})
        ) is not None:
           
            return JSONResponse(content=jsonable_encoder({"notifications": existing_notification}))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"Notification with ID ({notificationId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))
    
""" Delete a interface given its a notificationId """
@router.delete('/Notification/{notificationId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_interface(notificationId: str, response:Response):
    try:
        notifications = notification.delete_one({"_id":notificationId})
        
        if notifications.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail":"Notification has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail":f"Notification with ID ({notificationId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail":str(e)}))  


