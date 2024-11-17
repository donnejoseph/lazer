$(document).ready(function(){
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

  // Универсальная функция для добавления событий к видео и кнопке
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

  // Применяем функцию для каждого видео и кнопки
  setupVideoControls(document.getElementById('aboutUsVideo'), document.getElementById('playButton'));
  setupVideoControls(document.getElementById('reviewsVideo1'), document.getElementById('playButton1'));
  setupVideoControls(document.getElementById('reviewsVideo2'), document.getElementById('playButton2'));
  setupVideoControls(document.getElementById('reviewsVideo3'), document.getElementById('playButton3'));
});


const unitPrice = 2200;

function updateTotalPrice(quantity) {
  const totalPrice = unitPrice * quantity;
  document.getElementById("totalPrice").innerText = `${totalPrice.toLocaleString()} р.`;
}

function increaseQuantity() {
  let quantityInput = document.getElementById("quantity");
  let quantity = parseInt(quantityInput.value, 10);
  quantity += 1;
  quantityInput.value = quantity;
  updateTotalPrice(quantity);
}

function decreaseQuantity() {
  let quantityInput = document.getElementById("quantity");
  let quantity = parseInt(quantityInput.value, 10);
  if (quantity > 1) {
    quantity -= 1;
    quantityInput.value = quantity;
    updateTotalPrice(quantity);
  }

}

document.addEventListener("DOMContentLoaded", function () {
    const itemsPerClick = 10;

    // Находим все кнопки "Показать больше"
    const showMoreButtons = document.querySelectorAll(".btn-show-more");

    // Проходимся по каждой кнопке
    showMoreButtons.forEach(button => {
        const sectionId = button.id.split("-").pop(); // Получаем section_id из id кнопки
        const hiddenItems = document.querySelectorAll(`.product-items-section-5[data-section-id="${sectionId}"] .product-item.d-none`);

        button.addEventListener("click", function () {
            let shownCount = 0;

            hiddenItems.forEach(item => {
                if (shownCount < itemsPerClick && item.classList.contains("d-none")) {
                    item.classList.remove("d-none"); // Показываем скрытые элементы
                    shownCount++;
                }
            });

            // Если больше нечего показывать, скрываем кнопку
            if (document.querySelectorAll(`.product-items-section-5[data-section-id="${sectionId}"] .product-item.d-none`).length === 0) {
                button.style.display = "none";
            }
        });
    });
});


