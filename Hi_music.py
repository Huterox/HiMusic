from main_root import Root
from PIL import ImageTk ,Image
import threading
from music_get import music_text
import  time
import os
import tkinter.messagebox
import tkinter as tk
from urllib.request import urlretrieve
import tkinter.filedialog
import pygame
import eyed3

'''在某一个函数中使用另一个函数的变量要用全局这是毫无疑问的,但是同理要实现某一个功能是需要调用到闭包中的函数变量(内函数调用)也要使用全局
否则会被垃圾机制回收导致功能异常'''

'''
对自定义music_get的说明,这玩意返回一个列表包含字典独享在字典中具有所有的信息

'''

'''这是我们已经开发好的窗口接下来我们只需要对其进行开发调用'''
'''
重点说明
播放选项如下
self.my_load_f :: 导入本地歌单
self.my_load_love :: 我的喜爱歌曲
self.my_load_hand :: 已下载的歌曲
下载选项如下
self.my_load :: 下载至我喜爱
self.my_load_z :: 下载至文件中
self.my_load_z_m :: 自定义下载至
之后是进度条画布
其余的基本使用中文拼音标注
'''



'''设置信号'''
last_sing=''
label_exit=[]

list_sing=[] #用于存放歌曲信息,与搜索功能串通或者本地歌单的导入
#所有的在线相关的歌曲功能都与他关联
id_sing=0
#负责歌曲的切换
'''存放选中的歌曲的信息便于下载与显示'''
music_check={}
#线程交互,下载与显示下载中
sing_are_load=0
'''确定是否为网络控制'''
isinternet=1  #1是网络下载的播放 2是已下载 3是我喜欢 4是导入本地
hand_been_down=[]
my_love_music_play=[]
my_think_music_play=[]
page_which=0
show_label_info_hand=[]#负责与已下载(通过网络获取的本地信号)
show_label_info_love=[]
show_label_info_tkink=[]
#显示哪一面
id_hand_down=0
id_my_love=0
id_my_file=0

'''最后重要的信号是播放的信号'''
star_play=1
is_chang_sing=0
is_press_sing=1 #这是主界面播放按钮是否被按压的信号
is_linking = 0
is_bofangqi_do=0

is_press_sing_b = 0#这是在播放器页面stop 与 contuine的信号


'''这是是否下载在线歌曲的东东(信号)'''
hand_been_down_sing=0

'''窗口查看'''
look_bofangqi=[]


''''''
#播放的关联函数
def time_get(path):
    try:
        info_m=eyed3.load(path)
        time_info=info_m.info.time_secs
        if time_info>int(time_info):
            time_info=int(time_info)+1
        return time_info
    except :
        pass
def progress(path):

        global  is_press_sing ,is_chang_sing,is_linking ,image_go_progress,image_go,hand_been_down_sing
        global is_press_sing_b,fill_line
        try:

            is_linking = 1
            time_wait=time_get(path)/600

            image_go_progress=ImageTk.PhotoImage(file='media//zanting.png')
            root.bofang.configure(image=image_go_progress)
            fill_line = root.jindutiao.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="cyan")
            x = 600  # 进度条顶点为600
            n = 0 # 初始值为0
            if is_press_sing %2==0:
                is_press_sing_b=2
            while 1:
                if is_chang_sing:
                     break
                if is_press_sing_b==2 :
                    n +=1
                    root.jindutiao.coords(fill_line, (0, 0, n, 60))
                    root.jindutiao.update()
                    # 控制进度条流动的速度
                    time.sleep(time_wait)
                elif is_press_sing_b==1 :
                    time.sleep(1)

                if n==600:
                    break

            fill_line =root.jindutiao.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="gray")

            for t in range(x):
                n +=1
                # 以矩形的长度作为变量值更新
                root.jindutiao.coords(fill_line, (0, 0, n, 60))
                root.root.update()
                time.sleep(0)  # 时间为0，即飞速清空进度条


            image_go=ImageTk.PhotoImage(file='media//bofang.png')
            root.bofang.configure(image=image_go)
            #复位
            is_chang_sing = 0
            is_linking = 0
            is_press_sing = 1
            is_press_sing_b = 0
        except Exception as e:
            pass

