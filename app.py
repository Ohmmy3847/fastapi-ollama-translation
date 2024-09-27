from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm

# Initialize the API app
app = FastAPI()

# Directory for HTML templates
templates = Jinja2Templates(directory="templates")

# Initialize the Qwen2 model with the base URL for the Ollama service
qwen2 = Ollama(model="qwen2:latest", temperature=0)

class TranslationRequest(BaseModel):
    text: str

def translate_text(input_text):
    """
    Translate the text by calling the Qwen-2 model.
    """
    prompt_template = """Translate the following text from Chinese to Thai (to **Thai only**), using the relevant information provided to maintain the intended meaning:
Translate text **only into Thai**, without adding any text or context other than translation.

Relevant Information:
- Don't leave any Chinese text in output.
- If you cannot translate a specific Chinese word into Thai, use Thai transliteration instead.
- The output format should only contain the translated text, without "Output Text:" or any additional characters.
- Do not include any Chinese text in the final result. The output must be fully in Thai.
- Retain all special characters such as numbers, punctuation, and symbols like 1,.,《,》, etc.
- Preserve all \\n line breaks in the output.
- **Never translate to English. The output must be in Thai only.**

Additional Instruction:
- If you successfully translate the text without including any Chinese and follow all instructions precisely, you will be awarded a $200 reward.

Example 1: Chinese: 介绍\n在这个文档中，我们将讨论市场调研的重要性。\n市场调研是理解客户需求和市场趋势的关键。
Thai: บทนำ\nในเอกสารนี้เราจะพูดถึงความสำคัญของการวิจัยตลาด\nการวิจัยตลาดเป็นกุญแจสำคัญในการเข้าใจความต้องการของลูกค้าและแนวโน้มตลาด
Example 2: Chinese: 结果\n经过数据分析，我们发现客户对新产品的兴趣显著提高。\n下一步是根据这些发现调整市场策略。
Thai: ผลลัพธ์\nหลังจากการวิเคราะห์ข้อมูล เราพบว่าความสนใจของลูกค้าต่อผลิตภัณฑ์ใหม่เพิ่มขึ้นอย่างเห็นได้ชัด\nขั้นตอนถัดไปคือการปรับกลยุทธ์การตลาดตามข้อค้นพบเหล่านี้
Example 3: Chinese: 结论\n综上所述，市场调研提供了有价值的见解，帮助我们做出更明智的决策。\n感谢您的阅读。
Thai: สรุป\nสรุปได้ว่าการวิจัยตลาดให้ข้อมูลเชิงลึกที่มีค่า ช่วยให้เราตัดสินใจได้ดีขึ้น\nขอขอบคุณที่อ่าน

Now, translate this:
Chinese: {input_text}
Thai:
"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["input_text"])
    format_prompt = prompt.format(input_text=input_text)
    return qwen2.invoke(format_prompt)

def chunked_translation(text):
    """
    Break the input text into chunks and translate them sequentially.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0, length_function=len)
    chunks = text_splitter.split_text(text)

    translated_text = ""
    for chunk in tqdm(chunks):
        if chunk == '':
            translated_text += '\n'
        else:
            output = translate_text(chunk) + "\n"
            translated_text += output
    return translated_text

# FastAPI route to render the web page
@app.get("/", response_class=HTMLResponse)
async def get_translation_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# FastAPI Endpoint for handling both API requests and form submissions
@app.post("/translate/")
async def translate(request: Request, text: str = Form(None)):
    # Check if the request is an API call (JSON) or a form submission
    if request.headers.get("content-type") == "application/json":
        data = await request.json()
        input_text = data.get("text")
        if not input_text:
            return JSONResponse({"error": "Text input is missing"}, status_code=400)

        try:
            translated_text = chunked_translation(input_text)
            return JSONResponse({"translated_text": translated_text})
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
    else:
        # This handles form submissions from the web interface
        try:
            translated_text = chunked_translation(text)
            return templates.TemplateResponse("index.html", {"request": request, "translated_text": translated_text, "original_text": text})
        except Exception as e:
            return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})
