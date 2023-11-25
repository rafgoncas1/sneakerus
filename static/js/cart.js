var updateBtns = document.getElementsByClassName('update-cart')
for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
      var productId = this.dataset.product
      var size = this.dataset.size
      var action = this.dataset.action
      updateUserOrder(productId, size, action)
  })
}

function updateUserOrder(productId, size, action){
    
    var url = '/update_item/'
    var csrftoken = getCookie('csrftoken')
    
    fetch(url, {
        method:'POST',
        headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'size': size, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data.error) {
            alert(data.error);
        } else {
            window.location.reload()
        }
    })
}