def bofangqi(path,name):
    global v ,is_press_sing_b,is_bofangqi_do,isinternet,hand_been_down_sing

    is_bofangqi_do = 1
    if look_bofangqi:
        l=look_bofangqi.pop()
        l.destroy()
    root_ = tk.Toplevel()
    root_.title("音乐播放器")
    root_['background']='white'
    root_.iconbitmap(r'media\\Hitubiao.ico')
    root_.title('Hi音乐播放器v0.5')
    root_.resizable(width=False,height=False)
    image_=tk.PhotoImage(file=r'media\bofangqi.png')
    cavans=tk.Canvas(root_,bg='white')
    cavans.place(x=0,y=0)
    cavans.create_image(100,50,image = image_)
    look_bofangqi.append(root_)
    v=0.5
    def play():

        pygame.mixer.init()
        pygame.mixer.music.load(path)  # 加载本地文件
        pygame.mixer.music.set_volume(v)
        pygame.mixer.music.play()  # 播放音乐


    def stop():
        global is_press_sing_b
        pygame.mixer.music.pause() # 停止音乐
        is_press_sing_b=1 #1是停止



    def bofang():

        play()  #


    def go_again():  # 下一首
        global is_press_sing_b
        pygame.mixer.music.unpause()
        is_press_sing_b = 2


    def add_yinliang():
        global v
        if v==1:
            return
        v +=0.1
        pygame.mixer.music.set_volume(v)

    def jian():
        global v
        if v == 0:
            return
        v -= 0.1
        pygame.mixer.music.set_volume(v)

    play()#一打开就先播放
    if isinternet==3 or isinternet==4:
        str_l=''

        for x in name:
            if x=='(' or x==')':
                x=''
                str_l+='\n'

            if x!='(' or x !=')':
                str_l+=x


        root.see_bofang['text'] = str_l
    if isinternet==2:
        str_l=''

        for x in name:
            if x=='<' or x=='>' :
                x=''
                str_l+='\n'

            if x!='(' or x !=')':
                str_l+=x
        root.see_bofang['text'] = str_l
    if isinternet ==1 :
        pass

    root.see_bofang.configure(font=('宋体',10),fg='red')



    b1 =tk.Button(root_, text="+音量", width=10, command=add_yinliang,bg='pink',relief='solid')
    b1.grid(row=0, column=0, padx=10, pady=10)

    b2 = tk.Button(root_, text="继续", width=10, command=go_again,bg='pink',relief='solid')
    b2.grid(row=0, column=1, padx=10, pady=10)

    b3 =tk.Button(root_, text="-音量", width=10, command=jian,bg='pink',relief='solid')
    b3.grid(row=0, column=2, padx=10, pady=10)

    b4 = tk.Button(root_, text="停止", width=20, command=stop,bg='pink',relief='solid')
    b4.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

    b5 = tk.Button(root_, text="开始", width=20, command=bofang,bg='pink',relief='solid')
    b5.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
    def stop__(xincan):
        global  is_bofangqi_do
        # is_bofangqi_do = 0

        print('00')
        root_.destroy()


    #这tM不写也行,只是由于结构的问题我原来想实现一个功能来着
    root_.protocol("WM_DELETE_WINDOW", lambda : stop__('0'))
    root_.mainloop()


    #复位
    print('00')
    is_bofangqi_do = 0

'''负责显示歌曲图片信息'''
def pic_music_show():

    if list_sing:
        try:
            global  music_img_pic
            path=r'media\view\view.jpg'
            urlretrieve(music_check['pic'],path)
            music_img_pic=Image.open(path)
            music_img_pic=music_img_pic.resize((210,290),Image.ANTIALIAS)
            music_img_pic=ImageTk.PhotoImage(music_img_pic)
            root.see_bofang.configure(image=music_img_pic)
            root.see_bofang.update()

        except:
            pass





'''播放动态图'''

def update_u():
    #global sing_are_load
    unmdex = 25  # 设置帧数
    frames = [tk.PhotoImage(file='media\loading.gif', format='gif -index %i' % (i)) for i in range(unmdex)]

    def update(id_x):
        global sing_are_load
        if sing_are_load:
            sing_are_load = 0

            '''遇事不决直接删除再新建'''
            root.see_bofang.destroy()
            root.see_bofang = tk.Label(root.root, bg='azure',fg='gray', font=('宋体', 12), text='')
            root.see_bofang.place(x=860, y=340, width=170, height=230)
            root.see_bofang['text']='下载完成呦!'


            return
        frame = frames[id_x]
        id_x += 1
        root.see_bofang.configure(image=frame)
        root.root.after(100, update, id_x % unmdex)


    root.root.after(0, update, 0)


