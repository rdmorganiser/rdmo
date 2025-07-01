window.loopHeaderBackgroundImage = (timeout) => {
    const images = document.querySelectorAll('#header .header-image')

    let index = 0

    const setHeaderBackgroundImage = () => {
        images[index].classList.remove('header-image-visible')
        index = (index == images.length - 1) ? 0 : index + 1
        images[index].classList.toggle('header-image-visible')
        setTimeout(() => setHeaderBackgroundImage(), timeout)
    }

    setTimeout(() => setHeaderBackgroundImage(), timeout)
}
