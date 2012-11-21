(function(hole) {

    var HoleSetGeoPosition = function(config) {
        this.config = config;
        this.field = config.field;
        this.url = config.url;
        this.position = null;
        this.status_bar = CADDYBOOK.module('caddybook').ajax_status_bar;
        this.initialize();
    };

    HoleSetGeoPosition.prototype = {

        initialize: function() {
            if(!navigator.geolocation) {
                return false;
            }

            this.status_bar.setWarning('Waiting for location...');

            navigator.geolocation.getCurrentPosition(function(pos) {
                this.position = pos;
                this.save();
            }.bind(this), function() {
                /* Error callback */
                this.status_bar.setError('Unable to get location! Turn on GPS?');
            }.bind(this), {
                /* Options for geolocation */
                enableHighAccuracy: true,
                timeout: 50000,
                maximumAge: 0,
            });
        },

        save: function() {

            this.status_bar.setWarning('Saving location to server...');

            var req_data = {
                'csrfmiddlewaretoken': this.config.csrf_token,
                'lat': this.position.coords.latitude,
                'lon': this.position.coords.longitude,
                'field_id': this.field,
            };

            $.post(this.url, req_data, function(data, textStatus) {
                if(data.success) {
                    this.status_bar.setSuccess(
                        'Position saved! New distance for this hole: ' +
                        data.distance + ' meters');
                } else {
                    this.status_bar.setError('Unable to save position...');
                }
            }.bind(this), 'json');
        },
    };

    hole.HoleSetGeoPosition = HoleSetGeoPosition;

}(CADDYBOOK.module('hole')));
