
var displayButtons = document.getElementsByClassName("display_button");
var displayButtonHolder = document.querySelector(".display_button_holder");
var shop_holder = document.querySelector(".shop_holder");
var exit_shop_cart_order = document.querySelector("#exit_shop_cart_order")

function update_memory(memory){
    memory = memory.toString();
    console.log("MEMORY CHANGE")
    window.location.href = '/memory/' + memory;
}
function reset_displays(){
    items = document.getElementById("items");
    cart = document.getElementById("cart");
    order = document.getElementById("orders");
    shop_holder.classList.add('shop_holder_sky');
    shop_holder.classList.remove('shop_background_image');
    displayButtonHolder.style.display = 'flex'
    items.style.display = "none";
    cart.style.display = "none";
    order.style.display = "none";
    exit_shop_cart_order.style.display = 'none';
}

function display_shop(){
    exit_shop_cart_order.style.display = 'block';
    items = document.getElementById("items");
    shop_holder.classList.remove('shop_holder_sky');
    shop_holder.classList.add('shop_background_image');
    displayButtonHolder.style.display = 'None'
    items.style.display = "flex";
}
function display_cart(){
    exit_shop_cart_order.style.display = 'block';
    cart = document.getElementById("cart");
    shop_holder.classList.remove('shop_holder_sky');
    shop_holder.classList.add('shop_background_image');
    displayButtonHolder.style.display = 'None'
    cart.style.display = "flex";
}
function display_orders(){
    exit_shop_cart_order.style.display = 'block';
    order = document.getElementById("orders");
    shop_holder.classList.remove('shop_holder_sky');
    shop_holder.classList.add('shop_background_image');
    displayButtonHolder.style.display = 'None'
    order.style.display = "flex";
}
document.addEventListener("DOMContentLoaded", (event) => {
    memory = document.getElementById("memory_item_get").innerHTML
    if (memory == "SHOP"){
        display_shop()
    }
    if (memory == "CART"){
        display_cart()
    }
    if (memory == "ORDERS"){
        display_orders()
    }
    if (memory == "None"){
        reset_displays()
    }
    console.log(memory)
})