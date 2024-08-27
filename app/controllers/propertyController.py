from ..dataBase.contactDB import fetchAll, fetchOne, execute
from typing import List, Dict, Any, Optional
import os

def getAllProperties() -> List[Dict[str, Any]]:
    query = 'SELECT * FROM properties'
    return fetchAll(query)

def getPropertyById(property_id: int) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM properties WHERE id = %s'
    return fetchOne(query, [property_id])

def getPropertiesByUserId(user_id: int) -> List[Dict[str, Any]]:
    query = 'SELECT * FROM properties WHERE user_id = %s'
    return fetchAll(query, [user_id])

def addProperty( description: str, price: int, user_id: int,rooms: int,squareMeters: int) -> int:
    query = 'INSERT INTO properties (description, price, user_id,rooms,squareMeters) VALUES ( %s, %s, %s, %s, %s)'
    property_id=execute(query, [ description, price, user_id,rooms,squareMeters])   
    return property_id

def updateProperty(property_id: int, description: str, images: List[str], price: int,rooms: int,squareMeters: int) -> None:
    query = 'UPDATE properties SET description = %s, price = %s,rooms=%s,squareMeters=%s WHERE id = %s'
    execute(query, [ description, price,rooms,squareMeters, property_id])
    
    deleteImagesByPropertyId(property_id)
    for image in images:
        addImage(property_id, image)

def deleteProperty(property_id: int) -> None:
    deleteImagesByPropertyId(property_id)
    query = 'DELETE FROM properties WHERE id = %s'
    execute(query, [property_id])

def addImage(property_id: int, image_file) -> None:
    base_image_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'property{property_id}')
    os.makedirs(base_image_dir, exist_ok=True)
    
    image_filename = image_file.filename
    image_path = os.path.join(base_image_dir, image_filename)
    
    image_file.save(image_path)
    
    image_url = image_filename
    
    query = 'INSERT INTO property_images (property_id, image_url) VALUES (%s, %s)'
    execute(query, [property_id, image_url])


def deleteImagesByPropertyId(property_id: int) -> None:
    query = 'DELETE FROM property_images WHERE property_id = %s'
    execute(query, [property_id])

def getImagesByPropertyId(property_id: int) -> List[Dict[str, Any]]:
    query = 'SELECT image_url FROM property_images WHERE property_id = %s'
    return fetchAll(query, [property_id])

def addAddress(property_id: int,street_name: int ,street_number:str, city:str) -> None:
    query = 'INSERT INTO property_address (street_name,street_number,city,property_id) VALUES (%s, %s, %s, %s)'
    execute(query,[street_name,street_number,city,property_id])

def getAddressByPropertyId(property_id: int):
    query = 'SELECT * FROM property_address WHERE property_id = %s'
    return fetchOne(query, [property_id])
