import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from schemas import Announcement, Event
from database import create_document, get_documents, db

app = FastAPI(title="SMAN 1 Kertasari API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "SMAN 1 Kertasari API", "status": "ok"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Announcements endpoints
@app.post("/api/announcements", response_model=dict)
def create_announcement(announcement: Announcement):
    try:
        data = announcement.model_dump()
        if not data.get("date"):
            data["date"] = datetime.utcnow()
        inserted_id = create_document("announcement", data)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/announcements")
def list_announcements(limit: Optional[int] = 10):
    try:
        docs = get_documents("announcement", {}, limit)
        # convert ObjectId and datetime if needed
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
            if isinstance(d.get("date"), datetime):
                d["date"] = d["date"].isoformat()
            if isinstance(d.get("created_at"), datetime):
                d["created_at"] = d["created_at"].isoformat()
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Events endpoints
@app.post("/api/events", response_model=dict)
def create_event(event: Event):
    try:
        data = event.model_dump()
        inserted_id = create_document("event", data)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events")
def list_events(limit: Optional[int] = 10):
    try:
        docs = get_documents("event", {}, limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
            for key in ["start_date", "end_date", "created_at", "updated_at"]:
                if isinstance(d.get(key), datetime):
                    d[key] = d[key].isoformat()
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
