from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas import booking as booking_schema
from app.models.user import User
from app.services.gds_service import GDSService
from app.services.ai_service import AITravelService

router = APIRouter()
gds_service = GDSService()
ai_service = AITravelService()

@router.get("/search/flights")
async def search_flights(
    origin: str,
    destination: str,
    departure_date: datetime,
    return_date: Optional[datetime] = None,
    passengers: int = 1,
    cabin_class: str = "economy",
    current_user: User = Depends(get_current_user)
):
    flights = await gds_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        passengers=passengers,
        cabin_class=cabin_class
    )
    return flights

@router.get("/search/hotels")
async def search_hotels(
    location: str,
    check_in: datetime,
    check_out: datetime,
    guests: int = 1,
    rooms: int = 1,
    current_user: User = Depends(get_current_user)
):
    hotels = await gds_service.search_hotels(
        location=location,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        rooms=rooms
    )
    return hotels

@router.post("/book", response_model=booking_schema.Booking)
async def create_booking(
    *,
    db: Session = Depends(get_db),
    booking_in: booking_schema.BookingCreate,
    current_user: User = Depends(get_current_user)
):
    # Book through GDS
    booking_result = await gds_service.book_service(
        service_type=booking_in.booking_type,
        service_id=booking_in.service_id,
        booking_details=booking_in.dict()
    )
    
    if "error" in booking_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=booking_result["error"]
        )
    
    # Create booking record
    booking = crud_booking.create_with_user(
        db=db,
        obj_in=booking_in,
        user_id=current_user.id,
        booking_reference=booking_result["booking_reference"]
    )
    return booking

@router.get("/recommendations")
async def get_recommendations(
    destination: Optional[str] = None,
    budget: Optional[float] = None,
    travel_dates: Optional[List[datetime]] = None,
    current_user: User = Depends(get_current_user)
):
    recommendations = await ai_service.generate_travel_recommendations(
        user_preferences=current_user.travel_preferences,
        travel_history=current_user.booking_history,
        constraints={
            "destination": destination,
            "budget": budget,
            "travel_dates": travel_dates
        }
    )
    return recommendations
