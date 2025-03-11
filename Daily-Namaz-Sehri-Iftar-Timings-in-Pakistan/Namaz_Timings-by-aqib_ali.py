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
st.markdown(custom_css, unsafe_allow_html=True)

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
        time_obj = datetime.strptime(time_24h, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except ValueError:
        return time_24h

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
    asr_time = datetime.strptime(timings['Asr'], "%H:%M")
    hanafi_asr_time = (asr_time + timedelta(hours=1, minutes=30)).strftime("%H:%M")
    timings['Asr'] = hanafi_asr_time
    return timings

# Function to display Namaz and Sehri/Iftar timings
def display_timings(hanafi_timings, jafri_timings, today_date, tomorrow_date):
    st.write(f"### 🕌 Namaz Timings (Hanafi) - {today_date}")
    st.write(f"**Fajr:** {convert_to_12_hour_format(hanafi_timings['Fajr'])}")
    st.write(f"**Dhuhr:** {convert_to_12_hour_format(hanafi_timings['Dhuhr'])}")
    st.write(f"**Asr (Hanafi):** {convert_to_12_hour_format(hanafi_timings['Asr'])}")
    st.write(f"**Maghrib:** {convert_to_12_hour_format(hanafi_timings['Maghrib'])}")
    st.write(f"**Isha:** {convert_to_12_hour_format(hanafi_timings['Isha'])}")
    
    st.write(f"### 🌙 Sehri & Iftar Times - {today_date}")
    st.write(f"**Sehri (Hanafi):** {convert_to_12_hour_format(hanafi_timings['Fajr'])}")
    st.write(f"**Iftar (Hanafi):** {convert_to_12_hour_format(hanafi_timings['Maghrib'])}")
    st.write(f"**Sehri (Jafri):** {convert_to_12_hour_format(jafri_timings['Fajr'])}")
    st.write(f"**Iftar (Jafri):** {convert_to_12_hour_format(jafri_timings['Maghrib'])}")
    
    st.write(f"### 🕋 Sehri Timing - {tomorrow_date}")
    st.write(f"**Sehri (Hanafi):** {convert_to_12_hour_format(hanafi_timings['Fajr'])}")
    st.write(f"**Sehri (Jafri):** {convert_to_12_hour_format(jafri_timings['Fajr'])}")

# Streamlit App
def main():
    st.title("🕌 Daily Namaz Timings in Pakistan")
    
    selected_city = st.selectbox("Select a city", list(cities.keys()))
    
    if st.button("Get Timings"):
        city = cities[selected_city]
        today_date = datetime.now().strftime("%d-%m-%Y")
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        
        hanafi_timings = get_namaz_timings(city, today_date, method=1)
        jafri_timings = get_namaz_timings(city, today_date, method=7)
        
        if hanafi_timings and jafri_timings:
            hanafi_timings = adjust_asr_for_hanafi(hanafi_timings)
            display_timings(hanafi_timings, jafri_timings, today_date, tomorrow_date)
        else:
            st.error("Failed to fetch Namaz timings. Please try again later.")

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
