from PIL import Image
import sys
from fpdf import FPDF
from docx import Document
import pytesseract as tess
def recognize(image):
	return tess.image_to_string(Image.open("example.png"),config='-c preserve_interword_spaces=1')

def to_pdf():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial",size = 12)
	pdf.cell(200, 10, txt=recognize(sys.argv[0]),ln = 1, align="L")
	pdf.output(str(sys.argv[2])+".pdf")

def to_word():
	doc = Document()
	doc.add_paragraph(recognize(sys.argv[0]))
	doc.save(str(sys.argv[2])+".docx")

def to_txt():
	f = open(str(sys.argv[2])+".txt","w+")
	f.write(recognize(sys.argv[0]))
	f.close()

if sys.argv[2] == "pdf":
	to_pdf()
elif sys.argv[2] == "docx":
	to_word()
else:
	to_txt()