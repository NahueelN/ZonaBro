import MySQLdb
import MySQLdb.connections
from flask import current_app
from typing import Optional, List, Dict, Any

def getDbConnection() -> MySQLdb.connections:
    return MySQLdb.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB']
    )

def fetchAll(query: str, parameters: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
    if parameters is None:
        parameters = []
    connection = getDbConnection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results

def fetchOne(query: str, parameters: Optional[List[Any]] = None) -> Optional[Dict[str, Any]]:
    if parameters is None:
        parameters = []
    connection = getDbConnection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, parameters)
    result = cursor.fetchone()
    connection.close()
    return result

def execute(query: str, parameters: Optional[List[Any]] = None) -> Optional[int]:
    if parameters is None:
        parameters = []
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    last_insert_id = cursor.lastrowid
    connection.close()
    return last_insert_id