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
    Sen sotuvchilar uchun yordamchi AI agentsаn.

    TOPSHIRIQ:
    1. Uzbek tilida yoz barchar so'zlarni
    2. Toshkent shahridan IT xizmatlariga muhtoj 5 ta kichik biznesni top
    3. Har bir kompaniya uchun:
       - Kompaniya nomini yoz
       - Aloqa ma'lumotlarini top
       - Email manzilni top
       - Nima uchun ularga IT xizmati kerakligini tushuntir
       - Ularga murojaat xatini yoz

    4. Natijani shu formatda ber: {format_instructions}
    5. So'ngida 'save' toolidan foydalanib faylga saqla
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
query = "Toshkent shahridan IT xizmatlariga muhtoj 5 ta kichik kompaniyani top va tahlil qil"

# Agentni ishga tushirish
raw_response = agent_executor.invoke({"query": query})

# Natijani ko'rsatish
try:
    structured_response = parser.parse(raw_response.get('output'))
    # print(structured_response)
except Exception as e:
    print("Xatolik:", e)
