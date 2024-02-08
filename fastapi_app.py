from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException,Depends, Header
from fastapi.responses import JSONResponse
from add_documents import add_documents_from_pdf_bytes
import os
import sqlite3
import uvicorn
from utils import load_config
load_dotenv()
config = load_config()
app = FastAPI()

def get_api_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv("FASTAPI_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/metrics/")
def get_metrics(x_api_key: str = Depends(get_api_key)):
    conn = sqlite3.connect(config["sqlite"]["db_path"])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('SELECT * FROM telemetry WHERE timestamp >= ?', (thirty_days_ago_str,))
    rows = cursor.fetchall()

    metrics = [dict(row) for row in rows]

    conn.close()
    return metrics


@app.post("/upload/")
async def upload_file(files: list[UploadFile] = File(...), api_key: str = Depends(get_api_key)):
    pdf_bytes_list = []
    for file in files:
        if file.content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

        contents = await file.read()
        pdf_bytes_list.append(contents)
        await file.close()
    
    add_documents_from_pdf_bytes(pdf_bytes_list)
    return JSONResponse(status_code=200, content={"message": "Documents added successfully."})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

