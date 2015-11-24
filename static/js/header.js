var _current_image = 0;
var _max_image = 2;
var _timeout = 5000;

function swap_image() {
    $('.header-image-' + _current_image).removeClass('visible');
    if (_current_image >= _max_image) {
        _current_image = 0;
    } else {
        _current_image += 1;
    }
    $('.header-image-' + _current_image).addClass('visible');

    setTimeout(swap_image, _timeout);
}

$(document).ready(function() {
    setTimeout(swap_image, _timeout);
});
