"""
File: user.py
Path: /app/routers/user.py
Description: Definition of routes
CreatedAt: 01/03/2023
"""
# # Installed # #
from fastapi import APIRouter, Response, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# # Package # #
from ..models.user import User
from ..database import users
from ..utils import get_time, get_uuid

router = APIRouter()


""" Create a new user profile in the database."""
@router.post("/user", status_code=status.HTTP_201_CREATED, summary="Create an user", response_description="Create an user with all the information")
async def create(user:User):
    """
    Create an item with all the information:

    - **firstName**: required
    - **lastName**: required
    - **email**: required and unique
    - **phone**: required and unique
    - **password**: required
    """
    try:
        if (users.find_one({"email": user.email})) is not None:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder({"detail": "Email already exists"}))

        user = user.dict()
        user["created"] = user["updated"] = get_time()
        user["_id"] = get_uuid()
        try:
            result = users.insert_one(user)
            if result.acknowledged == True:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({"detail": "User has been created successfully"}))
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=jsonable_encoder({"detail": str(e)}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))


""" Retrieve all user profiles in the database."""
@router.get('/user', status_code=status.HTTP_200_OK)
async def get_all_user(page: int = 1, limit: int = 10):
    try:
        if not list(users.find()):
            return JSONResponse(content=jsonable_encoder({"detail":"No Data Found", "user": list(users.find())}))

        page = (page - 1) * limit
        userProfile = list(users.find().limit(limit).skip(page))
        return JSONResponse(content=jsonable_encoder({"total":users.count_documents({}), "user": userProfile}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))

""" Retrieve a user profile with a matching ID. """
@router.get('/{userId}', status_code=status.HTTP_200_OK)
async def get_user(userId: str):
    try:
        if (user := users.find_one({"_id": userId})) is not None:
            return JSONResponse(content=jsonable_encoder({"user": user}))
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"User with ID ({userId}) not found"}))

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))

"""Update a person by giving only the fields to update"""
@router.put("/{userId}", status_code=status.HTTP_200_OK)
async def update_user(user:User, userId: str):
    try:
        # user = {k: v for k, v in user.dict().items() if v is not None}
        user = user.dict()
        user["updated"] = get_time()
        if len(user) >= 1:
            update_result = users.update_one({"_id": userId}, {"$set": user})
        if update_result.modified_count == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"User with ID ({userId}) not found"}))

        if (
            existing_user := users.find_one({"_id": userId})
        ) is not None:
            #return existing_user
            return JSONResponse(content=jsonable_encoder({"user": existing_user}))

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"User with ID ({userId}) not found"}))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))

"""Delete a user given its user id"""
@router.delete("/{userId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(userId: str, response: Response):
    try:
        delete_user = users.delete_one({"_id": userId})
        if delete_user.deleted_count == 1:
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content=jsonable_encoder({"detail": "User has been deleted successfully"}))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=jsonable_encoder({"detail": f"User with ID ({userId}) not found"}))
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=jsonable_encoder({"detail": str(e)}))