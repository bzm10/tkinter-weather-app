# Import necessary modules
import tkinter as tk
from tkinter import ttk
import requests
import csv
from PIL import Image, ImageTk
from tkinter import messagebox

# Function to display weather icon based on the weather code
def display_icon(weather_window):
    global weather_code

    # Map weather codes to corresponding icon filenames
    if int(weather_code) in [0, 1]:
        path = "sun.png"
    elif int(weather_code) in [2, 3]:
        path = "cloud.png"
    elif int(weather_code) in [45, 48]:
        path = "fog.png"
    elif int(weather_code) in [51, 53, 55, 56, 57]:
        path = "drizzle.png"  # Corrected spelling
    elif int(weather_code) in [61, 63, 65, 80, 81, 82]:
        path = "rain.png"
    elif int(weather_code) in [66, 67]:
        path = "hail.png"
    elif int(weather_code) in [71, 73, 75, 85, 86, 77]:
        path = "snow.png"
    elif int(weather_code) in [95, 96, 99]:
        path = "thunderstorm.png"
    else:
        path = "error.png"

    # Load and resize the icon image
    icon_image = Image.open(f"icons/{path}")
    icon_image = icon_image.resize((90, 90), Image.Resampling.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Display the icon in the weather window
    icon_label = tk.Label(weather_window, image=icon_photo)
    icon_label.image = icon_photo  # Keep a reference to avoid garbage collection
    icon_label.pack(padx=10)  # Pack the label into the window

# Function to fetch and display weather data
def get_weather():
    global weather_code

    # get the selected city
    city = city_var.get()
    
    # Check if a city is selected
    if city == "Select a City":
        messagebox.showerror("Error", "Please select a city")
        return

    # Create a new window to display weather information
    weather_window = tk.Toplevel(root)
    weather_window.title("Weather Information")

    # Retrieve the selected city and its coordinates
    latitude, longitude = city_coordinates[city]

    # Construct the API request URL
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=weathercode,temperature_2m,wind_speed_10m,relative_humidity_2m"
    response = requests.get(url)
    weather_data = response.json()

    # Extract and display the current weather data
    current_weather = weather_data.get("current", {})
    temperature = current_weather.get("temperature_2m", "N/A")
    wind_speed = current_weather.get("wind_speed_10m", "N/A")
    humidity = current_weather.get("relative_humidity_2m", "N/A")
    weather_code = current_weather.get("weathercode", "N/A")

    # Unit conversion

    # Convert temperature Celsius or Fahrenheit
    if temp_unit.get() == "°F":
        temperature = (temperature * 9 / 5) + 32
        temperature = round(temperature, 1)
        temp_symbol = "°F"
    else:
        temp_symbol = "°C"

    # Convert wind speed to km/h or mph
    if wind_unit.get() == "mph":
        wind_speed = wind_speed * 0.621371
        wind_speed = round(wind_speed, 1)
        wind_label_symbol = "mph"
    else:
        wind_label_symbol = "km/h"

    # Define weather conditions based on WMO codes
    weather_conditions = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with light hail", 99: "Thunderstorm with heavy hail"
    }

    # Get the weather condition based on the weather code
    weather_condition = weather_conditions.get(weather_code, "Unknown")

    # Create labels to display weather information in the window
    weather_label1 = tk.Label(weather_window, text=f"Weather in {city}:", font=(None, 22))
    weather_label1.pack(padx=10, pady=2)

    display_icon(weather_window)  # Call the function to display the weather icon

    # Display the weather information
    weather_info = f"Temperature: {temperature} {temp_symbol}\nWind Speed: {wind_speed} {wind_label_symbol}\nHumidity: {humidity} %\nWeather Condition: {weather_condition}"
    weather_label = tk.Label(weather_window, text=weather_info, font=(None, 30))
    weather_label.pack(padx=10, pady=2)

    # Credits for the weather icons
    credits = tk.Label(weather_window, text="Icons by Icons8", font=(None, 10),cursor="hand2")
    credits.pack(padx=10, pady=2)

    # add a link to icons8
    def callback(event):
        import webbrowser
        webbrowser.open_new(r"https://icons8.com/")
    credits.bind("<Button-1>", callback)
      

# Load city coordinates from a CSV file
city_coordinates = {}
# Open the CSV file and read the data into a dictionary
with open('locations.csv', newline='') as csvfile:
    # Use the DictReader class to create a
    reader = csv.DictReader(csvfile)
    # Sort the data based on the city name
    sorted_data = sorted(reader, key=lambda x: x['City'])
    # Iterate over the sorted data and store the city coordinates in a dictionary
    for row in sorted_data:
        # Store the city name as the key and the coordinates as the value
        city_coordinates[row['City']] = (row['Latitude'], row['Longitude'])

# Set up the main application window
root = tk.Tk()
root.title("Weather App")

# Dropdown menu for city selection with a placeholder
city_var = tk.StringVar(value="Select a City")  # Set initial value as the placeholder
city_dropdown = ttk.Combobox(root, textvariable=city_var, height=20)
city_dropdown['values'] = ['Select a City'] + list(city_coordinates.keys())  # Add placeholder to the list of cities
city_dropdown['state'] = 'readonly'
city_dropdown.pack(padx=10, pady=10)

# Temperature unit

# label for temperature unit

temp_label = tk.Label(root, text="Temperature Unit:", font=(None, 12))
temp_label.pack(pady=5, anchor='w',padx=10)

temp_unit = tk.StringVar(value="°C")  # Set initial value as °C

# Create two Radiobuttons
celsius_radio = ttk.Radiobutton(root, text="°C", variable=temp_unit, value="°C")
fahrenheit_radio = ttk.Radiobutton(root, text="°F", variable=temp_unit, value="°F")

# Use pack to place the Radiobuttons next to each other
celsius_radio.pack(anchor='w', pady=5, padx=15)
fahrenheit_radio.pack(anchor='w', pady=5,padx=15)

# wind speed unit

# label for wind speed unit
wind_label = tk.Label(root, text="Wind Speed Unit:", font=(None, 12))
wind_label.pack(pady=5, anchor='w',padx=10)

wind_unit = tk.StringVar(value="km/h")  # Set initial value as km/h

# Create two Radiobuttons
kmh_radio = ttk.Radiobutton(root, text="km/h", variable=wind_unit, value="km/h")
mph_radio = ttk.Radiobutton(root, text="mph", variable=wind_unit, value="mph")

# Use pack to place the Radiobuttons next to each other
kmh_radio.pack(anchor='w', pady=5, padx=15)
mph_radio.pack(anchor='w', pady=5,padx=15)

# Add a button to fetch weather data
search_button = tk.Button(root, text="Show Weather", command=get_weather)
search_button.pack(padx=10, pady=10)

# credit to api
credit_label = tk.Label(root, text="Weather data by Open-Meteo.com", font=(None, 11),cursor="hand2")
credit_label.pack(pady=5)

# add a link to open-meteo
def callback(event):
    import webbrowser
    webbrowser.open_new(r"https://open-meteo.com/")
credit_label.bind("<Button-1>", callback)

# Start the Tkinter event loop
root.mainloop()
