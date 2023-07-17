import os
import requests
from bs4 import BeautifulSoup


def is_directory_empty(directory_path):
    try:
        with os.scandir(directory_path) as dir_iterator:
            next(dir_iterator)
    except StopIteration:
        return True
    return False


# The base URL for the site
base_url = "https://quizbowlpackets.com"

# The directory where you want to store the downloaded files
download_dir = "/Users/jeligooch/Desktop/git/quizbowl_data/packet_scraper/highschool"

# Get the main page HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the individual packet links on the main page
packet_links = soup.select('span.Name a')

# Loop through the packet links
for link in packet_links:
    # Create a new directory for this packet
    packet_name = link.text
    packet_dir = os.path.join(download_dir, packet_name)
    os.makedirs(packet_dir, exist_ok=True)

    if not is_directory_empty(packet_dir):
        continue

    # Get the packet page HTML
    packet_url = base_url + "/" + link.get('href')
    response = requests.get(packet_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the file download links on the packet page
    file_links = soup.select('li a')

    # Loop through the file links
    for file_link in file_links:
        # Check if the file is a .pdf, .docx, or other acceptable format
        if file_link.get('href').endswith(('.pdf', '.docx', '.txt', '.rtf', '.doc', '.zip')):
            # Download the file
            file_url = file_link.get('href')
            response = requests.get(file_url)
            file_name = os.path.join(packet_dir, file_url.split("/")[-1])

            with open(file_name, 'wb') as file:
                file.write(response.content)
