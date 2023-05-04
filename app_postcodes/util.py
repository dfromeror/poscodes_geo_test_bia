import geopy

def get_zipcode(lat, lon):

    geo_locator = geopy.Nominatim(user_agent='1234')
    r = geo_locator.reverse((lat, lon))
    return r.raw['address']['postcode']