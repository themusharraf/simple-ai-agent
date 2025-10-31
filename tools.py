# Kerakli kutubxonalarni import qilish
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


# TOOL 1: Natijalarni faylga saqlash
def save_to_txt(data: str, filename: str = "leads_output.txt"):
    """Bu funksiya natijalarni faylga yozadi"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Topilgan kompaniyalar ---\nVaqt: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Ma'lumot {filename} fayliga saqlandi"


# TOOL 2: Veb-saytni o'qish
def scrape_website(url: str) -> str:
    """Bu funksiya veb-saytdan matnni o'qiydi"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        # HTML-ni tozalash
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r'\s+', ' ', text)

        # Faqat 5000 belgini olamiz (tezlik uchun)
        return text[:5000]
    except Exception as e:
        return f"Xatolik: {e}"


# TOOL 3: Qidiruv so'rovlarini yaratish
def generate_search_queries(company_name: str) -> list[str]:
    """Kompaniya nomi bo'yicha qidiruv so'rovlari yaratadi"""
    keywords = ["IT xizmatlari", "texnologiya yechimlari", "kompyuter xizmatlari"]
    return [f"{company_name} {keyword}" for keyword in keywords]


# Asosiy qidiruv va o'qish funksiyasi
def search_and_scrape(company_name: str) -> str:
    """Internetda qidirib, saytlarni o'qiydi"""
    queries = generate_search_queries(company_name)
    results = []

    for query in queries:
        # Qidirish
        search_results = search.run(query)

        # URL manzillarni topish
        urls = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            search_results
        )

        # Birinchi URL-ni o'qish
        if urls:
            results.append(scrape_website(urls[0]))

    return " ".join(results)


# DuckDuckGo qidiruvini sozlash
search = DuckDuckGoSearchRun()

# Barcha toollarni e'lon qilish
search_tool = Tool(
    name="search",
    func=search.run,
    description="Internetdan ma'lumot qidiradi",
)

scrape_tool = Tool(
    name="scrape_website",
    func=search_and_scrape,
    description="Veb-saytni o'qiydi va ma'lumot topadi",
)

save_tool = Tool(
    name="save",
    func=save_to_txt,
    description="Ma'lumotni faylga saqlaydi",
)