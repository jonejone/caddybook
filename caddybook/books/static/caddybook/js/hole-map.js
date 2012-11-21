
(function(hole_map) {
    
    var HoleMapManager = function(container, tee_lat, tee_lon,
        basket_lat, basket_lon) {

        this.container = container;
        this.tee_pos = new google.maps.LatLng(tee_lat, tee_lon);
        this.basket_pos = new google.maps.LatLng(basket_lat,
            basket_lon);

        this.map_options = {
            center: this.tee_pos,
            zoom: 18, // # TODO: Should be calculated, not static
            mapTypeId: google.maps.MapTypeId.ROADMAP,
        };

        // TEMP
        $('#hole-tabs a:last').tab('show');

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
                icon: '/static/caddybook/img/basket-map-icon.png'
            });

        },
    
    };


    // Assign Manager to the scope
    hole_map.HoleMapManager = HoleMapManager;


}(CADDYBOOK.module('hole_map')));
