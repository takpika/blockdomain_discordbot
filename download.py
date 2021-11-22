# -*- coding: utf-8 -*-
import requests
import re
import os
import json

cwd = os.getcwd()

with open(cwd+"/blocklist_urls.txt", "r") as f:
    block_list_urls = f.read().split("\n")

with open(cwd+"/config.json", "r") as f:
    config = json.load(f)

path = config["list_path"]

def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def delete_comment(text):
    text = re.sub(r'#.*', '', text)
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
    return text

def check_list_type(text):
    # type 1: domain
    # type 2: ip domain
    # type 3: local-data: "domain. IN A ip"
    if "local-data:" in text:
        return 3
    elif "0.0.0.0" in text or "127.0.0.1" in text:
        return 2
    else:
        return 1

def parse_list_type1(text):
    text = delete_comment(text)
    # remove empty line
    text = text.replace("\t", "").replace(" ", "").replace('"', "").replace("\r","")
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
    return text

def parse_list_type2(text):
    text = delete_comment(text)
    # remove ip address
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '', text)
    text = text.replace("\t", "").replace(" ", "").replace('"', "").replace("\r","")
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
    return text

def parse_list_type3(text):
    text = delete_comment(text)
    text = re.sub(r'local-data:\s*"', '', text)
    text = re.sub(r'"\s*$', '', text)
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '', text)
    text = re.sub(r'\s*IN\s*A\s*', '', text)
    text = text[:-1]
    text = text.replace("\t", "").replace(" ", "").replace('"', "").replace("\r","")
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
    return text

def remove_local(text):
    local_domains = ["localhost", "localhost.localdomain", "local", "broadcasthost", "ip6-localhost", "ip6-loopback", "ip6-localnet", "ip6-mcastprefix", "ip6-allnodes", "ip6-allrouters", "ip6-allhosts"]
    for domain in local_domains:
        text = re.sub(r'.*%s$' % (domain), '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
    return text

if __name__ == "__main__":
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(len(block_list_urls)):
        text = download(block_list_urls[i])
        if text is None:
            print("[-] Download failed")
            continue
        if check_list_type(text) == 1:
            text = parse_list_type1(text)
        elif check_list_type(text) == 2:
            text = parse_list_type2(text)
        elif check_list_type(text) == 3:
            text = parse_list_type3(text)
        else:
            continue
        text = remove_local(text)
        with open(path+"block_list_%d.txt" % (i + 1), "w") as f:
            f.write(text)
        print("[+] Downloaded %d" % (i + 1))