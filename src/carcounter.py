import os
from PIL import Image
from io import BytesIO
import utils
import sk_api
import templatebuilder


class CarCounter:
    """
    Contains methods used to cooperate with sk api to count cars using specific area
    """
    urls = {
        "img_init": "https://spaceknow-imagery.appspot.com/imagery/search/initiate",
        "pipeline_status": "https://spaceknow-tasking.appspot.com/tasking/get-status",
        "img_retrieve": "https://spaceknow-imagery.appspot.com/imagery/search/retrieve",
        "cars_init": "https://spaceknow-kraken.appspot.com/kraken/release/cars/geojson/initiate",
        "cars_retrieve": "https://spaceknow-kraken.appspot.com/kraken/release/cars/geojson/retrieve",
        "imagery_init": "https://spaceknow-kraken.appspot.com/kraken/release/imagery/geojson/initiate",
        "imagery_retrieve": "https://spaceknow-kraken.appspot.com/kraken/release/imagery/geojson/retrieve",
        "getcar_templ": "https://spaceknow-kraken.appspot.com/kraken/grid/{}/cars.png",
        "getimg_temp": "https://spaceknow-kraken.appspot.com/kraken/grid/{}/truecolor.png"
    }

    def __init__(self, credentials, polygon):
        """
        :param credentials:
            dictionary with client id("id"), username("user") and password("pass")
        :param polygon: array of touples
            Contains coordinates for each polygon. Multipolygon is prohibited
        """
        self.polygon = polygon
        self.skapi = sk_api.skapi(credentials)

    def get_scenes(self, start_date, end_date):
        """
        Obtains ids of valid scenes for a given time period
        :param start_date: string
            start date : format "yyyy-MM-dd hh:mm:ss"
        :param end_date: string
            end date : format "yyyy-MM-dd hh:mm:ss"
        :return: array
             list of valid scene ids
        """
        scenes_request_json = templatebuilder.get_scenes_request(start_date, end_date, self.polygon)
        return self.skapi.get_paged(self.urls["img_init"],
                                    scenes_request_json,
                                    self.urls["img_retrieve"],
                                    lambda response: self.__filter_valid_cars_scenes(response["results"])
                                    )

    def __filter_valid_cars_scenes(self, scenes):
        """
        Filters scenes that have valid id
        :param scenes: dict
            dictionary with scene objects
        :return: array
            ids of valid scenes
        """

        def get_gsd(record):
            # the maximum represents the "worst" value to expect in search for gsd
            return max([band["gsd"] for band in record["bands"]])

        scenes_gsds = [(r["sceneId"], get_gsd(r)) for r in scenes]
        # valid (gsd < .55) scenes only
        return [sceneId for sceneId, gsd in scenes_gsds if gsd < .55]

    def get_cars_maps(self, dir_path, scenes):
        """
        Counts cars on each scene and returns its number and image
        :param dir_path: string
            output path
        :param scenes: array of string
            valid scene ids
        :return: array tuples (string, int)
             return array of tuples (path_to_image, car_amount)
        """
        return [self.__get_carmap_info(os.path.join(dir_path, "cars{}.png".format(str(i).zfill(3))), sid) for i, sid in
                enumerate(scenes)]

    def __get_carmap_info(self, img_path, scene_id):
        """
        Count car for a single scene and returns it with image path
        Saves the image along the way, to avoid storing it in memory.
        :param img_path: string
            Path to save image to
        :param scene_id:
            valid sceneId
        :return: tuple (string,int)
            tuple (path_to_image, car_amount)

        """

        cars_tile_info = self.get_kraken_tile_info(scene_id, self.urls["cars_init"], self.urls["cars_retrieve"])
        car_amount = self.count_cars(cars_tile_info)

        imagery_tile_info = self.get_kraken_tile_info(scene_id, self.urls["imagery_init"],
                                                      self.urls["imagery_retrieve"])

        composed_image = self.construct_image_from_tileinfo(cars_tile_info, imagery_tile_info)

        # saving right here since there could be too many images
        composed_image.save(img_path)
        return img_path, car_amount

    def construct_image_from_tileinfo(self, cars_tile_info, imagery_tile_info):
        """
        1)Uses info about tile to download cars.png tiles and truecolor.png
        2)Blend respecive tiles into single image using alpha blending
        3)Composes image from tiles.

        :param cars_tile_info: array
            tile info used to construct kraken cars url
        :param imagery_tile_info: array
            tile info used to construct kraken imagery url
        :return: Image
            image composed from tiles
        """
        imgs = []

        def get_img_from_url(url):
            try:
                response = self.skapi.get(url)
                return Image.open(BytesIO(response.content))
            except:
                return None


        # i need them to be in the same order no matter what
        both_tile_info = zip(sorted(cars_tile_info, key=lambda x: str(x[3]) + str(x[4]))
                             , sorted(imagery_tile_info, key=lambda x: str(x[3]) + str(x[4])))
        for cars_ti, imagery_ti in both_tile_info:
            cars_url = self.urls["getcar_templ"].format("/".join(cars_ti))
            cars_img = get_img_from_url(cars_url)

            imagery_url = self.urls["getimg_temp"].format("/".join(imagery_ti))
            imagery_img = get_img_from_url(imagery_url)

            blended = Image.blend(imagery_img, cars_img, .6)
            tile_xy = (cars_ti[3], cars_ti[4])
            imgs.append((tile_xy, blended))

        new_im = utils.construct_image(imgs)
        return new_im

    def count_cars(self, cars_tile_info):
        """
        Count cars on respective tile
        :param cars_tile_info: array
            uses tileinfo to obtain car number
        :return: int
            car umber
        """
        detection_url_template = "https://spaceknow-kraken.appspot.com/kraken/grid/{}/detections.geojson"
        detection_urls = [detection_url_template.format("/".join(tile_data)) for tile_data in cars_tile_info]
        count = 0
        for url in detection_urls:
            response = self.skapi.get(url)
            feature_json = utils.decode_content(response)

            presumed_cars_list = [(f.get("properties", {}).get("class", ""), f.get("properties", {}).get("count", 0))
                                  for f in
                                  feature_json.get("features", {})]
            presumed_cars_amount = sum([count for cls, count in presumed_cars_list if cls == "cars"])
            count = count + presumed_cars_amount
        return count

    def get_kraken_tile_info(self, scene_id, url_init, url_retrieve):
        """
        Downloads tile infos about scene.

        :param scene_id: string
            valid sceneId
        :param url_init: string
            url of init endpoint
        :param url_retrieve: string
            url of retrieve endpoint
        :return: array
            5 tile parameters
            [map_id, geometry_id, zoom, x, y]
        """

        kraken_init_json = templatebuilder.get_kraken_init_request(scene_id, self.polygon)

        def process(response):
            map_id = response["mapId"]
            geometry_id = "-"
            tile_info_array = []
            for tile in response["tiles"]:
                # todo replace with some structure
                tile_info = [map_id, geometry_id, str(tile[0]), str(tile[1]), str(tile[2])]
                tile_info_array.append(tile_info)
            return tile_info_array

        return self.skapi.get_paged(url_init, kraken_init_json, url_retrieve, process)

