from typing import List, Dict, Any
import openai
from app.core.config import get_settings
from datetime import datetime
import json

settings = get_settings()

class AITravelService:
    def __init__(self):
        self.api_key = settings.AI_SERVICE_KEY
        openai.api_key = self.api_key

    async def generate_travel_recommendations(
        self,
        user_preferences: Dict[str, Any],
        travel_history: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized travel recommendations based on user preferences and history.
        """
        # Construct the prompt for the AI model
        prompt = self._construct_recommendation_prompt(
            user_preferences,
            travel_history,
            constraints
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a travel expert AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse and structure the AI response
            recommendations = self._parse_ai_recommendations(response.choices[0].message.content)
            return recommendations
        
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []

    def analyze_user_preferences(
        self,
        search_history: List[Dict[str, Any]],
        booking_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze user's search and booking history to understand preferences.
        """
        preferences = {
            "preferred_destinations": [],
            "budget_range": {},
            "accommodation_preferences": [],
            "travel_style": [],
            "typical_duration": None,
            "seasonal_preferences": []
        }

        # Analyze booking history
        for booking in booking_history:
            self._update_preferences_from_booking(preferences, booking)

        # Analyze search history
        for search in search_history:
            self._update_preferences_from_search(preferences, search)

        return preferences

    def _construct_recommendation_prompt(
        self,
        user_preferences: Dict[str, Any],
        travel_history: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> str:
        """
        Construct a detailed prompt for the AI model.
        """
        return f"""
        Based on the following information, provide personalized travel recommendations:

        User Preferences:
        {json.dumps(user_preferences, indent=2)}

        Travel History:
        {json.dumps(travel_history, indent=2)}

        Constraints:
        {json.dumps(constraints, indent=2)}

        Please provide recommendations in the following format:
        1. Destination name
        2. Why it matches the user's preferences
        3. Best time to visit
        4. Estimated budget
        5. Suggested activities
        """

    def _parse_ai_recommendations(self, ai_response: str) -> List[Dict[str, Any]]:
        """
        Parse and structure the AI model's response into a standardized format.
        """
        try:
            # Implementation would depend on the actual response format
            # This is a placeholder structure
            recommendations = []
            # Parse the AI response and structure it
            return recommendations
        except Exception as e:
            print(f"Error parsing AI recommendations: {str(e)}")
            return []

    def _update_preferences_from_booking(
        self,
        preferences: Dict[str, Any],
        booking: Dict[str, Any]
    ) -> None:
        """
        Update user preferences based on a booking entry.
        """
        if "destination" in booking:
            preferences["preferred_destinations"].append(booking["destination"])
        
        if "total_cost" in booking:
            # Update budget range logic
            pass

    def _update_preferences_from_search(
        self,
        preferences: Dict[str, Any],
        search: Dict[str, Any]
    ) -> None:
        """
        Update user preferences based on a search entry.
        """
        if "searched_destination" in search:
            preferences["preferred_destinations"].append(search["searched_destination"])
        
        # Add more preference updates based on search patterns
