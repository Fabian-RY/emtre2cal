#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jul  8 13:04:24 2023

@author: fabian
"""

import requests

def upload_event(event_data, url, username, password):
    event_uid, event = event_data
    headers = {'Content-Type':'text/calendar'}
    response = requests.put(url + f'{event_uid}.ics', 
                data=event, 
                headers= headers,
                auth=(username, password))
    return response.status_code