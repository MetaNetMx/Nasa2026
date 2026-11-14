import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pathlib import Path
from clinical_engine import AstronautHealthEngine

app = FastAPI(
    title="ASTRONOVA Astronaut Health Decision Support API",
    description="Edge-autonomous clinical evaluation engine for deep space exploration missions.",
    version="2.0.0"
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class TelemetryPayload(BaseModel):
    visual_acuity_logmar: float = Field(default=0.05, description="Visual acuity LogMAR (0.0 = 20/20)")
    intraocular_pressure_mmhg: float = Field(default=17.5, description="Intraocular pressure (mmHg)")
    optic_disc_elevation_um: float = Field(default=140.0, description="Optic disc elevation (microns)")
    days_in_microgravity: int = Field(default=120, description="Cumulative days in microgravity")
    cumulative_dose_mgy: float = Field(default=95.0, description="Cumulative radiation dose (mGy)")
    daily_ambient_rate_ugy_hr: float = Field(default=65.0, description="Ambient radiation flux (uGy/hr)")
    spe_alert: bool = Field(default=False, description="Solar Particle Event alert flag")
    resting_hr_bpm: float = Field(default=68.0, description="Resting heart rate (bpm)")
    orthostatic_drop_mmhg: float = Field(default=12.0, description="Systolic blood pressure drop upon standing")
    hrv_rmssd_ms: float = Field(default=38.0, description="Heart rate variability RMSSD (ms)")
    daily_exercise_hours: float = Field(default=2.2, description="Daily ARED/CEVIS exercise hours")
    sleep_hours: float = Field(default=6.8, description="Sleep duration (hours)")
    sleep_efficiency_percent: float = Field(default=84.0, description="Sleep actigraphy efficiency (%)")
    cognitive_reaction_time_ms: float = Field(default=255.0, description="PVT cognitive reaction time (ms)")
    cabin_pco2_mmhg: float = Field(default=1.8, description="Cabin carbon dioxide partial pressure (mmHg)")

@app.get("/")
def get_dashboard():
    """Serve the interactive visual dashboard."""
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/api/evaluate")
def evaluate_crew_telemetry(payload: TelemetryPayload):
    """Execute autonomous NASA 5-hazard clinical assessment."""
    return AstronautHealthEngine.full_astronaut_assessment(payload.model_dump())

@app.get("/api/health")
def healthcheck():
    return {"status": "healthy", "system": "ASTRONOVA Medical Engine", "flight_mode": "Autonomous Edge"}

if __name__ == "__main__":
    print("Launching ASTRONOVA Medical Decision Support System on http://localhost:8050...")
    uvicorn.run(app, host="127.0.0.1", port=8050)
