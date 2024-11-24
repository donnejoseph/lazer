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


function addToCart(productId) {
    const quantityInput = document.getElementById('quantity');
    const quantity = parseInt(quantityInput.value, 10) || 1;

    fetch(`/add_to_cart/${productId}/`, {
        method: 'POST', // Changed to POST
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
        },
        body: JSON.stringify({ 'quantity': quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Товар добавлен в корзину');

            // Update the cart quantity badge in the header
            const badge = document.querySelector('.cart-quantity-badge');
            if (badge) {
                badge.textContent = data.cart_total_quantity;
            } else {
                // If badge doesn't exist, create it
                const cartLink = document.querySelector('.shopping-cart a');
                const span = document.createElement('span');
                span.classList.add('cart-quantity-badge');
                span.textContent = data.cart_total_quantity;
                cartLink.appendChild(span);
            }
        } else {
            alert(data.message || 'Ошибка добавления в корзину');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does the cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function updateQuantity(productId, action) {
    fetch(`/update_cart/${productId}/${action}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Получаем CSRF токен из куки
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновляем количество товара
            const quantityInput = document.getElementById(`quantity-${productId}`);
            const totalPriceElement = document.getElementById(`totalPrice-${productId}`);
            const totalPriceText = document.querySelector('.korzina-total-price-text');
            const cartTitle = document.querySelector('.korzina-title');
            const badge = document.querySelector('.cart-quantity-badge');

            // Проверяем данные перед обновлением
            if (data.new_quantity !== undefined && data.price !== undefined) {
                // Обновляем количество для конкретного товара
                if (quantityInput) {
                    quantityInput.value = data.new_quantity; // Обновляем значение количества в поле
                }

                // Обновляем общую цену для конкретного товара
                if (totalPriceElement) {
                    const newItemTotal = parseFloat(data.new_quantity) * parseFloat(data.price);
                    totalPriceElement.textContent = `${newItemTotal.toFixed(2)} р.`;
                }
            } else {
                console.error("Ошибка данных: некорректное количество или цена");
            }

            // Обновляем общую стоимость корзины
            if (totalPriceText && data.cart_total !== undefined) {
                totalPriceText.textContent = `${data.cart_total.toFixed(2)} р.`;
            } else {
                console.error("Ошибка данных: некорректная общая стоимость корзины");
            }

            // Обновляем заголовок "В корзине X товара"
            if (cartTitle) {
                const quantity = data.cart_total_quantity || 0; // Убеждаемся, что значение есть
                const word = getCorrectWord(quantity, ['товар', 'товара', 'товаров']);
                cartTitle.textContent = `В корзине ${quantity} ${word}`;
            }

            // Обновляем количество товаров в иконке корзины
            if (badge) {
                badge.textContent = data.cart_total_quantity || 0;
            } else if (data.cart_total_quantity > 0) {
                const cartLink = document.querySelector('.shopping-cart a');
                const span = document.createElement('span');
                span.classList.add('cart-quantity-badge');
                span.textContent = data.cart_total_quantity || 0;
                cartLink.appendChild(span);
            }
        } else {
            alert(data.message || 'Ошибка обновления корзины');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при обновлении корзины');
    });
}


function getCorrectWord(number, words) {
    const cases = [2, 0, 1, 1, 1, 2];
    return words[
        (number % 100 > 4 && number % 100 < 20)
            ? 2
            : cases[Math.min(number % 10, 5)]
    ];
}
