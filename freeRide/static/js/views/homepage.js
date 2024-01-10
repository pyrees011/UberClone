function calculateDistance(pickupAutocomplete, dropAutocomplete) {
    var origin = pickupAutocomplete.getPlace().geometry.location;
    var destination = dropAutocomplete.getPlace().geometry.location;

    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix(
        {
            origins: [origin],
            destinations: [destination],
            travelMode: 'DRIVING', // You can change this to suit your requirements
            unitSystem: google.maps.UnitSystem.METRIC,
            avoidHighways: false,
            avoidTolls: false
        },
        callback
    );
}

function callback(response, status) {
    if (status == 'OK') {
        var origins = response.originAddresses;
        var destinations = response.destinationAddresses;

        for (var i = 0; i < origins.length; i++) {
            var results = response.rows[i].elements;

            for (var j = 0; j < results.length; j++) {
                var element = results[j];
                var distance = element.distance.text;

                var numericDistance = parseFloat(distance.replace(/[^\d.]/g, ''));
                setPrices(numericDistance);
            }
        }
    } else {
        console.log('Error:', status);
    }
}


function setPrices(distance) {
    const green_fare = 6.8;
    const berline_fare = 13.3;
    const van_fare = 19.7;

    const green_price = (distance * green_fare).toFixed(2)
    const berline_price = (distance * berline_fare).toFixed(2)
    const van_price = (distance * van_fare).toFixed(2)

    // console.log(document.getElementById('car_fare').value)
    document.getElementById('car_fare').value = `${green_price}€`;

    document.getElementById('green_price').textContent = `${green_price}€`;
    document.getElementById('berline_price').textContent = `${berline_price}€`;
    document.getElementById('van_price').textContent = `${van_price}€`;
}

$(document).ready(function() {
    // Initialize Google Maps Places Autocomplete for pickup and drop-off input fields
    var pickupInput = document.getElementById('pickup');
    var dropInput = document.getElementById('drop');
    let latStart, longStart, latEnd, longEnd;

    var options = {
        types: ['geocode'],
        componentRestrictions: { country: "fr" } // Restrict results to geographical locations
    };

    var pickupAutocomplete = new google.maps.places.Autocomplete(pickupInput, options);
    var dropAutocomplete = new google.maps.places.Autocomplete(dropInput, options);

    google.maps.event.addListener(pickupAutocomplete, 'place_changed', function() {
        var nearPlace = pickupAutocomplete.getPlace();
        // Use nearPlace details as needed
        console.log('Selected Place:', nearPlace.name);
        latStart =  nearPlace.geometry.location.lat();
        longStart = nearPlace.geometry.location.lng();
    });

    // Similarly, you can add an event listener for the drop-off input if needed
    google.maps.event.addListener(dropAutocomplete, 'place_changed', function() {
        var nearPlace = dropAutocomplete.getPlace();
        // Use nearPlace details as needed
        console.log('Selected Place:', nearPlace.name);
        latEnd = nearPlace.geometry.location.lat();
        longEnd = nearPlace.geometry.location.lng();
        const submit = document.getElementById('submit').removeAttribute('disabled');
        calculateDistance(pickupAutocomplete, dropAutocomplete);
    });

    $('#submit').click(function (e) {
        e.preventDefault();
        // Perform form submission or other actions using the obtained lat/lng values
        setupMap(latStart,longStart,latEnd,longEnd);
        const vehicleType = document.getElementById('custom-vehicle-type');
        const searchForm = document.getElementById('search-form');
        const mapDiv = document.getElementById('map-div');

        searchForm.classList.remove('col-4');
        searchForm.classList.add('col-3');

        mapDiv.classList.remove('col-8');
        mapDiv.classList.add('col-4');
        mapDiv.style.marginRight = '10px';

        vehicleType.classList.add('active');
    });
});




mapboxgl.accessToken = 'pk.eyJ1IjoicmF1bmFrMTEiLCJhIjoiY2xwODZ2d2MyMmVrcTJvcXVuMGd6eHJsNCJ9.Ie3pcZ1ShSAafadHTa5iQw';
navigator.geolocation.getCurrentPosition(successLocation, errorLocation, { enableHighAccuracy: true })

function successLocation(position) {
    setUpMapDefault([position.coords.longitude, position.coords.latitude])
}

