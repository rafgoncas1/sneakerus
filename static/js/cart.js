var updateBtns = document.getElementsByClassName('update-cart')
for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
      var productId = this.dataset.product
      var size = this.dataset.size
      var action = this.dataset.action
      var quantity = this.dataset.quantity
      updateUserOrder(productId, size, action, quantity)
  })
}

function updateUserOrder(productId, size, action, quantity){
    console.log(quantity)
    
    var url = '/update_item/'
    var csrftoken = getCookie('csrftoken')

    body = JSON.stringify({'productId': productId, 'size': size, 'action': action, 'quantity': quantity})
    console.log(body)
    
    fetch(url, {
        method:'POST',
        headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
        },
        body: body,
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data.error) {
            alert(data.error);
        } else {
            if (data.success) {
                alert(data.success);
            }
            window.location.reload()
        }
    })
}