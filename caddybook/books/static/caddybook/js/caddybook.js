(function(window, document, undefined) {
    var mods = {};

    var CADDYBOOK = {
        module: function(name) {
            if (!mods[name]) {
                mods[name] = {};
            }

            return mods[name];
        }
    }

    window.CADDYBOOK = CADDYBOOK;
}(window, document));

(function(caddybook) {

    var AjaxStatusBar = function(container) {
        this.container = container;
        this.span = this.container.find('span');
        this.type = 'warning';
    };

    AjaxStatusBar.prototype = {
        setType: function(type) {
            this.span.removeClass('label-' + this.type);
            this.span.addClass('label-' + type);
            this.type = type;
        },

        setMessage: function(message) {
            this.span.html(message);
        },

        setSuccess: function(message) {
            this.setType('success');
            this.setMessage(message);
            this.show();
            this.container.delay(3000).fadeOut();
        },

        setError: function(message) {
            this.setType('important');
            this.setMessage(message);
            this.show();
            this.container.delay(3000).fadeOut();
        },

        setWarning: function(message) {
            this.setType('warning');
            this.setMessage(message);
            this.show();
        },

        hide: function() {
            this.container.hide();
        },

        show: function() {
            this.container.fadeIn();
        },
    };

    $(function() {
        var ajax_status_bar = new AjaxStatusBar($('.ajax-status-bar'));
        caddybook.ajax_status_bar = ajax_status_bar;
    });

}(CADDYBOOK.module('caddybook')));
