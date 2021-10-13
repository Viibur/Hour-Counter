import csv
from tkinter import *
import os

fieldnames = ['Date','Time','Description']

#function that reads in the csv file
def readable(name):
    allrows = []
    with open(str(name)+'.csv','r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            sentence = ', '.join(row)
            allrows.append(sentence.split(','))
        fieldnames = [allrows[0][0],allrows[0][1],allrows[0][2]]
    return allrows
        
# function for appending to the csv file  
def appendable(name,date,time,desc):
    if (len(date) == 8 and time.isdigit()):
        with open(str(name)+'.csv','a',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({fieldnames[0]: date, fieldnames[1]: time, fieldnames[2]: desc})

#function 
def out(name):
    out = Tk()
    
    rows = readable(name)
    y = 1
    text = Text(out)
    
    for i in rows:
        if len(i[0]) < 6:
            i[0] += '  '
        text.pack()
        a = ''
        for j in range(2,len(i)):
            if j < len(i)-1:
                a += i[j]+', '
            else:
                a += i[j]
        text.insert('%s.0'%(y),str(i[0])+" "+str(i[1])+" "+a.replace('"','')+'\n')
        y += 1
        
    out.mainloop()

# function to create the two date labels
def calc(name):
    calculator = Tk()
    
    dateLabel = Label(calculator,text="Start date(DD.MM.YY)")
    dateLabel.pack()
    dateInput = Entry(calculator)
    dateInput.pack()
    
    date2Label = Label(calculator,text="End date(DD.MM.YY)")
    date2Label.pack()
    date2Input = Entry(calculator)
    date2Input.pack()
    
    b = Button(calculator,text='Calculate hours', command = lambda : calcHours(name,dateInput.get(),date2Input.get(),calculator))
    b.pack()
    
    calculator.mainloop()

# function for calculating the time between two dates (in hours)
def calcHours(name,startDate, endDate,root):
    hours = 0
    rows = readable(name)
    dates = []
    for i in rows:
        dates.append(i[0])
    if (len(startDate) == len(endDate) == 8):
        date1 = startDate.split('.')
        date2 = endDate.split('.')
        
        d1di = int(date1[0]) # date1 day integer
        d1mi = int(date1[1]) # date1 month integer
        d1yi = int(date1[2]) # date1 year integer
        
        d2di = int(date2[0]) # date2 day integer
        d2mi = int(date2[1]) # date2 month integer
        d2yi = int(date2[2]) # date2 year integer
        
        
        if(d2di < 31):
            d2di += 1
        elif(d2di == 31):
            d2di = 1
            d2mi += 1
            if(d2mi == 13):
                d2mi = 1
                d2yi += 1
                d2di = 1
        
        while(str(d1di)+str(d1mi)+str(d1yi) != str(d2di)+str(d2mi)+str(d2yi)):
            if(d1yi > d2yi or (d1yi == d2yi and d1mi > d2mi)):
                break
            if(includes(d1di,d1mi,d1yi,dates)):
                hours += int(rows[dates.index(formatToString(d1di,d1mi,d1yi))][1])
            d1di += 1
            if(d1di >= 32):
                d1di = 1
                d1mi += 1
                if(d1mi >= 13):
                    d1mi = 1
                    d1yi += 1
    Label(root,text=hours).pack()
    
def includes(day,month,year,dates):
    if(day < 10):
        dayS = str(day)
        day = '0'+dayS
    if(month < 10):
        monthS = str(month)
        month = '0'+monthS
    if(year < 10):
        yearS = str(year)
        year = '0'+yearS
    if(str(day)+'.'+str(month)+'.'+str(year) in dates):
        return True
    return False
       
def formatToString(day,month,year):
    if(day < 10):
        dayS = str(day)
        day = '0'+dayS
    if(month < 10):
        monthS = str(month)
        month = '0'+monthS
    if(year < 10):
        yearS = str(year)
        year = '0'+yearS
    return str(day)+'.'+str(month)+'.'+str(year)
    
def intake(name):
    insert = Tk()
    
    y = 1
    
    dateLabel = Label(insert,text="Date(DD.MM.YY)")
    dateLabel.pack()
    dateInput = Entry(insert)
    dateInput.pack()
    
    hourLabel = Label(insert,text="Hours(integers)")
    hourLabel.pack()
    hourInput = Entry(insert)
    hourInput.pack()
    
    descLabel = Label(insert,text="Description")
    descLabel.pack()
    descInput = Entry(insert)
    descInput.pack()
    
    b = Button(insert,text='Insert into file', command = lambda : appendable(name,dateInput.get(),hourInput.get(),descInput.get()))
    b.pack()
    
    insert.mainloop()
    
def create(name):
    with open(str(name)+'.csv','w',newline='') as newFile:
        wr = csv.writer(newFile)
        wr.writerow(fieldnames)

def main():            
    top = Tk()
    
    sb = Scrollbar(top)
    sb.pack(side = LEFT)
    
    fileNames = []
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    for f in files:
        if ('.csv' in f):
            fileNames.append(f.replace('.csv',''))
    
    myList = Listbox(top,yscrollcommand = sb.set)
    myList.delete(0,END)
    
    for i in fileNames:
        myList.insert(END,i)
    
    myList.pack(side = LEFT)
    
    
    createLabel = Label(top,text="Create")
    createLabel.pack()
    createInput = Entry(top)
    createInput.pack()
    
    createFile = Button(top,text = 'Create',command = lambda : [create(createInput.get()),myList.insert(END,createInput.get())])
    createFile.pack()
    
    insert = Button(top,command = lambda : intake(myList.get(ACTIVE)),text = 'Insert')
    insert.pack()
    
    calculate = Button(top,command = lambda : calc(myList.get(ACTIVE)),text = 'Calculate')
    calculate.pack()
    
    show = Button(top,command = lambda : out(myList.get(ACTIVE)),text = 'Read')
    show.pack()
    
    
    top.mainloop()
main()
