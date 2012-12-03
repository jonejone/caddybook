(function(course) {

    /* Course stuff here */

    var CourseMap = function(config) {

        this.config = config;

        this.map_options = {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 18,
            center: this.getLatLng(this.config.holes[0].tee_pos),
        };

        this.map = new google.maps.Map(this.config.container,
            this.map_options);

        this.bounds = new google.maps.LatLngBounds();
        this.buildMarkers();
        this.setCenter();
    };

    CourseMap.prototype = {

        setCenter: function() {
            this.map.fitBounds(this.bounds);
            this.map.setCenter(this.bounds.getCenter());
        },

        getIconUrl: function(hole) {
            return 'http://chart.apis.google.com/chart?chst=d_map_pin_letter_withshadow' +
                '&chld=' + hole.hole_position + '|FF0000|000000';
        },

        buildMarkers: function() {
            $.each(this.config.holes, function(i, item) {
                if(item.tee_pos.lat && item.basket_pos.lat) {

                    var tee_pos = this.getLatLng(item.tee_pos);
                    var basket_pos = this.getLatLng(item.basket_pos);

                    var basket_marker = new google.maps.Marker({
                        position: basket_pos,
                        map: this.map,
                        icon: '/static/caddybook/img/basket-map-icon.png'
                    });

                    var tee_marker = new google.maps.Marker({
                        position: tee_pos,
                        map: this.map,
                        icon: this.getIconUrl(item),
                    });

                    var tee_basket_line = new google.maps.Polyline({
                        path: [tee_pos, basket_pos],
                        strokeColor: 'blue',
                        strokeOpacity: .6,
                        strokeWeight: 4,
                        map: this.map,
                    });

                    this.bounds.extend(basket_pos);
                    this.bounds.extend(tee_pos);
                }
            }.bind(this));
        },

        getLatLng: function(pos) {
            return new google.maps.LatLng(pos.lat, pos.lon);
        },
    };

    course.CourseMap = CourseMap;

}(CADDYBOOK.module('course')));
