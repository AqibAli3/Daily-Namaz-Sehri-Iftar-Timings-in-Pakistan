import streamlit as st
import requests
from datetime import datetime, timedelta

# Set page title and favicon
st.set_page_config(page_title="Daily Namaz Timings in Pakistan by Syed Aqib Ali", page_icon="🕌")

# Define custom CSS to style the app
custom_css = """
<style>
.contact-details {
    text-align: center;
    margin-top: 20px;
}
.contact-details p {
    font-size: 18px;
    font-weight: bold;
}
.contact-details a {
    margin: 0 10px;
    display: inline-block;
}
.contact-details img {
    width: 30px;
    height: 30px;
    transition: transform 0.2s;
}
.contact-details img:hover {
    transform: scale(1.2);
}
.title-header {
    text-align: center;
    color: #2E8B57;
}
.task-section, .namaz-timings {
    background-color: #E6F2FF;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 20px;
}
</style>
"""
# Define the cities
cities = {
    "Karachi": "Karachi",
    "Lahore": "Lahore",
    "Islamabad": "Islamabad",
    "Rawalpindi": "Rawalpindi",
    "Peshawar": "Peshawar",
    "Quetta": "Quetta",
    "Multan": "Multan",
    "Faisalabad": "Faisalabad",
    "Hyderabad": "Hyderabad",
    "Gujranwala": "Gujranwala"
}

# Function to convert 24-hour time to 12-hour time
def convert_to_12_hour_format(time_24h):
    try:
        # Parse the 24-hour time
        time_obj = datetime.strptime(time_24h, "%H:%M")
        # Convert to 12-hour format with AM/PM
        return time_obj.strftime("%I:%M %p")
    except ValueError:
        return time_24h  # Return as-is if parsing fails

# Function to fetch Namaz timings from Aladhan API
def get_namaz_timings(city, date, method):
    url = f"http://api.aladhan.com/v1/timingsByCity/{date}?city={city}&country=Pakistan&method={method}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]["timings"]
    else:
        return None

# Function to adjust Asr timing for Hanafi
def adjust_asr_for_hanafi(timings):
    # Convert Asr time to datetime object
    asr_time = datetime.strptime(timings['Asr'], "%H:%M")
    # Add 1 hour and 30 minutes to Asr time for Hanafi
    hanafi_asr_time = (asr_time + timedelta(hours=1, minutes=30)).strftime("%H:%M")
    # Update the timings dictionary
    timings['Asr'] = hanafi_asr_time
    return timings

# Function to calculate Jafri Sehri and Iftar timings
def calculate_jafri_timings(timings):
    # Convert Fajr and Maghrib times to datetime objects
    fajr_time = datetime.strptime(timings['Fajr'], "%H:%M")
    maghrib_time = datetime.strptime(timings['Maghrib'], "%H:%M")
    
    # Calculate Jafri Sehri (10 minutes earlier than Hanafi Fajr)
    jafri_sehri_time = (fajr_time - timedelta(minutes=10)).strftime("%H:%M")
    
    # Calculate Jafri Iftar (10 minutes later than Hanafi Maghrib)
    jafri_iftar_time = (maghrib_time + timedelta(minutes=10)).strftime("%H:%M")
    
    return jafri_sehri_time, jafri_iftar_time

# Function to display Namaz timings
def display_namaz_timings(timings, jafri_sehri, jafri_iftar, next_date_sehri_hanafi, next_date_sehri_jafri, today_date, tomorrow_date):
    st.write(f"### Namaz Timings (Hanafi) - {today_date}")
    st.write(f"**Fajr:** {convert_to_12_hour_format(timings['Fajr'])}")
    st.write(f"**Dhuhr:** {convert_to_12_hour_format(timings['Dhuhr'])}")
    st.write(f"**Asr (Hanafi):** {convert_to_12_hour_format(timings['Asr'])}")  
    st.write(f"**Maghrib:** {convert_to_12_hour_format(timings['Maghrib'])}")
    st.write(f"**Isha:** {convert_to_12_hour_format(timings['Isha'])}")

    # Highlight Sehri and Iftar times
    st.write(f"### Sehri & Iftar Times - {today_date}")
    st.write(f"**Sehri (Hanafi):** {convert_to_12_hour_format(timings['Fajr'])}")
    st.write(f"**Iftar (Hanafi):** {convert_to_12_hour_format(timings['Maghrib'])}")
    st.write(f"**Sehri (Jafri):** {convert_to_12_hour_format(jafri_sehri)}")
    st.write(f"**Iftar (Jafri):** {convert_to_12_hour_format(jafri_iftar)}")
    
    # Display next date's Sehri timing
    st.write(f"### Sehri Timing - {tomorrow_date}")
    st.write(f"**Sehri (Hanafi):** {convert_to_12_hour_format(next_date_sehri_hanafi)}")
    st.write(f"**Sehri (Jafri):** {convert_to_12_hour_format(next_date_sehri_jafri)}")

# Streamlit App
def main():
    st.title("Daily Namaz Timings in Pakistan")
    
    # Dropdown to select city
    selected_city = st.selectbox("Select a city", list(cities.keys()))
    
    # Fetch and display Namaz timings
    if st.button("Get Namaz Timings"):
        city = cities[selected_city]
        
        # Get today's date
        today_date = datetime.now().strftime("%d-%m-%Y")
        
        # Get tomorrow's date
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        
        # Fetch today's timings (Hanafi)
        timings = get_namaz_timings(city, today_date, method=1)
        if timings:
            # Adjust Asr timing for Hanafi
            timings = adjust_asr_for_hanafi(timings)
            # Calculate Jafri Sehri and Iftar timings
            jafri_sehri, jafri_iftar = calculate_jafri_timings(timings)
            
            # Fetch next date's Fajr timing for Hanafi and Jafri
            next_date_timings_hanafi = get_namaz_timings(city, tomorrow_date, method=1)
            next_date_timings_jafri = get_namaz_timings(city, tomorrow_date, method=2)
            
            if next_date_timings_hanafi and next_date_timings_jafri:
                next_date_sehri_hanafi = next_date_timings_hanafi['Fajr']
                next_date_fajr_jafri = datetime.strptime(next_date_timings_jafri['Fajr'], "%H:%M")
                next_date_sehri_jafri = (next_date_fajr_jafri - timedelta(minutes=10)).strftime("%H:%M")
            else:
                next_date_sehri_hanafi = "Not available"
                next_date_sehri_jafri = "Not available"
            
            # Display timings
            display_namaz_timings(timings, jafri_sehri, jafri_iftar, next_date_sehri_hanafi, next_date_sehri_jafri, today_date, tomorrow_date)
        else:
            st.error("Failed to fetch Namaz timings. Please try again later.")
 # Add contact details at the bottom
    st.markdown(
        """
        <div class="contact-details">
            <p>Contact Me:</p>
            <a href="https://www.linkedin.com/in/syed-aqib-ali/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn">
            </a>
            <a href="https://github.com/AqibAli3" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub">
            </a>
            <a href="https://wa.me/+923158796106" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
            </a>
            <a href="mailto:shaali254@gmail.com">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Mail_%28iOS%29.svg" alt="Email">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
if __name__ == "__main__":
    main()
