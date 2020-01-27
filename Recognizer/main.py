from PIL import Image
import sys
from fpdf import FPDF, HTMLMixin
from docx import Document
import pytesseract as tess
from table import Table
from table_main import find_table
import cv2 as cv
import numpy as np

#RECOGNIZING TEXT ON THE IMAGE

def transform(image,to):
	if to == "PIL":
		img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		im_pil = Image.fromarray(img)
		return im_pil
	else:
		opencvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
		return opencvImage



def recognize(image):
	return tess.image_to_string(image,config='-c preserve_interword_spaces=1')
 

 #Splitting images to table and no-table

class HTML2PDF(FPDF, HTMLMixin):
    pass

def image_split(image_path):
	image = Image.open(image_path)
	width,height = image.size
	cropped = []
	tabs = find_table(cv.imread(image_path))
	tabs.insert(0,Table(0,0,0,0)) 
	tabs.append(Table(0,height,0,0))
	for i in range(0,len(tabs)):
		cropped.append(image.crop((tab[i].x,tab[i].y,tab[i].x+tab[i].w,tab[i].y+ tab[i].h)))
		cropped.append(image.crop(0,tab[i].y+tab[i].h,width,tab[i+1].y))
	cropped = cropped[1:len(cropped)-1] 
	tabs = tabs[1:len(tabs)-1]
	return cropped,tabs 

#CREATING PDF DOCUMENT WITH RECOGNIZED TEXT

def to_pdf():
	htmlcode = ""
	im_pieces,tabs = image_split()
	for k in range(0,len(tabs)):
		if k%2==0 :
			htmlcode += "<p>" + (recognize(im_pieces[k])) + "</p>"
		else:
			htmlcode += "<table>"
			table_entries = tabs[k/2].get_table_entries()
			table_roi = transform(im_pieces[i],"cv")
			table_roi = cv.resize(im_pieces[i], (table.w * 3, table.h * 3))
    		for i in range(len(table_entries)):
    			htmlcode += "<tr>"
	        	row = table_entries[i]
			        for j in range(len(row)):  
			        	entry = row[j]
	            		entry_roi = table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3]  
			        	htmlcode += "<td> " + str(recognize(transform(table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3],"PIL"))) + "</td>"
			        htmlcode += "</tr>"
			htmlcode += "</table>"
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(htmlcode)
	"""
	pdf = FPDF()
	pdf.set_font("Arial",size = 12)
	pdf.cell(200, 10, txt=recognize(Image.open(sys.argv[1]),ln = 1, align="L"))
	"""
	pdf.output(str(sys.argv[2])+".pdf")


#CREATING WORD DOCUMENT WITH RECOGNIZED TEXT

def to_word():
	doc = Document()
	im_pieces,tabs = image_split(sys.argv[1])
	for k in range(0,len(tabs)):
		if k%2==0 :
			doc = doc.add_paragraph(recognize(im_pieces[k]))
		else:
			table_entries = tabs[k/2].get_table_entries()
			table = doc.add_table(rows = table_entries,cols = len(table_entries[0]))
			table_roi = transform(im_pieces[i],"cv")
			table_roi = cv.resize(im_pieces[i], (table.w * 3, table.h * 3))
    		for i in range(len(table_entries)):
	        	row = table_entries[i]
			        for j in range(len(row)):  
			        	entry = row[j]
	            		entry_roi = table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3]  
			        	table.cell(i,j).text = str(recognize(transform(table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3],"PIL")))

	doc.save(str(sys.argv[2])+".docx")


#CREATING TXT DOCUMENT WITH RECOGNIZED TEXT


def to_txt():
	f = open(str(sys.argv[2])+".txt","w+")
	im_pieces,tabs = image_split(sys.argv[1])
	for k in range(0,len(tabs)):
		if k%2==0 :
			f.write(recognize(im_pieces[k]))
		else:
			table_entries = tabs[k//2].get_table_entries()
			table_roi = transform(im_pieces[i],"cv")
			table_roi = cv.resize(im_pieces[i], (table.w * 3, table.h * 3))
    		for i in range(len(table_entries)):
	        	row = table_entries[i]
			        for j in range(len(row)):
			        	entry = row[j]
	            		entry_roi = table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3]  
			        	f.write(str(recognize(transform(table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3],"PIL")))+"\t")
			        f.write("\n")
	f.write(recognize(Image.open(sys.argv[1])))
	f.close()


if __name__ == "__main__":
    if sys.argv[3] == "pdf":
	to_pdf()
    elif sys.argv[3] == "docx":
	to_word()
    else:
	to_txt()

