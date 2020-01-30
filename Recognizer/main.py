from PIL import Image
import sys
from fpdf import FPDF, HTMLMixin
from docx import Document
import pytesseract as tess
from table import Table
from table_main import find_table
import cv2 as cv
import numpy as np
#=============================
#RECOGNIZING TEXT ON THE IMAGE
#=============================
def transform(image,to):
	if to == "PIL":
		img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
		im_pil = Image.fromarray(img)
		return im_pil
	else:
		opencvImage = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
		return opencvImage

def recognize(image):
	#,config='-c preserve_interword_spaces=1',config='--psm = 10'
	return tess.image_to_string(image)
 

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
	print(len(tabs))
	for i in range(0,len(tabs)-1):
		cropped.append(image.crop((tabs[i].x,tabs[i].y,tabs[i].x+tabs[i].w,tabs[i].y+ tabs[i].h)))
		cropped.append(image.crop((0,tabs[i].y+tabs[i].h,width,tabs[i+1].y)))
	cropped = cropped[1:]
	tabs = tabs[1:]
	return cropped,tabs 

#CREATING PDF DOCUMENT WITH RECOGNIZED TEXT

def to_pdf():
	htmlcode = ""
	im_pieces,tabs = image_split()
	for k in range(len(im_pieces)):
		print("k//2 ",k//2," k ",k)
		if k%2==0 :
			doc.add_paragraph(recognize(im_pieces[k]))
		else:
			table_entries = tabs[k//2].get_table_entries()
			htmlcode += "<p>" + (recognize(im_pieces[k])) + "</p>"
			print("Rows, cols",len(table_entries),len(table_entries[0]))
			htmlcode += "<table>"
			table_roi = transform(im_pieces[k],"cv")
			table_roi = cv.resize(table_roi, (tabs[k//2].w * 3, tabs[k//2].h * 3))
			
			try:
				for i in range(len(table_entries)):
					row = table_entries[i]
					for j in range(len(row)):  
						entry = row[j]
						entry_roi = table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3]
						htmlcode += "<td> " + str(recognize(transform(table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3],"PIL"))) + "</td>"
			except:
				print("Table Entries" ,len(table_entries))
			htmlcode+="</table>"
	pdf = HTML2PDF()
	pdf.add_page()
	pdf.write_html(htmlcode)
	pdf.output(str(sys.argv[2])+".pdf")


#CREATING WORD DOCUMENT WITH RECOGNIZED TEXT

def to_word():
	doc = Document()
	im_pieces,tabs = image_split(sys.argv[1]) 
	print("Lenght of image pieces",len(im_pieces))
	for k in range(len(im_pieces)):
		print("k//2 ",k//2," k ",k)
		if k%2==0 :
			doc.add_paragraph(recognize(im_pieces[k]))
		else:
			table_entries = tabs[k//2].get_table_entries()
			print("Rows, cols",len(table_entries),len(table_entries[0]))
			table = doc.add_table(rows = len(table_entries),cols =  len(table_entries[0]))
			table_roi = transform(im_pieces[k],"cv")
			table_roi = cv.resize(table_roi, (tabs[k//2].w * 3, tabs[k//2].h * 3))
			
			try:
				for i in range(len(table_entries)):
					row = table_entries[i]
					for j in range(len(row)):  
						entry = row[j]
						entry_roi = table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3]
						table.cell(i,j).text = str(recognize(transform(table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3],"PIL")))
			except:
				print("Table Entries" ,len(table_entries))
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
			print("Rows, cols",len(table_entries),len(table_entries[0]))
			table = doc.add_table(rows = len(table_entries),cols =  len(table_entries[0]))
			table_roi = transform(im_pieces[k],"cv")
			table_roi = cv.resize(table_roi, (tabs[k//2].w * 3, tabs[k//2].h * 3))
			try:
				for i in range(len(table_entries)):
					row = table_entries[i]
					for j in range(len(row)):  
						entry = row[j]
						entry_roi = table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3]
						f.write( str(recognize(transform(table_roi[entry[1] * 3: (entry[1] + entry[3]) * 3, entry[0] * 3:(entry[0] + entry[2]) * 3],"PIL"))) + "\t")
					fwrite("\n")
			except:
				print("Table Entries" ,len(table_entries))
	f.write(recognize(Image.open(sys.argv[1])))
	f.close()


if __name__ == "__main__":
    if sys.argv[3] == "pdf":
	to_pdf()
    elif sys.argv[3] == "docx":
	to_word()
    else:
	to_txt()