''''''

'''对于在线播放的下载动态图'''
def update_u_line():
    #global sing_are_load
    unmdex = 25  # 设置帧数
    frames = [tk.PhotoImage(file='media\loading.gif', format='gif -index %i' % (i)) for i in range(unmdex)]

    def update(id_x):
        global sing_are_load
        if sing_are_load:
            sing_are_load=0


            '''遇事不决直接删除再新建'''
            root.see_bofang.destroy()
            root.see_bofang = tk.Label(root.root, bg='azure',fg='gray', font=('宋体', 12), text='')
            root.see_bofang.place(x=860, y=340, width=170, height=230)
            root.see_bofang['text']=list_sing[id_sing]['name']+'\n'+list_sing[id_sing]['singer']

            return
        frame = frames[id_x]
        id_x += 1
        root.see_bofang.configure(image=frame)
        root.root.after(100, update, id_x % unmdex)


    root.root.after(0, update, 0)







'''负责下载歌曲'''
def download(url,path):
    try:
        # data_=requests.get(url)
        # data=data_.content
        # with open(path,'wb') as f:
        #     f.write(data)
        #     f.close()
        urlretrieve(url,path)
        print('111111111111')
    except Exception as e :
        tkinter.messagebox.showinfo('tips', e)
    return





'''主要负责标注选择的歌曲'''
def sing_link(name,y):
    label_sing=tk.Label(root.root,font=('Georgia',15),fg='gold',bg='azure',text=name)
    label_sing.place(x=230,y=y,width=600,height=51)
    label_exit.append(label_sing)
    return

'''搜索的控制函数'''
def sousou_b_com(xincan):
    global last_sing , list_sing ,music_check ,isinternet ,id_sing,is_bofangqi_do,hand_been_down_sing

    hand_been_down_sing=0
    is_bofangqi_do=0
    isinternet=1
    if label_exit:
        b=label_exit.pop()
        b.destroy()
    # if last_sing:
    #     if last_sing==root.entry_s.get():
    #         return
    if list_sing:
        list_sing.clear()
    key=root.entry_s.get()
    last_sing=key
    if  key :
        last_sing=key

        image_sousuozhong=ImageTk.PhotoImage(file='media\\sousuozhong.png')
        root.info_label.configure(image=image_sousuozhong)
        root.info_label['text'] = ''

        root.info_label.update()
        list_sing=music_text(key)
        str_=''
        for i in list_sing:
            str_+=i['name'].strip()+'<-->'+i['singer'].strip()+'\n'+'\n'

        root.info_label.configure(text=str_,font=('Georgia',14),fg='gray')
        root.info_label.update()
        look_link=list_sing[0]['name']+'<-->'+list_sing[0]['singer'].strip()
        sing_link(look_link,100)#初始之位100以45为间隔向下或向上
        music_check['name']=list_sing[0]['name']
        music_check['url'] = list_sing[0]['url']
        music_check['pic'] = list_sing[0]['pic']
        music_check['singer'] = list_sing[0]['singer']
        id_sing=0#复位
        #look_link_=list_sing[id_sing]['name']+'\n'+list_sing[id_sing]['singer'].strip()
        #root.see_bofang['text'] = look_link_
        pic_music_show()

    return


