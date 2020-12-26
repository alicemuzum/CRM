import csv
import tkinter as tk
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
from tkinter import messagebox #uyarı mesajları
from tkcalendar import Calendar,DateEntry
import sqlite3
import openpyxl                    #excel to db
from openpyxl import load_workbook #excel to db
import re,os                          #excle to db
import datetime
import pytz
from tkinter import filedialog
import base64
from base64 import b64decode
from io import BytesIO

'''EXCELİ DB YE YAZMA



def slugify(text, lower=1):
    if lower == 1:
        text = text.strip().lower()
    text = re.sub(r'[^\w _-]+', '', text)
    text = re.sub(r'[- ]+', '_', text)
    return text

#Replace with a database name
con = sqlite3.connect('test.db')
#replace with the complete path to youe excel workbook
wb = load_workbook(filename=r'abc.xlsx')

sheets = wb.get_sheet_names()

for sheet in sheets:
    ws = wb[sheet] 

    columns= []
    query = 'CREATE TABLE ' + str(slugify(sheet)) + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
    for row in ws.rows[0]:
        query += ', ' + slugify(row.value) + ' TEXT'
        columns.append(slugify(row.value))
    query += ');'

    con.execute(query)

    tup = []
    for i, rows in enumerate(ws):
        tuprow = []
        if i == 0:
            continue
        for row in rows:
            tuprow.append(unicode(row.value).strip()) if unicode(row.value).strip() != 'None' else tuprow.append('')
        tup.append(tuple(tuprow))


    insQuery1 = 'INSERT INTO ' + str(slugify(sheet)) + '('
    insQuery2 = ''
    for col in columns:
        insQuery1 += col + ', '
        insQuery2 += '?, '
    insQuery1 = insQuery1[:-2] + ') VALUES('
    insQuery2 = insQuery2[:-2] + ')'
    insQuery = insQuery1 + insQuery2

    con.executemany(insQuery, tup)
    con.commit()

con.close()
'''

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB():
	print("Inserting BLOB into table")
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()
	sql_insert_blob_query="""INSERT INTO foto VALUES(:fotom, :plaka_no, :tarih_foto)"""

	global paths,binary_data
	binary_data=[]
	paths = tk.filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf'),
                                                       ('JPG files', '*.jpg'),
                                                       ('PNG files', '*.png'),
                                                       ('all files', '.*')],
                                            initialdir=os.getcwd(),
                                            title="Select files", multiple=True)
	for idx,path in enumerate(paths):
		binary_data.append(convertToBinaryData(path))
		cursor.execute(sql_insert_blob_query,{'fotom':binary_data[idx],
			'plaka_no': car_plaka_entry.get(),
			'tarih_foto':datetime.datetime.now(pytz.timezone('Europe/Istanbul'))} )
	

	
	
	mydb.commit()
	print("Image file inserted successfully as a BLOB int table")

	cursor.close()
	mydb.close()




#row ve column lf3 e entry yerleştirmek için


def fetch_image():
	def photoForward(imgnum):
		global foto_label
		global button_forward
		global button_back
		global img

		foto_label.grid_forget()
		foto_label=tk.Label(image=img[imgnum-1])
		foto_label.grid(row=0,column=0,columnspan=3)

		button_forward= tk.Button(fotoframe,text=">>",command=lambda: photoForward(imgnum+1))
		button_back= tk.Button(fotoframe,text="<<",command=lambda: photoBack(imgnum-1))
		
		if imgnum==lenimg:
			button_forward=tk.Button(fotoframe,text=">>",state="disabled")

		button_back.grid(row=1,column=0)
		button_forward.grid(row=1,column=2)
		return

	def photoBack(imgnum):
		global foto_label
		global button_forward
		global button_back
		global img 

		foto_label.grid_forget()
		foto_label=tk.Label(image=img[imgnum-1])
		foto_label.grid(row=0,column=0,columnspan=3)

		button_forward= tk.Button(fotoframe,text=">>",command=lambda: photoForward(imgnum+1))
		button_back= tk.Button(fotoframe,text="<<",command=lambda: photoBack(imgnum-1))

		if imgnum==1:
			button_back=tk.Button(fotoframe,text="<<",state="disabled")

		button_back.grid(row=1,column=0)
		button_forward.grid(row=1,column=2)
		return

	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()

	#sql_fetch_blob_query = """SELECT * from foto where id = %s"""
	#emp_id=4
	sql_fetch_blob_query = """SELECT * from foto """
	#cursor.execute(sql_fetch_blob_query, (emp_id,))
	records=cursor.execute(sql_fetch_blob_query)
	records = cursor.fetchall()
	print("Fotolar elimizde")
	#print(records[0])


	
	fotoframe=tk.Toplevel()
	fotoframe.title("Fotoğraflar")
	fotoframe.geometry("500x500")
	TARGET_SIZE=(256,256)
	img=[]
	
	for record in records:
		image_data = record[0]
		loaded_img = PIL.Image.open(BytesIO(image_data))
		resized_img = loaded_img.resize(TARGET_SIZE)
		photo_img = PIL.ImageTk.PhotoImage(resized_img)
		img.append(photo_img)
		#base64_encoded= base64.b64encode(record[0])
		#base64_encoded_string= base64_encoded.decode('utf-8')
		#fotoimg= PIL.Image.open(base64_encoded)


		
		#imgobject = imgobject.resize((450, 350), PIL.Image.ANTIALIAS)
		#imgobj.paste(imgobject,((100,800),(100,100),(1000,100),(1000,800)))


		#imgobject=PIL.ImageTk.PhotoImage(data= record[0])
		#img.append(imgobject)
		
	#var=PIL.ImageTk.PhotoImage(data= records[0][0])
	lenimg=len(img)
	foto_label= tk.Label(fotoframe,image=img[0])
	foto_label.place(x=125,y=100)

	button_back=tk.Button(fotoframe,text="<<",command=photoBack,state="disabled")
	button_forward=tk.Button(fotoframe,text=">>",command=lambda:photoForward(2))
	button_back.place(x=150,y=400)
	button_forward.place(x=350,y=400)

	fotoframe.mainloop()

