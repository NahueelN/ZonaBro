from ..dataBase.contactDB import fetchAll, fetchOne, execute
from typing import List, Dict, Any, Optional
from werkzeug.utils import secure_filename
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

def addProperty(address: str, description: str, price: int, user_id: int,rooms: int,squareMeters: int) -> int:
    query = 'INSERT INTO properties (address, description, price, user_id,rooms,squareMeters) VALUES (%s, %s, %s, %s, %s, %s)'
    property_id=execute(query, [address, description, price, user_id,rooms,squareMeters])   
    return property_id

def updateProperty(property_id: int, address: str, description: str, images: List[str], price: int,rooms: int,squareMeters: int) -> None:
    query = 'UPDATE properties SET address = %s, description = %s, price = %s WHERE id = %s'
    execute(query, [address, description, price, property_id])
    
    # Update images in the property_images table
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
    
    query = 'INSERT INTO propertyImages (property_id, image_url) VALUES (%s, %s)'
    execute(query, [property_id, image_url])


def deleteImagesByPropertyId(property_id: int) -> None:
    query = 'DELETE FROM propertyImages WHERE property_id = %s'
    execute(query, [property_id])

def getImagesByPropertyId(property_id: int) -> List[Dict[str, Any]]:
    query = 'SELECT image_url FROM propertyimages WHERE property_id = %s'
    return fetchAll(query, [property_id])