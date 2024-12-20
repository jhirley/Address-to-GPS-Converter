import streamlit as st
import requests
from stqdm import stqdm
from time import sleep
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from io import BytesIO



def geocode_address(address):
    """
    Geocodes an address to its latitude and longitude coordinates.

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: A tuple containing the latitude and longitude of the address.
               If the address cannot be geocoded, returns (None, None).

    Raises:
        GeocoderTimedOut: If the geocoding service times out.
        Exception: For any other exceptions that may occur during geocoding.
    """
    # Create a geolocator object with a user agent "address-to-gps"
    geolocator = Nominatim(user_agent="address-to-gps")
    try:
        # Attempt to geocode the address with a timeout of 10 seconds
        location = geolocator.geocode(address, timeout=10)
        if location:
            # If the location is found, return its latitude and longitude
            return location.latitude, location.longitude
        else:
            # If the location is not found, return (None, None)
            return None, None
    except GeocoderTimedOut:
        # If a timeout error occurs, return (None, None)
        return None, None
    except Exception as e:
        # If any other exception occurs, return (None, None)
        return None, None

def main():
    # Set the title of the Streamlit app
    st.title("Address to GPS Converter")
    
    # Provide a description of the app's functionality
    st.write(
        "Upload an `.xls` spreadsheet with columns containing parts of an address (e.g., Street, City, State, Postal Code, Country). "
        "The app will combine these columns into full addresses and generate latitude and longitude."
    )

    # Create a file uploader widget to allow users to upload an Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xls", "xlsx"])
    if uploaded_file:
        try:
            # Read the uploaded file
            df = pd.read_excel(uploaded_file, dtype=str)
            
            # Handle missing values
            df = df.fillna("") # Replace zeros with empty strings
            df = df.replace(0, "") # Replace zeros with empty strings
            # Loop through the DataFrame and replace non-null, non-empty values with ""
            for col in df.columns:
                df[col] = df[col].apply(lambda x: "" if isinstance(x, str) and len(x) == 1 else x)
                df[col] = df[col].apply(lambda x: str(x).replace('"', '').replace("'", '') if isinstance(x, str) else x)

            # Display the uploaded spreadsheet
            st.write("Uploaded Spreadsheet:")
            st.dataframe(df)

            # Allow the user to select columns that make up the address
            address_columns = st.multiselect(
                "Select the columns that make up the address (in the correct order):",
                df.columns
            )

            # Create a button to convert the addresses to GPS coordinates
            if st.button("Convert Addresses"):
                if not address_columns:
                    st.error("Please select at least one column for the address.")
                    return

                # Create a geolocator object with a user agent "address-to-gps"
                geolocator = Nominatim(user_agent="address-to-gps")
                
                # Initialize lists to store latitude and longitude values
                latitudes = []
                longitudes = []


                # Concatenate selected columns to form full addresses
                df['Full_Address'] = df[address_columns].apply(
                    lambda row: ', '.join(row.values.astype(str)).strip(), axis=1
                )
                # Loop through the DataFrame and replace double commas with single commas
                for col in df.columns:
                    df[col] = df[col].apply(lambda x: str(x).replace(',,', ',') if isinstance(x, str) else x)
                    df[col] = df[col].apply(lambda x: str(x).replace(', ,', ',') if isinstance(x, str) else x)

                st.write("Converting addresses to GPS coordinates...")

                # Loop through each address in the DataFrame and geocode it
                # if you have not used stqdm before, you can replace it with a regular for loop
                # but check it out it is a nice progress bar for loops
                for address in stqdm(df['Full_Address'].tolist(), desc="Processing rows"):
                    sleep(.25)  # some sleep to avoid hitting the geocoding API too fast
                    lat, lon = geocode_address(address)

                    latitudes.append(lat)
                    longitudes.append(lon)

                # Ensure latitudes and longitudes are the same length as the DataFrame
                df["Latitude"] = latitudes
                df["Longitude"] = longitudes

                # Add Google Maps links
                df["Google_Maps_Link"] = df.apply(
                    lambda row: f"https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" 
                    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']) 
                    else "",
                    axis=1
                )

                # Display the updated spreadsheet
                st.write("Updated Spreadsheet:")
                st.dataframe(df)

                # Provide a download link for the updated spreadsheet
                output_buffer = BytesIO()
                df.to_excel(output_buffer, index=False, engine='openpyxl')
                output_buffer.seek(0)

                # Create a download button to download the updated spreadsheet
                st.download_button(
                    label="Download Updated Spreadsheet",
                    data=output_buffer,
                    file_name="converted_addresses.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        # Handle exceptionsY
        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
