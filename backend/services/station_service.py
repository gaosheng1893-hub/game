from fastapi import HTTPException
from common.database import get_db_connection

class StationService:
    @staticmethod
    def get_all_stations():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stations ORDER BY position")
        stations = cursor.fetchall()
        connection.close()
        return stations
    
    @staticmethod
    def get_station_by_id(station_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM stations WHERE id = %s", (station_id,))
        station = cursor.fetchone()
        
        if not station:
            connection.close()
            raise HTTPException(status_code=404, detail="站点不存在")
        
        cursor.execute("SELECT * FROM questions WHERE station_id = %s", (station_id,))
        questions = cursor.fetchall()
        station['questions'] = questions
        
        connection.close()
        return station