function errorLocation() {
    setUpMapDefault([2.349014, 48.864716])
}

function setUpMapDefault(center) {
    var start = { lat: 48.8662294, lng: 2.3077957 };

    mapboxgl.accessToken = 'pk.eyJ1IjoicmF1bmFrMTEiLCJhIjoiY2xwODZ2d2MyMmVrcTJvcXVuMGd6eHJsNCJ9.Ie3pcZ1ShSAafadHTa5iQw';

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [start.lng, start.lat],
        zoom: 14
    });
}

function setupMap(startlat,startlong,endlat, endlong) {
    // example origin and destination
    var start = { lat: startlat, lng: startlong };
    var finish = { lat: endlat, lng: endlong };

    mapboxgl.accessToken = 'pk.eyJ1IjoicmF1bmFrMTEiLCJhIjoiY2xwODZ2d2MyMmVrcTJvcXVuMGd6eHJsNCJ9.Ie3pcZ1ShSAafadHTa5iQw';

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [start.lng, start.lat],
        zoom: 14
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-right');

    var directions = new MapboxDirections({
        accessToken: mapboxgl.accessToken,
        profile: 'mapbox/driving',
        unit: 'metric',
        controls: {
            inputs: false,
            instructions: true,
            profileSwitcher: false
        }
    });

    directions.setOrigin([start.lng, start.lat]);
    directions.setDestination([finish.lng, finish.lat]);
    // directions.setRenderOptions({ routeColor: '#007cbf', routeWidth: 3 });

    map.addControl(directions, 'top-left');

}


let hidden_car = document.getElementById('car_type').value
let hidden_car_fare = document.getElementById('car_fare').value
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.custom-card');

    cards.forEach(function(card) {
        card.addEventListener('click', function() {
            // Remove 'active' class from all menu items
            cards.forEach(function(menuItem) {
                menuItem.classList.remove('active');
            });

            // Add 'active' class to the clicked menu item
            this.classList.add('active');
            hidden_car = card.getAttribute('value');
            hidden_car_fare = card.childNodes[5].textContent;
        });
    });
});

const payment_dropdown = document.getElementById('payment-dropdown');
const payment_options = document.querySelectorAll("#payment-dropdown-options");

payment_options.forEach(function(option) {
    option.addEventListener('click', function() {
        const payment_value = option.getAttribute('data-value');
        payment_dropdown.value = payment_value;
        payment_dropdown.innerHTML = payment_value
    })
})

const book_ride = document.getElementById('book_ride');
book_ride.addEventListener('click', handleClick = () => {
    
    const user_id = document.getElementById('user_id').value;
    const payment_type = document.getElementById('payment-dropdown').value;
    const pickup = document.getElementById('pickup').value;
    const drop = document.getElementById('drop').value;
    const pickup_time = document.getElementById('pickup_time').value;
    const ride_fare = document.getElementById('car_fare').value;

    const dataToSend = {
        'car_type': hidden_car,
        'pickup': pickup,
        'drop': drop,
        'ride_fare': ride_fare,
        'user_id': user_id,
        'payment_type': payment_type,
        'pickup_time': pickup_time,
    };

    // Make AJAX call to Flask route
    fetch('/add_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse the response body as JSON
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        
        const option_car_type = data.car_type;
        const option_request_id = data.request_id;
        // Redirect to the new page using JavaScript after successful request
        window.location.href = `/waiting_page/${option_request_id}/${option_car_type}`; // Replace with the URL you want to redirect to
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error scenarios here
    });
})

function acceptRide(request_id, car_type) {
    // Make AJAX call to Flask route
    fetch('/update_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'request_id': request_id, 'car_type': car_type, 'status': 'accepted' })
    })

    // fetch('/add_ride', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({ 'request_id': request_id, 'driver_id': driver_id })
    // })

    fetch('/add_driver_ride', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'request_id': request_id, 'car_type': car_type })
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse the response body as JSON
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Redirect to the new page using JavaScript after successful request
        window.location.href = `/driver_ongoing_ride/${request_id}/${car_type}`; // Replace with the URL you want to redirect to
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error scenarios here
    });
}

function over_ride(request_id, car_type) {
    fetch('/update_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'request_id': request_id, 'car_type': car_type, 'status': 'finished' })
    })
    
}

