document.addEventListener('DOMContentLoaded', function() {
    var propertyDataElement = document.getElementById('property-data');
    if (propertyDataElement) {
        var propertyData = JSON.parse(propertyDataElement.textContent);
        
        console.log('propertyData:', propertyData);  

        if (propertyData.latitude && propertyData.longitude) {
            var lat = parseFloat(propertyData.latitude);
            var lon = parseFloat(propertyData.longitude);

            var map = L.map('map').setView([lat, lon], 16); 

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            L.marker([lat, lon]).addTo(map)
                .bindPopup('Ubicación de la propiedad')
                .openPopup();
        } else {
            console.error('No se pudieron obtener las coordenadas del mapa.');
        }
    } else {
        console.error('Elemento de datos de propiedad no encontrado.');
    }
});