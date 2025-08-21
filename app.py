import os
import json
from io import BytesIO

import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, make_response
from dotenv import load_dotenv

# PDF Generation Imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# App Initialization & Configuration 
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# PDF Font Registration 
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))

#  AI Model Prompt 
SYSTEM_PROMPT = """
You are a "Smart Health Analyzer" AI. Your role is to analyze user-provided health symptoms
and provide helpful, safe, and informational advice.

**CRITICAL RULES:**
1.  **DO NOT provide a medical diagnosis.** Never say "you have..." or "it is likely...".
2.  **Always include a prominent disclaimer** to consult a healthcare professional.
3.  If symptoms sound severe (e.g., chest pain), your primary recommendation MUST be to "Seek immediate medical attention."
4.  **Respond in English.**
5.  **Structure your response in a clean JSON format** with three keys: "summary", "considerations", and "recommendations". The values should be arrays of strings.

Analyze the user's input and provide a response strictly in the JSON format described.
"""

# Flask Routes 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        user_input = request.json.get('symptoms')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"{SYSTEM_PROMPT}\n\nUser Input: \"{user_input}\""
        
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        ai_data = json.loads(cleaned_response)
        return jsonify(ai_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to analyze symptoms. Please try again."}), 500

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    data = request.json
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    titles = {
        'main': "Smart Health Analyzer Report", 
        'sum': "Identified Symptoms", 
        'con': "Potential Considerations", 
        'rec': "Recommended Actions", 
        'dis': "Disclaimer: This report is for informational purposes only."
    }
    
    width, height = letter
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'DejaVuSans'
    
    def draw_wrapped_text(surface, text_list, x, y_start, title):
        y = y_start
        surface.setFont('DejaVuSans', 14)
        surface.drawString(x, y, title)
        y -= 25
        for item in text_list:
            para = Paragraph(f"• {item}", styleN)
            w, h = para.wrapOn(surface, width - 2*x, height)
            if y - h < 50: # Page break
                surface.showPage()
                y = height - 50
            para.drawOn(surface, x, y - h)
            y -= (h + 10)
        return y

    p.setFont('DejaVuSans', 18)
    p.drawCentredString(width / 2.0, height - 50, titles['main'])
    y = height - 100
    y = draw_wrapped_text(p, data.get('summary', []), 50, y, titles['sum'])
    y = draw_wrapped_text(p, data.get('considerations', []), 50, y, titles['con'])
    y = draw_wrapped_text(p, data.get('recommendations', []), 50, y, titles['rec'])
    
    disclaimer = Paragraph(titles['dis'], styleN)
    disclaimer.wrapOn(p, width - 100, height)
    disclaimer.drawOn(p, 50, 40)

    p.save()
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=HealthReport.pdf'
    return response

if __name__ == '__main__':
    genai.configure(api_key=os.getenv("API_KEY"))
    app.run(debug=True)