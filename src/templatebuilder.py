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


def get_kraken_init_request(sceneId,polygon):
    return {
        "sceneId": sceneId,
        "extent": {
            "type": "Polygon",
            "coordinates": [polygon]
        }
    }
