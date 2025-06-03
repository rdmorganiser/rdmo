document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".header-image"); // Get all header images

    if (images.length === 0) return; // Exit if no images exist

    const maxImage = images.length - 1;
    const timeout = 5000;
    let currentImage = 0;

    function swapImage() {
        if (images.length === 0) return; // Safety check

        images.forEach(image => image.classList.remove("visible"));

        currentImage = (currentImage + 1) % (maxImage + 1);

        images[currentImage].classList.add("visible");
    }

    // Ensure the first image is visible on load
    images[currentImage].classList.add("visible");

    // Start the image swap loop
    setInterval(swapImage, timeout);
});
