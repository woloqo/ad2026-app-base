from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI ()

# In - memory database for our Agenda
agenda = {}
current_id = 1
class Contact (BaseModel) :
    name : str
    phone : str

@app.get("/")
def read_root () :
    return {"message": "Welcome to the Agenda API"}

@app.post("/contacts/")
def create_contact(contact: Contact):
    global current_id
    agenda[current_id] = contact.dict()
    current_id += 1
    return {"id": current_id-1, **contact.dict()}

@app.get("/contacts/")
def read_contacts () :
    return {"count": len(agenda), "contacts": agenda }

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: Contact):
    if contact_id not in agenda :
        raise HTTPException(status_code=404, detail="Contact not found")
    agenda[contact_id] = contact.dict()
    return {"id": contact_id, **contact.dict()}

@app.delete("/contacts/{contact_id}")
def delete_contact (contact_id: int):
    if contact_id not in agenda :
        raise HTTPException (status_code=404, detail="Contact not found")
    del agenda[contact_id]
    return{"status": "deleted", "id": contact_id}