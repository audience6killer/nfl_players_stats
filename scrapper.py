import requests
import json
from bs4 import BeautifulSoup, ResultSet

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def clean_text(text: str):
    return text.replace('\n', '').replace('\t', '')


class Scrapper(BeautifulSoup):
    def __init__(self, page_url: str):
        self.request = requests.get(url=page_url, headers=HEADERS)
        super().__init__(self.request.text, 'html.parser')

    def get_by_tag_and_class(self, filters: list, remove_spaces=False) -> list:
        """This method allows to get content based on a
        tag-class filter. The filters parameter should be a list of tuples (tag, class)"""
        objects = []
        for element in filters:
            objects.append(self.find(element[0], class_=element[1]).get_text())

        return objects

    def get_all_by_filter(self, filters_keys: list, filters_values: list) -> dict:
        """This method returns a dictionary of results. Find all the instances of
        that matches the filter (tag, class). Then creates a dictionary which key and values
        is determined by the dict_params (key, value)"""
        values = []
        keys = []

        if len(filters_values) != 1:
            raw_values = self.find_all(name=filters_values[0][0], class_=filters_values[0][1])
            values = self.recursive_search(filters=filters_values[1:], values=raw_values)
        else:
            values = self.find_all(name=filters_values[0][0], class_=filters_values[0][1])

        if len(filters_keys) != 1:
            raw_keys = self.find_all(name=filters_keys[0][0], class_=filters_keys[0][1])
            keys = self.recursive_search(filters=filters_keys[1:], values=raw_keys)
        else:
            keys = self.find_all(name=filters_keys[0][0], class_=filters_keys[0][1])

        return {clean_text(key.get_text()): clean_text(value.get_text()) for (key, value) in zip(keys, values)}

    def get_all_by_attribute(self, tag, attr) -> list:
        """This method returns a list of results based on the search of a tag and an attribute
        which will give us its value"""

        raw_values = self.find_all(name=tag)
        values = [value.get(attr) for value in raw_values if value.get(attr)]

        return [clean_text(value) for value in values]

    def get_all_recursive_search(self, filters: list) -> list:

        if len(filters) > 1:
            raw_values = self.find_all(name=filters[0][0], class_=filters[0][1])
            values = self.recursive_search(filters=filters[1:], values=raw_values)
        else:
            values = self.find_all(name=filters[0][0], class_=filters[0][1])

        return [clean_text(value.get_text()) for value in values if value.get_text()]

    def recursive_search(self, filters: list, values) -> list:
        if len(filters) > 0:
            new_values = []
            for value in values:
                # We check whether there is a class to filter or not
                class_ = filters[0][1]
                if class_:
                    new_value = value.find_all(filters[0][0], class_=class_)
                else:
                    new_value = value.find_all(filters[0][0])
                if new_value:
                    if len(new_value) > 1:
                        for i in new_value:
                            new_values.append(i)
                    else:
                        new_values.append(new_value[0])
            return self.recursive_search(filters=filters[1:], values=new_values)
        else:
            return values


