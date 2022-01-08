from dotenv import dotenv_values
from typing import List
from time import sleep
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import http.client
import json

connection = http.client.HTTPSConnection("cs.deals")


def request_status(ids: List[str]):
    for rid in ids:
        payload = "{\"requestIds\":[%d]}" % int(rid)
        headers = {'content-type': "application/json"}
        connection.request("POST", "/API/IScreenshots/GetByRequestIDs/v1", payload, headers)
        res = connection.getresponse()
        data = res.read().decode("utf-8")
        print(data)
        return rid, json.loads(data)


def queue_inspect(inspect_url: str):
    payload = '{"links":["%s"]}' % inspect_url
    headers = {'content-type': "application/json"}
    connection.request("POST", "/API/IScreenshots/QueueScreenshots/v1", payload, headers)
    res = connection.getresponse()
    data = json.loads(res.read().decode("utf-8"));
    if data['success']:
        requests = data['response']['requests']
        ids: List[str] = []
        for key in requests:
            ids.append(requests[key]['requestId'])
        return ids
    else:
        return ['error']




