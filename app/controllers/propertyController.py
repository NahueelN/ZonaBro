from ..dataBase.contactDB import fetchAll, fetchOne, execute
from typing import List, Dict, Any, Optional
from ..untils.sendMail import sendEmail
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

def getUserByPropertyId(property_id: int):
    query = '''
        SELECT u.id, u.name, u.email
        FROM properties p
        JOIN user u ON p.user_id = u.id
        WHERE p.id = %s
    '''
    result = fetchOne(query, [property_id])
    return result

def SearchPropertyByAddress(query: str) -> list:
    query_sql = '''
        SELECT p.id, p.description, p.price, p.user_id, p.rooms, p.squareMeters 
        FROM properties p
        JOIN property_address pa ON p.id = pa.property_id
        WHERE pa.street_name LIKE %s OR pa.city LIKE %s
    '''
    params = [f'%{query}%', f'%{query}%']
    properties = fetchAll(query_sql, params)
    
    properties_list = []
    for prop in properties:
        properties_list.append({
            'id': prop['id'],
            'description': prop['description'],
            'price': prop['price'],
            'user_id': prop['user_id'],
            'rooms': prop['rooms'],
            'squareMeters': prop['squareMeters']
        })
    
    return properties_list

def sendSellerInquiry(emailRequest,question,property):  
        user=getUserByPropertyId(property.get("id"))
        address=getAddressByPropertyId(property.get("id"))
        subject = "¡Nueva consulta sobre tu propiedad en %s!" % (address.get("city"))

        body = """
        Hola %s,

        ¡Espero que estés bien!

        Nos complace informarte que hemos recibido una nueva consulta sobre tu propiedad ubicada en %s %s, %s. A continuación, te proporcionamos los detalles de la consulta recibida:

        Consulta:
        %s

        Datos de contacto del interesado:
        %s

        Por favor, responde a esta consulta a la brevedad posible para continuar con la comunicación. Si necesitas más información o asistencia adicional, no dudes en ponerte en contacto con nosotros.

        Agradecemos mucho tu confianza y colaboración.

        ¡Saludos cordiales!

        ZonaBro
        """%(user.get("name"),address.get("street_name"),address.get("street_number"),address.get("city"),question,emailRequest)
        email=user.get("email")
        sendEmail(email,subject,body)