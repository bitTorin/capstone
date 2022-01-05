function permits(city) {



  fetch()

    url: city_data_url(city),
    type: "GET",
    data: {
      "$$app_token" : "YOURAPPTOKENHERE",
    }

  .then(response => response.json())
  .then(permit => {
    

function city_data_url(city) {
  if city = 'Austin':
    return 'https://data.austintexas.gov/resource/3syk-w9eu.json?permittype=BP&work_class=New'

  // if city = 'Denver':
  //   url = ''
  //
  // if city = 'New York':
  //   url = 'https://data.cityofnewyork.us/resource/rbx6-tga4.json' RESIDENCES ONLY??? https://data.cityofnewyork.us/browse?q=dob+now&sortBy=relevance
  //
  // if city = 'San Francisco':
  //   url = ''

}
