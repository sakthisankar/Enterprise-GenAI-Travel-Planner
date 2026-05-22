from __future__ import annotations

import asyncio
import logging
import traceback
from datetime import datetime, UTC
from typing import Dict, List

import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from openai_key import OPENAI_API_KEY, GOOGLE_API_KEY

# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(api_key=OPENAI_API_KEY)

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Enterprise GenAI Travel Platform",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ============================================================
# MODEL
# ============================================================

class TravelRequest(BaseModel):

    destination: str

    budget: float = Field(gt=0)

    days: int = Field(gt=0, le=365)

    travel_style: str

    food_preference: str

    transport_mode: str

# ============================================================
# GOOGLE PLACES  (unchanged)
# ============================================================

GOOGLE_PLACES_URL = (
    "https://maps.googleapis.com/maps/api/place/textsearch/json"
)

async def google_places_search(
    query: str,
    limit: int = 5
) -> List[Dict]:

    try:

        params = {
            "query": query,
            "key": GOOGLE_API_KEY
        }

        response = requests.get(
            GOOGLE_PLACES_URL,
            params=params,
            timeout=20
        )

        data = response.json()

        results = []

        for item in data.get("results", [])[:limit]:

            results.append({
                "name":    item.get("name", "N/A"),
                "rating":  item.get("rating", "N/A"),
                "address": item.get("formatted_address", "N/A")
            })

        return results

    except Exception as e:

        logger.error(f"Google API Error: {e}")
        return []

# ============================================================
# AGENTS  (unchanged)
# ============================================================

async def hotel_agent(destination: str):
    return await google_places_search(
        f"best luxury hotels in {destination}", limit=5
    )

async def attraction_agent(destination: str):
    return await google_places_search(
        f"top tourist attractions in {destination}", limit=10
    )

async def food_agent(destination: str):
    return await google_places_search(
        f"best local food restaurants in {destination}", limit=5
    )

# ============================================================
# BUDGET ENGINE  (unchanged)
# ============================================================

BUDGET_PROFILES = {

    "budget": {
        "hotel": 0.30,
        "food": 0.20,
        "transport": 0.15,
        "activities": 0.25,
        "emergency": 0.10,
    },

    "luxury": {
        "hotel": 0.50,
        "food": 0.20,
        "transport": 0.15,
        "activities": 0.10,
        "emergency": 0.05,
    },

    "family": {
        "hotel": 0.38,
        "food": 0.22,
        "transport": 0.15,
        "activities": 0.18,
        "emergency": 0.07,
    },

    "solo": {
        "hotel": 0.32,
        "food": 0.20,
        "transport": 0.18,
        "activities": 0.22,
        "emergency": 0.08,
    }
}

def calculate_budget(
    budget: float,
    days: int,
    style: str
):

    profile = BUDGET_PROFILES.get(
        style.lower(),
        BUDGET_PROFILES["budget"]
    )

    breakdown = {}

    for category, ratio in profile.items():

        total = round(budget * ratio, 2)
        daily = round(total / days, 2)

        breakdown[category] = {
            "total": total,
            "daily": daily
        }

    return breakdown

# ============================================================
# MAIN AI ENGINE
# ============================================================

async def generate_itinerary(req: TravelRequest):

    start_time = datetime.now(UTC)

    hotels, attractions, foods = await asyncio.gather(
        hotel_agent(req.destination),
        attraction_agent(req.destination),
        food_agent(req.destination)
    )

    budget = calculate_budget(
        req.budget,
        req.days,
        req.travel_style
    )

    prompt = f"""
You are a world-class AI travel planner.

Create a premium enterprise-level travel itinerary.

DESTINATION:
{req.destination}

BUDGET:
{req.budget}

DAYS:
{req.days}

TRAVEL STYLE:
{req.travel_style}

FOOD PREFERENCE:
{req.food_preference}

TRANSPORT:
{req.transport_mode}

HOTELS:
{hotels}

ATTRACTIONS:
{attractions}

FOOD OPTIONS:
{foods}

BUDGET BREAKDOWN:
{budget}

Generate:

1. Destination Overview
2. Best Hotels
3. Budget Breakdown
4. Day-by-Day Itinerary
5. Local Foods
6. Transport Strategy
7. Safety Tips
8. Hidden Gems
9. Packing Suggestions
10. Cultural Etiquette
11. Emergency Guidance
12. Best Apps To Use

Professional formatting.
"""

    # --------------------------------------------------------
    # OpenAI Chat Completions API
    # --------------------------------------------------------
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=3500,
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "You are an elite AI travel strategist."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    execution_time = (
        datetime.now(UTC) - start_time
    ).total_seconds()

    logger.info(
        f"Itinerary generated in {execution_time:.2f} seconds"
    )

    # --------------------------------------------------------
    # OpenAI returns response.choices[0].message.content
    # --------------------------------------------------------
    return {
        "destination":      req.destination,
        "generated_at":     datetime.now(UTC).isoformat(),
        "execution_time":   execution_time,
        "itinerary":        response.choices[0].message.content
    }

# ============================================================
# API ROUTE  (unchanged)
# ============================================================

@app.post("/generate-itinerary")
async def generate_api(req: TravelRequest):

    try:

        logger.info(f"Request received: {req.destination}")

        result = await generate_itinerary(req)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "result": result
            }
        )

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

# ============================================================
# ROOT  (unchanged)
# ============================================================

@app.get("/")
def root():
    return {
        "status":  "running",
        "project": "Enterprise Multi-Agent AI Travel Platform"
    }
