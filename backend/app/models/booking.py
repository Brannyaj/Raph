from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum, Float
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class BookingType(str, enum.Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    CAR = "car"
    HOME_RENTAL = "home_rental"
    CRUISE = "cruise"
    PRIVATE_JET = "private_jet"
    WEDDING_VENUE = "wedding_venue"
    HONEYMOON_PACKAGE = "honeymoon_package"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    booking_type = Column(Enum(BookingType))
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    
    # Booking details
    booking_reference = Column(String, unique=True)
    provider_reference = Column(String)
    booking_data = Column(JSON)  # Stores specific details based on booking type
    
    # Dates
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Financial
    total_cost = Column(Float)
    currency = Column(String, default="USD")
    payment_status = Column(String)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(String)
    
    # AI recommendations that led to this booking
    recommendation_data = Column(JSON)
