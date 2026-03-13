import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser


# -----------------------------
# Function to download HTML
# -----------------------------
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return None


# -----------------------------
# Function to get robots.txt
# -----------------------------
def get_robot_parser(base_url):
    robots_url = urljoin(base_url, "/robots.txt")

    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        parser.read()
    except:
        print("Could not read robots.txt")

    return parser


# -----------------------------
# Function to extract links
# -----------------------------
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for tag in soup.find_all("a", href=True):
        link = urljoin(base_url, tag["href"])
        links.append(link)

    return links


# -----------------------------
# Web crawler function
# -----------------------------
def crawl(start_url, max_depth=2, delay=2):

    visited = set()

    robot_parser = get_robot_parser(start_url)

    def recursive_crawl(url, depth):

        if depth > max_depth or url in visited:
            return

        if not robot_parser.can_fetch("*", url):
            print("Blocked by robots.txt:", url)
            return

        visited.add(url)

        print("Crawling:", url)

        html = get_html(url)

        if not html:
            return

        links = extract_links(html, url)

        time.sleep(delay)

        for link in links:
            recursive_crawl(link, depth + 1)

    recursive_crawl(start_url, 1)


# -----------------------------
# Run crawler
# -----------------------------
crawl("https://www.wikipedia.org", max_depth=2, delay=2)
