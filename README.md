---

# **ODDIY AI AGENT YARATISH** 
## Python va Langchain yordamida

---

## **KIRISH VA UMUMIY TUSHUNCHA**

### Ushbu loyiha nima haqida?
Biz oddiy AI agent yaratamiz. Bu agent:
- Internetdan ma'lumot qidiradi
- Veb-saytlarni o'qiydi
- Topilgan ma'lumotlarni tahlil qiladi  
- Bizga tayyor javob va hisobot beradi

### Misol:
Tasavvur qiling, sizga IT xizmatlari kerak bo'lgan kompaniyalar ro'yxati kerak. Ushbu agent:
1. Google orqali qidirib topadi
2. Kompaniyalarning veb-saytlarini o'qiydi
3. Aloqa ma'lumotlarini topadi
4. Har biriga murojaat xatini yozadi
5. Hammasini fayl sifatida saqlaydi

Bularning barchasi **bir necha soniyada** amalga oshadi!

---

## **QADAM 1: ASOSIY TUSHUNCHALAR**

### **Langchain nima?**
- Langchain - bu framework (tizim)
- U yordamida biz AI modellarni (ChatGPT, Gemini, Claude) ishlatadigan dasturlar yasaymiz
- Langchain bizga "toollar" (vositalar) beradi - bu AI uchun maxsus funksiyalar

### **Toollar (vositalar) nima?**
- Toollar - bu AI uchun imkoniyatlar
- Masalan: internetdan qidirish, saytni o'qish, faylga saqlash
- AI o'zi qaysi toolni ishlatishni hal qiladi

### **Bizning loyihamiz qanday ishlaydi?**
```
Foydalanuvchi → Topshiriq beradi
          ↓
       AI Agent (Gemini)
          ↓
    Toollardan foydalanadi:
    - Qidirish
    - Saytni o'qish  
    - Natijani saqlash
          ↓
      Tayyor javob
```

---

## **QADAM 2: TAYYORGARLIK**

### **Kerakli dasturlar:**

1. **Python** - dasturlash tili (python.org/downloads dan yuklab oling)
2. **VS Code** yoki boshqa kod muharrir
3. **API Key** - Google Gemini uchun (bepul)

---

## **QADAM 3: LOYIHANI SOZLASH (Step-by-Step)**

### **Qadam 3.1: Papka yaratish**
```
Kompyuteringizda yangi papka yarating
Masalan: "AI_Agent_Project"
```

### **Qadam 3.2: requirements.txt fayli yaratish**
Ushbu faylda kerakli kutubxonalar ro'yxati bo'ladi:

```txt
langchain==0.3.13
langchain-core==0.3.28
langchain-community==0.3.13
langchain-google-genai==2.0.8
python-dotenv==1.0.1
pydantic==2.10.6
duckduckgo-search==7.1.0
beautifulsoup4==4.12.3
requests==2.32.3
```

**Tushuntirish:**
- `langchain` - asosiy kutubxona
- `langchain-google-genai` - Gemini bilan ishlash uchun
- `duckduckgo-search` - internetda qidirish uchun
- `beautifulsoup4` - veb-saytlarni o'qish uchun
- `pydantic` - ma'lumot strukturasini yaratish uchun

### **Qadam 3.3: Virtual muhit yaratish**

**Windows uchun:**
```bash
python -m venv venv
```

**Mac/Linux uchun:**
```bash
python3 -m venv venv
```

**Nima bo'ldi?** Papkangizda `venv` papkasi paydo bo'ldi - bu alohida Python muhiti.

### **Qadam 3.4: Virtual muhitni faollashtirish**

**Windows:**
```bash
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Qanday bilish mumkin?** Terminal oldida `(venv)` so'zi paydo bo'ladi.

### **Qadam 3.5: Kutubxonalarni o'rnatish**
```bash
pip install -r requirements.txt
```

Bu jarayon 1-2 daqiqa davom etishi mumkin.

---

## **QADAM 4: API KEY OLISH**

### **Google Gemini API Key olish:**

1. **aistudio.google.com** saytiga kiring
2. Google akkauntingiz bilan kiring
3. **"Get API Key"** tugmasini bosing
4. **"Create new project"** tanlang
5. Paydo bo'lgan kalitni **Copy** qiling

### **API Key-ni saqlash:**

`.env` nomli yangi fayl yarating va ichiga quyidagini yozing:

```
GEMINI_API_KEY="bu_yerga_sizning_kalitingiz"
```

**MUHIM:** Bu faylni hech kimga ko'rsatmang!

---

## **QADAM 5: KODLASH BOSHLASH**

### **Ikkita asosiy fayl yaratamiz:**

1. **tools.py** - AI uchun vositalar
2. **main.py** - asosiy dastur

---

## **QADAM 6: TOOLS.PY - VOSITALAR FAYLINI YARATISH**

Bu faylda 3 ta tool bo'ladi:

### **Tool 1: Internetdan qidirish**
### **Tool 2: Veb-saytni o'qish**  
### **Tool 3: Natijani faylga saqlash**

### **To'liq kod (tools.py):**

```python
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
```

### **Talabalar uchun tushuntirish:**

**save_to_txt** - bu oddiy funksiya, faylga yozadi
**scrape_website** - saytdan matnni oladi (BeautifulSoup kutubxonasi yordamida)
**search_and_scrape** - qidirib, keyin o'qiydi

---

## **QADAM 7: MAIN.PY - ASOSIY DASTUR**

Bu yerda AI-ga topshiriq beramiz va u toollardan foydalanadi.

### **To'liq kod (main.py):**

```python
# Kutubxonalarni yuklash
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools import scrape_tool, search_tool, save_tool