'''下一首歌的函数处理'''
def next_sing(xincan):
    global id_sing ,isinternet,page_which,id_my_love,id_my_file,is_chang_sing,is_bofangqi_do,hand_been_down_sing
    if isinternet==1:
        hand_been_down_sing=0
        #global id_sing
        if list_sing:
            is_chang_sing = 1
            if id_sing+1>= len(list_sing):
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()
            id_sing +=1
            y=100+45*id_sing

            look_link=list_sing[id_sing]['name']+'<-->'+list_sing[id_sing]['singer'].strip()
            sing_link(look_link,y)#以45为间隔向下或向上
            music_check['name']=list_sing[id_sing]['name']
            music_check['url'] = list_sing[id_sing]['url']
            music_check['pic'] = list_sing[id_sing]['pic']
            music_check['singer'] = list_sing[id_sing]['singer']
            #look_link_=list_sing[id_sing]['name']+'\n'+list_sing[id_sing]['singer'].strip()
            #root.see_bofang['text'] = look_link_
            pic_music_show()
            is_bofangqi_do = 0
    elif isinternet==2:

        global id_hand_down
        if hand_been_down:
            is_chang_sing = 1
            id_hand_down += 1

            if id_hand_down >= len(hand_been_down):
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()


            if id_hand_down >= (page_which+1)*10 :
                page_which +=1
                root.info_label['text'] = show_label_info_hand[page_which]
                if label_exit:
                    b = label_exit.pop()
                    b.destroy()
            y = 100 + 45 * (id_hand_down - 10 * (page_which))
            print(id_hand_down)
            print(hand_been_down[id_hand_down]['sing_name'])
            sing_link(hand_been_down[id_hand_down]['sing_name'],y)
            is_bofangqi_do = 0



    elif isinternet==3:

        if my_love_music_play:
            is_chang_sing = 1
            id_my_love += 1

            if id_my_love >= len(my_love_music_play):
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()

            if id_my_love >= (page_which+1)*10 :
                page_which +=1
                root.info_label['text'] = show_label_info_love[page_which]
                if label_exit:
                    b = label_exit.pop()
                    b.destroy()
            y = 100 + 45 * (id_my_love- 10 * (page_which))
            #print(id_my_love)
            #print(my_love_music_play[id_my_love]['sing_name'])
            #print(my_love_music_play)
            sing_link(my_love_music_play[id_my_love]['sing_name'],y)
            is_bofangqi_do = 0


    elif isinternet==4:

        if my_think_music_play:
            is_chang_sing = 1
            id_my_file += 1

            if id_my_file >= len(my_think_music_play):
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()


            if id_my_file >= (page_which+1)*10 :
                page_which +=1
                root.info_label['text'] = show_label_info_love[page_which]
                if label_exit:
                    b = label_exit.pop()
                    b.destroy()
            y = 100 + 45 * (id_my_file- 10 * (page_which))
            #print(id_my_file)
            #print(my_think_music_play[id_my_file]['sing_name'])
            #print(my_love_music_play)
            sing_link(my_think_music_play[id_my_file]['sing_name'],y)
            is_bofangqi_do = 0



    return


'''上一首歌的处理方式'''

def  last_sing_com(xiuncan):

    global id_sing ,isinternet,page_which,is_chang_sing,is_bofangqi_do,hand_been_down_sing
    if isinternet==1:
        pic_music_show()
        hand_been_down_sing=0
        # global id_sing
        if list_sing:
            is_chang_sing = 1
            if id_sing <=0:
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()
            id_sing -=1
            y=100+45*id_sing

            look_link=list_sing[id_sing]['name']+'<-->'+list_sing[id_sing]['singer'].strip()
            sing_link(look_link,y)#以45为间隔向下或向上
            music_check['name']=list_sing[id_sing]['name']
            music_check['url'] = list_sing[id_sing]['url']
            music_check['pic'] = list_sing[id_sing]['pic']
            music_check['singer']=list_sing[id_sing]['singer']
            pic_music_show()
            is_bofangqi_do = 0

            #look_link_=list_sing[id_sing]['name']+'\n'+list_sing[id_sing]['singer'].strip()
            #root.see_bofang['text'] = look_link_
            #print(music_check)
            #区别不大最后还得堵塞而且会导致线程堵死页面卡顿所以直接使用单线程
            # t1 = threading.Thread(target=a)
            # t1.setDaemon(True)
            # t1.start()
            # t1.join()
            # t2 = threading.Thread(target=pic_music_show)
            # t2.setDaemon(True)
            # t2.start()
            # t2.join()
    elif isinternet==2:
        global id_hand_down
        if hand_been_down:
            is_chang_sing = 1

            if id_hand_down <= 0:
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()

            id_hand_down-=1

            if id_hand_down<page_which*10:
                page_which -=1
                root.info_label.destroy()
                root.info_label = tk.Label(root.root, bg='azure', font=('Georgia', 15), fg='gray', compound='center',text='', anchor='n')
                root.info_label.place(x=230, y=100, width=600, height=500)
                root.info_label['text'] = show_label_info_hand[page_which]
                if label_exit:
                    b = label_exit.pop()
                    b.destroy()
            y = 100 + 45 * (id_hand_down - 10 * (page_which))
            #print(id_hand_down)
            #print(hand_been_down[id_hand_down]['sing_name'])
            sing_link(hand_been_down[id_hand_down]['sing_name'],y)
            is_bofangqi_do = 0

    elif isinternet == 3:
        is_chang_sing = 1
        global id_my_love
        if my_love_music_play:

            if id_my_love <= 0:
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()

            id_my_love -= 1

            if id_my_love < page_which * 10:
                page_which -= 1
                root.info_label.destroy()
                root.info_label = tk.Label(root.root, bg='azure', font=('Georgia', 15), fg='gray', compound='center',text='', anchor='n')
                root.info_label.place(x=230, y=100, width=600, height=500)
                root.info_label['text'] = show_label_info_love[page_which]
                if label_exit:
                    b = label_exit.pop()
                    b.destroy()
            y = 100 + 45 * (id_my_love - 10 * (page_which))
            # print(id_my_love)
            # print(my_love_music_play[id_my_love]['sing_name'])
            sing_link(my_love_music_play[id_my_love]['sing_name'], y)
            is_bofangqi_do = 0

    elif isinternet == 4:
        global id_my_file
        if my_think_music_play:
            is_chang_sing = 1
            if id_my_file <= 0:
                return
            if label_exit:
                b = label_exit.pop()
                b.destroy()

            id_my_file -= 1

            if id_my_file< page_which * 10:
                page_which -= 1
                root.info_label.destroy()
                root.info_label = tk.Label(root.root, bg='azure', font=('Georgia', 15), fg='gray', compound='center',text='', anchor='n')
                root.info_label.place(x=230, y=100, width=600, height=500)
                root.info_label['text'] = show_label_info_tkink[page_which]
                if label_exit:
                    b = label_exit.pop()
                    b.destroy()
            y = 100 + 45 * (id_my_file - 10 * (page_which))
            # print(id_my_love)
            # print(my_love_music_play[id_my_love]['sing_name'])
            sing_link(my_think_music_play[id_my_file]['sing_name'], y)
            is_bofangqi_do = 0

    return#不用管最后函数格式(便于查看缩进结构)


