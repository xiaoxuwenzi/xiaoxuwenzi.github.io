# coding=utf-8
#!/usr/bin/python
import base64
import time
import json
from base.spider import Spider
import sys
sys.path.append('..')


class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "哔哩哔哩"

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "动态": "动态",
            "热门": "热门",
            "排行榜": "排行榜",
            "频道": "频道",
            "历史记录": "历史记录",
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
       # result['class'] = classes
        result['class'] = self.config['classes']
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        result = {
            'list': []
        }
        return result
    cookies = ''

    def getCookie(self):
        import requests
        import http.cookies
        # 这里加cookie
        raw_cookie_line = ""
        simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.update(simple_cookie)
        return cookie_jar

    def get_dynamic(self, pg):
        result = {}
        if int(pg) > 1:
            return result
        offset = ''
        videos = []
        for i in range(0, 10):
            url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page={0}&offset={1}'.format(
                pg, offset)
            rsp = self.fetch(url, cookies=self.getCookie())
            content = rsp.text
            jo = json.loads(content)
            if jo['code'] == 0:
                offset = jo['data']['offset']
                vodList = jo['data']['items']
                for vod in vodList:
                    if vod['type'] == 'DYNAMIC_TYPE_AV':
                        ivod = vod['modules']['module_dynamic']['major']['archive']
                        aid = str(ivod['aid']).strip()
                        title = ivod['title'].strip().replace(
                            "<em class=\"keyword\">", "").replace("</em>", "")
                        img = ivod['cover'].strip()
                        remark = str(ivod['duration_text']).strip()
                        videos.append({
                            "vod_id": aid,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark
                        })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def second_to_time(self, a):
        # 将秒数转化为 时分秒的格式
        if a < 3600:
            return time.strftime("%M:%S", time.gmtime(a))
        else:
            return time.strftime("%H:%M:%S", time.gmtime(a))

    def get_history(self, pg):
        result = {}
        url = 'http://api.bilibili.com/x/v2/history?pn=%s' % pg
        rsp = self.fetch(url, cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)  # 解析api接口,转化成json数据对象
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']
            for vod in vodList:
                if vod['duration'] > 0:  # 筛选掉非视频的历史记录
                    aid = str(vod["aid"]).strip()  # 获取 aid
                    # 获取标题
                    title = vod["title"].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("&quot;",
                                                                                                            '"')
                    # 封面图片
                    img = vod["pic"].strip()

                    # 获取已观看时间
                    if str(vod['progress']) == '-1':
                        process = str(self.second_to_time(
                            vod['duration'])).strip()
                    else:
                        process = str(self.second_to_time(
                            vod['progress'])).strip()
                    # 获取视频总时长
                    total_time = str(self.second_to_time(
                        vod['duration'])).strip()
                    # 组合 已观看时间 / 总时长 ,赋值给 remark
                    remark = process+' / '+total_time
                    videos.append({
                        "vod_id": aid,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark

                    })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_hot(self, pg):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={0}'.format(
            pg)
        rsp = self.fetch(url, cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace(
                    "<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_rank(self):
        result = {}
        url = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'
        rsp = self.fetch(url, cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace(
                    "<em class=\"keyword\">", "").replace("</em>", "")
                img = vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_channel(self, pg, cid):
        result = {}
        if int(pg) > 1:
            return result
        offset = ''
        videos = []
        for i in range(0, 5):
            url = 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id={0}&sort_type=hot&offset={1}&page_size=30'.format(
                cid, offset)
            rsp = self.fetch(url, cookies=self.getCookie())
            content = rsp.text
            print(content)
            jo = json.loads(content)
            if jo['code'] == 0:
                offset = jo['data']['offset']
                vodList = jo['data']['list']
                for vod in vodList:
                    if vod['card_type'] == 'rank':
                        rankVods = vod['items']
                        for ivod in rankVods:
                            aid = str(ivod['id']).strip()
                            title = ivod['name'].strip().replace(
                                "<em class=\"keyword\">", "").replace("</em>", "")
                            img = ivod['cover'].strip()
                            remark = str(ivod['duration']).strip()
                            videos.append({
                                "vod_id": aid,
                                "vod_name": title,
                                "vod_pic": img,
                                "vod_remarks": remark
                            })
                    elif vod['card_type'] == 'archive':
                        aid = str(vod['id']).strip()
                        title = vod['name'].strip().replace(
                            "<em class=\"keyword\">", "").replace("</em>", "")
                        img = vod['cover'].strip()
                        remark = str(vod['duration']).strip()
                        videos.append({
                            "vod_id": aid,
                            "vod_name": title,
                            "vod_pic": img,
                            "vod_remarks": remark
                        })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def categoryContent(self, tid, pg, filter, extend):
        print(tid, pg, filter, extend)
        result = {}
        if tid == "热门":
            return self.get_hot(pg=pg)
        if tid == "排行榜":
            return self.get_rank()
        if tid == '动态':
            return self.get_dynamic(pg=pg)
        if tid == '历史记录':
            return self.get_history(pg=pg)
        if tid == '频道':
            cid = '9222'
            if 'cid' in extend:
                cid = extend['cid']
            return self.get_channel(pg=pg, cid=cid)
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}'.format(
            tid, pg)
        if len(self.cookies) <= 0:
            self.getCookie()
        rsp = self.fetch(url, cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:
            rspRetry = self.fetch(url, cookies=self.getCookie())
            content = rspRetry.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['aid']).strip()
            title = tid + ":" + \
                vod['title'].strip().replace(
                    "<em class=\"keyword\">", "").replace("</em>", "")
            img = 'https:' + vod['pic'].strip()
            remark = str(vod['duration']).strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    def detailContent(self, array):
        aid = array[0]
        url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(
            aid)

        rsp = self.fetch(url, headers=self.header, cookies=self.getCookie())
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        title = jo['title'].replace(
            "<em class=\"keyword\">", "").replace("</em>", "")
        pic = jo['pic']
        desc = jo['desc']
        typeName = jo['tname']
        vod = {
            "vod_id": aid,
            "vod_name": title,
            "vod_pic": pic,
            "type_name": typeName,
            "vod_year": "",
            "vod_area": "bilidanmu",
            "vod_remarks": "",
            "vod_actor": jo['owner']['name'],
            "vod_director": jo['owner']['name'],
            "vod_content": desc
        }
        ja = jo['pages']
        playUrl = ''
        for tmpJo in ja:
            cid = tmpJo['cid']
            part = tmpJo['part']
            playUrl = playUrl + '{0}${1}_{2}#'.format(part, aid, cid)

        vod['vod_play_from'] = 'B站'
        vod['vod_play_url'] = playUrl

        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        search = self.categoryContent(tid=key, pg=1, filter=None, extend=None)
        result = {
            'list': search['list']
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        # https://www.555dianying.cc/vodplay/static/js/playerconfig.js
        result = {}

        ids = id.split("_")
        url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(
            ids[0], ids[1])
        rsp = self.fetch(url, cookies=self.getCookie())
        jRoot = json.loads(rsp.text)
        jo = jRoot['data']
        ja = jo['durl']

        maxSize = -1
        position = -1
        for i in range(len(ja)):
            tmpJo = ja[i]
            if maxSize < int(tmpJo['size']):
                maxSize = int(tmpJo['size'])
                position = i

        url = ''
        if len(ja) > 0:
            if position == -1:
                position = 0
            url = ja[position]['url']

        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        result["contentType"] = 'video/x-flv'
        return result

    config = {

        "classes": [

            {
                "type_name": "动态",
                "type_id": "动态"
            },
            {
                "type_name": "热门",
                "type_id": "热门"
            },
            {
                "type_name": "排行榜",
                "type_id": "排行榜"
            },
            {
                "type_name": "频道",
                "type_id": "频道"
            },
            {
                "type_name": "历史记录",
                "type_id": "历史记录"
            },
            {
                "type_name": "美食",
                "type_id": "美食超清"
            },
            {
                "type_name": "食谱",
                "type_id": "食谱"
            },
            {
                "type_name": "体育",
                "type_id": "体育超清"
            },
            {
                "type_name": "球星",
                "type_id": "球星"
            },
            {
                "type_name": "旅游",
                "type_id": "旅游"
            },
            {
                "type_name": "风景",
                "type_id": "风景4K"
            },
            {
                "type_name": "说案",
                "type_id": "说案"
            },
            {
                "type_name": "知名UP主",
                "type_id": "知名UP主"
            },
            {
                "type_name": "探索发现",
                "type_id": "探索发现超清"
            },
            {
                "type_name": "纪录片",
                "type_id": "纪录片超清"
            },
            {
                "type_name": "鬼畜",
                "type_id": "鬼畜"
            },
            {
                "type_name": "搞笑",
                "type_id": "搞笑"
            },
            {
                "type_name": "儿童",
                "type_id": "儿童"
            },
            {
                "type_name": "动物世界",
                "type_id": "动物世界"
            },
            {
                "type_name": "相声小品",
                "type_id": "相声小品超清"
            },
            {
                "type_name": "戏曲",
                "type_id": "戏曲"
            },
            {
                "type_name": "解说",
                "type_id": "解说"
            },

            {
                "type_name": "演讲",
                "type_id": "演讲"
            },
            {
                "type_name": "小姐姐",
                "type_id": "小姐姐超清"
            },
            {
                "type_name": "荒野求生",
                "type_id": "荒野求生超清"
            },
            {
                "type_name": "健身",
                "type_id": "健身"
            },
            {
                "type_name": "帕梅拉",
                "type_id": "帕梅拉"
            },
            {
                "type_name": "太极拳",
                "type_id": "太极拳"
            },

            {
                "type_name": "广场舞",
                "type_id": "广场舞"
            },
            {
                "type_name": "舞蹈",
                "type_id": "舞蹈"
            },
            {
                "type_name": "音乐",
                "type_id": "音乐"
            },
            {
                "type_name": "歌曲",
                "type_id": "歌曲"
            },
            {
                "type_name": "MV",
                "type_id": "MV4K"
            },
            {
                "type_name": "舞曲",
                "type_id": "舞曲超清"
            },
            {
                "type_name": "4K",
                "type_id": "4K"
            },
            {
                "type_name": "电影",
                "type_id": "电影"
            },
            {
                "type_name": "电视剧",
                "type_id": "电视剧"
            },
            {
                "type_name": "白噪音",
                "type_id": "白噪音超清"
            },
            {
                "type_name": "考公考证",
                "type_id": "考公考证"
            },

            {
                "type_name": "平面设计教学",
                "type_id": "平面设计教学"
            },
            {
                "type_name": "软件教程",
                "type_id": "软件教程"
            },
            {
                "type_name": "Windows",
                "type_id": "Windows"
            }

        ],


        "filter": {
            "考公考证": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "探索发现超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "电影": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "鬼畜": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "说案": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "说案"
                    },
                        {
                        "n": "汤圆",
                        "v": "汤圆说案"
                    },
                        {
                        "n": "唐唐",
                        "v": "唐唐说案"
                    },
                        {
                        "n": "罗翔",
                        "v": "罗翔说刑法"
                    },
                        {
                        "n": "何家弘",
                        "v": "何家弘说案"
                    },
                        {
                        "n": "韩诺",
                        "v": "韩诺说案"
                    },
                        {
                        "n": "老V",
                        "v": "老V说案"
                    },
                        {
                        "n": "禁播档案‼️",
                        "v": "禁播档案"
                    }
                    ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "演讲": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "全部演讲4K"
                    },
                        {
                        "n": "A艾跃进",
                        "v": "艾跃进演讲4K"
                    },
                        {
                        "n": "C超级演说家",
                        "v": "超级演说家4K"
                    },
                        {
                        "n": "D电影",
                        "v": "电影演讲4K"
                    },
                        {
                        "n": "D典籍里的中国",
                        "v": "典籍里的中国4K"
                    },
                        {
                        "n": "G感动中国",
                        "v": "感动中国4K"
                    },
                        {
                        "n": "G郭继承",
                        "v": "郭继承演讲4K"
                    },
                        {
                        "n": "H华春莹",
                        "v": "华春莹演讲4K"
                    },
                        {
                        "n": "L雷军",
                        "v": "雷军演讲4K"
                    },
                        {
                        "n": "L罗翔",
                        "v": "罗翔演讲4K"
                    },
                        {
                        "n": "R任正非",
                        "v": "任正非演讲4K"
                    },
                        {
                        "n": "TED",
                        "v": "TED演讲4K"
                    },
                        {
                        "n": "W汪文斌",
                        "v": "汪文斌演讲4K"
                    },
                        {
                        "n": "Y一刻",
                        "v": "一刻演讲4K"
                    },
                        {
                        "n": "Z赵立坚",
                        "v": "赵立坚演讲4K"
                    },
                        {
                        "n": "Z郑强",
                        "v": "郑强演讲4K"
                    }
                    ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "解说": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "解说"
                    },
                        {
                        "n": "电影",
                        "v": "电影解说"
                    },
                        {
                        "n": "电视",
                        "v": "电视解说"
                    },
                        {
                        "n": "历史",
                        "v": "历史解说"
                    },
                        {
                        "n": "动漫",
                        "v": "动漫解说"
                    },
                        {
                        "n": "小说",
                        "v": "小说解说"
                    }
                    ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "风景4K": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "风景4K"
                    },
                        {
                        "n": "A澳门",
                        "v": "澳门风景4K"
                    },
                        {
                        "n": "A安徽",
                        "v": "安徽风景4K"
                    },
                        {
                        "n": "B布达拉宫",
                        "v": "布达拉宫风景4K"
                    },
                        {
                        "n": "B北京",
                        "v": "北京风景4K"
                    },
                        {
                        "n": "C重庆",
                        "v": "重庆风景4K"
                    },
                        {
                        "n": "C草原",
                        "v": "草原风景4K"
                    },
                        {
                        "n": "D大海",
                        "v": "大海风景4K"
                    },
                        {
                        "n": "F福建",
                        "v": "福建风景4K"
                    },
                        {
                        "n": "G广东",
                        "v": "广东风景4K"
                    },
                        {
                        "n": "G广西",
                        "v": "广西风景4K"
                    },
                        {
                        "n": "G贵州",
                        "v": "贵州风景4K"
                    },
                        {
                        "n": "G甘肃",
                        "v": "甘肃风景4K"
                    },
                        {
                        "n": "H海南",
                        "v": "海南风景4K"
                    },
                        {
                        "n": "H河北",
                        "v": "河北风景4K"
                    },
                        {
                        "n": "H河南",
                        "v": "河南风景4K"
                    },
                        {
                        "n": "H湖北",
                        "v": "湖北风景4K"
                    },
                        {
                        "n": "H湖南",
                        "v": "湖南风景4K"
                    },
                        {
                        "n": "H黑龙江",
                        "v": "黑龙江风景4K"
                    },
                        {
                        "n": "J吉林",
                        "v": "吉林风景4K"
                    },
                        {
                        "n": "J江苏",
                        "v": "江苏风景4K"
                    },
                        {
                        "n": "J江西",
                        "v": "江西风景4K"
                    },
                        {
                        "n": "L辽宁",
                        "v": "辽宁风景4K"
                    },
                        {
                        "n": "M民宿",
                        "v": "民宿风景4K"
                    },
                        {
                        "n": "N内蒙古",
                        "v": "内蒙古风景4K"
                    },
                        {
                        "n": "N宁夏",
                        "v": "宁夏风景4K"
                    },
                        {
                        "n": "Q青海",
                        "v": "青海风景4K"
                    },
                        {
                        "n": "S上海",
                        "v": "上海风景4K"
                    },
                        {
                        "n": "S陕西",
                        "v": "陕西风景4K"
                    },
                        {
                        "n": "S四川",
                        "v": "四川风景4K"
                    },
                        {
                        "n": "S山西",
                        "v": "山西风景4K"
                    },
                        {
                        "n": "S山东",
                        "v": "山东风景4K"
                    },
                        {
                        "n": "T天津",
                        "v": "天津风景4K"
                    },
                        {
                        "n": "T台湾",
                        "v": "台湾风景4K"
                    },
                        {
                        "n": "T天空",
                        "v": "天空风景4K"
                    },
                        {
                        "n": "X西湖",
                        "v": "西湖风景4K"
                    },
                        {
                        "n": "X西藏",
                        "v": "西藏风景4K"
                    },
                        {
                        "n": "X新疆",
                        "v": "新疆风景4K"
                    },
                        {
                        "n": "X香港",
                        "v": "香港风景4K"
                    },
                        {
                        "n": "Y云南",
                        "v": "云南风景4K"
                    },
                        {
                        "n": "Z浙江",
                        "v": "浙江风景4K"
                    }
                    ]
            },
                {
                "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "MV4K": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "MV4K"
                },
                    {
                    "n": "A阿杜",
                    "v": "阿杜MV4K"
                },
                    {
                    "n": "A阿黛尔",
                    "v": "阿黛尔MV4K"
                },
                    {
                    "n": "BBeyond",
                    "v": "BeyondMV4K"
                },
                    {
                    "n": "BBy2",
                    "v": "By2MV4K"
                },
                    {
                    "n": "BBIGBANG",
                    "v": "BIGBANGMV4K"
                },
                    {
                    "n": "B布兰妮",
                    "v": "布兰妮MV4K"
                },
                    {
                    "n": "C陈奕迅",
                    "v": "陈奕迅MV4K"
                },
                    {
                    "n": "C蔡依林",
                    "v": "蔡依林MV4K"
                },
                    {
                    "n": "C初音未来",
                    "v": "初音未来MV4K"
                },
                    {
                    "n": "C蔡健雅",
                    "v": "蔡健雅MV4K"
                },
                    {
                    "n": "C陈小春",
                    "v": "陈小春MV4K"
                },
                    {
                    "n": "C草蜢",
                    "v": "草蜢MV4K"
                },
                    {
                    "n": "C陈慧娴",
                    "v": "陈慧娴MV4K"
                },
                    {
                    "n": "C崔健",
                    "v": "崔健MV4K"
                },
                    {
                    "n": "C仓木麻衣",
                    "v": "仓木麻衣MV4K"
                },
                    {
                    "n": "D戴荃",
                    "v": "戴荃MV4K"
                },
                    {
                    "n": "D动力火车",
                    "v": "动力火车MV4K"
                },
                    {
                    "n": "D邓丽君",
                    "v": "邓丽君MV4K"
                },
                    {
                    "n": "D丁当",
                    "v": "丁当MV4K"
                },
                    {
                    "n": "D刀郎",
                    "v": "刀郎MV4K"
                },
                    {
                    "n": "D邓紫棋",
                    "v": "邓紫棋MV4K"
                },
                    {
                    "n": "D戴佩妮",
                    "v": "戴佩妮MV4K"
                },
                    {
                    "n": "D邓丽君",
                    "v": "邓丽君MV4K"
                },
                    {
                    "n": "F飞儿乐队",
                    "v": "飞儿乐队MV4K"
                },
                    {
                    "n": "F费玉清",
                    "v": "费玉清MV4K"
                },
                    {
                    "n": "F费翔",
                    "v": "费翔MV4K"
                },
                    {
                    "n": "F方大同",
                    "v": "方大同MV4K"
                },
                    {
                    "n": "F房东的猫",
                    "v": "房东的猫MV4K"
                },
                    {
                    "n": "F凤飞飞",
                    "v": "凤飞飞MV4K"
                },
                    {
                    "n": "F凤凰传奇",
                    "v": "凤凰传奇MV4K"
                },
                    {
                    "n": "G古风歌曲",
                    "v": "古风歌曲4K"
                },
                    {
                    "n": "G国乐大典",
                    "v": "国乐大典4K"
                },
                    {
                    "n": "G郭采洁",
                    "v": "郭采洁MV4K"
                },
                    {
                    "n": "G光良",
                    "v": "光良MV4K"
                },
                    {
                    "n": "G郭静",
                    "v": "郭静MV4K"
                },
                    {
                    "n": "G郭富城",
                    "v": "郭富城MV4K"
                },
                    {
                    "n": "H胡彦斌",
                    "v": "胡彦斌MV4K"
                },
                    {
                    "n": "H胡夏",
                    "v": "胡夏MV4K"
                },
                    {
                    "n": "H韩红",
                    "v": "韩红MV4K"
                },
                    {
                    "n": "H黄品源",
                    "v": "黄品源MV4K"
                },
                    {
                    "n": "H黄小琥",
                    "v": "黄小琥MV4K"
                },
                    {
                    "n": "H花儿乐队",
                    "v": "花儿乐队MV4K"
                },
                    {
                    "n": "H黄家强",
                    "v": "黄家强MV4K"
                },
                    {
                    "n": "H后街男孩",
                    "v": "后街男孩MV4K"
                },
                    {
                    "n": "J经典老歌",
                    "v": "经典老歌4K"
                },
                    {
                    "n": "J贾斯丁比伯",
                    "v": "贾斯丁比伯MV4K"
                },
                    {
                    "n": "J金池",
                    "v": "金池MV4K"
                },
                    {
                    "n": "J金志文",
                    "v": "金志文MV4K"
                },
                    {
                    "n": "J焦迈奇",
                    "v": "焦迈奇MV4K"
                },
                    {
                    "n": "K筷子兄弟",
                    "v": "筷子兄弟MV4K"
                },
                    {
                    "n": "L李玟",
                    "v": "李玟MV4K"
                },
                    {
                    "n": "L林忆莲",
                    "v": "林忆莲MV4K"
                },
                    {
                    "n": "L李克勤",
                    "v": "李克勤MV4K"
                },
                    {
                    "n": "L刘宪华",
                    "v": "刘宪华MV4K"
                },
                    {
                    "n": "L李圣杰",
                    "v": "李圣杰MV4K"
                },
                    {
                    "n": "L林宥嘉",
                    "v": "林宥嘉MV4K"
                },
                    {
                    "n": "L梁静茹",
                    "v": "梁静茹MV4K"
                },
                    {
                    "n": "L李健",
                    "v": "李健MV4K"
                },
                    {
                    "n": "L林俊杰",
                    "v": "林俊杰MV4K"
                },
                    {
                    "n": "L李玉刚",
                    "v": "李玉刚MV4K"
                },
                    {
                    "n": "L林志炫",
                    "v": "林志炫MV4K"
                },
                    {
                    "n": "L李荣浩",
                    "v": "李荣浩MV4K"
                },
                    {
                    "n": "L李宇春",
                    "v": "李宇春MV4K"
                },
                    {
                    "n": "L洛天依",
                    "v": "洛天依MV4K"
                },
                    {
                    "n": "L林子祥",
                    "v": "林子祥MV4K"
                },
                    {
                    "n": "L李宗盛",
                    "v": "李宗盛MV4K"
                },
                    {
                    "n": "L黎明",
                    "v": "黎明MV4K"
                },
                    {
                    "n": "L刘德华",
                    "v": "刘德华MV4K"
                },
                    {
                    "n": "L罗大佑",
                    "v": "罗大佑MV4K"
                },
                    {
                    "n": "L林肯公园",
                    "v": "林肯公园MV4K"
                },
                    {
                    "n": "LLadyGaga",
                    "v": "LadyGagaMV4K"
                },
                    {
                    "n": "L旅行团乐队",
                    "v": "旅行团乐队MV4K"
                },
                    {
                    "n": "M莫文蔚",
                    "v": "莫文蔚MV4K"
                },
                    {
                    "n": "M毛不易",
                    "v": "毛不易MV4K"
                },
                    {
                    "n": "M梅艳芳",
                    "v": "梅艳芳MV4K"
                },
                    {
                    "n": "M迈克尔杰克逊",
                    "v": "迈克尔杰克逊MV4K"
                },
                    {
                    "n": "N南拳妈妈",
                    "v": "南拳妈妈MV4K"
                },
                    {
                    "n": "P朴树",
                    "v": "朴树MV4K"
                },
                    {
                    "n": "Q齐秦",
                    "v": "齐秦MV4K"
                },
                    {
                    "n": "Q青鸟飞鱼",
                    "v": "青鸟飞鱼MV4K"
                },
                    {
                    "n": "R容祖儿",
                    "v": "容祖儿MV4K"
                },
                    {
                    "n": "R热歌",
                    "v": "热歌MV4K"
                },
                    {
                    "n": "R任贤齐",
                    "v": "任贤齐MV4K"
                },
                    {
                    "n": "S水木年华",
                    "v": "水木年华MV4K"
                },
                    {
                    "n": "S孙燕姿",
                    "v": "孙燕姿MV4K"
                },
                    {
                    "n": "S苏打绿",
                    "v": "苏打绿MV4K"
                },
                    {
                    "n": "SSHE",
                    "v": "SHEMV4K"
                },
                    {
                    "n": "S孙楠",
                    "v": "孙楠MV4K"
                },
                    {
                    "n": "T陶喆",
                    "v": "陶喆MV4K"
                },
                    {
                    "n": "T谭咏麟",
                    "v": "谭咏麟MV4K"
                },
                    {
                    "n": "T田馥甄",
                    "v": "田馥甄MV4K"
                },
                    {
                    "n": "T谭维维",
                    "v": "谭维维MV4K"
                },
                    {
                    "n": "T逃跑计划",
                    "v": "逃跑计划MV4K"
                },
                    {
                    "n": "T田震",
                    "v": "田震MV4K"
                },
                    {
                    "n": "T谭晶",
                    "v": "谭晶MV4K"
                },
                    {
                    "n": "T屠洪刚",
                    "v": "屠洪刚MV4K"
                },
                    {
                    "n": "T泰勒·斯威夫特",
                    "v": "泰勒·斯威夫特MV4K"
                },
                    {
                    "n": "W王力宏",
                    "v": "王力宏MV4K"
                },
                    {
                    "n": "W王杰",
                    "v": "王杰MV4K"
                },
                    {
                    "n": "W吴克群",
                    "v": "吴克群MV4K"
                },
                    {
                    "n": "W王心凌",
                    "v": "王心凌MV4K"
                },
                    {
                    "n": "W汪峰",
                    "v": "汪峰MV4K"
                },
                    {
                    "n": "W伍佰",
                    "v": "伍佰MV4K"
                },
                    {
                    "n": "W王菲",
                    "v": "王菲MV4K"
                },
                    {
                    "n": "W五月天",
                    "v": "五月天MV4K"
                },
                    {
                    "n": "W汪苏泷",
                    "v": "汪苏泷MV4K"
                },
                    {
                    "n": "X徐佳莹",
                    "v": "徐佳莹MV4K"
                },
                    {
                    "n": "X弦子",
                    "v": "弦子MV4K"
                },
                    {
                    "n": "X萧亚轩",
                    "v": "萧亚轩MV4K"
                },
                    {
                    "n": "X许巍",
                    "v": "许巍MV4K"
                },
                    {
                    "n": "X薛之谦",
                    "v": "薛之谦MV4K"
                },
                    {
                    "n": "X许嵩",
                    "v": "许嵩MV4K"
                },
                    {
                    "n": "X小虎队",
                    "v": "小虎队MV4K"
                },
                    {
                    "n": "X萧敬腾",
                    "v": "萧敬腾MV4K"
                },
                    {
                    "n": "X谢霆锋",
                    "v": "谢霆锋MV4K"
                },
                    {
                    "n": "X徐小凤",
                    "v": "徐小凤MV4K"
                },
                    {
                    "n": "X信乐队",
                    "v": "信乐队MV4K"
                },
                    {
                    "n": "Y夜愿乐队",
                    "v": "夜愿乐队MV4K"
                },
                    {
                    "n": "Y原创音乐",
                    "v": "原创音乐MV4K"
                },
                    {
                    "n": "Y羽泉",
                    "v": "羽泉MV4K"
                },
                    {
                    "n": "Y粤语",
                    "v": "粤语MV4K"
                },
                    {
                    "n": "Y郁可唯",
                    "v": "郁可唯MV4K"
                },
                    {
                    "n": "Y叶倩文",
                    "v": "叶倩文MV4K"
                },
                    {
                    "n": "Y杨坤",
                    "v": "杨坤MV4K"
                },
                    {
                    "n": "Y庾澄庆",
                    "v": "庾澄庆MV4K"
                },
                    {
                    "n": "Y尤长靖",
                    "v": "尤长靖MV4K"
                },
                    {
                    "n": "Y易烊千玺",
                    "v": "易烊千玺MV4K"
                },
                    {
                    "n": "Y袁娅维",
                    "v": "袁娅维MV4K"
                },
                    {
                    "n": "Y杨丞琳",
                    "v": "杨丞琳MV4K"
                },
                    {
                    "n": "Y杨千嬅",
                    "v": "杨千嬅MV4K"
                },
                    {
                    "n": "Y杨宗纬",
                    "v": "杨宗纬MV4K"
                },
                    {
                    "n": "Z周杰伦",
                    "v": "周杰伦MV4K"
                },
                    {
                    "n": "Z张学友",
                    "v": "张学友MV4K"
                },
                    {
                    "n": "Z张信哲",
                    "v": "张信哲MV4K"
                },
                    {
                    "n": "Z张宇",
                    "v": "张宇MV4K"
                },
                    {
                    "n": "Z周华健",
                    "v": "周华健MV4K"
                },
                    {
                    "n": "Z张韶涵",
                    "v": "张韶涵MV4K"
                },
                    {
                    "n": "Z周深",
                    "v": "周深MV4K"
                },
                    {
                    "n": "Z纵贯线",
                    "v": "纵贯线MV4K"
                },
                    {
                    "n": "Z赵雷",
                    "v": "赵雷MV4K"
                },
                    {
                    "n": "Z周传雄",
                    "v": "周传雄MV4K"
                },
                    {
                    "n": "Z张国荣",
                    "v": "张国荣MV4K"
                },
                    {
                    "n": "Z周慧敏",
                    "v": "周慧敏MV4K"
                },
                    {
                    "n": "Z张惠妹",
                    "v": "张惠妹MV4K"
                },
                    {
                    "n": "Z周笔畅",
                    "v": "周笔畅MV4K"
                },
                    {
                    "n": "Z郑中基",
                    "v": "郑中基MV4K"
                },
                    {
                    "n": "Z张艺兴",
                    "v": "张艺兴MV4K"
                },
                    {
                    "n": "Z张震岳",
                    "v": "张震岳MV4K"
                },
                    {
                    "n": "Z中国好声音",
                    "v": "中国好声音MV4K"
                },
                    {
                    "n": "Z张雨生",
                    "v": "张雨生MV4K"
                },
                    {
                    "n": "Z郑智化",
                    "v": "郑智化MV4K"
                },
                    {
                    "n": "Z卓依婷",
                    "v": "卓依婷MV4K"
                },
                    {
                    "n": "Z中岛美雪",
                    "v": "中岛美雪MV4K"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],

            "帕梅拉": [{
                    "key": "order",
                    "name": "排序",
                    "value": [{
                        "n": "综合排序",
                        "v": "0"
                    },
                        {
                        "n": "最多点击",
                        "v": "click"
                    },
                        {
                        "n": "最新发布",
                        "v": "pubdate"
                    },
                        {
                        "n": "最多弹幕",
                        "v": "dm"
                    },
                        {
                        "n": "最多收藏",
                        "v": "stow"
                    }
                    ]
                    },
                    {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "帕梅拉"
                    },
                        {
                        "n": "瘦腿",
                        "v": "帕梅拉瘦腿"
                    },
                        {
                        "n": "腹部",
                        "v": "帕梅拉腹部"
                    },
                        {
                        "n": "手臂",
                        "v": "帕梅拉手臂"
                    },
                        {
                        "n": "热身",
                        "v": "帕梅拉热身"
                    },
                        {
                        "n": "舞蹈",
                        "v": "帕梅拉舞蹈"
                    },
                        {
                        "n": "燃脂",
                        "v": "帕梅拉燃脂"
                    },
                        {
                        "n": "有氧",
                        "v": "帕梅拉有氧"
                    },
                        {
                        "n": "拉伸",
                        "v": "帕梅拉拉伸"
                    }
                    ]
                    },
                    {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
                    }
                    ],

            "知名UP主": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "知名UP主"
                },
                    {
                    "n": "菠萝赛东",
                    "v": "菠萝赛东"
                },
                    {
                    "n": "冯提莫",
                    "v": "冯提莫"
                },
                    {
                    "n": "林延秋",
                    "v": "林延秋"
                },
                    {
                    "n": "-LKs-",
                    "v": "-LKs-"
                },
                    {
                    "n": "小约翰可汗",
                    "v": "小约翰可汗"
                },
                    {
                    "n": "low馆长",
                    "v": "low馆长"
                },
                    {
                    "n": "自说自话的总裁",
                    "v": "自说自话的总裁"
                },
                    {
                    "n": "所长林超",
                    "v": "所长林超"
                },
                    {
                    "n": "世界未解之谜M",
                    "v": "世界未解之谜M"
                },
                    {
                    "n": "李永乐老师官方",
                    "v": "李永乐老师官方"
                },
                    {
                    "n": "罗兹",
                    "v": "罗兹"
                },
                    {
                    "n": "回到2049",
                    "v": "回到2049"
                },
                    {
                    "n": "二次元的中科院物理所",
                    "v": "二次元的中科院物理所"
                },
                    {
                    "n": "毕导THU",
                    "v": "毕导THU"
                },
                    {
                    "n": "罗翔讲刑法",
                    "v": "罗翔讲刑法"
                },
                    {
                    "n": "戴博士实验室",
                    "v": "戴博士实验室"
                },
                    {
                    "n": "芳斯塔芙",
                    "v": "芳斯塔芙"
                },
                    {
                    "n": "参赛者网",
                    "v": "参赛者网"
                },
                    {
                    "n": "三维地图看世界",
                    "v": "三维地图看世界"
                },
                    {
                    "n": "有机社会",
                    "v": "有机社会"
                },
                    {
                    "n": "乌鸦校尉CaptainWuya",
                    "v": "乌鸦校尉CaptainWuya"
                },
                    {
                    "n": "果壳",
                    "v": "果壳"
                },
                    {
                    "n": "严伯钧",
                    "v": "严伯钧"
                },
                    {
                    "n": "是你们的康康",
                    "v": "是你们的康康"
                },
                    {
                    "n": "老爸评测",
                    "v": "老爸评测"
                },
                    {
                    "n": "硬核的半佛仙人",
                    "v": "硬核的半佛仙人"
                },
                    {
                    "n": "盗月社食遇记",
                    "v": "盗月社食遇记"
                },
                    {
                    "n": "我是郭杰瑞",
                    "v": "我是郭杰瑞"
                },
                    {
                    "n": "无穷小亮的科普日常",
                    "v": "无穷小亮的科普日常"
                },
                    {
                    "n": "papi酱",
                    "v": "papi酱"
                },
                    {
                    "n": "老番茄",
                    "v": "老番茄"
                },
                    {
                    "n": "绵羊料理",
                    "v": "绵羊料理"
                },
                    {
                    "n": "老师好我叫何同学",
                    "v": "老师好我叫何同学"
                },
                    {
                    "n": "敬汉卿",
                    "v": "敬汉卿"
                },
                    {
                    "n": "周六野Zoey",
                    "v": "周六野Zoey"
                },
                    {
                    "n": "木鱼水心",
                    "v": "木鱼水心"
                },
                    {
                    "n": "凉风Kaze",
                    "v": "凉风Kaze"
                },
                    {
                    "n": "小潮院长",
                    "v": "小潮院长"
                },
                    {
                    "n": "中国BOY超级大猩猩",
                    "v": "中国BOY超级大猩猩"
                },
                    {
                    "n": "李子柒",
                    "v": "李子柒"
                },
                    {
                    "n": "敖厂长",
                    "v": "敖厂长"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "太极拳": [{
                    "key": "order",
                    "name": "排序",
                    "value": [{
                        "n": "综合排序",
                        "v": "0"
                    },
                        {
                        "n": "最多点击",
                        "v": "click"
                    },
                        {
                        "n": "最新发布",
                        "v": "pubdate"
                    },
                        {
                        "n": "最多弹幕",
                        "v": "dm"
                    },
                        {
                        "n": "最多收藏",
                        "v": "stow"
                    }
                    ]
                    },
                    {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "太极拳"
                    },
                        {
                        "n": "邱慧芳",
                        "v": "太极拳邱慧芳"
                    },
                        {
                        "n": "陈氏",
                        "v": "太极拳陈氏"
                    },
                        {
                        "n": "武当",
                        "v": "太极拳武当"
                    },
                        {
                        "n": "二十四式",
                        "v": "太极拳二十四式"
                    },
                        {
                        "n": "三十六式",
                        "v": "太极拳三十六式"
                    },
                        {
                        "n": "五禽戏",
                        "v": "五禽戏"
                    },
                        {
                        "n": "八段锦",
                        "v": "八段锦"
                    }
                    ]
                    },
                    {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
                    }
                    ],
            "舞蹈": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "舞蹈"
                },
                    {
                    "n": "宅舞",
                    "v": "宅舞"
                },
                    {
                    "n": "街舞",
                    "v": "街舞"
                },
                    {
                    "n": "中国舞",
                    "v": "中国舞"
                },
                    {
                    "n": "广场舞",
                    "v": "广场舞"
                },
                    {
                    "n": "交谊舞",
                    "v": "交谊舞"
                },
                    {
                    "n": "教程",
                    "v": "舞蹈教程"
                }
                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "音乐": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "音乐"
                    },
                        {
                        "n": "钢琴曲",
                        "v": "钢琴曲"
                    },
                        {
                        "n": "协奏曲",
                        "v": "协奏曲r"
                    },
                        {
                        "n": "中国古风音乐",
                        "v": "中国古风音乐"
                    },
                        {
                        "n": "背景音乐",
                        "v": "背景音乐"
                    },
                        {
                        "n": "助眠音乐r",
                        "v": "助眠音乐"
                    },
                        {
                        "n": "胎教音乐",
                        "v": "胎教音乐"
                    }
                    ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "歌曲": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "歌曲"
                    },
                        {
                        "n": "香港歌曲",
                        "v": "香港歌曲"
                    },
                        {
                        "n": "台湾歌曲",
                        "v": "台湾歌曲"
                    },
                        {
                        "n": "内地歌曲",
                        "v": "内地歌曲"
                    },
                        {
                        "n": "英文歌曲",
                        "v": "英文歌曲"
                    },
                        {
                        "n": "日文歌曲",
                        "v": "日文歌曲"
                    },
                        {
                        "n": "小语种歌曲",
                        "v": "小语种歌曲"
                    }
                    ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "平面设计教学": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "平面设计教学"
                    },
                        {
                        "n": "Adobe Photoshop",
                        "v": "Adobe Photoshop教程"
                    },
                        {
                        "n": "Adobe Illustrator",
                        "v": "Adobe Illustrator教程"
                    },
                        {
                        "n": "CorelDRAW",
                        "v": "CorelDRAW教程"
                    },
                        {
                        "n": "Adobe InDesign",
                        "v": "Adobe InDesign教程"
                    },
                        {
                        "n": "Adobe Pagermaker",
                        "v": "Adobe Pagermaker教程"
                    },
                        {
                        "n": "SAI",
                        "v": "SAI教程"
                    },
                        {
                        "n": "Adobe Bridge",
                        "v": "Adobe Bridge教程"
                    },
                        {
                        "n": "Adobe Pagermaker",
                        "v": "Adobe Pagermake教程r"
                    },
                        {
                        "n": "3D Studio Max",
                        "v": "3D Studio Max教程"
                    },
                        {
                        "n": "PR",
                        "v": "PR教程"
                    },
                        {
                        "n": "AE",
                        "v": "AE教程"
                    },
                        {
                        "n": "CINEMA 4D",
                        "v": "CINEMA 4D教程"
                    }
                    ]
            },
                {
                "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "软件教程": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "软件教程"
                },
                    {
                    "n": "MT管理器",
                    "v": "MT管理器"
                },
                    {
                    "n": "NP管理器",
                    "v": "NP管理器"
                },
                    {
                    "n": "mixplorer",
                    "v": "mixplorer"
                },
                    {
                    "n": "脱壳",
                    "v": "脱壳"
                },
                    {
                    "n": "爬虫",
                    "v": "爬虫"
                },
                    {
                    "n": "json&jar",
                    "v": "json&jar"
                },
                    {
                    "n": "网盘挂载",
                    "v": "网盘挂载"
                },
                    {
                    "n": "alist+WebDav",
                    "v": "alist+WebDav"
                },
                    {
                    "n": "TVBox修改",
                    "v": "TVBox修改教程"
                },
                    {
                    "n": "EXCEL",
                    "v": "EXCEL教程"
                },
                    {
                    "n": "Git入门到精通",
                    "v": "Git入门到精通"
                },
                    {
                    "n": "java",
                    "v": "java教程"
                },
                    {
                    "n": "phyton",
                    "v": "phyton教程"
                },
                    {
                    "n": "xml",
                    "v": "xml教程"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "Windows": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "小姐姐超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "广场舞超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "舞曲超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "白噪音超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "搞笑": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "体育超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "4K": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "足球比赛合集超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "篮球超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "动物世界超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "荒野求生超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "纪录片超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],

            "食谱": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "食谱"
                },
                    {
                    "n": "川菜食谱",
                    "v": "川菜食谱"
                },
                    {
                    "n": "豫菜食谱",
                    "v": "豫菜食谱"
                },
                    {
                    "n": "淮扬菜食谱",
                    "v": "淮扬菜食谱"
                },
                    {
                    "n": "湘菜食谱",
                    "v": "湘菜食谱"
                },
                    {
                    "n": "鲁菜食谱",
                    "v": "鲁菜食谱"
                },
                    {
                    "n": "粤菜食谱",
                    "v": "粤菜食谱"
                },
                    {
                    "n": "潮菜食谱",
                    "v": "潮菜食谱"
                },
                    {
                    "n": "浙菜食谱",
                    "v": "浙菜食谱"
                },
                    {
                    "n": "徽菜食谱",
                    "v": "徽菜食谱"
                },
                    {
                    "n": "闽菜食谱",
                    "v": "闽菜食谱"
                },
                    {
                    "n": "苏菜食谱",
                    "v": "苏菜食谱"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "健身": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "健身"
                },
                    {
                    "n": "瘦腿",
                    "v": "瘦腿"
                },
                    {
                    "n": "腹部",
                    "v": "腹部"
                },
                    {
                    "n": "手臂",
                    "v": "手臂"
                },
                    {
                    "n": "热身",
                    "v": "热身"
                },
                    {
                    "n": "帕梅拉",
                    "v": "帕梅拉"
                },
                    {
                    "n": "燃脂",
                    "v": "燃脂"
                },
                    {
                    "n": "有氧",
                    "v": "有氧"
                },
                    {
                    "n": "拉伸",
                    "v": "拉伸"
                }
                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "窗白噪音": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "美食超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "美食超清"
                },
                    {
                    "n": "舌尖上的中国",
                    "v": "舌尖上的中国超清"
                },
                    {
                    "n": "老字号",
                    "v": "老字号美食超清"
                },
                    {
                    "n": "家常菜",
                    "v": "家常菜美食超清"
                },
                    {
                    "n": "香港美食探店",
                    "v": "香港美食探店超清"
                },
                    {
                    "n": "澳门美食探店",
                    "v": "澳门美食探店超清"
                },
                    {
                    "n": "上海美食探店",
                    "v": "上海美食探店超清"
                },
                    {
                    "n": "北京美食探店",
                    "v": "北京美食探店超清"
                },
                    {
                    "n": "重庆美食探店",
                    "v": "重庆美食探店超清"
                },
                    {
                    "n": "南京美食探店",
                    "v": "南京美食探店超清"
                },
                    {
                    "n": "广州美食探店",
                    "v": "广州美食探店超清"
                },
                    {
                    "n": "杭州美食探店",
                    "v": "杭州美食探店超清"
                },
                    {
                    "n": "成都美食探店",
                    "v": "成都美食探店超清"
                },
                    {
                    "n": "苏州美食探店",
                    "v": "苏州美食探店超清"
                },
                    {
                    "n": "武汉美食探店",
                    "v": "武汉美食探店超清"
                },
                    {
                    "n": "台湾美食探店",
                    "v": "台湾美食探店超清"
                },
                    {
                    "n": "川菜",
                    "v": "川菜美食超清"
                },
                    {
                    "n": "豫菜",
                    "v": "豫菜美食超清"
                },
                    {
                    "n": "淮扬菜",
                    "v": "淮扬菜美食超清"
                },
                    {
                    "n": "湘菜",
                    "v": "湘菜美食超清"
                },
                    {
                    "n": "鲁菜",
                    "v": "鲁菜美食超清"
                },
                    {
                    "n": "粤菜",
                    "v": "粤菜美食超清"
                },
                    {
                    "n": "潮菜",
                    "v": "潮菜美食超清"
                },
                    {
                    "n": "浙菜",
                    "v": "浙菜美食超清"
                },
                    {
                    "n": "徽菜",
                    "v": "徽菜美食超清"
                },
                    {
                    "n": "闽菜",
                    "v": "闽菜美食超清"
                },
                    {
                    "n": "东北菜",
                    "v": "东北菜美食超清"
                },
                    {
                    "n": "客家菜",
                    "v": "客家菜美食超清"
                },
                    {
                    "n": "苏菜",
                    "v": "苏菜美食超清"
                },

                    {
                    "n": "火锅",
                    "v": "火锅"
                },
                    {
                    "n": "面食",
                    "v": "面食"
                },
                    {
                    "n": "炒菜",
                    "v": "炒菜"
                },
                    {
                    "n": "点心",
                    "v": "点心"
                },
                    {
                    "n": "日料",
                    "v": "日料"
                },
                    {
                    "n": "小吃",
                    "v": "小吃"
                },
                    {
                    "n": "素食",
                    "v": "素食"
                },
                    {
                    "n": "蒸菜",
                    "v": "蒸菜"
                },
                    {
                    "n": "凉菜",
                    "v": "凉菜"
                },
                    {
                    "n": "早餐",
                    "v": "早餐"
                },
                    {
                    "n": "披萨",
                    "v": "披萨"
                }, {
                    "n": "烤鱼",
                    "v": "烤鱼"
                }, {
                    "n": "海鲜",
                    "v": "海鲜美食超清"
                }, {
                    "n": "汉堡",
                    "v": "汉堡"
                }, {
                    "n": "韩国菜",
                    "v": "韩国菜"
                },
                    {
                    "n": "泰国菜",
                    "v": "泰国菜"
                }, {
                    "n": "穆斯林菜",
                    "v": "穆斯林菜"
                }, {
                    "n": "法国菜",
                    "v": "法国菜"
                }, {
                    "n": "意大利菜",
                    "v": "意大利菜"
                },
                    {
                    "n": "西班牙菜",
                    "v": "西班牙菜"
                }, {
                    "n": "土耳其菜",
                    "v": "土耳其菜系"
                }, {
                    "n": "阿拉伯菜",
                    "v": "阿拉伯菜"
                }, {
                    "n": "德国菜",
                    "v": "德国菜"
                }

                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "广场舞": [{
                    "key": "order",
                    "name": "排序",
                    "value": [{
                        "n": "综合排序",
                        "v": "0"
                    },
                        {
                        "n": "最多点击",
                        "v": "click"
                    },
                        {
                        "n": "最新发布",
                        "v": "pubdate"
                    },
                        {
                        "n": "最多弹幕",
                        "v": "dm"
                    },
                        {
                        "n": "最多收藏",
                        "v": "stow"
                    }
                    ]
                    },
                    {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
                    }
                    ],
            "球星": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                    "key": "tid",
                    "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "球星"
                },
                    {
                    "n": "梅西",
                    "v": "梅西"
                },
                    {
                    "n": "C罗",
                    "v": "C罗"
                },
                    {
                    "n": "天下足球",
                    "v": "天下足球"
                },
                    {
                    "n": "罗纳尔多",
                    "v": "罗纳尔多"
                },
                    {
                    "n": "亨利",
                    "v": "亨利"
                },
                    {
                    "n": "小罗",
                    "v": "小罗"
                },
                    {
                    "n": "齐达内",
                    "v": "齐达内"
                },
                    {
                    "n": "贝克汉姆",
                    "v": "贝克汉姆"
                },
                    {
                    "n": "内马尔",
                    "v": "内马尔"
                },
                    {
                    "n": "德布劳内",
                    "v": "德布劳内"
                },
                    {
                    "n": "欧冠",
                    "v": "欧冠"
                },
                    {
                    "n": "世界杯",
                    "v": "世界杯"
                },
                    {
                    "n": "西甲",
                    "v": "西甲"
                },
                    {
                    "n": "英超",
                    "v": "英超"
                },
                    {
                    "n": "意甲",
                    "v": "意甲"
                },
                    {
                    "n": "德甲",
                    "v": "德甲"
                },
                    {
                    "n": "国米",
                    "v": "国米"
                },
                    {
                    "n": "皇马",
                    "v": "皇马"
                },
                    {
                    "n": "巴萨",
                    "v": "巴萨"
                },
                    {
                    "n": "巴黎圣日耳曼",
                    "v": "巴黎圣日耳曼"
                },
                    {
                    "n": "曼联",
                    "v": "曼联"
                },
                    {
                    "n": "曼城",
                    "v": "曼城"
                },
                    {
                    "n": "NBA",
                    "v": "NBA"
                },
                    {
                    "n": "詹姆斯",
                    "v": "詹姆斯"
                },
                    {
                    "n": "库里",
                    "v": "库里"
                },
                    {
                    "n": "杜兰特",
                    "v": "杜兰特"
                },
                    {
                    "n": "UFC",
                    "v": "UFC"
                },
                    {
                    "n": "斯诺克",
                    "v": "斯诺克"
                },
                    {
                    "n": "网球",
                    "v": "网球"
                },
                    {
                    "n": "F1",
                    "v": "F1"
                },
                    {
                    "n": "高尔夫",
                    "v": "高尔夫"
                }
                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "电视剧": [{
                    "key": "order",
                    "name": "排序",
                    "value": [{
                        "n": "综合排序",
                        "v": "0"
                    },
                        {
                        "n": "最多点击",
                        "v": "click"
                    },
                        {
                        "n": "最新发布",
                        "v": "pubdate"
                    },
                        {
                        "n": "最多弹幕",
                        "v": "dm"
                    },
                        {
                        "n": "最多收藏",
                        "v": "stow"
                    }
                    ]
                    },
                    {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
                    }
                    ],


            "相声小品超清": [{
                "key": "order",
                "name": "排序",
                "value": [{
                        "n": "综合排序",
                        "v": "0"
                },
                    {
                    "n": "最多点击",
                        "v": "click"
                },
                    {
                    "n": "最新发布",
                        "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                        "v": "dm"
                },
                    {
                    "n": "最多收藏",
                        "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                    "name": "分类",
                    "value": [{
                        "n": "全部",
                        "v": "相声小品"
                    },
                        {
                        "n": "单口相声",
                        "v": "单口相声"
                    },
                        {
                        "n": "群口相声",
                        "v": "群口相声"
                    },
                        {
                        "n": "德云社",
                        "v": "德云社"
                    },
                        {
                        "n": "青曲社",
                        "v": "青曲社"
                    },
                        {
                        "n": "郭德纲",
                        "v": "郭德纲"
                    },
                        {
                        "n": "岳云鹏",
                        "v": "岳云鹏"
                    },
                        {
                        "n": "曹云金",
                        "v": "曹云金"
                    },
                        {
                        "n": "评书",
                        "v": "评书"
                    },
                        {
                        "n": "小曲",
                        "v": "小曲"
                    },
                        {
                        "n": "二人转",
                        "v": "二人转"
                    },
                        {
                        "n": "春晚小品",
                        "v": "春晚小品"
                    },
                        {
                        "n": "赵本山",
                        "v": "赵本山"
                    },
                        {
                        "n": "陈佩斯",
                        "v": "陈佩斯"
                    },
                        {
                        "n": "冯巩",
                        "v": "冯巩"
                    },
                        {
                        "n": "宋小宝",
                        "v": "宋小宝"
                    },
                        {
                        "n": "赵丽蓉",
                        "v": "赵丽蓉"
                    },
                        {
                        "n": "郭达",
                        "v": "郭达"
                    },
                        {
                        "n": "潘长江",
                        "v": "潘长江"
                    },
                        {
                        "n": "郭冬临",
                        "v": "郭冬临"
                    },
                        {
                        "n": "严顺开",
                        "v": "严顺开"
                    },
                        {
                        "n": "文松",
                        "v": "文松"
                    },
                        {
                        "n": "开心麻花",
                        "v": "开心麻花"
                    },
                        {
                        "n": "屌丝男士",
                        "v": "屌丝男士"
                    },
                        {
                        "n": "喜剧综艺",
                        "v": "喜剧综艺"
                    }
                    ]
            },
                {
                "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ],
            "戏曲": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                "key": "tid",
                "name": "分类",
                "value": [{
                    "n": "全部",
                    "v": "戏曲"
                },
                    {
                    "n": "京剧",
                    "v": "京剧"
                },
                    {
                    "n": "越剧",
                    "v": "越剧"
                },
                    {
                    "n": "黄梅戏",
                    "v": "黄梅戏"
                },
                    {
                    "n": "评剧",
                    "v": "评剧"
                },
                    {
                    "n": "豫剧",
                    "v": "豫剧"
                },
                    {
                    "n": "昆曲",
                    "v": "昆曲"
                },
                    {
                    "n": "高腔",
                    "v": "高腔"
                },
                    {
                    "n": "梆子腔",
                    "v": "梆子腔"
                },
                    {
                    "n": "河北梆子",
                    "v": "河北梆子"
                },
                    {
                    "n": "晋剧",
                    "v": "晋剧"
                },
                    {
                    "n": "蒲剧",
                    "v": "蒲剧"
                },
                    {
                    "n": "雁剧",
                    "v": "雁剧"
                },
                    {
                    "n": "上党梆子",
                    "v": "上党梆子"
                },
                    {
                    "n": "秦腔",
                    "v": "秦腔"
                },
                    {
                    "n": "武安平调",
                    "v": "武安平调"
                },
                    {
                    "n": "二人台",
                    "v": "二人台"
                },
                    {
                    "n": "吉剧",
                    "v": "吉剧"
                },
                    {
                    "n": "龙江剧",
                    "v": "龙江剧"
                },
                    {
                    "n": "越调",
                    "v": "越调"
                },
                    {
                    "n": "河南曲剧",
                    "v": "河南曲剧"
                },
                    {
                    "n": "山东梆子",
                    "v": "山东梆子"
                },
                    {
                    "n": "淮剧",
                    "v": "淮剧"
                },
                    {
                    "n": "沪剧",
                    "v": "沪剧"
                },
                    {
                    "n": "滑稽戏",
                    "v": "滑稽戏"
                },
                    {
                    "n": "婺剧",
                    "v": "婺剧"
                },
                    {
                    "n": "绍剧",
                    "v": "绍剧"
                },
                    {
                    "n": "徽剧",
                    "v": "徽剧"
                },
                    {
                    "n": "闽剧",
                    "v": "闽剧"
                },
                    {
                    "n": "莆仙戏",
                    "v": "莆仙戏"
                },
                    {
                    "n": "梨园戏",
                    "v": "梨园戏"
                },
                    {
                    "n": "高甲戏",
                    "v": "高甲戏"
                },
                    {
                    "n": "赣剧",
                    "v": "赣剧"
                },
                    {
                    "n": "采茶戏",
                    "v": "采茶戏"
                },
                    {
                    "n": "汉剧",
                    "v": "汉剧"
                },
                    {
                    "n": "湘剧",
                    "v": "湘剧"
                },
                    {
                    "n": "祁剧",
                    "v": "祁剧"
                },
                    {
                    "n": "湖南花鼓戏",
                    "v": "湖南花鼓戏"
                },
                    {
                    "n": "粤剧",
                    "v": "粤剧"
                },
                    {
                    "n": "潮剧",
                    "v": "潮剧"
                },
                    {
                    "n": "桂剧",
                    "v": "桂剧"
                },
                    {
                    "n": "彩调",
                    "v": "彩调"
                },
                    {
                    "n": "壮剧",
                    "v": "壮剧"
                },
                    {
                    "n": "川剧",
                    "v": "川剧"
                },
                    {
                    "n": "黔剧",
                    "v": "黔剧"
                },
                    {
                    "n": "滇剧",
                    "v": "滇剧"
                },
                    {
                    "n": "傣剧",
                    "v": "傣剧"
                },
                    {
                    "n": "藏剧",
                    "v": "藏剧"
                },
                    {
                    "n": "皮影戏",
                    "v": "皮影戏"
                }
                ]
            },
                {
                "key": "duration",
                "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],
            "旅游": [{
                "key": "order",
                "name": "排序",
                "value": [{
                    "n": "综合排序",
                    "v": "0"
                },
                    {
                    "n": "最多点击",
                    "v": "click"
                },
                    {
                    "n": "最新发布",
                    "v": "pubdate"
                },
                    {
                    "n": "最多弹幕",
                    "v": "dm"
                },
                    {
                    "n": "最多收藏",
                    "v": "stow"
                }
                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                "value": [{
                    "n": "全部",
                    "v": "0"
                },
                    {
                    "n": "60分钟以上",
                    "v": "4"
                },
                    {
                    "n": "30~60分钟",
                    "v": "3"
                },
                    {
                    "n": "10~30分钟",
                    "v": "2"
                },
                    {
                    "n": "10分钟以下",
                    "v": "1"
                }
                ]
            }
            ],

            "游泳": [{
                "key": "tid",
                "name": "分类",
                "value": [{
                        "n": "全部",
                        "v": "泳姿"
                },
                    {
                    "n": "蝶泳",
                        "v": "蝶泳"
                },
                    {
                    "n": "仰泳",
                        "v": "仰泳"
                },
                    {
                    "n": "蛙泳",
                        "v": "蛙泳"
                },
                    {
                    "n": "自由泳",
                        "v": "自由泳"
                }
                ]
            },
                {
                    "key": "duration",
                    "name": "时长",
                    "value": [{
                        "n": "全部",
                        "v": "0"
                    },
                        {
                        "n": "60分钟以上",
                        "v": "4"
                    },
                        {
                        "n": "30~60分钟",
                        "v": "3"
                    },
                        {
                        "n": "10~30分钟",
                        "v": "2"
                    },
                        {
                        "n": "10分钟以下",
                        "v": "1"
                    }
                    ]
            }
            ]
        }
    }
    header = {}

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]
