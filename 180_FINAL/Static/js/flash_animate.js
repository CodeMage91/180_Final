
var goon_box = document.getElementById('goon_box');
goon_box.animate(
    [
        {opacity: 1,display:'flex'},
        {opacity: 1,display:'flex'},
        {opacity: 0.7,display:'flex'},
        {opacity:0,display:'none'}
    ],
    {
        duration: 4200,
        easing: 'linear',
        iterations: '1',
        fill: 'forwards'
    }
);