def clear_fields():
	global entries
	for entr in entries:
		entr.delete(0,"end")
	for idx,slave in enumerate(dp_ad):
		slave.destroy()
		dp_tutar[idx].destroy()
	for idx,slave in enumerate(op_ad):
		slave.destroy()
		op_kaporta[idx].destroy()
		op_boya[idx].destroy()
	for idx,slave in enumerate(ei_ad):
		slave.destroy()
		ei_tutar[idx].destroy()
	for idx,slave in enumerate(trim_ad):
		slave.destroy()
		trim_tutar[idx].destroy()
	for idx,slave in enumerate(mi_ad):
		slave.destroy()
		mi_tutar[idx].destroy()
	dp_ad.clear()
	dp_tutar.clear()
	op_ad.clear()
	op_kaporta.clear()
	op_boya.clear()
	ei_ad.clear()
	ei_tutar.clear()
	trim_ad.clear()
	trim_tutar.clear()
	mi_ad.clear()
	mi_tutar.clear()
	row_lf3=0
	row_lf4=0
	row_lf5=0
	row_lf6=0
	row_lf7=0
	column_lf3=0


def show_past():
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()

	sql_records_query0="SELECT * FROM musteri_arac "
	sql_records_query1="SELECT * FROM degisecek_parca"
	sql_records_query2="SELECT * FROM onarilacak_parca"
	sql_records_query3="SELECT * FROM elektrik_iscilikleri"
	sql_records_query4="SELECT * FROM trim_iscilikleri"
	sql_records_query5="SELECT * FROM mekanik_iscilikleri"
	cursor.execute(sql_records_query0)
	records=cursor.fetchall()
	cursor.execute(sql_records_query1)
	records_dp=cursor.fetchall()
	cursor.execute(sql_records_query2)
	records_op=cursor.fetchall()
	cursor.execute(sql_records_query3)
	records_ei=cursor.fetchall()
	cursor.execute(sql_records_query4)
	records_trim=cursor.fetchall()
	cursor.execute(sql_records_query5)
	records_mi=cursor.fetchall()
	satırcı=0
	for idx,record in enumerate(records):
		record_label=tk.Label(my_frame2,text=record)
		record_label.grid(row=idx,column=0,padx=20,pady=20)
		
	for idx,record in enumerate(records_dp):
		record_dp_label=tk.Label(my_frame2,text=str(record[0])+" "+str(record[1])+" "+str(record[2]))
		record_dp_label.grid(row=satırcı,column=1,padx=10,pady=10)
		satırcı+=1
	for idx,record in enumerate(records_op):
		record_op_label=tk.Label(my_frame2,text=str(record[0])+" "+str(record[1])+" "+str(record[2])+" "+str(record[3]))
		record_op_label.grid(row=satırcı,column=1,padx=10,pady=5)
		satırcı+=1
	for idx,record in enumerate(records_ei):
		record_ei_label=tk.Label(my_frame2,text=str(record[0])+" "+str(record[1])+" "+str(record[2]))
		record_ei_label.grid(row=satırcı,column=1,padx=10,pady=5)
		satırcı+=1
	for idx,record in enumerate(records_trim):
		record_trim_label=tk.Label(my_frame2,text=str(record[0])+" "+str(record[1])+" "+str(record[2]))
		record_trim_label.grid(row=satırcı,column=1,padx=10,pady=5)
		satırcı+=1
	for idx,record in enumerate(records_mi):
		record_mi_label=tk.Label(my_frame2,text=str(record[0])+" "+str(record[1])+" "+str(record[2]))
		record_mi_label.grid(row=satırcı,column=1,padx=10,pady=5)
		satırcı+=1


	mydb.commit()
	cursor.close()
	mydb.close()
	return 






def go_to_next_entry(event, entry_list, this_index):
    next_index = (this_index + 1) % len(entry_list)
    entry_list[next_index].focus_set()
'''
def takeParcaRows():
	mydb=mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="Fark4455.",
	database="goldgarage"
	)
	cursor=mydb.cursor(buffered=True)
	global get_values
	for item in entries:
		get_values.append(item.get())
	cursor.execute('INSERT INTO list_table (deneme) VALUES ("%s");', [','.join(get_values)])
	cursor.execute("SELECT * FROM list_table")
	result=cursor.fetchall()
	
	labell=tk.Label(my_frame2,text=str(result[0])+"\n")
	labell.pack()
	cursor.close()
	mydb.close()

def takeParcaRows():
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()
	global get_values
	for item in entries:
		get_values.append(item.get())
	results = cursor.executemany('INSERT INTO list_table (deneme) VALUES ("%s")', [(x,) for x in get_values]) 
	
	cursor.execute("SELECT * FROM list_table")
	result=cursor.fetchall()
	abc=len(result)
	for i in range(2):
		labell=tk.Label(my_frame2,text=result[abc-1-i])
		labell.pack()
	cursor.close()
	mydb.close()
'''
def add_row():
	global row_lf3,column_lf3
	dp_entry=tk.Entry(lf3,width=25)
	dp_tutar_entry=tk.Entry(lf3,width=10)
	dp_entry.grid(row=row_lf3,column=column_lf3)
	column_lf3+=1
	dp_tutar_entry.grid(row=row_lf3,column=column_lf3)
	dp_ad.append(dp_entry)
	dp_tutar.append(dp_tutar_entry)

	row_lf3+=1
	column_lf3=0

	if len(dp_ad)>0:
		sil_lf3=tk.Button(my_frame1,text="Sil",command=sil_row,state="active")
		sil_lf3.place(x=20,y=200)
	return

def sil_row():
	lendp=len(dp_ad)
	lendpp=len(dp_tutar)
	dp_ad[lendp-1].destroy()
	dp_tutar[lendpp-1].destroy()
	dp_ad.pop()
	dp_tutar.pop()
	if len(dp_ad)<=0:
		sil_lf3=tk.Button(my_frame1,text="Sil",command=sil_row,state="disabled")
		sil_lf3.place(x=20,y=200)
	
def add_row2():
	global row_lf4,column_lf3	
	my_entry=tk.Entry(lf4,width=25)
	tutar_entry=tk.Entry(lf4,width=10)
	boya_entry=tk.Entry(lf4,width=10)
	my_entry.grid(row=row_lf4,column=column_lf3)
	column_lf3+=1
	tutar_entry.grid(row=row_lf4,column=column_lf3)
	column_lf3+=1
	boya_entry.grid(row=row_lf4,column=column_lf3)
	op_ad.append(my_entry)
	op_kaporta.append(tutar_entry)
	op_boya.append(boya_entry)

	row_lf4+=1
	column_lf3=0

	if len(op_ad)>0:
		sil_lf4=tk.Button(my_frame1,text="Sil",command=sil_row2,state="active")
		sil_lf4.place(x=290,y=200)
	
	return

