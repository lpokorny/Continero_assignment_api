import requests

from logger_config import logger


class TestNasaApi:
    nasa_search_endpoint_url = "https://images-api.nasa.gov/search"
    year_start = 2018
    year_end = 2018
    page_size = 5
    media_type = {"image": "image", "video": "video"}
    keyword_0 = "Mars"
    keyword_1 = "Mars Reconnaissance Orbiter (MRO)"

    def run_nasa_api_search(self, **kwargs):
        parameters = {
            "year_start": kwargs.get("year_start"),
            "year_end": kwargs.get("year_end"),
            "media_type": kwargs.get("media_type"),
            "page_size": kwargs.get("page_size"),
            "keywords": kwargs.get("keywords"),
        }

        response = requests.get(url=self.nasa_search_endpoint_url, params=parameters)
        if response.status_code != 200:
            logger.error("API get request failed")
            raise Exception

        return response.json()

    def test_search_and_print_mars_images(self):
        parameters = {
            "year_start": self.year_start,
            "year_end": self.year_end,
            "media_type": self.media_type["image"],
            "page_size": self.page_size,
            "keywords": (self.keyword_0, self.keyword_1),
        }

        response = self.run_nasa_api_search(**parameters)

        printed_links = []
        for item in response["collection"]["items"]:
            links = item.get("links", [])
            for link in links:
                print(link.get("href"))
                printed_links.append(link.get("href"))

        try:
            assert len(printed_links) == self.page_size
        except AssertionError:
            logger.error(f"Expected {self.page_size} links to be printed, but got "
                         f"{len(printed_links)} links, there is probably not enough matching images")
            raise

        print(f"\n^^^ A total of {len(printed_links)} image links printed into the console ^^^\n\n")

    def test_search_and_check_mars_videos(self):

        parameters = {
            "year_start": self.year_start,
            "year_end": self.year_end,
            "media_type": self.media_type["video"],
            "keywords": self.keyword_0,
            "page_size": self.page_size,
        }

        response = self.run_nasa_api_search(**parameters)

        printed_links = []
        for item in response["collection"]["items"]:
            json_collection_response = requests.get(url=item["href"])
            json_collection = json_collection_response.json()

            mp4_found = False
            for data in json_collection:
                if data.endswith(".mp4"):
                    mp4_found = True
                    printed_links.append(data)
                    print(f"A video link was found within the collection, moving to another item. Link: {data}")
                    break
            try:
                if mp4_found is False:
                    raise Exception("No video link found in the collection")
            except Exception as e:
                logger.error(e)
                raise

        print(f"\n^^^ A total of {len(printed_links)} video links printed into the console ^^^\n\n")


