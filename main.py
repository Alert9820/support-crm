from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import CreateTicket, UpdateTicket
from database import tickets_collection, notes_collection
from datetime import datetime, timezone
from bson import ObjectId
import uuid

app = FastAPI()

# ─── Helper ───────────────────────────────────────
def format_ticket(ticket):
    ticket["_id"] = str(ticket["_id"])
    if "created_at" in ticket:
        ticket["created_at"] = ticket["created_at"].isoformat()
    if "updated_at" in ticket:
        ticket["updated_at"] = ticket["updated_at"].isoformat()
    return ticket

# ─── Frontend ─────────────────────────────────────
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# ─── CREATE TICKET ────────────────────────────────
@app.post("/api/tickets")
def create_ticket(data: CreateTicket):
    ticket = {
        "ticket_id": "TKT-" + str(uuid.uuid4())[:8].upper(),
        "customer_name": data.customer_name,
        "customer_email": data.customer_email,
        "subject": data.subject,
        "description": data.description,
        "status": "Open",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    tickets_collection.insert_one(ticket)
    return {"ticket_id": ticket["ticket_id"], "created_at": ticket["created_at"].isoformat()}

# ─── GET ALL TICKETS ──────────────────────────────
@app.get("/api/tickets")
def get_tickets(
    status: str = Query(None),
    search: str = Query(None)
):
    query = {}

    if status:
        query["status"] = status

    if search:
        query["$or"] = [
            {"customer_name": {"$regex": search, "$options": "i"}},
            {"customer_email": {"$regex": search, "$options": "i"}},
            {"ticket_id": {"$regex": search, "$options": "i"}},
            {"subject": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    tickets = list(tickets_collection.find(query).sort("created_at", -1))
    return [format_ticket(t) for t in tickets]

# ─── GET SINGLE TICKET ────────────────────────────
@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    ticket = tickets_collection.find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket = format_ticket(ticket)

    notes = list(notes_collection.find({"ticket_id": ticket_id}).sort("created_at", -1))
    for note in notes:
        note["_id"] = str(note["_id"])
        note["created_at"] = note["created_at"].isoformat()

    ticket["notes"] = notes
    return ticket

# ─── UPDATE TICKET ────────────────────────────────
@app.put("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, data: UpdateTicket):
    ticket = tickets_collection.find_one({"ticket_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = {"updated_at": datetime.now(timezone.utc)}

    if data.status:
        allowed = ["Open", "In Progress", "Closed"]
        if data.status not in allowed:
            raise HTTPException(status_code=400, detail="Invalid status")
        update_data["status"] = data.status

    tickets_collection.update_one(
        {"ticket_id": ticket_id},
        {"$set": update_data}
    )

    if data.note:
        notes_collection.insert_one({
            "ticket_id": ticket_id,
            "note_text": data.note,
            "created_at": datetime.now(timezone.utc)
        })

    return {"success": True, "updated_at": update_data["updated_at"].isoformat()}