def download_love(xincan):
    global is_bofangqi_do, sing_are_load
    is_bofangqi_do = 0

    if list_sing :
        def a():
            global sing_are_load
            path='love music'+'/'+list_sing[id_sing]['name']+'('+list_sing[id_sing]['singer']+')'+'.mp3'
            download(list_sing[id_sing]['url'],path)
            sing_are_load=1
            dict_={}
            dict_['sing_name']=list_sing[id_sing]['name']+'<-->'+list_sing[id_sing]['singer']
            dict_['path']=path
            hand_been_down.append(dict_)

            return
        t1 = threading.Thread(target=a)
        t1.start()
        t2 = threading.Thread(target=update_u)
        t2.start()

    return

def download_myfile(xincan):
     global is_bofangqi_do
     is_bofangqi_do = 0

     if list_sing:
        def a():
            global sing_are_load

            path=tkinter.filedialog.askdirectory()
            name=path+'/'+list_sing[id_sing]['name']+'('+list_sing[id_sing]['singer']+')'+'.mp3'
            download(list_sing[id_sing]['url'], name)
            sing_are_load=1
            hand_been_down.append(music_check)
            # print(hand_been_down)
            dict_={}
            dict_['sing_name']=list_sing[id_sing]['name']+'<-->'+list_sing[id_sing]['singer']
            dict_['path']=name
            hand_been_down.append(dict_)
            return

        t1 = threading.Thread(target=a)
        t1.start()
        t2 = threading.Thread(target=update_u)
        t2.start()
     return

def download_my_tk(xincan):
     global is_bofangqi_do
     is_bofangqi_do = 0

     if list_sing:
         def a():
            global sing_are_load
            path=tkinter.filedialog.asksaveasfilename()
            if path:
                name = path+'.mp3'

                download(list_sing[id_sing]['url'],name)
                sing_are_load = 1
                dict_ = {}
                dict_['sing_name'] = list_sing[id_sing]['name'] + '<-->' + list_sing[id_sing]['singer']
                dict_['path'] = name
                hand_been_down.append(dict_)
            return

         t1 = threading.Thread(target=a)
         t1.start()
         t2 = threading.Thread(target=update_u)
         t2.start()
     return

