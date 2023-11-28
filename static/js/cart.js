var updateBtns = document.getElementsByClassName('update-cart')
for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
      var productId = this.dataset.product
      var size = this.dataset.size
      var action = this.dataset.action
      var quantity = this.dataset.quantity
      if (user == 'AnonymousUser'){
        addCookieItem(productId, size, action, quantity)
      } else {
        updateUserOrder(productId, size, action, quantity)
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                if (data.success) {
                    alert(data.success);
                    window.location.reload()
                }
            }
        })
      }
  })
}

function addCookieItem(productId, size, action, quantity){
    var id = null;
        for (var key in cart){
            if (cart[key].productId == productId && cart[key].size == size){
                id = key
                break
            }
        }
    if (action == 'add'){
        if (id) {
            updateUserOrder(productId, size, action, parseInt(quantity) + parseInt(cart[id].quantity))
            .then((data) => {
                if (data.error) {
                    alert(data.error);
                } else {
                    if (data.success) {
                        cart[id].quantity = parseInt(quantity) + parseInt(cart[id].quantity)
                        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
                        alert(data.success);
                        window.location.reload()
                    }
                }
            })
            
        } else {
            updateUserOrder(productId, size, action, quantity)
            .then((data) => {
                if (data.error) {
                    alert(data.error);
                } else {
                    if (data.success) {
                        cart[Object.keys(cart).length] = {'productId': productId, 'size': size, 'quantity':quantity}
                        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
                        alert(data.success);
                        window.location.reload()
                    }
                }
            })
        }
    } else if (action == 'remove'){   
        if (id) {
            cart[id].quantity = parseInt(cart[id].quantity) - 1
            if (cart[id].quantity <= 0){
                delete cart[id]
            }
            console.log(cart)
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
            window.location.reload()
        }
    }
}

function updateUserOrder(productId, size, action, quantity){
    
    var url = '/update_item/'
    var csrftoken = getCookie('csrftoken')
    body = JSON.stringify({'productId': productId, 'size': size, 'action': action, 'quantity': quantity})
    
    var res = fetch(url, {
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

    return res
}