var skyBox = document.getElementById('skyBox');

Object.assign(skyBox.style,{
    backgroundImage: 'linear-gradient(0deg,rgba(11, 38, 0, 1) 9%, rgba(11, 38, 0, 0) 51%), url(../static/images/Mountains1.png)',
    height: '240px',
    paddingTop: '150px',
    backgroundRepeat: 'repeat-x',
    backgroundPosition: '40px',
    backgroundSize: 'contain',
    overflow: 'hidden',
    width: '100%',            
});

skyBox.animate(
    [
        {backgroundPosition: '816px' },
        {backgroundPosition:  '40px'}
    ],
    {
        duration: 12000,
        iterations: Infinity,
        easing: 'linear'
    }
);

var loginSubmit = document.getElementById('login_submit');
var horseCart = document.getElementById('horse_cart');

loginSubmit.addEventListener('mouseover', function(){
loginSubmit.style.color = 'gold';
horseCart.animate(
    [
        { opacity: 0,right: '0px'},
        { opacity: 1, right: '-70px'}
    ],
    {
        iterations: 1,
        easing: 'ease-in',
        duration: 420,
        fill: "forwards"
    }
)
});

loginSubmit.addEventListener('mouseout', function(){
loginSubmit.style.color = 'white';
horseCart.animate(
    [
        { opacity: 1},
        { opacity: 0}
    ],
    {
        iterations: 1,
        easing: 'ease-in',
        duration: 220,
        fill: "forwards"
    }
)
});

var _type = document.getElementById('_type');
var _weapon = document.getElementById('_weapon');
var _gift = document.getElementById('_gift');

var create_array = [_type,_weapon,_gift]

for(let i = 0; i < create_array.length; i++){
create_array[i].style.cursor = 'pointer';
create_array[i].addEventListener('mouseover', function(){
create_array[i].style.color = 'gold';
});
create_array[i].addEventListener('mouseout', function(){
create_array[i].style.color = 'white';
});
}


var creation_options_00 = document.getElementById('creation_options_00');
var creation_options_01 = document.getElementById('creation_options_01');
var creation_options_02 = document.getElementById('creation_options_02');

var creation_preview = document.getElementById('creation_preview');
creation_preview.style.backgroundImage = 'url(../static/images/users/blue_guy_idle_gif.gif)';

var type_a = document.getElementById('type_a');
var type_b = document.getElementById('type_b');
var type_c = document.getElementById('type_c');
var type_d = document.getElementById('type_d');
var type_f = document.getElementById('type_f');

const hidden_input_user_image = document.getElementById('user_image');
const hidden_input_user_image_small = document.getElementById('user_image_small');
const hidden_input_user_weapon = document.getElementById('starter_weapon_choice');
const hidden_input_user_gift = document.getElementById('starter_gift_choice');

var  types_desc = document.getElementById('types_desc');
var weapon_desc = document.getElementById('weapon_desc');
var gift_gift = document.getElementById('gift_desc');

var prev_type_pic = document.getElementById('prev_type_pic');
prev_type_pic.style.backgroundImage = 'linear-gradient(blue,black)';
prev_type_pic.innerHTML = 'B';

var prev_weapon_pic = document.getElementById('prev_weapon_pic');
prev_weapon_pic.style.backgroundImage= 'url(../static/images/weapons/sword_00.png)';
prev_weapon_pic.style.backgroundPosition='center';
prev_weapon_pic.style.backgroundSize='95%';

var prev_gift_pic = document.getElementById('prev_gift_pic');
prev_gift_pic.style.backgroundImage= 'url(../static/images/icons/icon_12.png)';
prev_gift_pic.style.backgroundPosition='center';
prev_gift_pic.style.backgroundSize='95%';

var starter_sword = document.getElementById('starter_sword');
var starter_staff = document.getElementById('starter_staff');
var starter_mace = document.getElementById('starter_mace');