#导入已下载
def hand_been_down_music(xincan):
    global isinternet ,page_which ,is_bofangqi_do
    is_bofangqi_do = 0

    # show_label_info_hand=[]
    if hand_been_down:
        page_which = 0  # 复位
        id_sing = 0
        isinternet=2
        i=1
        str_show_=''
        for every in hand_been_down:
            #print(every)
            str_show_i=every['sing_name']+'\n'+'\n'
            str_show_+=str_show_i
            if i % 10 == 0:
                show_label_info_hand.append(str_show_)
                str_show_=''
            elif i==len(hand_been_down):
                show_label_info_hand.append(str_show_)
            i+=1
        root.info_label.destroy()
        root.info_label = tk.Label(root.root, bg='azure', font=('Georgia', 15), fg='gray', compound='center',text='',anchor='n')
        root.info_label.place(x=230, y=100, width=600, height=500)
        root.info_label['text']=show_label_info_hand[page_which]
        sing_link(hand_been_down[id_hand_down]['sing_name'], 100)



#导入我喜欢
def my_like_music(xincan):
    global isinternet ,page_which ,id_my_love ,is_bofangqi_do
    is_bofangqi_do = 0

    path='love music'
    name_list=[]
    m_all = os.listdir(path)
    if m_all:
        # my_love_music_play.clear()
        page_which = 0  # 复位
        id_my_love = 0
        isinternet = 3


        for name_i in m_all:
            #print(name_i)
            if '.mp3' in name_i:
                dict_={}


                save_path=path+'/'+name_i
                #print(save_path)

                name_list.append(name_i.replace('.mp3',''))
                dict_['sing_name'] = name_i.replace('.mp3','')
                dict_['path'] = save_path
                #print(dict_)
                my_love_music_play.append(dict_)
        #print(my_love_music_play)
        i=1
        str_show_=''
        for every in name_list:
            #print(every)
            str_show_i=every+'\n'+'\n'
            str_show_+=str_show_i
            if i % 10 == 0:
                show_label_info_love.append(str_show_)
                str_show_=''
            elif i==len(name_list):
                show_label_info_love.append(str_show_)
            i+=1
        root.info_label.destroy()
        root.info_label = tk.Label(root.root, bg='azure', font=('Georgia', 15), fg='gray', compound='center',text='',anchor='n')
        root.info_label.place(x=230, y=100, width=600, height=500)
        root.info_label['text']=show_label_info_love[page_which]
        sing_link(my_love_music_play[id_my_love]['sing_name'],100)
    return

def my_file_music(xincan):

    global isinternet ,page_which ,id_my_file ,is_bofangqi_do
    is_bofangqi_do=0
    path = tkinter.filedialog.askdirectory()
    # print(path)
    name_list=[]
    m_all = os.listdir(path)
    if m_all:
        # my_love_music_play.clear()
        page_which = 0  # 复位
        id_my_file = 0
        isinternet = 4

        for name_i in m_all:
            #print(name_i)
            if '.mp3' in name_i:
                dict_={}


                save_path=path+'/'+name_i
                #print(save_path)

                name_list.append(name_i.replace('.mp3',''))
                dict_['sing_name'] = name_i.replace('.mp3','')
                dict_['path'] = save_path
                #print(dict_)
                my_think_music_play.append(dict_)
        print(my_think_music_play)

        i=1
        str_show_=''
        for every in name_list:
            #print(every)
            str_show_i=every+'\n'+'\n'
            str_show_+=str_show_i
            if i % 10 == 0:
                show_label_info_tkink.append(str_show_)
                str_show_=''
            elif i==len(name_list):
                show_label_info_tkink.append(str_show_)
            i+=1
        root.info_label.destroy()
        root.info_label = tk.Label(root.root, bg='azure', font=('Georgia', 15), fg='gray', compound='center',text='',anchor='n')
        root.info_label.place(x=230, y=100, width=600, height=500)
        root.info_label['text']=show_label_info_tkink[page_which]
        sing_link(my_think_music_play[id_my_file]['sing_name'],100)
    return



