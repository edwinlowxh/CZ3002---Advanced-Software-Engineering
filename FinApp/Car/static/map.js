var createTripSourceMarker;
var createTripDestinationMarker;
var createTripMap;
var updateTripSourceMarker;
var updateTripDestinationMarker;
var updateTripMap;

export function setUpdateTripSourceMarker(formQueryId, inputFieldId, latLong, title){
    updateTripSourceMarker = new google.maps.Marker({
        position: latLong,
        map: updateTripMap,
        icon: 'http://www.google.com/mapfiles/dd-start.png',
        title: title,
        draggable: true
    })

    google.maps.event.addListener(updateTripSourceMarker, 'dragend', function() {
        var position = updateTripSourceMarker.getPosition();
        $(`#${formQueryId} #${inputFieldId}-lat`).val(position.lat());
        $(`#${formQueryId} #${inputFieldId}-long`).val(position.lng());
        document.querySelector(`#${formQueryId} #${inputFieldId}-lat`).value = position.lat();
        document.querySelector(`#${formQueryId} #${inputFieldId}-long`).value = position.lng();
    });

    document.querySelector(`#${formQueryId} #${inputFieldId}-lat`).value = updateTripSourceMarker.getPosition().lat();
    document.querySelector(`#${formQueryId} #${inputFieldId}-long`).value = updateTripSourceMarker.getPosition().lng();
}

export function setUpdateTripDestinationMarker(formQueryId, inputFieldId, latLong, title){
    updateTripDestinationMarker = new google.maps.Marker({
        position: latLong,
        map: updateTripMap,
        icon: 'http://www.google.com/mapfiles/dd-start.png',
        title: title,
        draggable: true
    })

    google.maps.event.addListener(updateTripDestinationMarker, 'dragend', function() {
        var position = updateTripDestinationMarker.getPosition();
        $(`#${formQueryId} #${inputFieldId}-lat`).val(position.lat());
        $(`#${formQueryId} #${inputFieldId}-long`).val(position.lng());
        document.querySelector(`#${formQueryId} #${inputFieldId}-lat`).value = position.lat();
        document.querySelector(`#${formQueryId} #${inputFieldId}-long`).value = position.lng();
    });

    document.querySelector(`#${formQueryId} #${inputFieldId}-lat`).value = updateTripDestinationMarker.getPosition().lat();
    document.querySelector(`#${formQueryId} #${inputFieldId}-long`).value = updateTripDestinationMarker.getPosition().lng();
}

function searchBox(map, formQueryId, inputFieldId, markerName){
    const input = document.querySelector(`#${formQueryId} #${inputFieldId}`);
    const searchBox = new google.maps.places.SearchBox(input);   
    

    google.maps.event.addListener(searchBox, 'places_changed', function() {
        var place = searchBox.getPlaces()[0];

        const markerNameMap = {
            "createTripSourceMarker": createTripSourceMarker,
            "createTripDestinationMarker": createTripDestinationMarker,
            "updateTripSourceMarker": updateTripSourceMarker,
            "updateTripDestinationMarker": updateTripDestinationMarker
        }

        var marker = markerNameMap[markerName];

        if (!place.geometry) {
            return;
        }
        if (marker) {
            marker.setPosition(place.geometry.location);
        } else {
            marker = new google.maps.Marker({
                position: place.geometry.location,
                map: map,
                icon: 'http://www.google.com/mapfiles/dd-start.png',
                title: place.name,
                draggable: true
            });

            google.maps.event.addListener(marker, 'dragend', function() {
                var position = marker.getPosition();
                $(`#${formQueryId} #${inputFieldId}-lat`).val(position.lat());
                $(`#${formQueryId} #${inputFieldId}-long`).val(position.lng());
                document.querySelector(`#${formQueryId} #${inputFieldId}-lat`).value = position.lat();
                document.querySelector(`#${formQueryId} #${inputFieldId}-long`).value = position.lng();
            });
        }
        document.querySelector(`#${formQueryId} #${inputFieldId}-lat`).value = marker.getPosition().lat();
        document.querySelector(`#${formQueryId} #${inputFieldId}-long`).value = marker.getPosition().lng();
    });
}

export function initMap() {    
    // Create the map
    createTripMap = new google.maps.Map(document.getElementById('create-trip-map'), {
        center: {lat: 1.3521, lng: 103.8198},
        zoom: 11
    });

    updateTripMap = new google.maps.Map(document.getElementById('update-trip-map'), {
        center: {lat: 1.3521, lng: 103.8198},
        zoom: 11
    });
    
    // Add a search boxes
    searchBox(createTripMap, 'create-trip-form', 'source', 'createTripSourceMarker');
    searchBox(createTripMap, 'create-trip-form', 'destination', 'createTripDestinationMarker');
    searchBox(updateTripMap, 'update-trip-form', 'source', 'updateTripSourceMarker');
    searchBox(updateTripMap, 'update-trip-form', 'destination', 'updateTripDestinationMarker');
}

window.initMap = initMap;