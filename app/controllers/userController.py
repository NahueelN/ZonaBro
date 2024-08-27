from ..dataBase.contactDB import fetchAll, fetchOne, execute
from typing import List, Dict, Any, Optional
from app.models.entities.user import User

def getAllUser() -> List[Dict[str, Any]]:
    query = 'SELECT * FROM user'
    return fetchAll(query)

def getUserById(userId: int) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM user WHERE id = %s'
    return fetchOne(query, [userId])

def getUserByEmail(email: str) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM user WHERE email = %s'
    return fetchOne(query, [email])

def addUser(email: str, password: str, name: str) -> None:
    query = 'INSERT INTO user (email, password, name) VALUES (%s, %s, %s)'
    execute(query, [email, password, name])

def updateUser(useId: int, email: str, password: str, name: str) -> None:
    query = 'UPDATE properties SET email = %s, password = %s, name = %s WHERE id = %s'
    execute(query, [useId, email, password, name])

def deleteUser(userId: int) -> None:
    query = 'DELETE FROM user WHERE id = %s'
    execute(query, [userId])

def loginn(email,password):
    try:
        user= getUserByEmail(email) 
        if user != None and password==user.get("password"):
            return User(
            id=user['id'],
            email=user['email'],
            password=user['password'],
            name=user['name'],
        )
        else:
            return None
    except Exception as ex:
        raise Exception(ex)


