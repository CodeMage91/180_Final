     
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