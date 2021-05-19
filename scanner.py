#!/usr/bin/env python
import requests 
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links
 
    def extract_links_from(self, url):
        #response = self.session.get(url)
        #x = response.content
        #x= x.decode(errors= "ignore")
        #print(x)
        #z= re.findall('(?:href=")(.*?)"', x)
        #print(z)
        #return z
        response = self.session.get(url)
        links=[]
        parsed_html = BeautifulSoup(response.content.decode(errors= "ignore"),features="html.parser")
        #print(parsed_html.findAll("a"))
        for a_tag in parsed_html.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue 
            links.append(href)
        #print(links)
        return links
 
    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links= self.extract_links_from(url)
        #print(href_links)
        for link in href_links:
            link = urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        #response= response.content.decode()
        parsed_html = BeautifulSoup(response.content.decode(errors= "ignore"),features="html.parser")
        #print(parsed_html.findAll("form"))
        return parsed_html.findAll("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
        method = form.get("method")
        input_list = form.findAll("input")
        post_data= {}
        for input in input_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name]= input_value
            if method== "post":
                return self.session.post(post_url, data=post_data)
            return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n\n[+] Testing form in " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("[***] XSS discovered in " + link + " in the following form")
                    print(form)
                else:
                    print("[*] Not Vulnerable to XSS")

            if "=" in link:
                print("\n\n[+] Testing " + link)
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print("[***] Discovered XSS in " + link)
                else:
                    print("[*] Not Vulnerable to XSS")
        
    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('test)</scriPt>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content.decode(errors= "ignore")

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('test)</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content.decode(errors= "ignore")
