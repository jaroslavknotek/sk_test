import time
import requests
import utils


class skapi:
    """
    Contains lowlevel data and methods required to cooperate with spaceknow api
    """

    urls = {
        "pipeline_status": "https://spaceknow-tasking.appspot.com/tasking/get-status",
    }
    header = None

    def __init__(self, credentials):
        """

        :param credentials:
        dictionary with client id("id"), username("user") and password("pass")
        """
        self.auth_json = {
            "client_id": credentials["id"],
            "username": credentials["user"],
            "password": credentials["pass"],
            "connection": "Username-Password-Authentication",
            "grant_type": "password",
            "scope": "openid"
        }

    def get_paged(self, init_url, request_json, retrieve_url, process_response):
        """
        Works with async api.
        1) initiates job
        2) waits for it to finish
        3) get result using 'process_response' funciton
        4) if the result is paged, than it retrieves new page using cursor and repeates step 1
        :param init_url: string
            url that should be called to initiaite job
        :param request_json: dict
            request of initiaition
        :param retrieve_url:
            url of task retrieval
        :param process_response:
            function that is called on retrieved response
        :return:
        """
        results = []
        while True:
            init_json = self.post(init_url, request_json)
            pipeline_id, next_try = self.__init(init_json)
            self.__wait(pipeline_id, next_try)
            retrieved_content = self.post(retrieve_url, json={"pipelineId": pipeline_id})

            results = results + process_response(retrieved_content)

            cursor = retrieved_content.get("cursor", None)
            request_json["cursor"] = cursor

            if cursor is None:
                break
        return results

    def __init(self, response):
        """
        Initialize pipeline job
        :param response: dict
            generic dictionary containing pipelineId
        :return: (string,int)
            pipelineId and next_try
        """
        pipeline_id = response["pipelineId"]
        # todo perform numerical check
        next_try = int(response["nextTry"])
        return pipeline_id, next_try

    def __wait(self, pipeline_id, next_try):
        """
        Waits until pipeline has finished
        :param pipeline_id: string
            Id of the pipeline
        :param next_try:
            number of seconds it should wait until next call
        :return:
        """
        status = 'PROCESSING'
        while status == 'PROCESSING':
            time.sleep(next_try)
            status_json = self.post(self.urls["pipeline_status"], json={"pipelineId": pipeline_id})
            status = status_json["status"]
            next_try = int(status_json.get("nextTry", "5"))

        if status != "RESOLVED":
            raise ValueError("Error during searching for images")

    def post(self, url, json):
        """
        Performs authenticated POST request
        :param url: url
        :param json: request payload
        :return: dict
            response body
        """
        self.__authenticate()
        response = requests.post(url, json=json, headers=self.header)
        return utils.decode_content(response)

    def get(self, url):
        """
        Performs GET request
        :param url: url
        :return: response
        """
        return requests.get(url)

    def __authenticate(self):
        """
        Obtains token according to input credential. Token is cached. It might expire.
        Throws error upon invalid authentication
        """

        if self.header:
            # todo handle token expiration
            return

        url_authorized = "https://spaceknow.auth0.com/oauth/ro"
        auth = requests.post(url_authorized, json=self.auth_json)
        decoded = utils.decode_content(auth)
        if "id_token" not in decoded:
            # todo use more precise exception
            raise ValueError("Authentication was unsuccessful!")

        token = decoded["id_token"]
        self.header = {"authorization": "Bearer " + token,
                       "content-type": "application/json;charset=utf-8"}
