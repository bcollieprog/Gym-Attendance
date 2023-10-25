# Gym Attendance Mapping - The lazy man's solution to busy gyms
## Background 

For years now I have been going to the gym routinely. 
In recent times, I have encountered a question repeatedly; which gym should go to? 
The gym I am a member of, "Revo Gym", has many locations across Perth and Australia. In recent years, their membership has grown so dramatically that it has become difficult to use the gym if you pick your time wrong. 


<hr>

## The Problem 
***"How can I better understand which gym to go to and when to ensure low gym attendance?"***


Luckily, there was a way to develop a solution. The gym hosts a website for live member counts at each gym. Each location had it's own dedicated count, from which data could be scraped in real time to gain insight. 

<hr>

### Idea Outline

In order to gather the attendance data, I decided to use a webscraper to gather this data in realtime. 
The Revo website https://revofitness.com.au/livemembercount/, has dropdowns for each location. In order to map each location, I need positional coordinates for each location, which was gathered manually through Google. 

Inspecting the html of the webpage reveals the name of the HTML asset necessary to be scraped. 

The following libraries are needed to run the program:


```python
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
```

<br>

The URL of the webpage needs to be assigned:


```python
url = "https://revofitness.com.au/livemembercount/"
```

<br>

Each location has several bits of information for it's coordinates, HTML asset name and name of the location:


```python
location_coordinates = {
    "Banksia Grove": {"lat": -31.672501, "lng": 115.746849, "value": "banksia-grove"},
    "Belmont": {"lat": -31.964600, "lng": 115.935509, "value": "belmont"},
    "Cockburn": {"lat": -32.1263833, "lng": 115.830261, "value": "cockburn"},
    "Canning Vale": {"lat": -32.090169092344475, "lng": 115.91887857705403, "value": "canning-vale"},
    "Cannington": {"lat": -32.015549893973635, "lng": 115.93979642957694, "value": "cannington"},
    "Claremont": {"lat": -31.9763005, "lng": 115.7817048, "value": "claremont"},
    "Innaloo": {"lat": -31.8953548, "lng": 115.8011121, "value": "innaloo"},
    "Joondalup": {"lat": -31.7487718, "lng": 115.7653477, "value": "joondalup"},
    "Kelmscott": {"lat": -32.1157098, "lng": 116.0168508, "value": "kelmscott"},
    "Kwinana": {"lat": -32.2461406, "lng": 115.8151724, "value": "kwinana"},
    "Midland": {"lat": -31.8981609, "lng": 116.0169634, "value": "midland"},
    "Mount Hawthorn": {"lat": -31.9224346, "lng": 115.8412221, "value": "mount-hawthorn"},
    "Mirrabooka": {"lat": -31.86907, "lng": 115.86119, "value": "mirrabooka"},
    "Morley": {"lat": -31.8961967, "lng": 115.8944065, "value": "morley"},
    "Myaree": {"lat": -32.0410415, "lng": 115.8157906, "value": "myaree"},
    "Northbridge": {"lat": -31.9449892, "lng": 115.8531079, "value": "northbridge"},
    "O'Connor": {"lat": -32.0568007, "lng": 115.7928479, "value": "oconnor"},
    "Scarborough": {"lat": -31.8952171, "lng": 115.7573181, "value": "scarborough"},
    "Shenton Park": {"lat": -31.9538897, "lng": 115.7970556, "value": "shenton-park"},
    "Victoria Park": {"lat": -31.9687955, "lng": 115.8896312, "value": "victoria-park"}
}
```

<br>

The next step is to create the map object for which any items can be added. For this, I used Folium as it is a good interactive platform for easily creating customizable maps:


```python
csv_filename = "data.csv"

m = folium.Map(
    location=[-32.023663961724345, 115.86145511966623],
    zoom_start=11.5,
    tiles= "CartoDB positron",
    attr="Stamen Toner Lite",
)
m
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc="&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;

    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;

        &lt;script&gt;
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        &lt;/script&gt;

    &lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;
    &lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://code.jquery.com/jquery-1.12.4.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
            &lt;style&gt;
                #map_8cf137080d314377fabd69041d34c3b1 {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
                .leaflet-container { font-size: 1rem; }
            &lt;/style&gt;

&lt;/head&gt;
&lt;body&gt;


            &lt;div class=&quot;folium-map&quot; id=&quot;map_8cf137080d314377fabd69041d34c3b1&quot; &gt;&lt;/div&gt;

&lt;/body&gt;
&lt;script&gt;


            var map_8cf137080d314377fabd69041d34c3b1 = L.map(
                &quot;map_8cf137080d314377fabd69041d34c3b1&quot;,
                {
                    center: [-32.023663961724345, 115.86145511966623],
                    crs: L.CRS.EPSG3857,
                    zoom: 11.5,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );





            var tile_layer_b74fc416d8f93e2321f7019b4e9548e4 = L.tileLayer(
                &quot;https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png&quot;,
                {&quot;attribution&quot;: &quot;\u0026copy; \u003ca target=\&quot;_blank\&quot; href=\&quot;http://www.openstreetmap.org/copyright\&quot;\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca target=\&quot;_blank\&quot; href=\&quot;http://cartodb.com/attributions\&quot;\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca target=\&quot;_blank\&quot; href =\&quot;http://cartodb.com/attributions\&quot;\u003eattributions\u003c/a\u003e&quot;, &quot;detectRetina&quot;: false, &quot;maxNativeZoom&quot;: 18, &quot;maxZoom&quot;: 18, &quot;minZoom&quot;: 0, &quot;noWrap&quot;: false, &quot;opacity&quot;: 1, &quot;subdomains&quot;: &quot;abc&quot;, &quot;tms&quot;: false}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);

&lt;/script&gt;
&lt;/html&gt;" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



The location coordinates correspond to my city of Perth, Western Australia. 
<br>
An important part of my decision to use Folium for mapping is that is hughly customizable for aesthetics. As such, I changed the theme of the map to Stamen Tiles' Toner Lite

<br>
In order to access the webpage in short amounts of time with a webscraper, there is a popup that is necessary to overcome. As such, I included a function for clicking outside of the banner (in this instance, I chose for it to click the 'heading') to dismiss it:


```python
def dismiss_banners(driver):
    element_selector = "p.ticker-heading"
    element = driver.find_element(By.CSS_SELECTOR, element_selector)
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
```

<br>
Now comes the part that I'm interested in; webscraping the attendance data for each location. 

<br>For this, I am going to ammend it to a CSV file. I had originally planned on exporting the data to R for better graphing capailities, but was satisfied with what Folium was able to provide in Python. 

<br> Each element of the following chunk has been anotated for ease of reading: 


```python
def scrape_and_append_to_csv_for_location(location, driver):
    try:
        # Find element by HTML ID
        dropdown = driver.find_element(By.ID, "gyms-wa")

        # Select the value for the location, as named above
        dropdown.send_keys(location_coordinates[location]["value"])

        # Wait for web content to load 
        time.sleep(2)

        # Dismiss banners and any overlays by clicking on the same element as the attendance number
        dismiss_banners(driver)

        # Get the page source after dismissing the banners
        page_source = driver.page_source

        # Use beautifulsoup to parse the html page
        soup = BeautifulSoup(page_source, "html.parser")

        # Use CSS selector to extract the attendance value 
        target_element = soup.select_one(f"span.the-number#{location_coordinates[location]['value']}-number")
        if target_element:
            attendance = int(target_element.get_text(strip=True))  # Convert attendance to an integer, because it can only be an int
        else:
            attendance = "N/A"

        # Get current timestamp
        timestamp = datetime.now().strftime('%m-%d %H:%M')

        #This following part was added later in the code to make the output CSV easier to use 
        # Change Lat and Long coordinates to floats before storing
        lat = float(location_coordinates[location]['lat'])
        lng = float(location_coordinates[location]['lng'])

        # Append data to CSV file
        with open(csv_filename, "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([timestamp, location, attendance, lat, lng])

        print(f"Data scraped at {timestamp} for {location}: {attendance}")

        # Create the colourmap to visualise attendance easier 
        attendance_colormap = colourmap(["green", "yellow", "red"], None, 0, 100, )

        # Add Location names to markers
        folium.Marker(
            location=[location_coordinates[location]["lat"], location_coordinates[location]["lng"]],
            icon=folium.DivIcon(
                icon_anchor = (25,10),
                html=f"""<div style="text-align: center; font-size: 12pt; color: black; font-family: helvetica;">{location}</div>"""
            ),
        ).add_to(m)

        # Add a marker to the Folium map for each location
        folium.CircleMarker(
            location=(location_coordinates[location]['lat'], location_coordinates[location]["lng"]),
            radius=attendance / 2,  
            color=attendance_colormap(attendance),  
            fill=True,
            fill_color=attendance_colormap(attendance),  
            fill_opacity=attendance / 150,  
            popup=f"{location}: {attendance}",
            tooltip=f"Attendance: {attendance}",
        ).add_to(m)

        m.save("attendance_map.html")

    except Exception as e:
        print("Error:", e)
```

<br> The next step was to include the use of paralell scrapers using Concurrent Futures. This would make the process much quicker and allow it to be run more regularly. Without it, the process took about 40 seconds to run, which is cut down greatly to about 20seconds with the use of concurrent scrapers.

<br> The following code was used:


```python
def scrape_data_in_parallel():
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        service = Service(executable_path="/Users/abcd/geckodriver", log_output=None)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.get(url)

        # Clear the CSV file and write data
        # The program was having trouble with ammending new data, so this was added to account for this
        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Date", "Location", "Attendance", "Coordinates"])

        # Threadpool executor can use up to 5 executors, but the ROI on time seemed to max out around 3
        with concurrent.futures.ThreadPoolExecutor(max_workers= 3) as executor:
            # Use executor.map to parallelize data scraping for multiple locations
            executor.map(lambda location: scrape_and_append_to_csv_for_location(location, driver), location_coordinates)

        # Close the WebDriver
        driver.quit()

    except Exception as e:
        print("Error:", e)


```

<hr>

## The Final Product
After all of that, we can call the function responsible for scraping and see what we end up with:


```python
scrape_data_in_parallel()
m
```

    Data scraped at 10-25 10:13 for Belmont: 38
    Data scraped at 10-25 10:13 for Banksia Grove: 30
    Data scraped at 10-25 10:13 for Cockburn: 23
    Data scraped at 10-25 10:13 for Canning Vale: 67
    Data scraped at 10-25 10:13 for Cannington: 52
    Data scraped at 10-25 10:13 for Claremont: 44
    Data scraped at 10-25 10:13 for Innaloo: 55
    Data scraped at 10-25 10:13 for Joondalup: 70
    Data scraped at 10-25 10:13 for Kelmscott: 13
    Data scraped at 10-25 10:13 for Kwinana: 44
    Data scraped at 10-25 10:13 for Midland: 25
    Data scraped at 10-25 10:13 for Mount Hawthorn: 35
    Data scraped at 10-25 10:13 for Mirrabooka: 42
    Data scraped at 10-25 10:13 for Morley: 44
    Data scraped at 10-25 10:13 for Myaree: 44
    Data scraped at 10-25 10:13 for Northbridge: 12
    Data scraped at 10-25 10:13 for O'Connor: 38
    Data scraped at 10-25 10:13 for Scarborough: 100
    Data scraped at 10-25 10:13 for Shenton Park: 23
    Data scraped at 10-25 10:13 for Victoria Park: 24





<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc="&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;

    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;

        &lt;script&gt;
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        &lt;/script&gt;

    &lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;
    &lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://code.jquery.com/jquery-1.12.4.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
            &lt;style&gt;
                #map_8cf137080d314377fabd69041d34c3b1 {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
                .leaflet-container { font-size: 1rem; }
            &lt;/style&gt;

&lt;/head&gt;
&lt;body&gt;


            &lt;div class=&quot;folium-map&quot; id=&quot;map_8cf137080d314377fabd69041d34c3b1&quot; &gt;&lt;/div&gt;

&lt;/body&gt;
&lt;script&gt;


            var map_8cf137080d314377fabd69041d34c3b1 = L.map(
                &quot;map_8cf137080d314377fabd69041d34c3b1&quot;,
                {
                    center: [-32.023663961724345, 115.86145511966623],
                    crs: L.CRS.EPSG3857,
                    zoom: 11.5,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );





            var tile_layer_b74fc416d8f93e2321f7019b4e9548e4 = L.tileLayer(
                &quot;https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png&quot;,
                {&quot;attribution&quot;: &quot;\u0026copy; \u003ca target=\&quot;_blank\&quot; href=\&quot;http://www.openstreetmap.org/copyright\&quot;\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca target=\&quot;_blank\&quot; href=\&quot;http://cartodb.com/attributions\&quot;\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca target=\&quot;_blank\&quot; href =\&quot;http://cartodb.com/attributions\&quot;\u003eattributions\u003c/a\u003e&quot;, &quot;detectRetina&quot;: false, &quot;maxNativeZoom&quot;: 18, &quot;maxZoom&quot;: 18, &quot;minZoom&quot;: 0, &quot;noWrap&quot;: false, &quot;opacity&quot;: 1, &quot;subdomains&quot;: &quot;abc&quot;, &quot;tms&quot;: false}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var marker_d205d930b41d41ca9cf88a15c0018ba6 = L.marker(
                [-31.9646, 115.935509],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_f9484d105aea3ccd030d9f6254b3075f = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eBelmont\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_d205d930b41d41ca9cf88a15c0018ba6.setIcon(div_icon_f9484d105aea3ccd030d9f6254b3075f);


            var circle_marker_6e687878cf525e198c5469a5c51caf68 = L.circleMarker(
                [-31.9646, 115.935509],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#c2e100ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#c2e100ff&quot;, &quot;fillOpacity&quot;: 0.25333333333333335, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 19.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_51d92948de80536f4e16bb2fdb4e68c0 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_a07df8a3ab7f77cb25aed06550a1f4c5 = $(`&lt;div id=&quot;html_a07df8a3ab7f77cb25aed06550a1f4c5&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Belmont: 38&lt;/div&gt;`)[0];
                popup_51d92948de80536f4e16bb2fdb4e68c0.setContent(html_a07df8a3ab7f77cb25aed06550a1f4c5);



        circle_marker_6e687878cf525e198c5469a5c51caf68.bindPopup(popup_51d92948de80536f4e16bb2fdb4e68c0)
        ;




            circle_marker_6e687878cf525e198c5469a5c51caf68.bindTooltip(
                `&lt;div&gt;
                     Attendance: 38
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_09a9e5850b9895125b140e2ae5a9c868 = L.marker(
                [-31.672501, 115.746849],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_d76696b6516607b9f6d0bd1e87dea709 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eBanksia Grove\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_09a9e5850b9895125b140e2ae5a9c868.setIcon(div_icon_d76696b6516607b9f6d0bd1e87dea709);


            var circle_marker_880389374188c65f114e5ed4c63c2262 = L.circleMarker(
                [-31.672501, 115.746849],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#99cd00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#99cd00ff&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 15.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_153059f249ee9f5d63b3d9b62a27f27d = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_3b7f6d5ca0a67f76703646a3f52e4faf = $(`&lt;div id=&quot;html_3b7f6d5ca0a67f76703646a3f52e4faf&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Banksia Grove: 30&lt;/div&gt;`)[0];
                popup_153059f249ee9f5d63b3d9b62a27f27d.setContent(html_3b7f6d5ca0a67f76703646a3f52e4faf);



        circle_marker_880389374188c65f114e5ed4c63c2262.bindPopup(popup_153059f249ee9f5d63b3d9b62a27f27d)
        ;




            circle_marker_880389374188c65f114e5ed4c63c2262.bindTooltip(
                `&lt;div&gt;
                     Attendance: 30
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_2f2253d465778f929a38447a4428d954 = L.marker(
                [-32.1263833, 115.830261],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_309133dce7fac9a00a53da358cd236de = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eCockburn\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_2f2253d465778f929a38447a4428d954.setIcon(div_icon_309133dce7fac9a00a53da358cd236de);


            var circle_marker_05817d329ee933b7b26ac4446ac5f472 = L.circleMarker(
                [-32.1263833, 115.830261],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#75bb00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#75bb00ff&quot;, &quot;fillOpacity&quot;: 0.15333333333333332, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 11.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_c0acf143003a496639f3ac29fd0bf147 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_73eb2b317853783935d86ca1dd2719d7 = $(`&lt;div id=&quot;html_73eb2b317853783935d86ca1dd2719d7&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Cockburn: 23&lt;/div&gt;`)[0];
                popup_c0acf143003a496639f3ac29fd0bf147.setContent(html_73eb2b317853783935d86ca1dd2719d7);



        circle_marker_05817d329ee933b7b26ac4446ac5f472.bindPopup(popup_c0acf143003a496639f3ac29fd0bf147)
        ;




            circle_marker_05817d329ee933b7b26ac4446ac5f472.bindTooltip(
                `&lt;div&gt;
                     Attendance: 23
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_df2428dc8c6a9f195220f605eb7f6860 = L.marker(
                [-32.090169092344475, 115.91887857705403],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_a94870e6520e368d66ad1d47984f01b7 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eCanning Vale\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_df2428dc8c6a9f195220f605eb7f6860.setIcon(div_icon_a94870e6520e368d66ad1d47984f01b7);


            var circle_marker_d4aa3d3a4536fc1007da8c61d4bde475 = L.circleMarker(
                [-32.090169092344475, 115.91887857705403],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ffa800ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ffa800ff&quot;, &quot;fillOpacity&quot;: 0.44666666666666666, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 33.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_25249c9c1464e707c6da0917355eb9ce = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_3e39987eb3af23b37d076df2c52fa995 = $(`&lt;div id=&quot;html_3e39987eb3af23b37d076df2c52fa995&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Canning Vale: 67&lt;/div&gt;`)[0];
                popup_25249c9c1464e707c6da0917355eb9ce.setContent(html_3e39987eb3af23b37d076df2c52fa995);



        circle_marker_d4aa3d3a4536fc1007da8c61d4bde475.bindPopup(popup_25249c9c1464e707c6da0917355eb9ce)
        ;




            circle_marker_d4aa3d3a4536fc1007da8c61d4bde475.bindTooltip(
                `&lt;div&gt;
                     Attendance: 67
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_e374535256422bec8b13fe8f772d4835 = L.marker(
                [-32.015549893973635, 115.93979642957694],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_5c5f74c6212eae4ff39dfb989473750c = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eCannington\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_e374535256422bec8b13fe8f772d4835.setIcon(div_icon_5c5f74c6212eae4ff39dfb989473750c);


            var circle_marker_cf671a34cb7d09594359cf31c88d2fb4 = L.circleMarker(
                [-32.015549893973635, 115.93979642957694],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#fff500ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#fff500ff&quot;, &quot;fillOpacity&quot;: 0.3466666666666667, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 26.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_fd8e3c28fdc9c38ca6d0bfb219f53fbe = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_c384d3cac3cb2240fabf2249b3f2a02b = $(`&lt;div id=&quot;html_c384d3cac3cb2240fabf2249b3f2a02b&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Cannington: 52&lt;/div&gt;`)[0];
                popup_fd8e3c28fdc9c38ca6d0bfb219f53fbe.setContent(html_c384d3cac3cb2240fabf2249b3f2a02b);



        circle_marker_cf671a34cb7d09594359cf31c88d2fb4.bindPopup(popup_fd8e3c28fdc9c38ca6d0bfb219f53fbe)
        ;




            circle_marker_cf671a34cb7d09594359cf31c88d2fb4.bindTooltip(
                `&lt;div&gt;
                     Attendance: 52
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_3797a8c4a2e78d38f16013350f81f4ac = L.marker(
                [-31.9763005, 115.7817048],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_926280b64d3853b4ad1c22f868ff9738 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eClaremont\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_3797a8c4a2e78d38f16013350f81f4ac.setIcon(div_icon_926280b64d3853b4ad1c22f868ff9738);


            var circle_marker_33f6806f44812b414b6acf1d43ddc865 = L.circleMarker(
                [-31.9763005, 115.7817048],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e1f000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e1f000ff&quot;, &quot;fillOpacity&quot;: 0.29333333333333333, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 22.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_ddf104936afd61fb967c18ab00af5143 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_52c23ed7bb466b37aaa170a21b3e1c0d = $(`&lt;div id=&quot;html_52c23ed7bb466b37aaa170a21b3e1c0d&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Claremont: 44&lt;/div&gt;`)[0];
                popup_ddf104936afd61fb967c18ab00af5143.setContent(html_52c23ed7bb466b37aaa170a21b3e1c0d);



        circle_marker_33f6806f44812b414b6acf1d43ddc865.bindPopup(popup_ddf104936afd61fb967c18ab00af5143)
        ;




            circle_marker_33f6806f44812b414b6acf1d43ddc865.bindTooltip(
                `&lt;div&gt;
                     Attendance: 44
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_a2b4c5265b3cdba4c436ecdd52be3b81 = L.marker(
                [-31.8953548, 115.8011121],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_d2ff639fb62930a2e1603a5bd5bb1a26 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eInnaloo\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_a2b4c5265b3cdba4c436ecdd52be3b81.setIcon(div_icon_d2ff639fb62930a2e1603a5bd5bb1a26);


            var circle_marker_0ec3e99544ae28320b2a6f8795c777dd = L.circleMarker(
                [-31.8953548, 115.8011121],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ffe600ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ffe600ff&quot;, &quot;fillOpacity&quot;: 0.36666666666666664, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 27.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_fb5c852f8be61cc15d237a07e2eb648d = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_54b2e0ca277fb056a04184632940e867 = $(`&lt;div id=&quot;html_54b2e0ca277fb056a04184632940e867&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Innaloo: 55&lt;/div&gt;`)[0];
                popup_fb5c852f8be61cc15d237a07e2eb648d.setContent(html_54b2e0ca277fb056a04184632940e867);



        circle_marker_0ec3e99544ae28320b2a6f8795c777dd.bindPopup(popup_fb5c852f8be61cc15d237a07e2eb648d)
        ;




            circle_marker_0ec3e99544ae28320b2a6f8795c777dd.bindTooltip(
                `&lt;div&gt;
                     Attendance: 55
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_0c561b5fbe3094d64ae81b78d747f03f = L.marker(
                [-31.7487718, 115.7653477],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_cc9f1683e9fb65cf48db84acd60b8527 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eJoondalup\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_0c561b5fbe3094d64ae81b78d747f03f.setIcon(div_icon_cc9f1683e9fb65cf48db84acd60b8527);


            var circle_marker_1eecfaea8c80dfaff431be8e58d53548 = L.circleMarker(
                [-31.7487718, 115.7653477],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ff9900ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ff9900ff&quot;, &quot;fillOpacity&quot;: 0.4666666666666667, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 35.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_d8331312eed903a69c0dc1ce605bb7a2 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_af6cfeaa5b0cac4bf794cb5783295a75 = $(`&lt;div id=&quot;html_af6cfeaa5b0cac4bf794cb5783295a75&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Joondalup: 70&lt;/div&gt;`)[0];
                popup_d8331312eed903a69c0dc1ce605bb7a2.setContent(html_af6cfeaa5b0cac4bf794cb5783295a75);



        circle_marker_1eecfaea8c80dfaff431be8e58d53548.bindPopup(popup_d8331312eed903a69c0dc1ce605bb7a2)
        ;




            circle_marker_1eecfaea8c80dfaff431be8e58d53548.bindTooltip(
                `&lt;div&gt;
                     Attendance: 70
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_ab9c24360b5b941a055459160a20b0fe = L.marker(
                [-32.1157098, 116.0168508],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_41b892f3cf38fbab637a2e3e662646c8 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eKelmscott\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_ab9c24360b5b941a055459160a20b0fe.setIcon(div_icon_41b892f3cf38fbab637a2e3e662646c8);


            var circle_marker_4cb24dd5f5986192bcd79f5d6d6fbf18 = L.circleMarker(
                [-32.1157098, 116.0168508],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#42a100ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#42a100ff&quot;, &quot;fillOpacity&quot;: 0.08666666666666667, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 6.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_5a0a53aaf99179f6b373bb76a798587e = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_63b0cbd770c7b70b92e8220c92901290 = $(`&lt;div id=&quot;html_63b0cbd770c7b70b92e8220c92901290&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Kelmscott: 13&lt;/div&gt;`)[0];
                popup_5a0a53aaf99179f6b373bb76a798587e.setContent(html_63b0cbd770c7b70b92e8220c92901290);



        circle_marker_4cb24dd5f5986192bcd79f5d6d6fbf18.bindPopup(popup_5a0a53aaf99179f6b373bb76a798587e)
        ;




            circle_marker_4cb24dd5f5986192bcd79f5d6d6fbf18.bindTooltip(
                `&lt;div&gt;
                     Attendance: 13
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_59b624d08bb9ef59f1471b1a8db3600c = L.marker(
                [-32.2461406, 115.8151724],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_4d452874503acb941d2ee2b095f599b4 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eKwinana\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_59b624d08bb9ef59f1471b1a8db3600c.setIcon(div_icon_4d452874503acb941d2ee2b095f599b4);


            var circle_marker_698c4516b29bed288e5826ad33575d88 = L.circleMarker(
                [-32.2461406, 115.8151724],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e1f000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e1f000ff&quot;, &quot;fillOpacity&quot;: 0.29333333333333333, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 22.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_859f7dcc8706cec1c0c26363d90bfa1b = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_f958f48f43ea1fc841c13bab49416ce0 = $(`&lt;div id=&quot;html_f958f48f43ea1fc841c13bab49416ce0&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Kwinana: 44&lt;/div&gt;`)[0];
                popup_859f7dcc8706cec1c0c26363d90bfa1b.setContent(html_f958f48f43ea1fc841c13bab49416ce0);



        circle_marker_698c4516b29bed288e5826ad33575d88.bindPopup(popup_859f7dcc8706cec1c0c26363d90bfa1b)
        ;




            circle_marker_698c4516b29bed288e5826ad33575d88.bindTooltip(
                `&lt;div&gt;
                     Attendance: 44
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_6ba07e3c389cce1c2d9fd187e9a53d15 = L.marker(
                [-31.8981609, 116.0169634],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_85e2531732909366033761c16844210a = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eMidland\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_6ba07e3c389cce1c2d9fd187e9a53d15.setIcon(div_icon_85e2531732909366033761c16844210a);


            var circle_marker_47bcb7fc715742f8252e83e12a9dface = L.circleMarker(
                [-31.8981609, 116.0169634],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#7fc000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#7fc000ff&quot;, &quot;fillOpacity&quot;: 0.16666666666666666, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 12.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_b0c0b060ca4b6483e56598d8e442bc07 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_f783d86a557d2d9b9ba1a622f563deea = $(`&lt;div id=&quot;html_f783d86a557d2d9b9ba1a622f563deea&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Midland: 25&lt;/div&gt;`)[0];
                popup_b0c0b060ca4b6483e56598d8e442bc07.setContent(html_f783d86a557d2d9b9ba1a622f563deea);



        circle_marker_47bcb7fc715742f8252e83e12a9dface.bindPopup(popup_b0c0b060ca4b6483e56598d8e442bc07)
        ;




            circle_marker_47bcb7fc715742f8252e83e12a9dface.bindTooltip(
                `&lt;div&gt;
                     Attendance: 25
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_27873bf55fc1238f99abccfa9dbe3815 = L.marker(
                [-31.9224346, 115.8412221],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_4cc7b0dae87bd2927fe5d8259b081807 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eMount Hawthorn\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_27873bf55fc1238f99abccfa9dbe3815.setIcon(div_icon_4cc7b0dae87bd2927fe5d8259b081807);


            var circle_marker_4c60b0ca4a075546dc3d4ade539ec4a8 = L.circleMarker(
                [-31.9224346, 115.8412221],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#b3d900ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#b3d900ff&quot;, &quot;fillOpacity&quot;: 0.23333333333333334, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 17.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_4d07d2b932f28f8fec4a4807534b4c7f = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_9d4e12f95dca611ef02516656edb125d = $(`&lt;div id=&quot;html_9d4e12f95dca611ef02516656edb125d&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Mount Hawthorn: 35&lt;/div&gt;`)[0];
                popup_4d07d2b932f28f8fec4a4807534b4c7f.setContent(html_9d4e12f95dca611ef02516656edb125d);



        circle_marker_4c60b0ca4a075546dc3d4ade539ec4a8.bindPopup(popup_4d07d2b932f28f8fec4a4807534b4c7f)
        ;




            circle_marker_4c60b0ca4a075546dc3d4ade539ec4a8.bindTooltip(
                `&lt;div&gt;
                     Attendance: 35
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_c5fc7442122c62624aa39337d9742724 = L.marker(
                [-31.86907, 115.86119],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_20d3a620f04a8050d14780f9b4177eeb = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eMirrabooka\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_c5fc7442122c62624aa39337d9742724.setIcon(div_icon_20d3a620f04a8050d14780f9b4177eeb);


            var circle_marker_44705ee25106b25f5e3e9a21686b8090 = L.circleMarker(
                [-31.86907, 115.86119],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#d7eb00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#d7eb00ff&quot;, &quot;fillOpacity&quot;: 0.28, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 21.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_ee627ebae59fc75cb3a1e750873971d2 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_878a503ec7dcfab87e325069c94d9b89 = $(`&lt;div id=&quot;html_878a503ec7dcfab87e325069c94d9b89&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Mirrabooka: 42&lt;/div&gt;`)[0];
                popup_ee627ebae59fc75cb3a1e750873971d2.setContent(html_878a503ec7dcfab87e325069c94d9b89);



        circle_marker_44705ee25106b25f5e3e9a21686b8090.bindPopup(popup_ee627ebae59fc75cb3a1e750873971d2)
        ;




            circle_marker_44705ee25106b25f5e3e9a21686b8090.bindTooltip(
                `&lt;div&gt;
                     Attendance: 42
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_aa95aedd85afeaab3e0485a2996731e6 = L.marker(
                [-31.8961967, 115.8944065],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_a3b89679a072909f5483a8db118c01e1 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eMorley\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_aa95aedd85afeaab3e0485a2996731e6.setIcon(div_icon_a3b89679a072909f5483a8db118c01e1);


            var circle_marker_c4b1ca77f502266d436662db0db62a1f = L.circleMarker(
                [-31.8961967, 115.8944065],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e1f000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e1f000ff&quot;, &quot;fillOpacity&quot;: 0.29333333333333333, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 22.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_9c6f6f7e88b10541dc7dcd806b00218c = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_575a88f51410408a35deb022f0d1d201 = $(`&lt;div id=&quot;html_575a88f51410408a35deb022f0d1d201&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Morley: 44&lt;/div&gt;`)[0];
                popup_9c6f6f7e88b10541dc7dcd806b00218c.setContent(html_575a88f51410408a35deb022f0d1d201);



        circle_marker_c4b1ca77f502266d436662db0db62a1f.bindPopup(popup_9c6f6f7e88b10541dc7dcd806b00218c)
        ;




            circle_marker_c4b1ca77f502266d436662db0db62a1f.bindTooltip(
                `&lt;div&gt;
                     Attendance: 44
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_06572400ee5d804b76d19f2354cd095d = L.marker(
                [-32.0410415, 115.8157906],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_dc2096c0870763781cd8b83c700173a9 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eMyaree\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_06572400ee5d804b76d19f2354cd095d.setIcon(div_icon_dc2096c0870763781cd8b83c700173a9);


            var circle_marker_b516b9b59b16dfa2e3248f3c59926d0b = L.circleMarker(
                [-32.0410415, 115.8157906],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#e1f000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#e1f000ff&quot;, &quot;fillOpacity&quot;: 0.29333333333333333, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 22.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_697d96f90e813567904413e1d4a2e2f6 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_e291126ae8ae5ed4f137ba60c3904137 = $(`&lt;div id=&quot;html_e291126ae8ae5ed4f137ba60c3904137&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Myaree: 44&lt;/div&gt;`)[0];
                popup_697d96f90e813567904413e1d4a2e2f6.setContent(html_e291126ae8ae5ed4f137ba60c3904137);



        circle_marker_b516b9b59b16dfa2e3248f3c59926d0b.bindPopup(popup_697d96f90e813567904413e1d4a2e2f6)
        ;




            circle_marker_b516b9b59b16dfa2e3248f3c59926d0b.bindTooltip(
                `&lt;div&gt;
                     Attendance: 44
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_5f1519ef4db3f8fc67114c67791a15e8 = L.marker(
                [-31.9449892, 115.8531079],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_dd6b526b83af8df95beb8cb2470c6a0a = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eNorthbridge\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_5f1519ef4db3f8fc67114c67791a15e8.setIcon(div_icon_dd6b526b83af8df95beb8cb2470c6a0a);


            var circle_marker_ff9347c73939135feb823a3e866ec922 = L.circleMarker(
                [-31.9449892, 115.8531079],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#3d9f00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#3d9f00ff&quot;, &quot;fillOpacity&quot;: 0.08, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 6.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_f4eb642bb21c66bae950d4860b83dadd = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_2b11f3b3f7468dd59f2450fcd4b511b9 = $(`&lt;div id=&quot;html_2b11f3b3f7468dd59f2450fcd4b511b9&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Northbridge: 12&lt;/div&gt;`)[0];
                popup_f4eb642bb21c66bae950d4860b83dadd.setContent(html_2b11f3b3f7468dd59f2450fcd4b511b9);



        circle_marker_ff9347c73939135feb823a3e866ec922.bindPopup(popup_f4eb642bb21c66bae950d4860b83dadd)
        ;




            circle_marker_ff9347c73939135feb823a3e866ec922.bindTooltip(
                `&lt;div&gt;
                     Attendance: 12
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_95c08949eb9aa65d3ab176b281860495 = L.marker(
                [-32.0568007, 115.7928479],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_91614b0a79a28d397d31aa8d7984c6d6 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eO\u0027Connor\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_95c08949eb9aa65d3ab176b281860495.setIcon(div_icon_91614b0a79a28d397d31aa8d7984c6d6);


            var circle_marker_6c93ba9da9141e0b8fb4b8f28ef49b65 = L.circleMarker(
                [-32.0568007, 115.7928479],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#c2e100ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#c2e100ff&quot;, &quot;fillOpacity&quot;: 0.25333333333333335, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 19.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_c955595e1be993a5db1ff3dd4ce88ab0 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_45814a168d6377a7e73b12ced26e73d9 = $(`&lt;div id=&quot;html_45814a168d6377a7e73b12ced26e73d9&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;O&#x27;Connor: 38&lt;/div&gt;`)[0];
                popup_c955595e1be993a5db1ff3dd4ce88ab0.setContent(html_45814a168d6377a7e73b12ced26e73d9);



        circle_marker_6c93ba9da9141e0b8fb4b8f28ef49b65.bindPopup(popup_c955595e1be993a5db1ff3dd4ce88ab0)
        ;




            circle_marker_6c93ba9da9141e0b8fb4b8f28ef49b65.bindTooltip(
                `&lt;div&gt;
                     Attendance: 38
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_c4cecba3b0c6fb4e665a7b9ef28a48d2 = L.marker(
                [-31.8952171, 115.7573181],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_0812cc46d1511140bfa8ca07352f8428 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eScarborough\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_c4cecba3b0c6fb4e665a7b9ef28a48d2.setIcon(div_icon_0812cc46d1511140bfa8ca07352f8428);


            var circle_marker_24aaa31e45cd9e403c6f3c98cbb8ee22 = L.circleMarker(
                [-31.8952171, 115.7573181],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#ff0000ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#ff0000ff&quot;, &quot;fillOpacity&quot;: 0.6666666666666666, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 50.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_ed12a274b8ffe798a0a68c5b361d014a = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_e231f2e68b3975c003f8aeceb10a3a69 = $(`&lt;div id=&quot;html_e231f2e68b3975c003f8aeceb10a3a69&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Scarborough: 100&lt;/div&gt;`)[0];
                popup_ed12a274b8ffe798a0a68c5b361d014a.setContent(html_e231f2e68b3975c003f8aeceb10a3a69);



        circle_marker_24aaa31e45cd9e403c6f3c98cbb8ee22.bindPopup(popup_ed12a274b8ffe798a0a68c5b361d014a)
        ;




            circle_marker_24aaa31e45cd9e403c6f3c98cbb8ee22.bindTooltip(
                `&lt;div&gt;
                     Attendance: 100
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_6b57b0c4a8563bc824c8a880192b989f = L.marker(
                [-31.9538897, 115.7970556],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_a81d450bc82fe0ba5e82573865117649 = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eShenton Park\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_6b57b0c4a8563bc824c8a880192b989f.setIcon(div_icon_a81d450bc82fe0ba5e82573865117649);


            var circle_marker_0276cc1f6b5bacd7f2b2236009fd2b17 = L.circleMarker(
                [-31.9538897, 115.7970556],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#75bb00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#75bb00ff&quot;, &quot;fillOpacity&quot;: 0.15333333333333332, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 11.5, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_e414fd24068f04d34c4c54978093e83f = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_c7bfed47918cdbbc361044d90e383e78 = $(`&lt;div id=&quot;html_c7bfed47918cdbbc361044d90e383e78&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Shenton Park: 23&lt;/div&gt;`)[0];
                popup_e414fd24068f04d34c4c54978093e83f.setContent(html_c7bfed47918cdbbc361044d90e383e78);



        circle_marker_0276cc1f6b5bacd7f2b2236009fd2b17.bindPopup(popup_e414fd24068f04d34c4c54978093e83f)
        ;




            circle_marker_0276cc1f6b5bacd7f2b2236009fd2b17.bindTooltip(
                `&lt;div&gt;
                     Attendance: 23
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );


            var marker_3569d5ca0798a440ea9ccacafe9abf5f = L.marker(
                [-31.9687955, 115.8896312],
                {}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


            var div_icon_d338278f3e9a0a2924392af5f09bc40a = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\u003cdiv style=\&quot;text-align: center; font-size: 12pt; color: black; font-family: helvetica;\&quot;\u003eVictoria Park\u003c/div\u003e&quot;, &quot;iconAnchor&quot;: [25, 10]});
            marker_3569d5ca0798a440ea9ccacafe9abf5f.setIcon(div_icon_d338278f3e9a0a2924392af5f09bc40a);


            var circle_marker_bed9e3f411094efba37b95a9ac816439 = L.circleMarker(
                [-31.9687955, 115.8896312],
                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#7abd00ff&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#7abd00ff&quot;, &quot;fillOpacity&quot;: 0.16, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 12.0, &quot;stroke&quot;: true, &quot;weight&quot;: 3}
            ).addTo(map_8cf137080d314377fabd69041d34c3b1);


        var popup_7ccee4fa04d178c9ee5568d9a467452b = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});



                var html_4350af8a25c000177950880660c0200b = $(`&lt;div id=&quot;html_4350af8a25c000177950880660c0200b&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;Victoria Park: 24&lt;/div&gt;`)[0];
                popup_7ccee4fa04d178c9ee5568d9a467452b.setContent(html_4350af8a25c000177950880660c0200b);



        circle_marker_bed9e3f411094efba37b95a9ac816439.bindPopup(popup_7ccee4fa04d178c9ee5568d9a467452b)
        ;




            circle_marker_bed9e3f411094efba37b95a9ac816439.bindTooltip(
                `&lt;div&gt;
                     Attendance: 24
                 &lt;/div&gt;`,
                {&quot;sticky&quot;: true}
            );

&lt;/script&gt;
&lt;/html&gt;" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



<br>

## Final Thoughts

This is a program that I use routinely, nearly daily. I have it run on command linked with another Google automation program that allows it to be run using voice command to a Google Home. 
From here, it displays on my monitor showing me which gym is best to go to. 

<br> 

In the future, I want to ammend the program to include a decision engine; making suggestions based on attendance, distance, realtime travel estimations and gym features.


```python

```
