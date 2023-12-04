var sizeButtons = document.getElementsByClassName('size-btn');
var updateCart = document.querySelector('.update-cart');
for (var i = 0; i < sizeButtons.length; i++) {
  if (sizeButtons[i].getAttribute('data-stock') <= 0) {
    sizeButtons[i].disabled = true;
  }
  sizeButtons[i].addEventListener('click', function() {
    for (var j = 0; j < sizeButtons.length; j++) {
      sizeButtons[j].classList.remove('selected');
    }
    this.classList.add('selected');
    updateCart.setAttribute('data-size', this.textContent);
    updateCart.disabled = false;
  });
}
