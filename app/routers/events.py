from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import EventCreate, EventOut
from app.dependencies import user_dependency, db_dependency
from app.crud import delete_event, get_event, get_events, create_event, join_event, leave_event, update_event
from sqlalchemy.orm import Session
from app.database_connection import get_db
from dotenv import load_dotenv
from typing import List

load_dotenv() # 載入 .env 檔案

router = APIRouter()

@router.get("/events", response_model=List[EventOut], tags=["Events"])
def list_events(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
    ):
    events = get_events(db, skip=skip, limit=limit)
    return events

@router.get("/events/{event_id}", response_model=EventOut, tags=["Events"])
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    print("hi from get_event_by_id")
    event = get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Event with ID {event_id} not found"
        )
    return event


#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # This handles token extraction automatically

@router.post("/events", response_model=EventOut, tags=["Events"])
def create_new_event(db: db_dependency, current_user: user_dependency, event: EventCreate): #, current_user: User = Depends(get_current_user)
    print("hi from create_new_event")
    #current_user = get_current_user(db, oauth2_scheme)
    #check_organizer_role(current_user)  # 檢查使用者是否是 organizer 待補
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print(f"Current User: {current_user}")
    print(f"Current User id: ", current_user.user_id)
    print(type(current_user.user_id))
    new_event = create_event(db, event, current_user.user_id)
    return new_event


@router.put("/events/{event_id}", response_model=EventOut, tags=["Events"])
def update_current_event(
    event_id: int, 
    event: EventCreate, 
    db: Session = Depends(get_db)
):
    existing_event = get_event(db, event_id=event_id)
    if not existing_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Event with ID {event_id} not found"
        )
    updated_event = update_event(db, event_id, event)
    return updated_event
'''
async def create_new_event(event: EventCreate, db: Session = Depends(get_db)):
    # Manually extract the token using oauth2_scheme
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Create an instance of OAuth2PasswordBearer
    try:
        # Now, simulate extracting the token manually
        token = oauth2_scheme(db)  # This will give you the token from the request header
        print(f"Extracted Token: {token}")
        
        # Manually debug the `get_current_user` function
        current_user = await get_current_user(db, token)  # Pass the token manually to get_current_user function
        print(f"Current User: {current_user}")
        
        if not current_user:
            print("User is unauthorized")
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        new_event = create_event(db, event, current_user.user_id)
        return new_event
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
'''
'''
async def create_new_event(event: EventCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print("hi from create_new_event")

    # Now `token` contains the JWT token from the Authorization header.
    current_user = await get_current_user(db, token)  # Use the `await` to call async function
    print(f"Current User: {current_user}")
    
    if not current_user:
        print("User is unauthorized")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    new_event = create_event(db, event, current_user.user_id)
    return new_event
'''

'''
'''