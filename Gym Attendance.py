import time
import webbrowser
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


# URL of the webpage you want to scrape
url = "https://revofitness.com.au/livemembercount/"

# CSV file name
csv_filename = "data1.csv"

# Mapping of location names to latitude and longitude coordinates
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

# Create the map
m = folium.Map(
    location=[-32.023663961724345, 115.86145511966623],
    zoom_start=11.5,
    tiles="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}.png",
    attr="Stamen Terrain",
)
# Allow location services
folium.plugins.LocateControl().add_to(m),


# Function to dismiss banners and simulate clicking outside
def dismiss_banners(driver):
    element_selector = "p.ticker-heading"
    element = driver.find_element(By.CSS_SELECTOR, element_selector)
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()


# Function to scrape data and append to CSV for a single location
def scrape_and_append_to_csv_for_location(location, driver):
    try:
        # Find the dropdown element by its ID
        dropdown = driver.find_element(By.ID, "gyms-wa")

        # Select the desired location's option by value
        dropdown.send_keys(location_coordinates[location]["value"])

        # Wait for a moment to allow dynamic content to load (adjust as needed)
        time.sleep(2)

        # Dismiss banners and any overlays by clicking on the same element as the attendance number
        dismiss_banners(driver)

        # Get the page source after dismissing the banners
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract the attendance data using CSS selector
        target_element = soup.select_one(f"span.the-number#{location_coordinates[location]['value']}-number")
        if target_element:
            attendance = int(target_element.get_text(strip=True))  # Convert attendance to an integer
        else:
            attendance = "N/A"

        # Get current timestamp
        timestamp = datetime.now().strftime('%m-%d %H:%M')

        # Change Lat and Long coordinates to floats before storing
        lat = float(location_coordinates[location]['lat'])
        lng = float(location_coordinates[location]['lng'])

        # Append data to CSV file
        with open(csv_filename, "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            # CSV row format: Date, Location, Attendance, Coordinates
            csv_writer.writerow([timestamp, location, attendance, lat, lng])

        print(f"Data scraped at {timestamp} for {location}: {attendance}")

        attendance_colormap = colourmap(["green", "yellow", "red"], None, 0, 100, )

        # Add labels to markers
        folium.Marker(
            location=[location_coordinates[location]["lat"], location_coordinates[location]["lng"]],
            icon=folium.DivIcon(
                icon_anchor = (25,10),
                html=f"""<div style="text-align: center; font-size: 15pt; color: black; font-family: helvetica;">{location}</div>"""
            ),
        ).add_to(m)

        # Add a marker to the Folium map for each location
        folium.CircleMarker(
            location=(location_coordinates[location]['lat'], location_coordinates[location]["lng"]),
            radius=attendance / 2,  # Adjust the factor to control circle size
            color=attendance_colormap(attendance),  # Circle color
            fill=True,
            fill_color=attendance_colormap(attendance),  # Fill color
            fill_opacity=attendance / 150,  # Fill opacity
            popup=f"{location}: {attendance}",
            tooltip=f"Attendance: {attendance}",
        ).add_to(m)

        m.save("attendance_map_new.html")

    except Exception as e:
        print("Error:", e)


# Function to parallelize data scraping
def scrape_data_in_parallel():
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        service = Service(executable_path="/Users/abcd/geckodriver", log_output=None)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.get(url)

        # Clear the CSV file and write the header
        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Date", "Location", "Attendance", "Coordinates"])

        # Create a ThreadPoolExecutor with a maximum of 5 threads (adjust as needed)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Use executor.map to parallelize data scraping for multiple locations
            executor.map(lambda location: scrape_and_append_to_csv_for_location(location, driver), location_coordinates)

        # Close the WebDriver
        driver.quit()

    except Exception as e:
        print("Error:", e)


# Call the parallel scraping function once
scrape_data_in_parallel()
webbrowser.open("attendance_map_new.html", new=2)