def player_music(xincan):
    global id_my_file, is_press_sing, is_press_sing_b,id_sing,id_my_love,sing_are_load,id_hand_down,is_linking

    #网络下载的

    if isinternet==1:

        if list_sing:
            is_press_sing += 1
            str___=list_sing[id_sing]['name']+'x'+list_sing[id_sing]['singer'].strip()
            path_music = r'music\{}.mp3'.format(str___)
            # print(path_music)
            name='xincan'
            def a():

                global sing_are_load,hand_been_down_sing
                mucic_url=list_sing[id_sing]['url']
                str___ = list_sing[id_sing]['name']+'x'+ list_sing[id_sing]['singer'].strip()
                path_own = r'music\{}.mp3'.format(str___)
                print(path_own)

                download(mucic_url,path_own)
                sing_are_load = 1
                hand_been_down_sing=1
                print('ok')
                print(hand_been_down_sing)
                print(list_sing[id_sing]['name'])
            if hand_been_down_sing==0:
                t1 = threading.Thread(target=a)
                t1.start()
                t2 = threading.Thread(target=update_u_line)
                t2.start()
            while 1:

                if hand_been_down_sing ==1:
                    break
                time.sleep(1)

            if is_linking == 0:
                def x_1():
                    progress(path_music)

                t1 = threading.Thread(target=x_1)
                t1.start()
            if is_bofangqi_do == 0:
                bofangqi(path_music, name)
            if is_press_sing % 2 == 0:

                is_press_sing_b = 2
                pygame.mixer.music.unpause()

            elif is_press_sing % 2 != 0:
                is_press_sing_b = 1
                pygame.mixer.music.pause()
            return





    #已下载的
    elif isinternet==2:

        path_music=hand_been_down[id_hand_down]['path']
        name=hand_been_down[id_hand_down]['sing_name']
        is_press_sing += 1
        if is_linking == 0:
            def x_1():
                progress(path_music)

            t1 = threading.Thread(target=x_1)
            t1.start()
        if is_bofangqi_do == 0:
            bofangqi(path_music, name)
        if is_press_sing % 2 == 0:

            is_press_sing_b = 2
            pygame.mixer.music.unpause()

        elif is_press_sing % 2 != 0:
            is_press_sing_b = 1
            pygame.mixer.music.pause()

    elif isinternet ==3:

        is_press_sing += 1
        print(is_press_sing)
        if my_love_music_play:
            path_music=my_love_music_play[id_my_love]['path']
            name = my_love_music_play[id_my_love]['sing_name']
            # print(name)
            # print(path_music)

            if is_linking == 0:
                def x_1():
                        progress(path_music)
                t1=threading.Thread(target=x_1)
                t1.start()
            if is_bofangqi_do ==0:
                bofangqi(path_music,name)
            if  is_press_sing % 2 ==0 :

                is_press_sing_b = 2
                pygame.mixer.music.unpause()

            elif  is_press_sing % 2 !=0 :
                is_press_sing_b = 1
                pygame.mixer.music.pause()

    elif isinternet == 4:


        is_press_sing += 1
        if my_think_music_play:
            path_music=my_think_music_play[id_my_file]['path']
            name = my_think_music_play[id_my_file]['sing_name']
            # print(name)
            # print(path_music)

            if is_linking == 0:
                def x_1():
                        progress(path_music)
                t1=threading.Thread(target=x_1)
                t1.start()
            if is_bofangqi_do ==0:
                bofangqi(path_music,name)
            if  is_press_sing % 2 ==0 :

                is_press_sing_b = 2
                pygame.mixer.music.unpause()

            elif  is_press_sing % 2 !=0 :
                is_press_sing_b = 1
                pygame.mixer.music.pause()



if __name__ =="__main__":

    root=Root()
    root.label_main()#由于布局的问题这两个顺序不要换
    root.button_main()

    root.sousuo_b.bind('<Button-1>',lambda a:sousou_b_com('0'))
    root.xiayishou.bind('<Button-1>',lambda a:next_sing('0'))
    root.shangyishou.bind('<Button-1>',lambda a:last_sing_com('0'))

    root.my_load.bind('<Button-1>',lambda a:download_love('0'))
    root.my_load_z.bind('<Button-1>',lambda a:download_myfile('0'))
    root.my_load_z_m.bind('<Button-1>',lambda a:download_my_tk('0'))

    root.my_load_hand.bind('<Button-1>',lambda a:hand_been_down_music('0'))
    root.my_load_love.bind('<Button-1>',lambda a:my_like_music('0'))
    root.my_load_f.bind('<Button-1>',lambda a:my_file_music('0'))


    root.bofang.bind('<Button-1>',lambda a:player_music('0'))

    root.mainloop()