# API kalitini yuklash
load_dotenv()


# Har bir kompaniya ma'lumotining strukturasi
class LeadResponse(BaseModel):
    company: str  # Kompaniya nomi
    contact_info: str  # Aloqa ma'lumotlari
    email: str  # Email manzil
    summary: str  # Qisqacha tavsif
    outreach_message: str  # Murojaat xati
    tools_used: list[str]  # Ishlatilgan toollar


# Kompaniyalar ro'yxati strukturasi
class LeadResponseList(BaseModel):
    leads: list[LeadResponse]


# AI modelni tanlash (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Javob formatini belgilash
parser = PydanticOutputParser(pydantic_object=LeadResponseList)

# AI-ga topshiriq berish (PROMPT)
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Sen sotuvchilar uchun yordamchi AI agentsан.

    TOPSHIRIQ:
    1. Vancouver shahridan IT xizmatlariga muhtoj 5 ta kichik biznesni top
    2. Har bir kompaniya uchun:
       - Kompaniya nomini yoz
       - Aloqa ma'lumotlarini top
       - Email manzilni top
       - Nima uchun ularga IT xizmati kerakligini tushuntir
       - Ularga murojaat xatini yoz

    3. Natijani shu formatda ber: {format_instructions}
    4. So'ngida 'save' toolidan foydalanib faylga saqla
    """),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

# Toollarni ro'yxatga olish
tools = [scrape_tool, search_tool, save_tool]

# Agentni yaratish
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Agentni ishga tushirish uchun executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Topshiriqni aniqlash
query = "Vancouver shahridan IT xizmatlariga muhtoj 5 ta kichik kompaniyani top va tahlil qil"

# Agentni ishga tushirish
raw_response = agent_executor.invoke({"query": query})

# Natijani ko'rsatish
try:
    structured_response = parser.parse(raw_response.get('output'))
    print(structured_response)
except Exception as e:
    print("Xatolik:", e)
```

### **Kodni tushuntirish:**

**Qism 1: Import** - kerakli kutubxonalarni yuklash
**Qism 2: BaseModel** - ma'lumot strukturasi (Pydantic)
**Qism 3: LLM** - AI modelni tanlash
**Qism 4: Prompt** - AI-ga yo'riqnoma
**Qism 5: Agent** - hamma narsani birlashtirish

---

## **QADAM 8: DASTURNI ISHGA TUSHIRISH**

Terminal ochib, quyidagini yozing:

**Windows:**
```bash
python main.py
```

**Mac/Linux:**
```bash
python3 main.py
```

### **Nima bo'ladi?**

1. AI Gemini ishga tushadi
2. U toollarni ishlatib boshlanadi
3. Siz terminalda ko'rasiz:
   - Qaysi toolni ishlayotganini
   - Nima topilayotganini
   - Qanday fikrlayotganini

4. Oxirida `leads_output.txt` fayli yaratiladi
5. Unda 5 ta kompaniya, ularning ma'lumotlari va murojaat xatlari bo'ladi

---

## **NATIJA VA XULOSA**

### **Nima yaratdik?**

Biz **AI Agent** yaratdik. Bu agent:
- ✅ O'zi qidiradi
- ✅ O'zi tahlil qiladi
- ✅ O'zi xat yozadi
- ✅ O'zi natijani saqlaydi

### **Bu nimaga foydali?**

- Vaqt tejash (soatlarga bajariladigan ish bir necha soniyada)
- Xatoliklar kamayadi
- Ko'p ma'lumotni tez qayta ishlash

### **Keyingi bosqichlar:**

1. Boshqa AI modellarni sinab ko'ring (OpenAI, Claude)
2. Ko'proq toollar qo'shing (email yuborish, Excel yaratish)
3. Veb-interfeys qo'shing (Flask, Django)
4. Ma'lumotlar bazasiga ulanadi

---

## **DARSDA AMALIY MASHQ**

### **Talabalar bilan qilish kerak bo'lgan mashqlar:**

1. **Oddiy mashq:** Faqat qidiruv toolini ishlatib, bitta kompaniya haqida ma'lumot topish
2. **O'rta mashq:** Promptni o'zgartiring - boshqa shahar yoki boshqa soha
3. **Qiyin mashq:** Yangi tool qo'shing - masalan, email jo'natish

---
