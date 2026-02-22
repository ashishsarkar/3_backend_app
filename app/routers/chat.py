"""Chat router — keyword replies + MongoDB chat history persistence."""

from datetime import datetime
from fastapi import APIRouter
from app.mongodb import chat_collection
from app.schemas.mongo import ChatRequest

router = APIRouter()


def _generate_reply(msg: str) -> str:
    m = msg.strip().lower()
    if not m:
        return "How can I help you today?"
    if any(w in m for w in ("hello", "hi", "hey")):
        return "Hello! I'm your booking assistant. I can help you search for flights, hotels, or create a bundle. What would you like to do?"
    if any(w in m for w in ("flight", "fly")):
        return "You can search flights from the home page. Enter your origin and destination to see available flights."
    if any(w in m for w in ("hotel", "stay")):
        return "You can search hotels by location. Use the hotel search to find available options."
    if any(w in m for w in ("book", "reserv")):
        return "To book, first search for a flight or hotel, select your choice, and proceed to checkout."
    if "cancel" in m:
        return "You can cancel bookings from the My Bookings page. Open it from the menu."
    if any(w in m for w in ("wallet", "credit")):
        return "Check your wallet balance in the Profile page. You can top up credits there."
    if "alert" in m or "price" in m:
        return "You can set price alerts from the Price Alerts page. I'll notify you when prices drop below your target."
    if "help" in m:
        return "I can help with: searching flights, searching hotels, bookings, cancellations, price alerts, and wallet. What do you need?"
    return "I'm here to help with flights and hotels. Try asking about booking, searching, or cancellations."


@router.post("/")
async def chat(body: ChatRequest):
    reply = _generate_reply(body.message)
    now = datetime.utcnow()
    col = chat_collection()

    # Persist both turns to MongoDB
    await col.insert_many([
        {"session_id": body.session_id, "role": "user", "text": body.message, "timestamp": now},
        {"session_id": body.session_id, "role": "assistant", "text": reply, "timestamp": now},
    ])

    return {"reply": reply, "message": reply}


@router.get("/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    """Retrieve the last N messages for a session."""
    col = chat_collection()
    cursor = col.find(
        {"session_id": session_id},
        {"_id": 0, "session_id": 0},
    ).sort("timestamp", 1).limit(limit)
    messages = await cursor.to_list(length=limit)
    return {"messages": messages}


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """Clear all chat history for a session."""
    col = chat_collection()
    result = await col.delete_many({"session_id": session_id})
    return {"deleted": result.deleted_count}
