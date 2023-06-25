from PIL import Image,ImageTk
import tkinter as tk
import os
import weather
import threading







class  Root():
    '''坑点警告,tkinter的线程容易冲突建议将多个按钮或标签分组打包好一个方法
    否者容易造成线程堵塞冲突,冲而导致功能异常
    此外最好不要使用直接后面place 或者pack等直接防止的方法
    '''



    def __init__(self):

        self.root=tk.Tk()

        self.root.geometry('1100x750')
        self.root.title('Hi音乐v1.01')
        self.root.iconbitmap(r'media\\Hitubiao.ico')
        self.root['background']='white'
        self.root.resizable(width=False,height=False)



    def button_main(self):
        #搜索按钮
        self.sousuo_b=tk.Button(self.root,font=('宋体', 14),relief='solid',text='搜索')
        self.sousuo_b.place(x=750,y=20,width=80,height=30)


        #播放控制按钮
        self.bofang_img=ImageTk.PhotoImage(file='media\\bofang.png')
        self.bofang=tk.Button(self.root,image=self.bofang_img,relief='solid')
        self.bofang.place(x=515,y=610,width=70,height=50)

        self.shangyishou_img=ImageTk.PhotoImage(file='media\\shangyisou.png')
        self.shangyishou = tk.Button(self.root, image=self.shangyishou_img, relief='solid')
        self.shangyishou.place(x=400, y=610, width=100, height=50)

        self.xiayishou_img=ImageTk.PhotoImage(file='media\\xiayishou.png')
        self.xiayishou = tk.Button(self.root, image=self.xiayishou_img, relief='solid')
        self.xiayishou.place(x=595, y=610, width=100, height=50)

        #我的音乐按钮


        self.my_music = tk.Label(self.root, bg='white', fg='gray', font=('宋体', 12), text='我的音乐', justify='left')
        self.my_music.place(x=-10, y=250, width=140, height=20)

        self.my_load_f = tk.Button(self.root,font=('宋体', 10),relief='flat',text='导入本地歌单',bg='white' )
        self.my_load_f.place(x=0,y=280,width=140, height=20)

        self.my_load_love= tk.Button(self.root,font=('宋体', 10),relief='flat',text='我的喜爱歌曲',bg='white' )
        self.my_load_love.place(x=0,y=310,width=140, height=20)

        self.my_load_hand= tk.Button(self.root,font=('宋体', 10),relief='flat',text='已下载的歌曲',bg='white' )
        self.my_load_hand.place(x=0,y=340,width=140, height=20)

        #下载选项按钮

        self.my_load=tk.Button(self.root,font=('宋体', 10),relief='flat',text='下载至我喜爱',bg='white' )
        self.my_load.place(x=0,y=400,width=140, height=20)

        self.my_load_z=tk.Button(self.root,font=('宋体', 10),relief='flat',text='下载至文件中',bg='white' )
        self.my_load_z.place(x=0,y=430,width=140, height=20)

        self.my_load_z_m=tk.Button(self.root,font=('宋体', 10),relief='flat',text='自定义下载至',bg='white' )
        self.my_load_z_m.place(x=0,y=460,width=140, height=20)


    def label_main(self):

        self.image_log=ImageTk.PhotoImage(file='media\\main_look.png')
        self.log=tk.Label(self.root,image=self.image_log,compound="center",text='')
        self.log.place(x=0,y=0,width=140,height=185)
        self.label_log=tk.Label(self.root,text='Hi音乐!',bg='white',fg='red',font=('宋体',12))
        self.label_log.place(x=0,y=185,width=140,height=20)
        self.entry_s=tk.Entry(self.root,font=('宋体', 14),fg='gray',relief='solid')
        self.entry_s.place(x=300,y=20,width=400,height=30)

        #天气获取套件
        self.image_w=ImageTk.PhotoImage(file='media\\weather_black.png')
        self.weather_pic=tk.Label(self.root,bg='white',image=self.image_w).place(x=880,y=20,width=200,height=200)

        self.weather_str=weather.get_weather()
        self.weather_text=tk.Label(self.root,bg='white',text=self.weather_str)
        self.weather_text.place(x=880,y=220,width=200,height=30)

        # 我的音乐标签

        self.my_canv = tk.Canvas(self.root, bg='white').place(x=0, y=225, width=150, height=150)

        #下载选项
        self.my_canv_l = tk.Canvas(self.root, bg='white').place(x=0, y=360, width=150, height=150)

        self.my_music_l = tk.Label(self.root, bg='white', fg='gray', font=('宋体', 12), text='下载选项', justify='left')
        self.my_music_l.place(x=-10, y=370, width=140, height=20)



        #信息展示模块
        self.hi_img=ImageTk.PhotoImage(file='media\\Hi.png')
        self.info_label=tk.Label(self.root,image=self.hi_img,bg='azure',font=('Georgia',15),fg='gray',compound='center',text='')
        self.info_label.place(x=230,y=100,width=600,height=500)

        #self.info_label = tk.Label(self.root, bg='azure').place(x=230, y=100, width=600, height=500)
        # 播放歌曲栏目

        self.my_canv_l = tk.Canvas(self.root, bg='white').place(x=850, y=300, width=200, height=300)

        self.bofang=tk.Label(self.root, bg='white', fg='black', font=('宋体', 12), text='小小展览')
        self.bofang.place(x=880,y=310,width=100,height=20)
        self.see_bofang=tk.Label(self.root,bg='azure',fg='gray', font=('宋体', 12),text='')
        self.see_bofang.place(x=860,y=340,width=170,height=230)

        #进度条使用canvas实现
        self.jindutiao=tk.Canvas(self.root, width=465, height=22, bg="gray")
        self.jindutiao.place(x=230,y=670,width=600,height=10)




        #填充模块不用管
        self.tianchongzuoxia_img=ImageTk.PhotoImage(file='media\\tianchongzuoxia.png')
        self.tianchongzuoxia=tk.Label(self.root,image=self.tianchongzuoxia_img,bg='white').place(x=0,y=510,width=180,height=250)

        self.tianchongyouxia_img=ImageTk.PhotoImage(file='media\\tiancongyouxia.png')
        self.tianchongyouxia=tk.Label(self.root,image=self.tianchongyouxia_img).place(x=850,y=610,width=200,height=130)

    def mainloop(self):
        self.root.mainloop()


if __name__=='__main__':
    def thread_it(func, *args):
        '''将函数放入线程中执行'''
        # 创建线程
        t = threading.Thread(target=func, args=args)


        # 启动线程
        t.start()




    root=Root()
    def aaa(a):
        print('223')
    root.label_main()

    root.button_main()

    root.sousuo_b.bind("<Button-1>",lambda a :aaa('2'))
    root.mainloop()