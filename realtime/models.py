"""
Pydantic models for FastAPI real-time service.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MatchEvent(BaseModel):
    """Match event model."""
    id: str
    event_type: str
    minute: int
    player_name: str
    team_name: str
    description: Optional[str] = None


class LiveMatchState(BaseModel):
    """Live match state model."""
    match_id: str
    current_minute: int
    home_score: int
    away_score: int
    possession: dict
    momentum: str
    last_events: List[dict] = []
    attacks: List[dict] = []
    dangerous_attacks: List[dict] = []


class PollResult(BaseModel):
    """Poll result model."""
    poll_id: str
    total_votes: int
    results: List[dict]


class WebSocketMessage(BaseModel):
    """Generic WebSocket message."""
    type: str
    data: Optional[dict] = None
    timestamp: Optional[str] = None