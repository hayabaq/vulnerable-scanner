#!/usr/bin/env python
import requests
from BeautifulSoup import BeautifulSoup
def requests(url): ...

target_url = "http://10.0.2.20/mutillidae/index.php?page=dns-lookup.php"
response = requests(target_url)
parsed_html = BeautifulSoup(response.content)
forms_list = parsed_html.findAll("form")
for form in forms_list:
    action = form.get("action")
    print(action)
    method = form.get("method")
    print(method)
    input_list = form.findAll("input")
    for input in input_list:
        input_name = input.get("name")
        print(input_name)
