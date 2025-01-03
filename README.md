# Raph - AI-Powered Travel Planning Platform

Raph is an innovative AI-powered travel planning and booking software that revolutionizes the way people plan and book their travels. It serves as a comprehensive replacement for traditional travel agents while providing personalized, data-driven recommendations and real-time booking capabilities.

## Features

- AI-powered personalized travel recommendations
- Real-time booking integration with Global Distribution System (GDS)
- Live pricing for:
  - Flights
  - Hotels
  - Car rentals
  - Private home rentals
  - Boat cruises and yacht rentals
  - Private jet charters
  - Honeymoon destinations
  - Wedding venues
- User preference learning and behavior analysis
- 24/7 real-time support and assistance
- Intelligent travel itinerary planning

## Technical Requirements

- Python 3.9+
- FastAPI
- PostgreSQL
- Redis
- React (Frontend)
- Docker

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run the development server: `uvicorn main:app --reload`

## Project Structure

```
raph/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   └── main.py
├── frontend/
│   ├── public/
│   └── src/
├── docker/
└── docs/
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/raph
REDIS_URL=redis://localhost:6379
GDS_API_KEY=your_gds_api_key
AI_SERVICE_KEY=your_ai_service_key
```

## License

MIT License