def sil_row2():
	lenop=len(op_ad)
	lenkapo=len(op_kaporta)
	lenboya=len(op_boya)
	op_ad[lenop-1].destroy()
	op_kaporta[lenkapo-1].destroy()
	op_boya[lenboya-1].destroy()
	op_boya.pop()
	op_ad.pop()
	op_kaporta.pop()
	if len(op_ad)<=0:
		sil_lf4=tk.Button(my_frame1,text="Sil",command=sil_row2,state="disabled")
		sil_lf4.place(x=290,y=200)
	return

def add_row3():
	global row_lf5,column_lf3
	my_entry=tk.Entry(lf5,width=25)
	tutar_entry=tk.Entry(lf5,width=10)
	my_entry.grid(row=row_lf5,column=column_lf3)
	column_lf3+=1
	tutar_entry.grid(row=row_lf5,column=column_lf3)
	ei_ad.append(my_entry)
	ei_tutar.append(tutar_entry)
	row_lf5+=1
	column_lf3=0
	if len(ei_ad)>0:
		sil_lf5=tk.Button(my_frame1,text="Sil",command=sil_row3,state="active")
		sil_lf5.place(x=610,y=200)
	
	return

def sil_row3():
	lenei=len(ei_ad)
	leneit=len(ei_tutar)
	ei_ad[lenei-1].destroy()
	ei_tutar[leneit-1].destroy()
	ei_ad.pop()
	ei_tutar.pop()
	if len(ei_ad)<=0:
		sil_lf5=tk.Button(my_frame1,text="Sil",command=sil_row3,state="disabled")
		sil_lf5.place(x=610,y=200)
	
	return
def add_row4():
	global row_lf6,column_lf3
	my_entry=tk.Entry(lf6,width=25)
	tutar_entry=tk.Entry(lf6,width=10)
	my_entry.grid(row=row_lf6,column=column_lf3)
	column_lf3+=1
	tutar_entry.grid(row=row_lf6,column=column_lf3)
	trim_ad.append(my_entry)
	trim_tutar.append(tutar_entry)
	row_lf6+=1
	column_lf3=0
	if len(trim_ad)>0:
		sil_lf6=tk.Button(my_frame1,text="Sil",command=sil_row4,state="active")
		sil_lf6.place(x=875,y=200)
	
	return

def sil_row4():
	lentr=len(trim_ad)
	lentrt=len(trim_tutar)
	trim_ad[lentr-1].destroy()
	trim_tutar[lentrt-1].destroy()
	trim_ad.pop()
	trim_tutar.pop()
	if len(trim_ad)<=0:
		sil_lf6=tk.Button(my_frame1,text="Sil",command=sil_row4,state="disabled")
		sil_lf6.place(x=875,y=200)
	
	return

def add_row5():
	global row_lf7,column_lf3
	my_entry=tk.Entry(lf7,width=25)
	tutar_entry=tk.Entry(lf7,width=10)
	my_entry.grid(row=row_lf7,column=column_lf3)
	column_lf3+=1
	tutar_entry.grid(row=row_lf7,column=column_lf3)
	mi_ad.append(my_entry)
	mi_tutar.append(tutar_entry)
	row_lf7+=1
	column_lf3=0
	if len(mi_ad)>0:
		sil_lf7=tk.Button(my_frame1,text="Sil",command=sil_row5,state="active")
		sil_lf7.place(x=1100,y=200)
	
	return

def sil_row5():
	lenmi=len(mi_ad)
	lenmit=len(mi_tutar)
	mi_ad[lenmi-1].destroy()
	mi_tutar[lenmit-1].destroy()
	mi_ad.pop()
	mi_tutar.pop()
	if len(mi_ad)<=0:
		sil_lf7=tk.Button(my_frame1,text="Sil",command=sil_row5,state="disabled")
		sil_lf7.place(x=1100,y=200)
	
	return


def numberControl():
	error=True
	for idx,ent in enumerate(entries):

		if idx==1:
			try:
				int(cust_phone_entry.get())
			except ValueError:
				messagebox.showwarning("Hata!","Telefon No için lütfen sadece sayı giriniz, boşluk kullanmayınız!")
				error=False 
		if idx==3:
			try:
				int(cust_dosya_entry.get())
			except ValueError:
				messagebox.showwarning("Hata!","Dosya için lütfen sadece sayı giriniz, boşluk kullanmayınız!")
				error=False
		if idx==5:
			try:
				int(car_model_entry.get())
			except ValueError:
				messagebox.showwarning("Hata!","Model için lütfen sadece sayı giriniz, boşluk kullanmayınız!")
				error=False
		if idx==9:
			try:
				int(car_km_entry.get())
			except ValueError:
				messagebox.showwarning("Hata!","Kilometre için lütfen sadece sayı giriniz, boşluk kullanmayınız!")
				error=False
	return error
				


def create_database():
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()
	cursor.execute("SHOW DATABASES")
	for db in cursor:
		print(db)
	cursor.close()
	mydb.close()

