from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import base64
import uuid
from datetime import datetime
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="DevOps Tools API",
    description="Simple utility API for demonstrations",
    version="1.0.0"
)

class TextInput(BaseModel):
    text: str

class URLInput(BaseModel):
    url: str

urls = {}

@app.get("/")
def home():
    return {"message": "Welcome to the DevOps Tools API!",
        "docs_url": "/docs"}

@app.get("/health")
def health():
    return{"status": "healthy",
           "timestamp": datetime.now().isoformat()
           }

@app.post("/hash/md5")
def hash_md5(data: TextInput):
    result = hashlib.md5(data.text.encode()).hexdigest()
    return {"input": data.text, "md5": result}

@app.post("/encode/base64")
def encode_base64(data: TextInput):
    result = base64.b64encode(data.text.encode()).decode()
    return {"input": data.text, "base64": result}

@app.post("/decode/base64")
def decode_base64(data: TextInput):
    try:
        result = base64.b64decode(data.text).decode()
        return {"input": data.text, "decoded": result}
    except Exception as e:
        raise HTTPException(400, f"Invalid base64: {str(e)}")
    
@app.post("/shorten")
def shorten_url(data: URLInput):
    code = str(uuid.uuid4())[:8]
    urls[code] = data.url
    return {"message": "associated UUID with url",
            "uuid": code 
            }

@app.get("/s/{code}")
def get_url(code: str):
    if code not in urls:
        raise HTTPException(404, "URL not found")
    long_url = urls[code]    
    return{"url": long_url}

@app.get("/stats")
def stats():
    return {
        "total_urls": len(urls),
        "total_endpoints": 9
    }