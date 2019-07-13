from math import sin, cos, sqrt, atan2, radians



def distpy(la1,la2,lng1,lng2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(la1)
    lon1 = radians(la2)
    lat2 = radians(lng1)
    lon2 = radians(lng2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    print(distance)
    return distance