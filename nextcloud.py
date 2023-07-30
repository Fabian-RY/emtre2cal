#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jul  8 13:04:24 2023

@author: fabian
"""

import requests

def upload_event(event_data, url:str, username:str, password: str) -> int:
    event_uid, event = event_data
    headers = {'Content-Type':'text/calendar'}
    response = requests.put(url + f'{event_uid}.ics', 
                data=event, 
                headers= headers,
                auth=(username, password))
    return response.status_code

def check_if_event_exists(events, event, url:str, user:str, password:str) -> bool:
    
    return True

def get_events(calendar_url:str, username:str, password:str) -> list:

    # Set up the headers for the request
    headers = {
        'Content-Type': 'application/xml',
        'Depth': '1'
    }
    events_url:str = calendar_url+"?export&accept=jcal"
    # Send the request to get all events in the calendar
    response = requests.get(events_url, headers=headers, auth=(username, password))
    if response.status_code == 200:
        return(response.json())
    else: 
        raise Exception(f"Unable to connect to API at {events_url}")