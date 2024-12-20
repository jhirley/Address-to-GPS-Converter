
# Address to GPS Converter

This project provides a Streamlit app that converts addresses from an Excel file into GPS coordinates (latitude and longitude) using the Nominatim geocoding service. Users can upload a `.xls` or `.xlsx` file containing parts of an address (Street, City, State, Postal Code, Country), and the app will combine these parts, geocode the addresses, and return the latitude and longitude for each address.

## Features
- Upload an Excel file containing address data.
- Automatically combine address columns into full addresses.
- Geocode the addresses to latitude and longitude.
- Display the updated data with GPS coordinates.
- Download the updated spreadsheet with added latitude, longitude, and Google Maps links.

## Requirements
- Python 3.7+
- Streamlit
- Pandas
- Geopy
- stqdm
- openpyxl

## Installation

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jhirley/Address-to-GPS-Converter.git
   cd Address-to-GPS-Converter
   pip install -r requirements.txt
   streamlit run app.py
   http://localhost:8501/

### Docker Setup
1. If you have docker-compose installed, you can start the app using the following command:
    ```bash
    docker-compose up
    http://localhost:8501/

With these instructions, users will be able to quickly set up and run the app both locally and using Docker.
