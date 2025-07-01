from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment, effects
import uuid, os, datetime
from supabase import create_client

# --- Supabase setup ---
supabase_url = "https://qknvfjmxtbbyipjkmdde.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrbnZmam14dGJ5aXBqa21kZGUiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTc1MTMzNzA0NCwiZXhwIjoyMDY2OTEzMDQ0fQ.a-zRXOVGAF9kNtMTfPmymHMlShBPmkwvyotpGu6H2aU"
supabase = create_client(supabase_url, supabase_key)

app = FastAPI()

def upload_to_supabase(file_path, supabase_filename):
    with open(file_path, "rb") as f:
        res = supabase.storage.from_("previews").upload(path=f"processed/{supabase_filename}", file=f)
        if res.get("error"):
            raise Exception(f"Upload failed: {res['error']['message']}")
        public_url = supabase.storage.from_("previews").get_public_url(f"processed/{supabase_filename}")
        return public_url

def save_soundcard_row(audio_url, fx_chain, artist_match):
    new_id = str(uuid.uuid4())
    data = {
        "id": new_id,
        "artist_match": artist_match,
        "fx_chain": fx_chain,
        "audio_url": audio_url,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    supabase.table("SoundCards").insert(data).execute()
    return new_id

@app.post("/analyze")
async def analyze_vocal(file: UploadFile = File(...)):
    file_location = f"temp_{uuid.uuid4()}.wav"
    with open(file_location, "wb+") as f:
        f.write(await file.read())

    audio = AudioSegment.from_file(file_location)

    # --- Real FX ---
    audio = effects.high_pass_filter(audio, cutoff=2000)
    audio = effects.normalize(audio)
    audio = audio + 3
    reverb = audio[-500:].fade_out(300)
    audio = audio.overlay(reverb)

    processed_file_name = f"processed_{uuid.uuid4()}.wav"
    audio.export(processed_file_name, format="wav")

    # Upload to Supabase
    audio_url = upload_to_supabase(processed_file_name, processed_file_name)

    # Example FX metadata
    fx_chain = {
        "Auto-Tune": "35% correction, Key: C Minor",
        "EQ": "+3 dB @ 2.5 kHz",
        "Compression": "4:1 Ratio, +3 dB gain",
        "Reverb": "1.8 sec decay",
        "Delay": "1/8th note"
    }
    artist_match = {
        "name": "Billie Eilish",
        "match_pct": 92,
        "confidence": 98
    }

    # Save DB row
    save_soundcard_row(audio_url, fx_chain, artist_match)

    os.remove(file_location)
    os.remove(processed_file_name)

    return JSONResponse({
        "message": "Processing complete",
        "audio_url": audio_url,
        "fx_chain": fx_chain,
        "artist_match": artist_match
    })