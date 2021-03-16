function initPopovers(page) {
    var opts = {
        html: true,
        sanitize: false,
        trigger: 'manual',
        template: '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-title"></div><div class="popover-content"></div><div class="popover-buttons"><button class="btn btn-sm">Dismiss all tips</button> <button class="btn btn-primary btn-sm popover-next">Next</button></div></div>',
        viewport: {
            selector: '.content > .container',
            padding: 10
        }
    };

    function showPopover(selector, nextSelector = null) {
        $(selector).popover(opts).popover('show');

        $('.popover-next').click(function() {
            $(selector).popover('hide');

            if (nextSelector) {
                showPopover(nextSelector);
            }
        });
    }

    showPopover('#create-project', '#import-project')
}
