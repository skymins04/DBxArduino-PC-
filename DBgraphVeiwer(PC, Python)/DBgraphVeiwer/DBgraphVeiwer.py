from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, font
import os
from os import chdir
from os.path import expanduser
import subprocess
import sys, time
from io import BytesIO
import urllib.request as urlreq
from PIL import Image, ImageTk

def main() :
    global homedir
    homedir = os.getcwd()
    global userHome
    userHome = expanduser('~')

    version = 'v.1.0.3'

    """ 메인창 설정 """
    mainW = Tk()
    ttk.Style().theme_use('vista')
    mainW.iconbitmap('BetaMan.ico')
    mainW.title('DB graph Veiwer')
    mainW.geometry('380x500')
    mainW.resizable(width=True,height=False)
    
    """ 타이틀 & 로고 """
    titleFont = font.Font(mainW,size=25,family='malgun')
    title = Label(mainW,text='DB graph Veiwer',height=2) #타이틀
    title['font']=titleFont
    title.pack()

    logo = PhotoImage(file='logo.png') #로고 이미지
    Label(mainW,image=logo,height=200).pack()

    """ 프레임 정의 """
    widgetF = ttk.Frame(mainW); widgetF.pack(); #필수 메뉴 프레임
    Label(mainW,text='--------------------------------| 옵션 |--------------------------------',height=2).pack() #필수 메뉴와 선택 메뉴 구분선
    optionF = ttk.Frame(mainW); optionF.pack(); #선택 메뉴 및 종속 프레임
    optionRow0 = ttk.Frame(optionF); optionRow0.pack(anchor=W);
    optionRow1 = ttk.Frame(optionF); optionRow1.pack(anchor=W);
    optionRow2 = ttk.Frame(optionF); optionRow2.pack(anchor=W);
    infoBarF = ttk.Frame(mainW); infoBarF.pack(anchor=E);

    """ UI 정의 """
    ##상단 메뉴
    topMenu = Menu(mainW)
    mainW.config(menu=topMenu)
    
    file = Menu(topMenu)
    
    file.add_command(label='Open CSV')
    topMenu.add_cascade(label='File',menu=file)

    help = Menu(topMenu)

    help.add_command(label='사용방법',command=lambda:os.system('help.html'))
    topMenu.add_cascade(label='Help',menu=help)

    ##필수 메뉴
    Label(widgetF,text='서버주소: ').grid(row=0,column=0,sticky=W)
    global serAddrEnt; serAddrEnt = ttk.Entry(widgetF,width=30); serAddrEnt.grid(row=0,column=1,sticky=W);
    veiwGraphBtn = ttk.Button(widgetF,text='그래프 보기', command=lambda:veiwGraph(serAddrEnt.get(),DBnameEnt.get(),TBnameEnt.get(),unitEnt.get(),heightEnt.get(),minEnt.get(),addxEnt.get(),addyEnt.get(),str(bool(showPointChe.get())),str(bool(showValueChe.get())))); veiwGraphBtn.grid(row=0,column=2,sticky=E);
    
    Label(widgetF,text='DB명: ').grid(row=1,column=0,sticky=W)
    global DBnameEnt; DBnameEnt = ttk.Entry(widgetF,width=15); DBnameEnt.grid(row=1,column=1,sticky=W);
    DBlistBtn = ttk.Button(widgetF,text='DB 찾기',command=lambda:DBlist(serAddrEnt.get())); DBlistBtn.grid(row=1,column=2,sticky=E);

    Label(widgetF,text='테이블명: ').grid(row=2,column=0,sticky=W)
    global TBnameEnt; TBnameEnt = ttk.Entry(widgetF,width=15); TBnameEnt.grid(row=2,column=1,sticky=W);
    TBlistBtn = ttk.Button(widgetF,text='테이블 찾기', command=lambda:TBlist(serAddrEnt.get(),DBnameEnt.get())); TBlistBtn.grid(row=2,column=2,sticky=E);

    ##선택 메뉴
    #Row0
    Label(optionRow0,text='단위: ',height=2).pack(side=LEFT)
    unitEnt = ttk.Entry(optionRow0,width=3); unitEnt.insert(END,'5'); unitEnt.pack(side=LEFT);

    Label(optionRow0,text=' 포인트당 간격(px): ').pack(side=LEFT)
    heightEnt = ttk.Entry(optionRow0,width=3); heightEnt.insert(END,'3'); heightEnt.pack(side=LEFT);

    Label(optionRow0,text=' 최소 표현치: ').pack(side=LEFT)
    minEnt = ttk.Entry(optionRow0,width=5); minEnt.insert(END,'0'); minEnt.pack(side=LEFT);

    #Row1
    Label(optionRow1,text='그래프 가로길이 추가(px): ').pack(side=LEFT)
    addxEnt = ttk.Entry(optionRow1,width=6); addxEnt.insert(END,'0'); addxEnt.pack(side=LEFT);

    Label(optionRow1,width=2).pack(side=LEFT) #시각적으로 깔끔하게 정렬하기 위해 넣은 쓰레기 코드

    showPointChe = IntVar()
    ttk.Checkbutton(optionRow1,text='노드 보기',variable=showPointChe).pack(side=LEFT)

    #Row2
    Label(optionRow2,text='그래프 세로길이 추가(px): ').pack(side=LEFT)
    addyEnt = ttk.Entry(optionRow2,width=6); addyEnt.insert(END,'0'); addyEnt.pack(side=LEFT);

    Label(optionRow2,width=2).pack(side=LEFT) #시각적으로 깔끔하게 정렬하기 위해 넣은 쓰레기 코드 

    showValueChe = IntVar()
    ttk.Checkbutton(optionRow2,text='노드값 보기',variable=showValueChe).pack(side=LEFT)

    ##정보 바
    Label(infoBarF,text=version+', BetaMan(skymin0417@gmail.com, github.com/skymins04)').pack()
    mainW.mainloop()

