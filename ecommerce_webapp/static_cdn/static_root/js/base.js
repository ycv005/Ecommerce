$(document).ready(function(){
    // Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find(".search-input") //find the name attribute with q as value
    var typingTimer;
    var typingInterval=1000; //1.0 sec

    searchInput.keyup(function(){
      // works when key is released
      clearTimeout(typingTimer)
      typingTimer = setTimeout(perfomSearch, typingInterval)
    })

    searchInput.keydown(function(){
      // works when key is pressed
      clearTimeout(typingTimer)
    })
    function perfomSearch(){
      var query = searchInput.val()
      window.location.href = '/search/?q=' + query
    }

    // Ajax in Cart + Remove product
    var productForm = $(".form-product-ajax")
    productForm.submit(function(event){
      event.preventDefault()
      var thisForm = $(this)
      var actionEndpoint = thisForm.attr("action")
      var httpMethod = thisForm.attr("method")
      var formData = thisForm.serialize()
      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var cart_update = thisForm.find(".cart-add-remove")
          if (data.product_added){
            cart_update.html("<button class='btn btn-outline-success' type='submit'>Remove from Cart</button>")
          }
          else{
            cart_update.html("<button class='btn btn-outline-success' type='submit'>Added to Cart</button>")
          }
          var count = $(".nav-bar-cartItemCount")
          count.text(data.cartItemCount)
          var currentPath = window.location.href
          if(currentPath.indexOf("cart")!= -1){
            refreshCart()
          }
        },
        error: function(errorData){
          alert("An Error Occured")
        }
      })
    })
    function refreshCart(){
      console.log("in refresh cart")
      var cartTable = $(".cart-table")
      var cartBody = cartTable.find(".cart-body")
      // cartBody.html("<h2>Changed</h2>")
      var productRows = cartBody.find(".cart-product");

      // go to the endpoint(url) and get data
      var updateCartUrl = '/api/cart/'
      var updateCartMethod = "GET";
      var data={};
      $.ajax({
        url: updateCartUrl,
        method: updateCartMethod,
        data: data,
        success: function(data) {
          console.log("via api, success")
          var hiddenProductRemoveForm = $(".cart-item-remove-form")
          if (data.products.length>0){
            productRows.html("")
            $.each(data.products, function(index, value){
              var newCartItemProductRemove = hiddenProductRemoveForm.clone()
              newCartItemProductRemove.css("display", "block")
              newCartItemProductRemove.find(".cart-item-product-id").val(value.id)
              cartBody.prepend("<tr><th scope='row'><a href='"+ value.url + "'>"+ value.name+"</a>" + newCartItemProductRemove.html()+"<td>" + value.price + "</td></tr>")
            })
            cartBody.find(".cart-subtotal").text(data.subtotal)
            cartBody.find(".cart-total").text(data.total)
          }
          else{ //refresh page
            window.location.href = currentPath
          }
        },
        error: function (data) {
          alert("An Error Occured")
        }
      })
    }
  })