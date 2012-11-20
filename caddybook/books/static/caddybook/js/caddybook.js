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

