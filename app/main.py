from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

MICROSERVICE_LINK = "https://appbox.qatar.cmu.edu/313-teams/team_name/"


MENTORS = {
    "1": "Seckhen",
    "2": "Aadi",
    "3": "Steve",
    "4": "Seckhen",
    "5": "Aadi",
    "6": "Steve",
}

@app.get("/team_info/{team_id}")
def get_team_info(team_id: str):
    if not team_id:
        raise HTTPException(status_code=404, detail="Missing team id")

    team_id = team_id.strip().lower()  

    try:
        response = requests.get(MICROSERVICE_LINK + team_id, timeout=5)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Could not reach core team service: {e}")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Team not found in core service")
    if not response.ok:
        raise HTTPException(status_code=502, detail=f"Core team service error: {response.text}")

    try:
        data = response.json()
        print(data)  #
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid JSON from core service")

    team_name = data.get("team_name")
    if not team_name:
        raise HTTPException(status_code=502, detail="Core service response missing 'team_name'")

    mentor = MENTORS.get(team_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Invalid team id")


    try:
        team_id_val = int(team_id)
    except ValueError:
        team_id_val = team_id

    return {
        "team_id": team_id_val,
        "team_name": team_name,  
        "mentor": mentor
    }
