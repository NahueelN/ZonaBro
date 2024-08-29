from ..dataBase.contactDB import fetchAll, fetchOne, execute
from datetime import datetime
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

def addPropertyDB(description: str,images, price: int, user_id: int, rooms: int, squareMeters: int) -> int:
    today = datetime.now().strftime('%Y-%m-%d') 
    query = '''
        INSERT INTO properties (description, price, user_id, rooms, squareMeters, date_added)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    parameters = [description, price, user_id, rooms, squareMeters, today]
    property_id = execute(query, parameters)
    for image in images:
        if image:
            addImage(property_id, image)
    return property_id

def updateProperty(property_id: int, description: str,images, price: int,rooms: int,squareMeters: int) -> None:
    query = 'UPDATE properties SET description = %s, price = %s,rooms=%s,squareMeters=%s WHERE id = %s'
    print("aca")
    deleteImagesByPropertyId(property_id)
    
    for image in images:
        if image:
            addImage(property_id, image)
    execute(query, [ description, price,rooms,squareMeters, property_id])

def deleteProperty(property_id: int) -> None:
    deleteImagesByPropertyId(property_id)
    deleteAddressByPropertyId(property_id)
    query = 'DELETE FROM properties WHERE id = %s'
    execute(query, [property_id])

def deleteAddressByPropertyId(property_id: int) -> None:
    query = 'DELETE FROM property_address WHERE property_id = %s'
    execute(query, [property_id])

def deleteImagesByPropertyId(property_id: int) -> None:
    base_image_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'property{property_id}')
    if os.path.isdir(base_image_dir):
        for filename in os.listdir(base_image_dir):
            file_path = os.path.join(base_image_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(base_image_dir)
    query = 'DELETE FROM property_images WHERE property_id = %s'
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


def getImagesByPropertyId(property_id: int) -> List[Dict[str, Any]]:
    query = 'SELECT image_url FROM property_images WHERE property_id = %s'
    return fetchAll(query, [property_id])

def addAddress(property_id: int,street_name: str ,street_number:int, city:str) -> None:
    query = 'INSERT INTO property_address (street_name,street_number,city,property_id) VALUES (%s, %s, %s, %s)'
    execute(query,[street_name,street_number,city,property_id])

def updateAddress(property_id: int,street_name: str ,street_number:int, city:str) -> None:
    query = 'UPDATE property_address SET street_name = %s, street_number = %s,city=%s WHERE property_id = %s'
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


def getPropertyByOrder(order_by=None) -> list:
    if order_by == 'price_asc':
        order = 'price ASC'
    elif order_by == 'price_desc':
        order = 'price DESC'
    elif order_by == 'date_asc':
        order = 'date_added ASC'
    elif order_by == 'date_desc':
        order = 'date_added DESC'
    else:
        return None 
    
    query = f"SELECT * FROM properties ORDER BY {order}"
    return fetchAll(query)