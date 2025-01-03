from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
from app.core.config import get_settings
import json

settings = get_settings()

class GDSService:
    def __init__(self):
        self.api_key = settings.GDS_API_KEY
        self.base_url = "https://api.gds-provider.com/v1"  # Replace with actual GDS API endpoint
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: Optional[datetime] = None,
        passengers: int = 1,
        cabin_class: str = "economy"
    ) -> List[Dict[str, Any]]:
        """
        Search for available flights using the GDS API.
        """
        endpoint = f"{self.base_url}/flights/search"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date.isoformat(),
            "passengers": passengers,
            "cabin_class": cabin_class
        }
        
        if return_date:
            params["return_date"] = return_date.isoformat()

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return []

    async def search_hotels(
        self,
        location: str,
        check_in: datetime,
        check_out: datetime,
        guests: int = 1,
        rooms: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search for available hotels using the GDS API.
        """
        endpoint = f"{self.base_url}/hotels/search"
        params = {
            "location": location,
            "check_in": check_in.isoformat(),
            "check_out": check_out.isoformat(),
            "guests": guests,
            "rooms": rooms
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return []

    async def search_car_rentals(
        self,
        location: str,
        pickup_date: datetime,
        return_date: datetime,
        vehicle_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for available car rentals using the GDS API.
        """
        endpoint = f"{self.base_url}/cars/search"
        params = {
            "location": location,
            "pickup_date": pickup_date.isoformat(),
            "return_date": return_date.isoformat()
        }
        
        if vehicle_type:
            params["vehicle_type"] = vehicle_type

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return []

    async def search_cruises(
        self,
        departure_port: str,
        destination: str,
        departure_date: datetime,
        duration: int,
        passengers: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Search for available cruises using the GDS API.
        """
        endpoint = f"{self.base_url}/cruises/search"
        params = {
            "departure_port": departure_port,
            "destination": destination,
            "departure_date": departure_date.isoformat(),
            "duration": duration,
            "passengers": passengers
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return []

    async def book_service(
        self,
        service_type: str,
        service_id: str,
        booking_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Book a travel service (flight, hotel, car, etc.) through the GDS API.
        """
        endpoint = f"{self.base_url}/{service_type}/book"
        payload = {
            "service_id": service_id,
            **booking_details
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                return {"error": f"Booking failed with status {response.status}"}

    async def get_live_prices(
        self,
        service_type: str,
        service_ids: List[str]
    ) -> Dict[str, float]:
        """
        Get real-time prices for specified services.
        """
        endpoint = f"{self.base_url}/{service_type}/prices"
        params = {
            "service_ids": ",".join(service_ids)
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return {}
