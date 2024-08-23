document.addEventListener('DOMContentLoaded', function() {
    var carouselImages = document.querySelectorAll('#carousel-{{ property.id }} .carousel-item img');
    var modalCarousel = document.getElementById('modalCarousel');

    carouselImages.forEach(function(image) {
        image.addEventListener('click', function() {
            var imageIndex = Array.from(carouselImages).indexOf(image);
            var modalCarouselInstance = new bootstrap.Carousel(modalCarousel);
            modalCarouselInstance.to(imageIndex);
        });
    });
});