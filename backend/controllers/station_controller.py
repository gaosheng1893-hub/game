from fastapi import APIRouter
from services.station_service import StationService

router = APIRouter()

@router.get("/stations")
async def get_stations():
    return StationService.get_all_stations()

@router.get("/stations/{station_id}")
async def get_station(station_id: int):
    return StationService.get_station_by_id(station_id)
