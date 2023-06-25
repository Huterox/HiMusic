import urllib.request
import re
import tkinter.messagebox
import tkinter



'''这段代码来自于远古时代懒得去优化了'''
def get_weather():
    try:
        html = urllib.request.urlopen(r'http://www.weather.com.cn/weather/101240201.shtml')
        urllib.request.urlcleanup()
        read = html.read().decode('utf-8')
        def get_way(path,string):
            path_way=path
            path_get=re.compile(path_way)
            ture_key=path_get.findall(string,re.M)
            return str(ture_key)
        path_html='<input type="hidden" id="hidden_title" value=".*"'
        see_html=get_way(path_html,read)
        path_see='v.*°C'
        see_weather=get_way(path_see,see_html)
        day=get_way('.*日',see_weather).strip('[\"\']')
        weather=get_way('周.*°C',see_weather).strip('[\']')
        # print(weather)
        return weather
    except Exception as e:
        tkinter.messagebox.showinfo('tips', '请检查您的网络呦')


if __name__=="__main__":
    weather=get_weather()
    print(weather)


'''进度条临时存放'''

