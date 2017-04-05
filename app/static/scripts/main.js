var Utils = {
    renderFieldErrorTooltip: function (selector, msg, placement) {
        var elem;
        if (typeof placement === 'undefined') {
            placement = 'right'; // default to right-aligned tooltip
        }
        elem = $(selector);
        elem.tooltip({'title_en_US': msg, 'trigger': 'manual', 'placement': placement});
        elem.tooltip('show');
        elem.addClass('error');
        elem.on('focus click', function(e) {
            elem.removeClass('error');
            elem.tooltip('hide');
        });
    }
};


/* SIDENAV */

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function toggleNav() {
    $('#maincontent').toggleClass('show_aside');

      $('.text_sidebar').toggle(300);
}



/* Your custom JavaScript here */

