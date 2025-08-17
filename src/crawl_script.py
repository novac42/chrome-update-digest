import requests
from bs4 import BeautifulSoup
import html2text
import re
from config_manager import get_enterprise_url

def get_version_from_url(url):
    match = re.search(r'answer/(\d+)', url)
    if match:
        return match.group(1)
    return 'unknown'

def main():
    url = get_enterprise_url()
    version = get_version_from_url(url)
    output_filename = f"{version}-chrome-enterprise.md"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Attempt to find the main content area
    # Based on previous browser_view, content is often within div with class 'zippy-wrapper' or 'article-container'
    main_content = soup.find('div', class_='zippy-wrapper')
    if not main_content:
        main_content = soup.find('div', class_='article-container')
    if not main_content:
        main_content = soup.find('div', class_='article-content') # Another common class
    if not main_content:
        main_content = soup.find('div', id='article-content') # Another common id

    if not main_content:
        print("Could not find main content div. Attempting to parse entire body.")
        main_content = soup.body

    if not main_content:
        print("Could not find any content to parse.")
        return

    # Initialize html2text converter
    h = html2text.HTML2Text()
    h.body_width = 0  # Disable line wrapping
    h.ignore_links = False
    h.ignore_images = False
    h.unicode_snob = True
    h.skip_internal_links = True
    h.inline_links = False
    h.protect_links = True
    h.single_line_break = True # Treat <br> as single line break

    markdown_content = h.handle(str(main_content))

    # Post-processing for better Markdown:
    # Remove excessive blank lines
    markdown_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_content)
    # Remove common unwanted elements like 

