
(function(hole_map) {
    
    var HoleMapManager = function(config) {

        this.config = config;
        this.container = config.container;

        this.tee_pos = new google.maps.LatLng(config.tee_lat,
            config.tee_lon);

        this.basket_pos = new google.maps.LatLng(
            config.basket_lat, config.basket_lon);

        this.map_options = {
            center: this.tee_pos,
            zoom: 18, // # TODO: Should be calculated, not static
            mapTypeId: google.maps.MapTypeId.ROADMAP,
        };

        this.map = new google.maps.Map(this.container, this.map_options);
        this.buildMarkers();
        this.setCenter();
    };

    HoleMapManager.prototype = {

        setCenter: function() {
            /* We need to create Bounds around the markers
                to center the map on the bound instead of marker */
            var bounds = new google.maps.LatLngBounds();

            bounds.extend(this.tee_pos);
            bounds.extend(this.basket_pos);

            /* This will auto-zoom based on bounds */
            this.map.fitBounds(bounds);

            /* Set the map position  based on boudns */
            this.map.setCenter(bounds.getCenter());
        },

        rebuildMarkers: function() {

            this.tee_basket_line.setMap(null);
            this.tee_marker.setMap(null);
            this.basket_marker.setMap(null);
            this.buildMarkers();
            this.setCenter();

        },
        
        buildMarkers: function() {

            this.tee_basket_line = new google.maps.Polyline({
                path: [this.tee_pos, this.basket_pos],
                strokeColor: 'blue',
                strokeOpacity: .6,
                strokeWeight: 4,
                map: this.map,
            });

            this.tee_marker = new google.maps.Marker({
                position: this.tee_pos,
                map: this.map,
            });

            this.basket_marker = new google.maps.Marker({
                position: this.basket_pos,
                map: this.map,
                icon: this.config.static_url + 'caddybook/img/basket-map-icon.png'
            });

        },
    
    };


    // Assign Manager to the scope
    hole_map.HoleMapManager = HoleMapManager;


}(CADDYBOOK.module('hole_map')));
