from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Arisyn backend running fine 🚀"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Save file
    contents = await file.read()
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    # Here you would do audio analysis logic
    result = {"vocal_chain": "Simulated FX settings example"}

    # Clean up file
    os.remove(file_path)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)