
function animateSliderThumb(event){
    if (event.value < 50){
        event.style.setProperty('--thumb-image', `url('../img/snow.png')`)
    }
    else{
        event.style.setProperty('--thumb-image', `url('../img/fire.png')`)
    }
}
