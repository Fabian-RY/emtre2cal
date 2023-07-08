#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jul  8 13:04:15 2023

@author: fabian
"""

import collections
import json
import requests
import datetime
from icalendar import Event as iCalEvent
from icalendar import Calendar as iCalCalendar
import uuid

LOCALIDAD =  "{localidad}"
LOCALIDAD2 = "localidad"
DIRECCION = "direccion"
DESDE = "{desde}"
HASTA = "{hasta}"
HOY = "hoy"
UBICACION = "ubicacion"
CP="cp"
FECHA="fechaPlanificada"
NOMBRE = "nombreEcoparque"
LATITUD = "latitud"
LONGITUD = "longitud"

def format_date_time(date):
    day = str(date.day) if date.day >= 10 else "0"+str(date.day)
    month = str(date.month) if date.month >= 10 else "0"+str(date.month)
    year = str(date.year)
    return str(day)+str(month)+ str(year)

def build_api_link(baselink, city, from_date, to_date):
    if from_date == HOY:
        from_date = datetime.datetime.today()
    to_date = from_date + datetime.timedelta(days=int(to_date))
    from_date = format_date_time(from_date)
    to_date = format_date_time(to_date)
    link = baselink.replace(LOCALIDAD, city)
    link = link.replace(DESDE, from_date)
    return link.replace(HASTA, to_date)

def get_api_results(link, verify=False):
    data = requests.get(link, verify=verify)
    data.raise_for_status()
    return json.loads(data.content)
    pass

def parse_api_results(json_api, filtro):
    for key in json_api:
        ubi = key[UBICACION]
        if(filtro[LOCALIDAD2] is not None and
           ubi[LOCALIDAD2] != filtro[LOCALIDAD2]):
            print(f"Filtered by localidad: {LOCALIDAD2}")
            continue
        elif (filtro[CP] is not None and ubi[CP] != filtro[CP]):
            print(f"Filtered by CP: {filtro[CP]}")
            continue
        direccion = ubi[DIRECCION]
        fecha = key[FECHA].split("/")
        fecha = fecha[2]+fecha[1]+fecha[0]
        lat= ubi[LATITUD]
        long = ubi[LONGITUD]
        event_uid = str(uuid.uuid4())
        event_name = key["nombreEcoparque"]
        event_description = "Localización de Ecoparques moviles en València"
        event_ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ExampleCorp//ExampleCalDAVClient//EN
BEGIN:VEVENT
UID:{event_uid}
DTSTAMP;VALUE=DATE:{fecha}
DTSTART;VALUE=DATE:{fecha}
GEO:{lat};{long}
LOCATION: {ubi[DIRECCION]}
SUMMARY:Ecoparque Movil {ubi[DIRECCION]}
DESCRIPTION:{event_description}
END:VEVENT
END:VCALENDAR
"""     
        #print(event_ics)
        yield (event_uid, event_ics)
    return list()
