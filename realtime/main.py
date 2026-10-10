"""
FastAPI real-time service for WebSocket connections.
This runs as a separate service alongside Django.
"""
import asyncio
import json
from typing import Dict, Set, Optional
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis
from pydantic import BaseModel

app = FastAPI(
    title="LiveScore Real-Time Service",
    version="1.0.0",
    description="WebSocket service for live sports updates"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client: Optional[aioredis.Redis] = None

# Connection managers for different channels
class ConnectionManager:
    """Manages WebSocket connections grouped by channel."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)
    
    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
            if not self.active_connections[channel]:
                del self.active_connections[channel]
    
    async def broadcast(self, channel: str, message: dict):
        """Send message to all connections in a channel."""
        if channel in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    dead_connections.add(connection)
                except Exception:
                    dead_connections.add(connection)
            
            # Clean dead connections
            for conn in dead_connections:
                self.disconnect(conn, channel)
    
    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception:
            pass
    
    def get_channel_stats(self):
        """Get connection statistics."""
        return {
            channel: len(connections)
            for channel, connections in self.active_connections.items()
        }


manager = ConnectionManager()


@app.on_event("startup")
async def startup():
    """Initialize Redis connection and start listener."""
    global redis_client
    
    redis_client = aioredis.from_url(
        "redis://127.0.0.1:6379/2",
        encoding="utf-8",
        decode_responses=True
    )
    
    # Start Redis listener task
    asyncio.create_task(redis_listener_task())
    
    print("🚀 FastAPI real-time service started")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    global redis_client
    if redis_client:
        await redis_client.close()
    print("👋 FastAPI real-time service stopped")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "LiveScore Real-Time Service",
        "status": "running",
        "connections": manager.get_channel_stats(),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    redis_status = "connected" if redis_client and await redis_client.ping() else "disconnected"
    return {
        "status": "healthy",
        "redis": redis_status,
        "active_channels": len(manager.active_connections),
        "connections": manager.get_channel_stats(),
    }


@app.websocket("/ws/match/{match_id}")
async def match_websocket(websocket: WebSocket, match_id: str):
    """
    WebSocket endpoint for live match updates.
    Clients connect here to receive real-time match data.
    """
    channel = f"match_{match_id}"
    await manager.connect(websocket, channel)
    
    try:
        # Send initial match data from Redis cache
        if redis_client:
            cached = await redis_client.get(f"cache:match:{match_id}")
            if cached:
                await websocket.send_json({
                    "type": "initial_state",
                    "data": json.loads(cached)
                })
        
        # Keep connection alive and handle client messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.utcnow().isoformat()})
            elif message.get("type") == "subscribe_events":
                # Client wants specific event types
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    except Exception as e:
        manager.disconnect(websocket, channel)
        print(f"WebSocket error for match {match_id}: {e}")


@app.websocket("/ws/matches/live")
async def live_matches_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for all live matches summary.
    """
    channel = "live_matches"
    await manager.connect(websocket, channel)
    
    try:
        # Send initial live matches
        if redis_client:
            cached = await redis_client.get("cache:live_matches")
            if cached:
                await websocket.send_json({
                    "type": "initial_live_matches",
                    "data": json.loads(cached)
                })
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


@app.websocket("/ws/poll/{poll_id}")
async def poll_websocket(websocket: WebSocket, poll_id: str):
    """
    WebSocket endpoint for live poll updates.
    """
    channel = f"poll_{poll_id}"
    await manager.connect(websocket, channel)
    
    try:
        # Send initial poll results
        if redis_client:
            cached = await redis_client.get(f"cache:poll:{poll_id}")
            if cached:
                await websocket.send_json({
                    "type": "initial_poll_results",
                    "data": json.loads(cached)
                })
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


@app.websocket("/ws/competition/{competition_id}")
async def competition_websocket(websocket: WebSocket, competition_id: str):
    """
    WebSocket endpoint for competition-level updates (standings, etc.).
    """
    channel = f"competition_{competition_id}"
    await manager.connect(websocket, channel)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


@app.post("/api/v1/polls/{poll_id}/vote")
async def vote_poll(
    poll_id: str,
    user_id: str = Query(...),
    option_id: str = Query(...)
):
    """
    HTTP endpoint for voting (can be used by mobile apps or as fallback).
    """
    # In production, validate vote and save to database
    # Then publish update to Redis
    
    if redis_client:
        vote_data = {
            "poll_id": poll_id,
            "user_id": user_id,
            "option_id": option_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await redis_client.publish(
            f"poll_{poll_id}",
            json.dumps({"type": "new_vote", "data": vote_data})
        )
    
    return {"status": "accepted", "poll_id": poll_id, "option_id": option_id}


async def redis_listener_task():
    """
    Background task that listens to Redis pub/sub channels
    and forwards messages to WebSocket clients.
    """
    if not redis_client:
        return
    
    pubsub = redis_client.pubsub()
    
    # Subscribe to all relevant patterns
    await pubsub.psubscribe("match_*", "live_matches", "poll_*", "competition_*")
    
    print("📡 Redis listener started - waiting for messages...")
    
    async for message in pubsub.listen():
        if message["type"] == "pmessage":
            try:
                channel = message["channel"]
                data = json.loads(message["data"])
                
                # Forward to WebSocket connections
                await manager.broadcast(channel, data)
                
            except json.JSONDecodeError:
                pass
            except Exception as e:
                print(f"Error processing Redis message: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )