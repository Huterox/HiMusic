import requests
import json
from tkinter import messagebox

# 获取音乐数据
def music_text(kw):

    # 请求头
    try:
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
            "Cookie":"_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P",
            "Referer": "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
            "csrf": "HYZQI4KPK3P",
        }
        # 参数列表
        params = {
            "key": kw,
            # 页数
            "pn": "1",
            # 音乐数
            "rn": "10",
            "httpsStatus": "1",
            "reqId": "cc337fa0-e856-11ea-8e2d-ab61b365fb50",
        }
        # 创建列表,后面下载需要
        music_list = []
        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
        res = requests.get(url = url,headers = headers,params = params,timeout=8)
        res.encoding = "utf-8"
        text = res.text
        # 转成json数据
        json_list = json.loads(text)
        # 发现data中list是存主要数据的地方
        datapack = json_list["data"]["list"]
        #print(datapack)
        # 遍历拿到所需要的数据，音乐名称，歌手，id...
        a = 0
        for i in datapack:
            # 音乐名
            music_pic=i['pic']
            music_name = i["name"]
            # 歌手
            music_singer = i["artist"]
            # 待会需要的id先拿到
            rid = i["rid"]
            # 随便试听拿到一个音乐的接口,这是的rid就用得上了
            api_music = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3" \
                        "&br=128kmp3&from=web&t=1598528574799&httpsStatus=1" \
                        "&reqId=72259df1-e85a-11ea-a367-b5a64c5660e5".format(rid)
            api_res = requests.get(url = api_music)
            # 打印发现真实的url确实在里面
            # print(api_res.text)

            music_url = json.loads(api_res.text)["url"]

            # 大功告成，试试效果
            # 把数据存到字典方便下载时查找
            music_dict = {}
            music_dict["id"] = a
            music_dict['pic']=music_pic
            music_dict["name"] = music_name
            music_dict["url"] = music_url
            music_dict["singer"] = music_singer
            music_list.append(music_dict)
            a += 1
        return music_list
    except Exception as e:
        messagebox.showinfo('tips','搜索不到请换一首歌呀')
if __name__=='__main__':
    s=''
    list=music_text('十年')
    for i in list:
        print(i)
    print(len(list))
