function initOverlays(url_name) {
    var baseurl = $('meta[name="baseurl"').attr('content');
    var csrftoken = getCookie('csrftoken');
    var opts = {
        html: true,
        sanitize: false,
        trigger: 'manual',
        template: '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-title"></div><div class="popover-content"></div></div>',
        viewport: {
            selector: '.content > .container',
            padding: 10
        }
    };

    function showPopover(response) {
        $('[data-overlay]').popover('hide');
        $('[data-overlay="' + response.overlay + '"]').popover(opts).popover('show');

        $('.popover-next').unbind().click(function() {
            fetchResponse('next');
        });
        $('.popover-dismiss').unbind().click(function() {
            fetchResponse('dismiss');
        });

        if (response.last) {
            $('.popover-next').hide();
            $('.popover-dismiss').addClass('btn-primary');
        }
    }

    function getCookie(name) {
        // from https://docs.djangoproject.com/en/stable/ref/csrf/
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function fetchResponse(action) {
        $.ajax({
            url: baseurl + 'api/v1/overlays/overlays/' + url_name + '/' + action + '/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: showPopover
        });
    }

    fetchResponse('current');
}
