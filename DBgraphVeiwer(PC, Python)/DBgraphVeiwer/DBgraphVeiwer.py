from io import BytesIO
from tkinter import *
from tkinter import messagebox as msg
import os
from os import chdir
import sys, time
import urllib.request
from PIL import Image, ImageTk
"""
    적용 조건:
        1.서버 홈디렉토리에 DBxArduino/dynamicGraph.php라는 그래프 이미지(.png) 반환 파일이 있어야함(GD 라이브러리)
        2.DBxArduino/dynamicGraph.php 파일이 이 뷰어의 옵션(DB,TB,unit,height,min,addx,addy,showPoint,showValue)를 지원해야함
        3.반환된 그래프 이미지는 .png 포멧의 파일이어야함
        4.서버 홈디렉토리에 DBxArduino/veiwList.php라는 DB/TB 목록 반환 파일이 있어야함(,로 구분 / 옵션: DB=DB명, list=리스트 종류)
        5.테이블 구조는 1.id, 2.time(timestamp), 3.그래프에 표시할 데이터들...
"""

def main() :
    global homeroot
    homeroot = os.getcwd()
    version = 'v.1.0.2.2'

    win = Tk()
    win.iconbitmap('BetaMan.ico')
    win.title('DB graph Veiwer')
    win.resizable(width=False, height=False)

    logo = PhotoImage(file='logo.png')
    Label(win,image=logo).pack()

    row0 = Frame(win)
    row0.pack(anchor=W)
    row1 = Frame(win)
    row1.pack(anchor=W)
    row2 = Frame(win)
    row2.pack(anchor=W)
    row3 = Frame(win)
    row3.pack()
    row4 = Frame(win)
    row4.pack(anchor=W)
    row5 = Frame(win)
    row5.pack(anchor=W)
    row6 = Frame(win)
    row6.pack(anchor=W)
    row7 = Frame(win)
    row7.pack(anchor=E)

    #Frame row0
    Label(row0,text='서버 :').pack(side=LEFT)
    global ent1
    ent1 = Entry(row0,width=30)
    ent1.pack(side=LEFT)

    btn1 = Button(row0,text='그래프 보기',command=lambda:veiwGraph(dbname.get(),ent1.get(),ent2.get(),ent3.get(),ent4.get(),ent5.get(),ent6.get(),ent7.get(),str(bool(Che1var.get())),str(bool(Che2var.get()))))
    btn1.pack(side=LEFT)

    #Frame row1
    Label(row1,text='DB명 :').pack(side=LEFT)
    global dbname
    dbname = Entry(row1,width=14)
    dbname.pack(side=LEFT)

    dbbtn = Button(row1,text='DB 리스트',command=lambda:DBlist(ent1.get()))
    dbbtn.pack(side=LEFT)

    #Frame row2
    Label(row2,text='테이블명 :').pack(side=LEFT)
    global ent2
    ent2 = Entry(row2,width=14)
    ent2.pack(side=LEFT)

    btn2 = Button(row2,text='테이블 리스트',command=lambda:TBlist(ent1.get(),dbname.get()))
    btn2.pack(side=LEFT)

    #Frame row3
    Label(row3,text='----------------------- 옵션 -----------------------',height=2).pack()

    #Frame row4
    Label(row4,text='단위 :').pack(side=LEFT)
    ent3 = Entry(row4,width=3)
    ent3.insert(END,'5')
    ent3.pack(side=LEFT)

    Label(row4,text='포인트당 간격(px) :').pack(side=LEFT)
    ent4 = Entry(row4,width=3)
    ent4.insert(END,'3')
    ent4.pack(side=LEFT)

    Label(row4,text='최소 표현치 :').pack(side=LEFT)
    ent5 = Entry(row4,width=5)
    ent5.insert(END,'0')
    ent5.pack(side=LEFT)

    #Frame row5
    Label(row5,text='그래프 가로 길이 추가(px) :').pack(side=LEFT)
    ent6 = Entry(row5,width=7)
    ent6.insert(END,'0')
    ent6.pack(side=LEFT)

    Che1var = IntVar()
    Checkbutton(row5,text='포인트 보기',variable=Che1var).pack(side=LEFT)

    #Frame row6
    Label(row6,text='그래프 세로 길이 추가(px) :').pack(side=LEFT)
    ent7 = Entry(row6,width=7)
    ent7.insert(END,'0')
    ent7.pack(side=LEFT)

    Che2var = IntVar()
    Checkbutton(row6,text='그래프 값 보기',variable=Che2var).pack(side=LEFT)

    #Frame row7
    Label(row7,text=version+', made by BetaMan(skymin04@gmail.com)').pack()

    win.mainloop()