""" 함수들 """

#테이블 목록 및 선택
def TBlist(ser,DBname) :
    TB = Toplevel()
    TB.iconbitmap('BetaMan.ico')
    TB.title(' ')
    TB.resizable(width=False, height=False)

    def selectColumn(e) :
        TBnameEnt.delete(0,END)
        TBnameEnt.insert(0,decodelist.split(',')[listbox.curselection()[0]])
        TB.destroy()
    def exitlist() :
        TB.destroy()

    Label(TB,text=ser+', '+DBname+' 의 테이블',width=30).pack()

    url = 'http://'+ser+'/DBxArduino/veiwList.php?DB='+DBname+'&list=TB';
    _list = urlreq.urlopen(url)
    decodelist = str(_list.read().decode('utf-8'))

    listbox = Listbox(TB)
    for i in range(len(decodelist.split(','))) :
        listbox.insert(i+1,str(i+1)+'. '+decodelist.split(',')[i])
    listbox.pack()

    ttk.Button(TB,text='닫기',command=lambda:exitlist()).pack()

    listbox.bind('<Double-Button-1>', selectColumn)

#테이블 목록 및 선택
def DBlist(ser) :
    DB = Toplevel()
    DB.iconbitmap('BetaMan.ico')
    DB.title(' ')
    DB.resizable(width=False, height=False)

    def selectColumn(e) :
        DBnameEnt.delete(0,END)
        DBnameEnt.insert(0,decodelist.split(',')[listbox.curselection()[0]])
        DB.destroy()
    def exitlist() :
        DB.destroy()

    Label(DB,text=serAddrEnt.get()+' 의 DB',width=30).pack()

    url = 'http://'+ser+'/DBxArduino/veiwList.php?list=DB';
    _list = urlreq.urlopen(url)
    decodelist = str(_list.read().decode('utf-8'))

    listbox = Listbox(DB)
    for i in range(len(decodelist.split(','))) :
        listbox.insert(i+1,str(i+1)+'. '+decodelist.split(',')[i])
    listbox.pack()

    ttk.Button(DB,text='닫기',command=lambda:exitlist()).pack()

    listbox.bind('<Double-Button-1>', selectColumn)

#서버에서 받아온 그래프 이미지 출력
def veiwGraph(_ser,DBname,TBname,unit,height,min,addx,addy,point,value) :
    veiwer = Toplevel()
    veiwer.iconbitmap('BetaMan.ico')
    veiwer.title('veiw Graph')
    veiwer.resizable(width=False, height=False)

    url = 'http://'+_ser+'/DBxArduino/dynamicGraph.php?'+'DB='+DBname+'&TB='+TBname+'&unit='+unit+'&height='+height+'&min='+min+'&addx='+addx+'&addy='+addy+'&showPoint='+point+'&showValue='+value
    img = loadGraph(url)
    imgTK = ImageTk.PhotoImage(img)

    img_lbl = Label(veiwer,image=imgTK)
    img_lbl.image = imgTK
    img_lbl.pack()

    """
    이미지 || csv file 저장
    """
    savePath = userHome+'\\Documents\\DBgraphVeiwer\\'+_ser+'\\'+DBname+'\\'+TBname

    def saveGraph():
        now = time.localtime()
        filename = "%04d-%02d-%02d_%02d-%02d-%02d_%s_%s.png" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, _ser, TBname)
        
        if not os.path.exists(savePath+'\\graph') :
            os.makedirs(savePath+'\\graph')
        
        chdir(savePath+'\\graph')
        img.save(filename)
        chdir(homedir)

        msg.showinfo(title='이미지로 저장',message=filename+' 를 저장했습니다\n(위치: '+savePath+'\\graph\\'+filename+')')

    def saveCSV():
        now = time.localtime()
        filename = "%04d-%02d-%02d_%02d-%02d-%02d_%s_%s.csv" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, _ser, TBname)
        
        if not os.path.exists(savePath+'\\csv') :
            os.makedirs(savePath+'\\csv')
        
        chdir(savePath+'\\csv')
        urlreq.urlretrieve('http://'+_ser+'/DBxArduino/exportCSV.php?fname='+filename+'&TB='+TBname+'&DB='+DBname,filename)
        chdir(homedir)
        
        msg.showinfo(title='.csv 파일로 저장',message=filename+' 를 저장했습니다 (위치: '+userHome+'\\Documents\\DBgraphVeiwer\\'+_ser+'\\'+DBname+'\\'+TBname+'\\csv\\'+filename+')')

    ttk.Button(veiwer,text='이미지로 저장',command=lambda:saveGraph()).pack(side=LEFT)
    ttk.Button(veiwer,text='.csv 파일로 저장',command=lambda:saveCSV()).pack(side=LEFT)

#서버에서 그래프 이미지 불러오기
def loadGraph(url) :
    u = urlreq.urlopen(url)
    _raw = u.read()
    u.close()
    _im = Image.open(BytesIO(_raw))
    return _im

if __name__ == '__main__' :
    main()