# -*- coding: utf-8 -*-
import discord
import re, os, json

cwd = os.getcwd()

with open(cwd+"/config.json", "r") as f:
    config = json.load(f)

discord_TOKEN = config["discord_token"]
client = discord.Client()
path = config["list_path"]
if path[0] != "/":
    if path[0] == ".":
        path = cwd + path[1:]
    else:
        path = cwd + "/" + path
if path[-1] != "/":
    path += "/"
block_domains = []

def parse_url(text):
    url_list = []
    url_pattern = re.compile(r'http[s]?://[\w/:%#\$&\?\(\)~\.=\+\-]+')
    url_list = url_pattern.findall(text)
    return url_list

def parse_domain(url):
    domain = ""
    domain_pattern = re.compile(r'https?://([\w/:%#\$&\?\(\)~\.=\+\-]+)')
    domain = domain_pattern.search(url).group(1).split("/")[0]
    return domain

def load_list(path):
    file_list = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            file_list.append(file)
    for file in file_list:
        with open(path + file, "r") as f:
            domains = f.read().split("\n")
            domains = list(filter("", domains))
            block_domains.extend(domains)

@client.event
async def on_ready():
    print("Discord: ログインしました")
    load_list(path)
    print(len(block_domains))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    urls = parse_url(message.content)
    domains = [parse_domain(url) for url in urls]
    if any(domain in block_domains for domain in domains):
        if config["send_reply"] == 1 and config["delete"] != 1:
            await message.channel.send("注意: このサイトは危険な可能性があります。")
        if config["delete"] == 1:
            await message.delete()
            print("Discord: メッセージを削除しました")
            if config["send_reply"] == 1:
                mention = ""
                if config["mention"] == 1:
                    mention = message.author.mention
                await message.channel.send(mention+"送信されたメッセージに危険性のあるURLが含まれていたため、メッセージを削除しました。")

if __name__ == "__main__":
    client.run(discord_TOKEN)