
(function(hole_map) {
    
    var HoleMapManager = function(container, tee_lat, tee_lon,
        basket_lat, basket_lon) {

        this.container = container;
        this.tee_pos = new google.maps.LatLng(tee_lat, tee_lon);
        this.basket_pos = new google.maps.LatLng(basket_lat,
            basket_lon);

        this.map_options = {
            center: this.tee_pos, // TODO: Should be in center of tee/basket
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

            this.map.setCenter(bounds.getCenter());
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


}(CADDYBOOK.module('hole_map')))


$(function() {

        
    /*

    var container = $('#hole-map-container').get(0);
    
    var tee_lat = {{ hole.tee_pos.latitude }};
    var tee_lon = {{ hole.tee_pos.longitude }};
    var basket_lat = {{ hole.basket_pos.latitude }};
    var basket_lon = {{ hole.basket_pos.longitude }};

    var tee_position = new google.maps.LatLng(
        tee_lat, tee_lon);

    var basket_position = new google.maps.LatLng(
        basket_lat, basket_lon);

    
    var options = {
        center: tee_position,
        zoom: 18,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    
    var map = new google.maps.Map(container, options);


     $('#hole-tabs a:last').tab('show'); 

     */
});

