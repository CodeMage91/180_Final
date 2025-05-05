     
var nav00 = document.getElementById('nav_00');
var navText00 = document.getElementById('nav_text_00');

var nav01 = document.getElementById('nav_01');
var navText01 = document.getElementById('nav_text_01');

var nav02 = document.getElementById('nav_02');
var navText02 = document.getElementById('nav_text_02');

var nav03 = document.getElementById('nav_03');
var navText03 = document.getElementById('nav_text_03');

var nav04 = document.getElementById('nav_04');
var navText04 = document.getElementById('nav_text_04');

var nav05 = document.getElementById('nav_05');
var navText05 = document.getElementById('nav_text_05');

var nav06 = document.getElementById('nav_06');
var navText06 = document.getElementById('nav_text_06');

var nav07 = document.getElementById('nav_07');
var navText07 = document.getElementById('nav_text_07');
    //here I set up some divs and text under them in a loop to add hover, style flex to be shown 
    //and animation
    var navArray =[nav00,nav01,nav02,nav03,nav04,nav05,nav06,nav07];
    var navTextArray = [navText00,navText01,navText02,navText03,navText04,navText05,navText06,navText07];

    for (let i = 0; i < navArray.length; i++) {
        navArray[i].addEventListener('mouseover', function(){
            navArray[i].style.cursor = 'pointer';
            navTextArray[i].style.display = 'flex';
            navArray[i].animate(
                [
                    {scale : '1'},
                    {scale : '1.2'},
                    {scale : '1.1'}
                ],
                {
                    easing: 'ease-in',
                    duration: 500,
                    fill: 'forwards'
                
                }
            )
        });
    }  

    for (let i = 0; i < navArray.length; i++) {
        navArray[i].addEventListener('mouseout', function () {
            navTextArray[i].style.display = 'none';
            navArray[i].animate(
                [
                    {scale : '1.1'},
                    {scale : '1'}
                ],
                {
                    easing: 'ease-in',
                    duration: 200,
                    fill: 'forwards'
                }
            )
        });
    }
    var star_box = document.getElementById('star_box');

    Object.assign(star_box.style,{
        backgroundImage: 'linear-gradient(0deg,rgba(11, 38, 0, 1) 9%, rgba(11, 38, 0, 0) 51%), url(../static/images/starlitSky.png)',
        height: '240px',
        paddingTop: '150px',
        backgroundRepeat: 'repeat-x',
        backgroundPosition: '40px',
        backgroundSize: 'contain',
        overflow: 'hidden',
        width: '100%',            
    });

    star_box.animate(
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

var chest = document.getElementById('chest');
Object.assign(chest.style,{
    cursor: 'pointer'
});