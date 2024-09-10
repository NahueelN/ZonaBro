from ..dataBase.contactDB import fetchAll, fetchOne, execute
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..untils.sendMail import sendEmail
import os
def getAllProperties() -> List[Dict[str, Any]]:
    query = 'SELECT * FROM properties'
    try:
        return fetchAll(query)
    except Exception as e:
        print(f"Error fetching all properties: {e}")
        return []

def getPropertyById(property_id: int) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM properties WHERE id = %s'
    try:
        return fetchOne(query, [property_id])
    except Exception as e:
        print(f"Error fetching property by ID: {e}")
        return None

def getPropertiesByUserId(user_id: int) -> List[Dict[str, Any]]:
    query = 'SELECT * FROM properties WHERE user_id = %s'
    try:
        return fetchAll(query, [user_id])
    except Exception as e:
        print(f"Error fetching properties by user ID: {e}")
        return []

def addPropertyDB(description: str, images, price: int, user_id: int, rooms: int, squareMeters: int) -> int:
    today = datetime.now().strftime('%Y-%m-%d') 
    query = '''
        INSERT INTO properties (description, price, user_id, rooms, squareMeters, date_added)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    parameters = [description, price, user_id, rooms, squareMeters, today]
    try:
        property_id = execute(query, parameters)
        for image in images:
            if image:
                addImage(property_id, image)
        return property_id
    except Exception as e:
        print(f"Error adding property to database: {e}")
        return -1

def updateProperty(property_id: int, description: str, images, price: int, rooms: int, squareMeters: int) -> None:
    query = 'UPDATE properties SET description = %s, price = %s, rooms = %s, squareMeters = %s WHERE id = %s'
    try:
        deleteImagesByPropertyId(property_id)
        for image in images:
            if image:
                addImage(property_id, image)
        execute(query, [description, price, rooms, squareMeters, property_id])
    except Exception as e:
        print(f"Error updating property: {e}")

def deleteProperty(property_id: int) -> None:
    try:
        deleteImagesByPropertyId(property_id)
        deleteAddressByPropertyId(property_id)
        query = 'DELETE FROM properties WHERE id = %s'
        execute(query, [property_id])
    except Exception as e:
        print(f"Error deleting property: {e}")

def deleteAddressByPropertyId(property_id: int) -> None:
    query = 'DELETE FROM property_address WHERE property_id = %s'
    try:
        execute(query, [property_id])
    except Exception as e:
        print(f"Error deleting address by property ID: {e}")

def deleteImagesByPropertyId(property_id: int) -> None:
    base_image_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'property{property_id}')
    try:
        if os.path.isdir(base_image_dir):
            for filename in os.listdir(base_image_dir):
                file_path = os.path.join(base_image_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(base_image_dir)
        query = 'DELETE FROM property_images WHERE property_id = %s'
        execute(query, [property_id])
    except Exception as e:
        print(f"Error deleting images by property ID: {e}")

def addImage(property_id: int, image_file) -> None:
    base_image_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', f'property{property_id}')
    try:
        os.makedirs(base_image_dir, exist_ok=True)
        image_filename = image_file.filename
        image_path = os.path.join(base_image_dir, image_filename)
        image_file.save(image_path)
        image_url = image_filename
        query = 'INSERT INTO property_images (property_id, image_url) VALUES (%s, %s)'
        execute(query, [property_id, image_url])
    except Exception as e:
        print(f"Error adding image: {e}")

def getImagesByPropertyId(property_id: int) -> List[Dict[str, Any]]:
    query = 'SELECT image_url FROM property_images WHERE property_id = %s'
    try:
        return fetchAll(query, [property_id])
    except Exception as e:
        print(f"Error fetching images by property ID: {e}")
        return []

def addAddress(property_id: int, street_name: str, street_number: int, city: str) -> None:
    query = 'INSERT INTO property_address (street_name, street_number, city, property_id) VALUES (%s, %s, %s, %s)'
    try:
        execute(query, [street_name, street_number, city, property_id])
    except Exception as e:
        print(f"Error adding address: {e}")

def updateAddress(property_id: int, street_name: str, street_number: int, city: str) -> None:
    query = 'UPDATE property_address SET street_name = %s, street_number = %s, city = %s WHERE property_id = %s'
    try:
        execute(query, [street_name, street_number, city, property_id])
    except Exception as e:
        print(f"Error updating address: {e}")

def getAddressByPropertyId(property_id: int) -> Optional[Dict[str, Any]]:
    query = 'SELECT * FROM property_address WHERE property_id = %s'
    try:
        return fetchOne(query, [property_id])
    except Exception as e:
        print(f"Error fetching address by property ID: {e}")
        return None

def getUserByPropertyId(property_id: int) -> Optional[Dict[str, Any]]:
    query = '''
        SELECT u.id, u.name, u.email
        FROM properties p
        JOIN user u ON p.user_id = u.id
        WHERE p.id = %s
    '''
    try:
        return fetchOne(query, [property_id])
    except Exception as e:
        print(f"Error fetching user by property ID: {e}")
        return None

def searchPropertyByAddress(query: str) -> List[Dict[str, Any]]:
    query_sql = '''
        SELECT p.id, p.description, p.price, p.user_id, p.rooms, p.squareMeters 
        FROM properties p
        JOIN property_address pa ON p.id = pa.property_id
        WHERE pa.street_name LIKE %s OR pa.city LIKE %s
    '''
    params = [f'%{query}%', f'%{query}%']
    try:
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
    except Exception as e:
        print(f"Error searching properties by address: {e}")
        return []

def sendSellerInquiry(emailRequest, question, property):  
    try:
        user = getUserByPropertyId(property.get("id"))
        address = getAddressByPropertyId(property.get("id"))
        if not user or not address:
            print("Error: User or address not found.")
            return
        
        subject = f"¡Nueva consulta sobre tu propiedad en {address.get('city')}!"
        body = f"""
        Hola {user.get('name')},

        ¡Espero que estés bien!

        Nos complace informarte que hemos recibido una nueva consulta sobre tu propiedad ubicada en {address.get('street_name')} {address.get('street_number')}, {address.get('city')}. A continuación, te proporcionamos los detalles de la consulta recibida:

        Consulta:
        {question}

        Datos de contacto del interesado:
        {emailRequest}

        Por favor, responde a esta consulta a la brevedad posible para continuar con la comunicación. Si necesitas más información o asistencia adicional, no dudes en ponerte en contacto con nosotros.

        Agradecemos mucho tu confianza y colaboración.

        ¡Saludos cordiales!

        ZonaBro
        """

        email = user.get("email")
        sendEmail(email, subject, body)
    except Exception as e:
        print(f"Error sending seller inquiry: {e}")

def getPropertyByOrder(order_by=None) -> List[Dict[str, Any]]:
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
    try:
        return fetchAll(query)
    except Exception as e:
        print(f"Error fetching properties by order: {e}")
        return []