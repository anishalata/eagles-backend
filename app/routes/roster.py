from fastapi import APIRouter
from app.services.roster_api import get_eagles_roster

router = APIRouter()

@router.get("/eagles-roster")
def eagles_roster():
    roster_data = get_eagles_roster()
    return roster_data  # not print()