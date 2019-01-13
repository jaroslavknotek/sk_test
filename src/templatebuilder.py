def get_scenes_request(startDate, endDate, polygon):
    return {
        "provider": "gbdx",
        "dataset": "idaho-pansharpened",
        "startDatetime": startDate,
        "endDatetime": endDate,
        "extent": {
            "type": "GeometryCollection",
            "geometries": [
                {
                    "type": "Polygon",
                    "coordinates": [polygon]
                }
            ]
        }
    }

def get_auth_template( id,user,password):
    return {
        "client_id": id,
        "username": user,
        "password": password,
        "connection": "Username-Password-Authentication",
        "grant_type": "password",
        "scope": "openid"
    }

def get_kraken_init_request(sceneId, polygon):
    return {
        "sceneId": sceneId,
        "extent": {
            "type": "Polygon",
            "coordinates": [polygon]
        }
    }