type_a.onclick = function(){
creation_preview.style.backgroundImage = 'url(../static/images/users/red_gal_idle.gif)';
prev_type_pic.style.backgroundImage = 'linear-gradient(red,black)';
prev_type_pic.innerHTML = 'A';
hidden_input_user_image.value =type_a.getAttribute('data-image');
hidden_input_user_image_small.value =type_a.getAttribute('data-image-small');
}
type_b.onclick = function(){
creation_preview.style.backgroundImage = 'url(../static/images/users/green_gal_idle.gif)';
prev_type_pic.style.backgroundImage = 'linear-gradient(green,black)';
prev_type_pic.innerHTML = 'A';
hidden_input_user_image.value =type_b.getAttribute('data-image');
hidden_input_user_image_small.value =type_b.getAttribute('data-image-small');
}
type_c.onclick = function(){
creation_preview.style.backgroundImage = 'url(../static/images/users/blue_gal_idle.gif)';
prev_type_pic.style.backgroundImage = 'linear-gradient(blue,black)';
prev_type_pic.innerHTML = 'A';
hidden_input_user_image.value =type_c.getAttribute('data-image');
hidden_input_user_image_small.value =type_c.getAttribute('data-image-small');
}
type_d.onclick = function(){
creation_preview.style.backgroundImage = 'url(../static/images/users/red_guy_idle.gif)';
prev_type_pic.style.backgroundImage = 'linear-gradient(red,black)';
prev_type_pic.innerHTML = 'B';
hidden_input_user_image.value =type_d.getAttribute('data-image');
hidden_input_user_image_small.value =type_d.getAttribute('data-image-small');
}
type_e.onclick = function(){
creation_preview.style.backgroundImage = 'url(../static/images/users/green_guy_idle.gif)';
prev_type_pic.style.backgroundImage = 'linear-gradient(green,black)';
prev_type_pic.innerHTML = 'B';
hidden_input_user_image.value =type_e.getAttribute('data-image');
hidden_input_user_image_small.value =type_e.getAttribute('data-image-small');
}
type_f.onclick = function(){
creation_preview.style.backgroundImage = 'url(../static/images/users/blue_guy_idle_gif.gif)';
prev_type_pic.style.backgroundImage = 'linear-gradient(blue,black)';
prev_type_pic.innerHTML = 'B';
hidden_input_user_image.value =type_f.getAttribute('data-image');
hidden_input_user_image_small.value =type_f.getAttribute('data-image-small');
}

_type.onclick = function(){
creation_options_00.style.display = 'flex';
creation_options_01.style.display = 'none';
creation_options_02.style.display = 'none';
types_desc.style.display = 'flex';
weapon_desc.style.display = 'none';
gift_desc.style.display = 'none';
}

_weapon.onclick = function(){
creation_options_00.style.display = 'none';
creation_options_01.style.display = 'flex';
creation_options_02.style.display = 'none';
types_desc.style.display = 'none';
weapon_desc.style.display = 'flex';
gift_desc.style.display = 'none';
}

_gift.onclick = function(){
creation_options_00.style.display = 'none';
creation_options_01.style.display = 'none';
creation_options_02.style.display = 'flex';
types_desc.style.display = 'none';
weapon_desc.style.display = 'none';
gift_desc.style.display = 'flex';
}

starter_sword.onclick = function(){
prev_weapon_pic.style.backgroundImage='url(../static/images/weapons/sword_00.png)';
prev_weapon_pic.style.backgroundPosition='center';
prev_weapon_pic.style.backgroundSize='95%';
hidden_input_user_weapon.value = starter_sword.getAttribute('data');
}

starter_staff.onclick = function(){
prev_weapon_pic.style.backgroundImage='url(../static/images/weapons/staff_00.png)';
prev_weapon_pic.style.backgroundPosition='center';
prev_weapon_pic.style.backgroundSize='95%';
hidden_input_user_weapon.value = starter_staff.getAttribute('data');
}

starter_mace.onclick = function(){
prev_weapon_pic.style.backgroundImage='url(../static/images/weapons/mace_00.png)';
prev_weapon_pic.style.backgroundPosition='center';
prev_weapon_pic.style.backgroundSize='95%';
hidden_input_user_weapon.value = starter_mace.getAttribute('data');
}

var gift_00 = document.getElementById('gift_00');
var gift_01 = document.getElementById('gift_01');
var gift_02 = document.getElementById('gift_02');
var gift_03 = document.getElementById('gift_03');
var gift_04 = document.getElementById('gift_04');
var gift_05 = document.getElementById('gift_05');

gift_btn_array = [gift_00,gift_01,gift_02,gift_03,gift_04,gift_05];
for(let i = 0; i < gift_btn_array.length;i++){
gift_btn_array[i].addEventListener('mouseover',function(){
gift_btn_array[i].style.color = 'gold';
});
gift_btn_array[i].addEventListener('mouseout',function(){
gift_btn_array[i].style.color = 'white';
});
}


gift_00.onclick = function(){
prev_gift_pic.style.backgroundImage='url(../static/images/icons/icon_13.png)';
}

gift_01.onclick = function(){
prev_gift_pic.style.backgroundImage='url(../static/images/icons/icon_02.png)';
}

gift_02.onclick = function(){
prev_gift_pic.style.backgroundImage='url(../static/images/icons/icon_08.png)';
}

gift_03.onclick = function(){
prev_gift_pic.style.backgroundImage='url(../static/images/icons/icon_09.png)';
}

gift_04.onclick = function(){
prev_gift_pic.style.backgroundImage='url(../static/images/icons/icon_11.png)';
}

gift_05.onclick = function(){
prev_gift_pic.style.backgroundImage='url(../static/images/icons/icon_12.png)';
}
