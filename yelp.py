import rauth
import requests

def main():

  origin = "ORIGIN"
  destination = "DESTINATION"

  route = get_route(origin, destination)
  mileage = 0.0

  for step in route["routes"][0]["legs"][0]["steps"]:
    restaurants = find_restaurants(step["end_location"]["lat"], step["end_location"]["lng"], "thai")
    mileage += step["distance"]["value"]

    if len(restaurants) > 0:
      # print step["end_location"]["lat"], step["end_location"]["lng"]
      print round(mileage/1609, 2), "miles away"

    for restaurant in restaurants:
      print restaurant

    if len(restaurants) > 0:
      print "\n"

def set_yelp_params(lat, lng, term):
  params = {}
  params["term"] = term
  params["ll"] = "{},{}".format(str(lat),str(lng))
  params["radius_filter"] = "1609"
  params["limit"] = "6"
  params["sort"] = "2"
  return params

def find_restaurants(lat, lng, term):

  # set yelp params
  params = set_yelp_params(lat, lng, term)

  # keys/tokens
  consumer_key = "CONSUMER KEY"
  consumer_secret = "CONSUMER SECRET"
  token = "TOKEN"
  token_secret = "TOKEN SECRET"

  # create session
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)

  # make and format request
  request = session.get("http://api.yelp.com/v2/search", params=params)
  session.close()

  json = request.json()
  return create_restaurant_list(json)


def create_restaurant_list(json):

  # create a list of names
  names = []
  restaurants = json["businesses"]

  # add names to list
  for x in range(len(restaurants)-1):
    names.insert(x, restaurants[x]["name"].encode('utf-8'))
  return names

def get_route(origin, destination):
  params = {}
  params["origin"] = origin
  params["destination"] = destination
  params["key"] = "KEY"

  request = requests.get("https://maps.googleapis.com/maps/api/directions/json", params=params)

  data = request.json()
  return data

main()
