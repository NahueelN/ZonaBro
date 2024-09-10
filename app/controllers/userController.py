from ..dataBase.contactDB import fetchAll, fetchOne, execute
from typing import List, Dict, Any, Optional
from app.models.entities.user import User

def getAllUser() -> List[Dict[str, Any]]:
    query = 'SELECT * FROM user'
    try:
        return fetchAll(query)
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []

def getUserById(userId: int) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM user WHERE id = %s'
    try:
        return fetchOne(query, [userId])
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None

def getUserByEmail(email: str) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM user WHERE email = %s'
    try:
        return fetchOne(query, [email])
    except Exception as e:
        print(f"Error fetching user by email: {e}")
        return None

def addUser(email: str, password: str, name: str) -> None:
    query = 'INSERT INTO user (email, password, name) VALUES (%s, %s, %s)'
    try:
        execute(query, [email, password, name])
    except Exception as e:
        print(f"Error adding user: {e}")

def updateUser(userId: int, email: str, password: str, name: str) -> None:
    query = 'UPDATE user SET email = %s, password = %s, name = %s WHERE id = %s'
    try:
        execute(query, [email, password, name, userId])
    except Exception as e:
        print(f"Error updating user: {e}")

def deleteUser(userId: int) -> None:
    query = 'DELETE FROM user WHERE id = %s'
    try:
        execute(query, [userId])
    except Exception as e:
        print(f"Error deleting user: {e}")

def loginn(email: str, password: str) -> Optional[User]:
    try:
        user = getUserByEmail(email)
        if user and password == user.get("password"):
            return User(
                id=user['id'],
                email=user['email'],
                password=user['password'],
                name=user['name'],
            )
        else:
            return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None
    
def updateUser(user_id, email, password, name):
    user_query = "SELECT * FROM user WHERE id = %s"
    user = fetchOne(user_query, [user_id])
    
    if not user:
        raise ValueError('Usuario no encontrado')
    update_query = """
    UPDATE user
    SET email = %s,
        name = %s,
        password = %s
    WHERE id = %s
    """
    
    password_value = password if password else user['password']
    print(email, name, password_value, user_id)
    execute(update_query, [email, name, password_value, user_id])

def checkPassword(user_id: int, password: str) -> bool:

    query = "SELECT password FROM user WHERE id = %s"

    user = fetchOne(query, [user_id])
    
    if user and 'password' in user:
        print(user['password'])
        print(password)
        return user['password'] == password
    
    return False