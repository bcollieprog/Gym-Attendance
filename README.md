# Gym-Attendance
## Background 
For years now I have been going to the gym routinely. 
In recent times, I have encountered a question repeatedly; which gym should go to? 
The gym I am a member of, "Revo Gym", has many locations across Perth and Australia. In recent years, their membership has grown so dramatically that it has become difficult to use the gym if you pick your time wrong. 

## The Problem 
***"How can I better understand which gym to go to and when to ensure low gym attendance?"***
Luckily, there was a way to develop a solution. The gym hosts a website for live member counts at each gym. Each location had it's own dedicated count, from which data could be scraped in real time to gain insight. 

## Idea Outline
In order to gather the attendance data, I decided to use a webscraper to gather this data in realtime. 
The Revo website https://revofitness.com.au/livemembercount/, has dropdowns for each location. In order to map each location, I need positional coordinates for each location, which was gathered manually through Google. 

Inspecting the html of the webpage reveals the name of the HTML asset necessary to be scraped. 

The following libraries are needed to run the program:

'''
import time
from datetime import datetime
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import concurrent.futures
import folium
from folium.plugins import LocateControl
from branca.colormap import LinearColormap as colourmap
import webbrowser
'''
