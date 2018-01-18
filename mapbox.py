from mapbox import Directions

service = Directions(access_token="pk.eyJ1IjoibXVraWxhbmUiLCJhIjoiY2pibTFlcG4wNHFtaDJxcWdubW4wY2lybSJ9.-IOHNJU3H9XrPrqLwG0qhQ")

origin = {
	'type': 'Feature',
	'properties': {'name': 'Portland, OR'},
	'geometry': {
		'type': 'Point',
		'coordinates': [-122.7282, 45.5801]
	}
}
destination = {
	'type': 'Feature',
	'properties': {'name': 'Bend, OR'},
	'geometry': {
		'type': 'Point',
		'coordinates': [-121.3153, 44.0582]
	}
}
response = service.directions([origin, destination], 'mapbox.walking')
print(response.json())

