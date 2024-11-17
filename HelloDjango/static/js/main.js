$(document).ready(function () {
    // Инициализация карусели OwlCarousel
    $(".owl-carousel").owlCarousel({
        items: 3,
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive: {
            0: { items: 1 },
            600: { items: 2 },
            1000: { items: 5 }
        }
    });

    // Универсальная функция для управления видео
    function setupVideoControls(videoElement, playButtonElement) {
        if (videoElement && playButtonElement) {
            playButtonElement.addEventListener('click', () => {
                if (videoElement.paused) {
                    videoElement.play();
                    playButtonElement.style.display = 'none';
                } else {
                    videoElement.pause();
                    playButtonElement.style.display = 'block';
                }
            });

            videoElement.addEventListener('click', () => {
                if (!videoElement.paused) {
                    videoElement.pause();
                    playButtonElement.style.display = 'block';
                }
            });

            videoElement.addEventListener('ended', () => {
                playButtonElement.style.display = 'block';
            });
        }
    }

    // Применяем функцию для всех видео
    const videos = [
        { video: 'aboutUsVideo', button: 'playButton' },
        { video: 'reviewsVideo1', button: 'playButton1' },
        { video: 'reviewsVideo2', button: 'playButton2' },
        { video: 'reviewsVideo3', button: 'playButton3' },
    ];

    videos.forEach(({ video, button }) => {
        const videoElement = document.getElementById(video);
        const playButtonElement = document.getElementById(button);
        setupVideoControls(videoElement, playButtonElement);
    });

    // Скрипт для кнопок "Показать больше"
    const itemsPerClick = 10;

    // Находим все кнопки "Показать больше"
    document.querySelectorAll(".btn-show-more").forEach(button => {
        const sectionId = button.id.split("-").pop(); // Получаем section_id из id кнопки
        const hiddenItemsSelector = `.product-items-section-5[data-section-id="${sectionId}"] .product-item.d-none`;

        button.addEventListener("click", function () {
            let shownCount = 0;
            const hiddenItems = document.querySelectorAll(hiddenItemsSelector);

            hiddenItems.forEach(item => {
                if (shownCount < itemsPerClick) {
                    item.classList.remove("d-none"); // Показываем скрытые элементы
                    shownCount++;
                }
            });

            // Если больше нечего показывать, скрываем кнопку
            if (document.querySelectorAll(hiddenItemsSelector).length === 0) {
                button.style.display = "none";
            }
        });
    });
});

// Скрипты для управления основным изображением
function changeMainImage(imageUrl) {
    const mainImage = document.getElementById('main-image');
    if (mainImage) {
        mainImage.src = imageUrl; // Изменяем src у основного изображения
    }
}

// Скрипты для управления количеством товара
const unitPrice = 2200;

function updateTotalPrice(quantity) {
    const totalPrice = unitPrice * quantity;
    const totalPriceElement = document.getElementById("totalPrice");
    if (totalPriceElement) {
        totalPriceElement.innerText = `${totalPrice.toLocaleString()} р.`;
    }
}

function increaseQuantity() {
    const quantityInput = document.getElementById("quantity");
    if (quantityInput) {
        let quantity = parseInt(quantityInput.value, 10) || 1;
        quantity += 1;
        quantityInput.value = quantity;
        updateTotalPrice(quantity);
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById("quantity");
    if (quantityInput) {
        let quantity = parseInt(quantityInput.value, 10) || 1;
        if (quantity > 1) {
            quantity -= 1;
            quantityInput.value = quantity;
            updateTotalPrice(quantity);
        }
    }
}