#테이블 목록 및 선택
def TBlist(ser,dbname) :
    TB = Toplevel()
    TB.iconbitmap('BetaMan.ico')
    TB.title('table list')
    TB.resizable(width=False, height=False)

    def selectColumn(e) :
        ent2.delete(0,END)
        ent2.insert(0,decodelist.split(',')[listbox.curselection()[0]])
        TB.destroy()
    def exitlist() :
        TB.destroy()

    Label(TB,text=ent1.get()+'의 테이블:').pack()

    url = 'http://'+ser+'/DBxArduino/veiwList.php?DB='+dbname+'&list=TB';
    _list = urllib.request.urlopen(url)
    decodelist = str(_list.read().decode('utf-8'))

    listbox = Listbox(TB)
    for i in range(len(decodelist.split(','))) :
        listbox.insert(i+1,str(i+1)+'. '+decodelist.split(',')[i])
    listbox.pack()

    Button(TB,text='닫기',command=lambda:exitlist()).pack()

    listbox.bind('<Double-Button-1>', selectColumn)

#테이블 목록 및 선택
def DBlist(ser) :
    DB = Toplevel()
    DB.iconbitmap('BetaMan.ico')
    DB.title('DB list')
    DB.resizable(width=False, height=False)

    def selectColumn(e) :
        dbname.delete(0,END)
        dbname.insert(0,decodelist.split(',')[listbox.curselection()[0]])
        DB.destroy()
    def exitlist() :
        DB.destroy()

    Label(DB,text=ent1.get()+'의 DB:').pack()

    url = 'http://'+ser+'/DBxArduino/veiwList.php?list=DB';
    _list = urllib.request.urlopen(url)
    decodelist = str(_list.read().decode('utf-8'))

    listbox = Listbox(DB)
    for i in range(len(decodelist.split(','))) :
        listbox.insert(i+1,str(i+1)+'. '+decodelist.split(',')[i])
    listbox.pack()

    Button(DB,text='닫기',command=lambda:exitlist()).pack()

    listbox.bind('<Double-Button-1>', selectColumn)

#서버에서 받아온 그래프 이미지 출력
def veiwGraph(DBname,_ser,graph,unit,height,min,addx,addy,point,value) :
    veiwer = Toplevel()
    veiwer.iconbitmap('BetaMan.ico')
    veiwer.title('veiw Graph')
    veiwer.resizable(width=False, height=False)

    url = 'http://'+_ser+'/DBxArduino/dynamicGraph.php?'+'DB='+DBname+'&TB='+graph+'&unit='+unit+'&height='+height+'&min='+min+'&addx='+addx+'&addy='+addy+'&showPoint='+point+'&showValue='+value
    img = loadGraph(url)
    imgTK = ImageTk.PhotoImage(img)

    def saveGraph():
        now = time.localtime()
        filename = "%04d-%02d-%02d_%02d-%02d-%02d_%s_%s.png" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, _ser, graph)
        if not os.path.exists('C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\graph') :
            os.makedirs('C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\graph')
        chdir('C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\graph')
        img.save(filename)
        chdir(homeroot)
        msg.showinfo(title='이미지로 저장',message=filename+' 를 저장했습니다\n(위치: '+'C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\graph'+filename+')')

    def saveCSV():
        now = time.localtime()
        filename = "%04d-%02d-%02d_%02d-%02d-%02d_%s_%s.csv" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, _ser, graph)
        if not os.path.exists('C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\csv') :
            os.makedirs('C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\csv')
        chdir('C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\csv')
        urllib.request.urlretrieve('http://'+ent1.get()+'/DBxArduino/exportCSV.php?fname='+filename+'&TB='+ent2.get()+'&DB='+dbname.get(),filename)
        chdir(homeroot)
        msg.showinfo(title='.csv 파일로 저장',message=filename+' 를 저장했습니다 (위치: '+'C:\\DBgraphVeiwer\\'+ent1.get()+'\\'+dbname.get()+'\\'+ent2.get()+'\\csv'+filename+')')

    img_lbl = Label(veiwer,image=imgTK)
    img_lbl.image = imgTK
    img_lbl.pack()
    Button(veiwer,text='이미지로 저장',command=lambda:saveGraph()).pack(side=LEFT)
    Button(veiwer,text='.csv 파일로 저장',command=lambda:saveCSV()).pack(side=LEFT)

#서버에서 그래프 이미지 불러오기
def loadGraph(ser) :
    u = urllib.request.urlopen(ser)
    _raw = u.read()
    u.close()
    _im = Image.open(BytesIO(_raw))
    return _im

if __name__ == "__main__" :
    main()
