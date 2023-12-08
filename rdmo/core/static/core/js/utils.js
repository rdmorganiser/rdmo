function showMore(element) {
    $(element).siblings('.more').show();
    $(element).siblings('.show-less').show();
    $(element).hide();
}

function showLess(element) {
    $(element).siblings('.more').hide();
    $(element).siblings('.show-more').show();
    $(element).hide();
}
