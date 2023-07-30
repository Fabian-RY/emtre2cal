#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jul  8 13:03:21 2023

@author: fabian
"""

import argparse
import collections

import sys
import json
import logging

import emtre
import nextcloud

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="config", type=str, default=None)
    return parser.parse_args()


def parse_parameters(config_file_path: str):
    with open(config_file_path) as fhand:
        config = json.load(fhand)
    return config

def check_arguments(arguments: argparse.ArgumentParser):
    if arguments.config is None:
        print("No config added, ples add info with -c")
        sys.exit(-1)
        

def logging_conf():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Starting log")
    pass

def main():
    arguments = parseargs()
    check_arguments(arguments)
    logging_conf()
    config = parse_parameters(arguments.config)
    link = emtre.build_api_link(config["emtre_url"], config["localidad"], 
                                config["desde"], int(config["hasta"]))
    logging.info(f"Connecting to EMTRE api at: {link}")
    json_results = emtre.get_api_results(link)
    logging.info(f"Obtained {len(json_results)} events")
    # Giving None to default dict produces a standard dict. With a lambda
    # we can use None as the default value
    filtro = collections.defaultdict(lambda: None)
    filtro["cp"] = config["cp"]
    parsed_info = emtre.parse_api_results(json_results, 
                                          filtro) 
    url = f"""{config['nextcloud_url']}/{config['username']}/{config['calendar']}/"""
    logging.info(f"Events will be saved in {url}")
    current_events = nextcloud.get_events(url, config['username'], config["password"])
    for event in parsed_info:
        if (nextcloud.check_if_event_exists(current_events, event, url, config['username'], config["password"])):
            logging.info("Event already saved")
            continue
        logging.info("Event will be save as {event.id}")
        code = nextcloud.upload_event(event, url, 
                 config["username"], config["password"])
        

if __name__=="__main__":
    main()