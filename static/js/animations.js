
function animateSliderThumb(event){
    rateComment = event.nextElementSibling
    if (event.value < 50){
        if (event.value <= 25){
            rateComment.innerHTML = "Yea, this take mostly makes sense"
        }
        if (event.value == 0){
            rateComment.innerHTML = "This is the most sane take in the history of takes"
        }
        event.style.setProperty('--thumb-image', `url('../img/snow.png')`)

    }
    else{
        if (event.value == 50){
            rateComment.innterHTML = "IDK how I feel about this take yet"
        }
        if (event.value >=75){
            rateComment.innerHTML = "Wow! That's a pretty hot take "
        }
        if (event.value == 100){ 
            rateComment.innerHTML = "This Take is taking you to hell"
        }
        event.style.setProperty('--thumb-image', `url('../img/fire.png')`)
    }
}