def create_table():
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS degisecek_parca(entry text,\
		tutar int,\
		plaka_no text,\
		tarih_dp timestamp)''')
	cursor.execute("CREATE TABLE IF NOT EXISTS musteri_arac(cust_name text,\
		cust_phone INT,\
		cust_sigorta text,\
		cust_dosya INT,\
		car_plaka text,\
		car_marka text,\
		car_model INT(4),\
		car_hasar text,\
		car_fdate DATETIME,\
		car_estdate DATETIME,\
		car_km INT(7),\
		car_eksper text,\
		car_geldate datetime,\
		tarih timestamp)")
	cursor.execute('''CREATE TABLE IF NOT EXISTS onarilacak_parca(entry text,\
		kaporta int,\
		boya int,\
		plaka_no text,\
		tarih_op timestamp)''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS elektrik_iscilikleri(entry text,\
		tutar int,\
		plaka_no text,\
		tarih_ei timestamp)''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS trim_iscilikleri(entry text,\
		tutar int,\
		plaka_no text,\
		tarih_ti timestamp)''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS mekanik_iscilikleri(entry text,\
		tutar int,\
		plaka_no text,\
		tarih_mi timestamp)''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS foto(fotom text,\
		plaka_no text,\
		tarih_foto timestamp)''')

	#cursor.execute('INSERT INTO list_table (deneme) VALUES (?);', [','.join(entries)])
	#cursor.execute("SELECT * FROM list_table")
	#resultt=cursor.fetchall()
	#for thing in result:
	#	print(thing)
	print("Database değiştirildi ")
	mydb.commit()
	cursor.close()
	mydb.close()

def add_customer():
	if(numberControl()):
		sql_string="INSERT INTO musteri_arac  VALUES (:cust_name, :cust_phone,:cust_sigorta,:cust_dosya,:car_plaka,:car_marka,:car_model,:car_hasar,:car_fdate,:car_estdate,:car_km,:car_eksper,:car_geldate,:tarih)"
	
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		cursor.execute(sql_string,
			{
				'cust_name': cust_name_entry.get(),
				'cust_phone': cust_phone_entry.get(),
				'cust_sigorta': cust_sigorta_entry.get(),
				'cust_dosya': cust_dosya_entry.get(),
				'car_plaka': car_plaka_entry.get(),
				'car_marka': car_marka_entry.get(),
				'car_model': car_model_entry.get(),
				'car_hasar': car_damage_entry.get(),
				'car_fdate': car_fdate_entry.get_date(),
				'car_estdate': car_est_entry.get_date(),
				'car_km': car_km_entry.get(),
				'car_eksper': car_eksper_entry.get(),
				'car_geldate': car_gel_date_entry.get_date(),
				'tarih': datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
			})

		mydb.commit()
		cursor.close()
		mydb.close()
		degisecek_parca_add()
		onarım_parca_add()
		elektrik_isclilik_add()
		trim_iscilikleri_add()
		mekanik_iscilik_add()
		clear_fields()
	else:
		return

def degisecek_parca_add():
	if(len(dp_ad)>0):
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		for idx,thing in enumerate(dp_ad):
			cursor.execute('INSERT INTO degisecek_parca VALUES (:entry,:tutar,:plaka_no,:tarih_dp)',
			{
			'entry':dp_ad[idx].get(),
			'tutar': dp_tutar[idx].get(),
			'plaka_no': car_plaka_entry.get(),
			'tarih_dp': datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
			})
		mydb.commit()
		cursor.close()
		mydb.close()
	else: 
		print("dp_ad boş")
		return

def onarım_parca_add():
	if(len(op_ad)>0):
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		for idx,thing in enumerate(op_ad):
			cursor.execute('INSERT INTO onarilacak_parca VALUES (:entry,:kaporta,:boya,:plaka_no,:tarih_op)',
			{
			'entry':op_ad[idx].get(),
			'kaporta': op_kaporta[idx].get(),
			'boya': op_boya[idx].get(),
			'plaka_no': car_plaka_entry.get(),
			'tarih_op': datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
			})
		mydb.commit()
		cursor.close()
		mydb.close()
	else: 
		print("op_ad boş")
		return

def elektrik_isclilik_add():
	if(len(ei_ad)>0):
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		for idx,thing in enumerate(ei_ad):
			cursor.execute('INSERT INTO elektrik_iscilikleri VALUES (:entry,:tutar,:plaka_no,:tarih_ei)',
			{
			'entry':ei_ad[idx].get(),
			'tutar': ei_tutar[idx].get(),
			'plaka_no': car_plaka_entry.get(),
			'tarih_ei': datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
			})
		mydb.commit()
		cursor.close()
		mydb.close()
	else: 
		print("ei_ad boş")
		return

def trim_iscilikleri_add():
	if(len(trim_ad)>0):
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		for idx,thing in enumerate(trim_ad):
			cursor.execute('INSERT INTO trim_iscilikleri VALUES (:entry,:tutar,:plaka_no,:tarih_ti)',
			{
			'entry':trim_ad[idx].get(),
			'tutar': trim_tutar[idx].get(),
			'plaka_no': car_plaka_entry.get(),
			'tarih_ti': datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
			})
		mydb.commit()
		cursor.close()
		mydb.close()
	else: 
		print("trim_ad boş")
		return

def mekanik_iscilik_add():
	if(len(mi_ad)>0):
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		for idx,thing in enumerate(mi_ad):
			cursor.execute('INSERT INTO mekanik_iscilikleri VALUES (:entry,:tutar,:plaka_no,:tarih_mi)',
			{
			'entry':mi_ad[idx].get(),
			'tutar': mi_tutar[idx].get(),
			'plaka_no': car_plaka_entry.get(),
			'tarih_mi': datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
			})
		mydb.commit()
		cursor.close()
		mydb.close()
	else: 
		print("mi_ad boş")
		return

	
def degisecekFrame():
	global isconn


	#databaseye bağlı mı değil mi
	if isconn==False:
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		isconn=True


		
	cursor.execute("SELECT * FROM degisecek_parca WHERE plaka_no=?",(showSelected_plaka[1],))
	recording=cursor.fetchall()
	print("DATABASE RECORDİNG")
	print(recording)

	#eğer deigsecek parca entryleri varsa onları ilk önce sil 
	
	for item in degisecek_info_list:
		item.destroy()

	degisecek_info_list.clear()

	#degisecek parca entryleri olusrtur
	x=0
	y=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx==2:
				break
			if y>1:
				x=x+1
				y=0
			my_entry=tk.Entry(degisecek_parca_frame)
			my_entry.grid(row=x,column=y)
			y+=1
			degisecek_info_list.append(my_entry)



	#entryleri doldur
	flag=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx>1:
				break
			degisecek_info_list[flag].insert(0,record)
			flag+=1


	if isconn==True:
		cursor.close()
		mydb.close()
		isconn=False

def onarilacakFrame():
	global isconn
	#databaseye bağlı mı değil mi
	if isconn==False:
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		isconn=True
		
	cursor.execute("SELECT * FROM onarilacak_parca WHERE plaka_no=?",(showSelected_plaka[1],))
	recording=cursor.fetchall()
	print(recording)

	#eğer deigsecek parca entryleri varsa onları ilk önce sil 
	
	for item in onarilacak_info_list:
		item.destroy()

	onarilacak_info_list.clear()

	#degisecek parca entryleri olusrtur
	x=0
	y=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx==2:
				break
			if y>1:
				x=x+1
				y=0
			my_entry=tk.Entry(onarim_parca_frame)
			my_entry.grid(row=x,column=y)
			y+=1
			onarilacak_info_list.append(my_entry)



	#entryleri doldur
	flag=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx>1:
				break
			onarilacak_info_list[flag].insert(0,record)
			flag+=1


	if isconn==True:
		cursor.close()
		mydb.close()
		isconn=False
		
def eiFrame():
	global isconn
	#databaseye bağlı mı değil mi
	if isconn==False:
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		isconn=True
		
	cursor.execute("SELECT * FROM elektrik_iscilikleri WHERE plaka_no=?",(showSelected_plaka[1],))
	recording=cursor.fetchall()
	print(recording)

	#eğer deigsecek parca entryleri varsa onları ilk önce sil 
	
	for item in elektrik_info_list:
		item.destroy()

	elektrik_info_list.clear()

	#degisecek parca entryleri olusrtur
	x=0
	y=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx==2:
				break
			if y>1:
				x=x+1
				y=0
			my_entry=tk.Entry(elektrik_iscilikleri_frame)
			my_entry.grid(row=x,column=y)
			y+=1
			elektrik_info_list.append(my_entry)



	#entryleri doldur
	flag=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx>1:
				break
			elektrik_info_list[flag].insert(0,record)
			flag+=1


	if isconn==True:
		cursor.close()
		mydb.close()
		isconn=False

def trimFrame():
	global isconn
	#databaseye bağlı mı değil mi
	if isconn==False:
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		isconn=True
		
	cursor.execute("SELECT * FROM trim_iscilikleri WHERE plaka_no=?",(showSelected_plaka[1],))
	recording=cursor.fetchall()
	print(recording)

	#eğer deigsecek parca entryleri varsa onları ilk önce sil 
	
	for item in trim_info_list:
		item.destroy()

	trim_info_list.clear()

	#degisecek parca entryleri olusrtur
	x=0
	y=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx==2:
				break
			if y>1:
				x=x+1
				y=0
			my_entry=tk.Entry(elektrik_iscilikleri_frame)
			my_entry.grid(row=x,column=y)
			y+=1
			trim_info_list.append(my_entry)



	#entryleri doldur
	flag=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx>1:
				break
			trim_info_list[flag].insert(0,record)
			flag+=1


	if isconn==True:
		cursor.close()
		mydb.close()
		isconn=False

def mekanikFrame():
	global isconn
	#databaseye bağlı mı değil mi
	if isconn==False:
		mydb= sqlite3.connect('customers.db')
		cursor = mydb.cursor()
		isconn=True
		
	cursor.execute("SELECT * FROM mekanik_iscilikleri WHERE plaka_no=?",(showSelected_plaka[1],))
	recording=cursor.fetchall()
	print(recording)

	#eğer deigsecek parca entryleri varsa onları ilk önce sil 
	
	for item in mekanik_info_list:
		item.destroy()

	mekanik_info_list.clear()

	#degisecek parca entryleri olusrtur
	x=0
	y=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx==2:
				break
			if y>1:
				x=x+1
				y=0
			my_entry=tk.Entry(mekanik_iscilikleri_frame)
			my_entry.grid(row=x,column=y)
			y+=1
			mekanik_info_list.append(my_entry)



	#entryleri doldur
	flag=0
	for records in recording:
		for idx,record in enumerate(records):
			if idx>1:
				break
			mekanik_info_list[flag].insert(0,record)
			flag+=1


	if isconn==True:
		cursor.close()
		mydb.close()
		isconn=False
		
		
def fillTree():
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()

	cursor.execute("SELECT * FROM musteri_arac")

	
	for child in my_tree.get_children():
		my_tree.delete(child)

	print("HEPSİ SİLİNDİ")

	count_2=-1
	for record in cursor.fetchall():
		count_2 += 1
		if count_2 % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count_2, text="", values=(record[0], record[4], record[7],record[8]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count_2, text="", values=(record[0], record[4], record[7],record[8]), tags=('oddrow',))

		

	print(my_tree.item(1)['values'])
	
	print("count_2 = "+str(count_2))

	cursor.close()
	mydb.commit()
	mydb.close()

def showSelected():	
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()
	global showSelected_plaka
	global isconn
	isconn=True
	showSelected_plaka=[]
	showSelected_plaka.clear()

	#Treeview seçilen satır
	sel=my_tree.selection()
	for value in my_tree.item(sel)['values']:
		print(value)
		showSelected_plaka.append(value)
			
			
	
	#Eğer daha önceden other_info doldurulduysa onu boşaltan kısım
	if save_changes_list:
		for entry in save_changes_list:
			entry.delete(0,"end")

	#Ugly way to query but it works idc
	cursor.execute("SELECT * FROM musteri_arac WHERE car_plaka=?",(showSelected_plaka[1],))
	for records in cursor.fetchall():
		for idx,record in enumerate(records):
			if idx<13:
				save_changes_list[idx].insert(0,record)
				

	
	
	mydb.commit()
	cursor.close()
	mydb.close()
	isconn=False

	degisecekFrame()
	onarilacakFrame()
	eiFrame()
	trimFrame()
	mekanikFrame()
	showSelected_plaka.clear()

def deleteSelectedRec():
	global count_2
	mydb= sqlite3.connect('customers.db')
	cursor = mydb.cursor()

	showSelected_plaka=[]
	showSelected_plaka.clear()
	#Treeview seçilen satır
	line= my_tree.selection()
	for value in my_tree.item(line)['values']:
		print(value)
		showSelected_plaka.append(value)

	cursor.execute("DELETE FROM musteri_arac WHERE car_plaka=?",(showSelected_plaka[1],))
	cursor.execute("DELETE FROM degisecek_parca WHERE plaka_no=?",(showSelected_plaka[1],))
	cursor.execute("DELETE FROM onarilacak_parca WHERE plaka_no=?",(showSelected_plaka[1],))
	cursor.execute("DELETE FROM elektrik_iscilikleri WHERE plaka_no=?",(showSelected_plaka[1],))
	cursor.execute("DELETE FROM trim_iscilikleri WHERE plaka_no=?",(showSelected_plaka[1],))
	cursor.execute("DELETE FROM mekanik_iscilikleri WHERE plaka_no=?",(showSelected_plaka[1],))

	my_tree.delete(my_tree.selection())
	print("Deleted selected record")
	mydb.commit()
	cursor.close()
	mydb.close()
	showSelected_plaka.clear()
	count_2-=1
	print("count_2= "+ str(count_2))
	return

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    genel_canvas.configure(scrollregion=genel_canvas.bbox("all"))


#Tkinter
root=tk.Tk()
root.title("Gold Garage")
root.iconbitmap("bubu.ico")
#root.geometry("500x500")

root.fullScreenState = False
root.attributes("-fullscreen", root.fullScreenState)

root.w, root.h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (root.w, root.h))
        


#root.iconbitmap('Z:/AC/myCRM/cario.ico')

#TAB
my_notebook= ttk.Notebook(root)
my_notebook.pack()# pady tabin roota oturmasını ayarlıyo
my_frame1= tk.Frame(my_notebook,width=root.w,height=root.h,bg="lightgrey")
my_frame2= tk.Frame(my_notebook,width=root.w,height=root.h,bg="lightgrey")
my_frame1.pack(fill="both",expand=1)
my_frame2.pack(fill="both",expand=1)
my_notebook.add(my_frame1,text="Yeni Araç")
my_notebook.add(my_frame2,text="Araç Geçmişi")

#Canvas Objects
canvas=tk.Canvas(my_frame1,width=my_frame1.winfo_screenwidth(),height=my_frame1.winfo_screenheight(),bg="lightgrey")
canvas.place(x=0,y=0)

canvas.create_line(250,195,250,700,width=1,fill="grey")#soldan birinci dikey çizgi
canvas.create_line(0,195,1350,195,width=1,fill="grey")#üst yatay çizgi
canvas.create_line(600,195,600,700,width=1,fill="grey")#soldan ikinci
canvas.create_line(835,195,835,700,width=1,fill="grey")#soldan üçüncü
canvas.create_line(1090,195,1090,700,width=1,fill="grey")#soldan dördüncü

#LabelFrame

s = ttk.Style()
s.configure('TLabelframe', background='lightgrey',relief="solid")
s.configure('Red.TLabelframe.Label', font=('helvetica', 14, 'bold'),relief="solid", background='lightgrey')


lf=ttk.Labelframe(my_frame1,text="Araç / Eksper Bilgileri",style="Red.TLabelframe")
lf2=ttk.Labelframe(my_frame1,text="Müşteri / Sigorta Bilgileri",style="Red.TLabelframe")
lf2.place(x=10,y=10)
lf.place(x=250,y=10)
degisecek_parca_basligi=tk.Label(my_frame1,text="Değişecek Parçalar",bg="lightgrey",font="Helvetica")
degisecek_parca_basligi.place(x=45,y=200)
lf3=ttk.Frame(my_frame1,style="Red.TLabelframe")
lf3.place(x=10,y=225)
onarim_parca_basligi=tk.Label(my_frame1,text="Onarım Parçaları / Kaporta / Boya",font="Helvetica",bg="lightgrey")
onarim_parca_basligi.place(x=310,y=200)
lf4=ttk.Frame(my_frame1,style="Red.TLabelframe")
lf4.place(x=285,y=225)
elektrik_iscilikleri_basligi=tk.Label(my_frame1,text="Elektrik İşçilikleri",font="Helvetica",bg="lightgrey")
elektrik_iscilikleri_basligi.place(x=640,y=200)
lf5=ttk.Frame(my_frame1,style="Red.TLabelframe")
lf5.place(x=605,y=225)
trim_iscilikleri_basligi=tk.Label(my_frame1,text="Trim İşçilikleri",font="Helvetica",bg="lightgrey")
trim_iscilikleri_basligi.place(x=920,y=200)
lf6=ttk.Frame(my_frame1,style="Red.TLabelframe")
lf6.place(x=850,y=225)
mekanik_iscilikleri_basligi=tk.Label(my_frame1,text="Mekanik ve Diğer İşçilikler",font="Helvetica",bg="lightgrey")
mekanik_iscilikleri_basligi.place(x=1125,y=200)
lf7=ttk.Frame(my_frame1,style="Red.TLabelframe")
lf7.place(x=1100,y=225)

#Yeni Araç Labelları

cust_name_label=tk.Label(lf2,text="Müşteri",bg="lightgrey")
cust_name_label.grid(row=0,column=0,sticky="w",padx=10)
cust_phone_label=tk.Label(lf2,text="Telefon No",bg="lightgrey")
cust_phone_label.grid(row=1,column=0,sticky="w",padx=10)
cust_sigorta_label=tk.Label(lf2,text="Sigorta",bg="lightgrey")
cust_sigorta_label.grid(row=2,column=0,sticky="w",padx=10)
cust_dosya_label=tk.Label(lf2,text="Dosya",bg="lightgrey")
cust_dosya_label.grid(row=3,column=0,sticky="w",padx=10)
car_plaka_label=tk.Label(lf,text="Plaka",bg="lightgrey")
car_plaka_label.grid(row=0,column=0,sticky="w",padx=10)
car_marka_label=tk.Label(lf,text="Marka",bg="lightgrey")
car_marka_label.grid(row=1,column=0,sticky="w",padx=10)
car_model_label=tk.Label(lf,text="Model",bg="lightgrey")
car_model_label.grid(row=2,column=0,sticky="w",padx=10)
car_damage_label=tk.Label(lf,text="Hasar",bg="lightgrey")
car_damage_label.grid(row=0,column=2,padx=10,sticky="w")
car_incoming_date=tk.Label(lf,text="Araç Geliş",bg="lightgrey")
car_incoming_date.grid(row=1, column=2,padx=10,sticky="w")
car_est_date=tk.Label(lf,text="Tahmini Teslim",bg="lightgrey")
car_est_date.grid(row=2,column=2,padx=10,sticky="w")
car_km_label=tk.Label(lf,text="Km",bg="lightgrey")
car_km_label.grid(row=0,column=4,padx=10,sticky="w")
car_eksper_label=tk.Label(lf,text="Eksper",bg="lightgrey")
car_eksper_label.grid(row=1,column=4,padx=10,sticky="w")
car_gel_date_label=tk.Label(lf,text="Gel.Tarihi",bg="lightgrey")
car_gel_date_label.grid(row=2,column=4,padx=10,sticky="w")

#entryler
cust_name_entry=tk.Entry(lf2)
cust_name_entry.grid(row=0,column=1,pady=5)
cust_phone_entry=tk.Entry(lf2)
cust_phone_entry.grid(row=1,column=1,pady=5)
cust_sigorta_entry=tk.Entry(lf2)
cust_sigorta_entry.grid(row=2,column=1,pady=5)
cust_dosya_entry=tk.Entry(lf2)
cust_dosya_entry.grid(row=3,column=1,pady=5)
car_plaka_entry=tk.Entry(lf)
car_plaka_entry.grid(row=0,column=1,pady=5)
car_marka_entry=tk.Entry(lf)
car_marka_entry.grid(row=1,column=1,pady=5)
car_model_entry=tk.Entry(lf)
car_model_entry.grid(row=2,column=1,pady=5,columnspan=1)
car_damage_entry=tk.Entry(lf)
car_damage_entry.grid(row=0,column=3)
car_fdate_entry= DateEntry(lf, width=12, background='darkblue', foreground='white', borderwidth=2,locale='tr_TR')
car_fdate_entry.grid(row=1,column=3)
car_est_entry= DateEntry(lf, width=12, background='darkblue', foreground='white', borderwidth=2,locale='tr_TR')
car_est_entry.grid(row=2,column=3)
car_km_entry=tk.Entry(lf)
car_km_entry.grid(row=0,column=5)
car_eksper_entry=tk.Entry(lf)
car_eksper_entry.grid(row=1,column=5)
car_gel_date_entry= DateEntry(lf, width=15, background='darkblue', foreground='white', borderwidth=2,locale='tr_TR')
car_gel_date_entry.grid(row=2,column=5)

#Buttons 
#myButt=tk.Button(my_frame1,text="Do th Thingé!",command=thing)
#myButt.grid(row=5,column=3)
row_lf3=1
row_lf4=1
row_lf5=1
row_lf6=1
row_lf7=1
column_lf3= 0
add_to_table_button=tk.Button(my_frame1,text="Kaydet",command=add_customer)
add_to_table_button.place(x=900,y=50)
add_entry_lf3=tk.Button(my_frame1,text="Ekle",command=add_row)
add_entry_lf3.place(x=190,y=200)
cust_name_entry.focus()
add_entry_lf4=tk.Button(my_frame1,text="Ekle",command=add_row2)
add_entry_lf4.place(x=555,y=200)
add_entry_lf5=tk.Button(my_frame1,text="Ekle",command=add_row3)
add_entry_lf5.place(x=775,y=200)
add_entry_lf6=tk.Button(my_frame1,text="Ekle",command=add_row4)
add_entry_lf6.place(x=1040,y=200)
add_entry_lf7=tk.Button(my_frame1,text="Ekle",command=add_row5)
add_entry_lf7.place(x=1315,y=200)


deneme=tk.Button(my_frame1,text="Database Oluştur",command=create_table)
deneme.place(x=900,y=10)


# Eklemeli Listedeki tüm widgetları listlere ekleme
dp_ad=[]
dp_tutar=[]
op_ad=[]
op_kaporta=[]
op_boya=[]
ei_ad=[]
ei_tutar=[]
trim_ad=[]
trim_tutar=[]
mi_ad=[]
mi_tutar=[]
get_values=[]

#Liste Silme Tuşları
sil_lf3=tk.Button(my_frame1,text="Sil",command=sil_row,state="disabled",width=3)
sil_lf3.place(x=20,y=200)
sil_lf4=tk.Button(my_frame1,text="Sil",command=sil_row2,state="disabled",width=3)
sil_lf4.place(x=280,y=200)
sil_lf5=tk.Button(my_frame1,text="Sil",command=sil_row3,state="disabled",width=3)
sil_lf5.place(x=610,y=200)
sil_lf6=tk.Button(my_frame1,text="Sil",command=sil_row4,state="disabled",width=3)
sil_lf6.place(x=875,y=200)
sil_lf7=tk.Button(my_frame1,text="Sil",command=sil_row5,state="disabled",width=3)
sil_lf7.place(x=1100,y=200)

#Seperator
#ttk.Separator(my_frame1).grid(row=0,column=2,sticky="ew")
#Iterate cursor by pressing enter<
entries = [cust_name_entry,cust_phone_entry,cust_sigorta_entry,cust_dosya_entry,car_plaka_entry,car_marka_entry,car_model_entry,car_damage_entry,car_fdate_entry,car_est_entry,car_km_entry,car_eksper_entry,car_gel_date_entry]

for idx, entry in enumerate(entries):
    entry.bind("<Return>", lambda e, idx=idx: go_to_next_entry(e, entries, idx))
    

#ARAÇ GEÇMİŞİ TAB#######################################################################################################################################
#######################################################################################################################################################3

isconn=False#database conn var mı yok mu


style_2 = ttk.Style()
#Pick a theme
style_2.theme_use("default")
style_2.configure("Treeview", 
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3"
	)
# Change selected color
style_2.map('Treeview', 
	background=[('selected', 'blue')])
# Create Treeview Frame
tree_frame = tk.Frame(my_frame2)
tree_frame.place(x=870,y=10)

other_info=tk.Frame(my_frame2,bg="lightgrey")
other_info.place(x=10,y=10)

genel_frame=tk.Frame(my_frame2,bg="lightgrey")
genel_frame.place(x=10,y=200)

genel_canvas=tk.Canvas(genel_frame,borderwidth=0,background="grey",width=600,height=400)


# Treeview Scrollbar
tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

#Genelframe içindeki frameler
degisecek_parca_frame=tk.Frame(genel_frame,bg="lightgrey")
onarim_parca_frame=tk.Frame(genel_frame,bg="lightgrey")
elektrik_iscilikleri_frame=tk.Frame(genel_frame,bg="lightgrey")
trim_frame=tk.Frame(genel_frame,bg="lightgrey")
mekanik_iscilikleri_frame=tk.Frame(genel_frame,bg="lightgrey")


genel_scroll=tk.Scrollbar(genel_frame,orient="vertical",command=genel_canvas.yview)
genel_canvas.configure(yscrollcommand=genel_scroll.set)
genel_scroll.pack(side="left",fill="y")

genel_canvas.pack(side="right",fill="both",expand="true")
genel_canvas.create_window((200,100),window=degisecek_parca_frame,anchor="nw")
genel_canvas.create_window((500,100),window=onarim_parca_frame,anchor="nw")
genel_canvas.create_window((200,300),window=elektrik_iscilikleri_frame,anchor="nw")
genel_canvas.create_window((200,500),window=trim_frame,anchor="nw")
genel_canvas.create_window((200,700),window=mekanik_iscilikleri_frame,anchor="nw")

degisecek_parca_frame.bind("<Configure>",lambda event,canvas=genel_canvas: onFrameConfigure(genel_canvas))
onarim_parca_frame.bind("<Configure>",lambda event,canvas=genel_canvas: onFrameConfigure(genel_canvas))
elektrik_iscilikleri_frame.bind("<Configure>",lambda event,canvas=genel_canvas: onFrameConfigure(genel_canvas))
trim_frame.bind("<Configure>",lambda event,canvas=genel_canvas: onFrameConfigure(genel_canvas))
mekanik_iscilikleri_frame.bind("<Configure>",lambda event,canvas=genel_canvas: onFrameConfigure(genel_canvas))

# Create Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse",height=20)
# Pack to the screen
my_tree.pack()

#Configure the scrollbar

tree_scroll.config(command=my_tree.yview)


my_tree['columns']=("Müşteri","Plaka","Hasar","Geliş Tarihi")
my_tree.column("#0",width=0,stretch="no")
my_tree.column("Müşteri",anchor="w",width=130)
my_tree.column("Plaka",anchor="center",width=90)
my_tree.column("Hasar",anchor="w",width=150)
my_tree.column("Geliş Tarihi",anchor="w",width=90)

#Create Headings
my_tree.heading('#0',text="",anchor="w")
my_tree.heading("Müşteri",text="Müşteri",anchor="w")
my_tree.heading("Plaka",text="Plaka",anchor="center")
my_tree.heading('Hasar',text="Hasar",anchor="w")
my_tree.heading('Geliş Tarihi',text="Geliş Tarihi",anchor="w")


# Create striped row tags
count_2=0

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

fillTree()


selected_info_button=tk.Button(my_frame2,text="bilgileri göster",command=showSelected)
selected_info_button.place(x=700,y=100)

refresh_button=tk.Button(my_frame2,text="Yenile",command=fillTree)
refresh_button.place(x=700,y=150)

delete_selected=tk.Button(my_frame2,text="Sil",command=deleteSelectedRec)
delete_selected.place(x=700,y=200)

#Other_info Labellar

gecmis_musteri=tk.Label(other_info,text="Müşteri :",bg="lightgrey")
gecmis_musteri.grid(row=0,column=0,sticky="w",pady=5)
gecmis_telefon=tk.Label(other_info,text="Telefon :",bg="lightgrey")
gecmis_telefon.grid(row=1,column=0,sticky="w",pady=5)
gecmis_sigorta=tk.Label(other_info,text="Sigorta :",bg="lightgrey")
gecmis_sigorta.grid(row=2,column=0,sticky="w",pady=5)
gecmis_dosya=tk.Label(other_info,text="Dosya :",bg="lightgrey")
gecmis_dosya.grid(row=3,column=0,sticky="w",pady=5)

gecmis_plaka=tk.Label(other_info,text="Plaka :",bg="lightgrey")
gecmis_plaka.grid(row=0,column=2,sticky="w",pady=5,padx=5)
gecmis_marka=tk.Label(other_info,text="Marka :",bg="lightgrey")
gecmis_marka.grid(row=1,column=2,sticky="w",pady=5,padx=5)
gecmis_model=tk.Label(other_info,text="Model :",bg="lightgrey")
gecmis_model.grid(row=2,column=2,sticky="w",pady=5,padx=5)
gecmis_hasar=tk.Label(other_info,text="Hasar :",bg="lightgrey")
gecmis_hasar.grid(row=3,column=2,sticky="w",pady=5,padx=5)

gecmis_gelis=tk.Label(other_info,text="Geliş Tarihi :",bg="lightgrey")
gecmis_gelis.grid(row=0,column=4,sticky="w",pady=5,padx=5)
gecmis_gidis=tk.Label(other_info,text="Gidiş Tarihi :",bg="lightgrey")
gecmis_gidis.grid(row=1,column=4,sticky="w",pady=5,padx=5)
gecmis_km=tk.Label(other_info,text="Kilometre :",bg="lightgrey")
gecmis_km.grid(row=2,column=4,sticky="w",pady=5,padx=5)
gecmis_eksper=tk.Label(other_info,text="Eksper :",bg="lightgrey")
gecmis_eksper.grid(row=3,column=4,sticky="w",pady=5,padx=5)
gecmis_geldate=tk.Label(other_info,text="Gel.Tarihi",bg="lightgrey")
gecmis_geldate.grid(row=4,column=4,sticky="w",pady=5,padx=5)

#BU 2 SATIR DATE ENTRYİ SONRADAN EKLEDİĞİMİZ İÇİN
gecmis_geldate_entry=DateEntry(other_info, width=12, background='darkblue', foreground='white', borderwidth=2,locale='tr_TR')
gecmis_geldate_entry.grid(row=4,column=5,sticky="w")


#info entry listeleri
degisecek_info_list=[]
onarilacak_info_list=[]
elektrik_info_list=[]
trim_info_list=[]
mekanik_info_list=[]
#Other_info entry ekleme
save_changes_list=[]
if not save_changes_list:
	for x in range(1,6,2):
		for y in range(4):
			local_entry=tk.Entry(other_info)
			local_entry.grid(row=y,column=x)
			save_changes_list.append(local_entry)
else:
	messagebox.showwarning("Bir şeyler ters gitti\nHata kodu: 001")
	save_changes_list.clear()
save_changes_list.append(gecmis_geldate_entry)

#degisecek parca frame labelları


'''
show_records=tk.Button(my_frame2,text="Kayıtları Göster",command=show_past)
show_records.grid(row=0,column=3)
delete_all=tk.Button(my_frame2,text="Tüm Kayıtları Sil",command=delete_all_Rec)
delete_all.grid(row=1,column=3)
foto_button=tk.Button(my_frame2,text="Fotoğraflar",command=fetch_image)
foto_button.grid(row=0,column=4)
foto_add_button=tk.Button(my_frame1,text="Fotoğraf Ekle",command=insertBLOB)
foto_add_button.place(x=1000,y=50)
'''
root.mainloop()