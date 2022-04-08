import requests
import time
import json

import numpy as np
import pandas as pd


class Crawler():
    def __init__(self, pid, header) -> None:
        self.pid = pid
        self.header = header
    
    def craw(self):
        # 基本信息 url
        url_basic = 'https://aiqicha.baidu.com/compdata/navigationListAjax?pid={}'.format(self.pid)
        # 企业风险 url
        url2_risk = 'https://aiqicha.baidu.com/riskv2/riskBannerTotalajax?pid={}'.format(self.pid)

        # 爬取企业的基本信息
        r_basic = requests.get(url_basic, headers=self.header)#, params=param)
        # 爬取企业的风险信息
        r_risk = requests.get(url2_risk, headers=self.header)#, params=param)

        if r_basic.status_code==200 and r_risk.status_code==200:
            print('pid:{} 爬取基本信息成功'.format(self.pid))
            text_basic = r_basic.text
            js_basic = json.loads(text_basic)
            print('pid:{} 爬取风险信息成功'.format(self.pid))
            text_risk = r_risk.text
            js_risk = json.loads(text_risk)
            return [js_basic, js_risk]
        # else:
        #     print('pid:{} 警告，爬取失败'.format(self.pid))

def craw(pid, header):
    # 基本信息 url
    url_basic = 'https://aiqicha.baidu.com/compdata/navigationListAjax?pid={}'.format(pid)
    # 企业风险 url
    url2_risk = 'https://aiqicha.baidu.com/riskv2/riskBannerTotalajax?pid={}'.format(pid)

    # 爬取企业的基本信息
    r_basic = requests.get(url_basic, headers=header)#, params=param)
    if r_basic.status_code==200:
        print('pid:{} 爬取基本信息成功'.format(pid))
    text_basic = r_basic.text

    # 爬取企业的风险信息
    r_risk = requests.get(url2_risk, headers=header)#, params=param)
    if r_risk.status_code==200:
        print('pid:{} 爬取风险信息成功'.format(pid))
    text_risk = r_risk.text

    js_basic = json.loads(text_basic)
    js_risk = json.loads(text_risk)
    return js_basic, js_risk

def store(pid, js_basic, js_risk):
    # 存储爬取的文件
    with open("./json/pid{}_basic.pkl".format(pid), "w", encoding="utf-8") as pid_basic:
        json.dump(js_basic, pid_basic, ensure_ascii=False)
    with open("./json/pid{}_risk.pkl".format(pid), "w", encoding="utf-8") as pid_risk:
        json.dump(js_risk, pid_risk, ensure_ascii=False)
    # 读取爬取的文件
    # with open("./json/pid{}_risk.pkl".format(pid), "r", encoding="utf-8") as tf:
    #     js = json.load(tf)

if __name__ == '__main__':
    # 创建表格
    clm=['借款人', 'pid', '自身风险', '关联风险', '变更提醒', '基本信息', '重点关注', '知识产权', '企业发展',
       '经营状况', '数据解读', '新闻资讯', '爱企查图谱', '工商注册', '股东信息', '股权穿透图', '主要人员',
       '企业受益股东', '疑似实际控制人', '最终受益人', '对外投资', '控股企业', '变更记录', '企业年报', '分支机构',
       '总公司', '司法解析', '裁判文书', '失信被执行人', '经营异常', '行政处罚', '知识产权出质', '股权出质',
       '动产抵押', '清算组信息', '简易注销公告', '股权冻结', '严重违法', '税务违法', '开庭公告', '司法拍卖',
       '被执行人', '法院公告', '立案信息', '限制高消费', '终本案件', '税务非正常户', '环保处罚', '工程异常',
       '欠税公告', '债券违约', '破产重整', '土地抵押', '网站备案', '商标信息', '专利信息', '软件著作权信息',
       '作品著作权', '融资信息', '核心成员', '企业品牌项目', '竞品信息', '投资机构', '私募基金', '行政许可',
       '质量监督检查', '食品抽检结果', '抽查检查', '双随机抽检', '资质证书', '财务指标', '利润表', '资产负债表',
       '现金流量表', '微博', '微信公众号', 'APP', '公司研报', '相关研报', '相关公告', '地块公示', '土地转让',
       '购地信息', '一般纳税人', '询价评估', '招投标', '进出口信用', '客户', '供应商', '上榜榜单', '招聘信息',
       '工资待遇', '债券信息', '建筑资质', '信用评级', '企业图谱', '企业实力']
    data = pd.DataFrame(columns=clm)
    data.to_csv("data.csv")


    # pid_list = list(pd.read_excel('企查查_pid.xlsx')['pid'])
    data_a = pd.read_csv('企查查_pid.csv')

    for i in range(len(data_a)):
        borrower = data_a['借款人'][i]
        url = data_a['url'][i]
        pid = data_a['pid'][i]

        # 爬取的企业 id
        # pid = '77293893623015'
        # 自己的header
        header = {
            'cookie' : '',
            'user-agent': '',
            'referer': 'https://aiqicha.baidu.com/'
        }
        crawler = Crawler(pid=pid, header=header)  # 创建一个爬虫
        try:
            js = crawler.craw()  # 开始爬取
            js_basic, js_risk = js[0], js[1]
            store(pid, js_basic, js_risk)  # 保存爬取的json文件
        except:
            print('pid:{} 警告，爬取失败 loop'.format(pid))


        data_app = pd.DataFrame(
            [{
                '借款人': borrower,
                # 'url':url,
                'pid':pid,
                '自身风险':js_risk['data']['selfRiskTotal'],
                '关联风险':js_risk['data']['unionRiskTotal'],
                '变更提醒':js_risk['data']['changeNoticeTotal'],
                '基本信息':js_basic['data'][0]['children'],
                '重点关注':js_basic['data'][1]['children'],
                '知识产权':js_basic['data'][2]['children'],
                '企业发展':js_basic['data'][3]['children'],
                '经营状况':js_basic['data'][4]['children'],
                '数据解读':js_basic['data'][5]['children'],
                '新闻资讯':js_basic['data'][6]['children'],
                # '基本信息' 里面的数据
                '爱企查图谱': None,
                '工商注册': None,
                '股东信息': None,
                '股权穿透图': None,
                '主要人员': None,
                '企业受益股东': None,
                '疑似实际控制人': None,
                '最终受益人': None,
                '对外投资': None,
                '控股企业': None,
                '变更记录': None,
                '企业年报': None,
                '分支机构': None,
                '总公司': None,
                # 重点关注里面的信息
                '司法解析': None,
                '裁判文书': None,
                '失信被执行人': None,
                '经营异常': None,
                '行政处罚': None,
                '知识产权出质': None,
                '股权出质': None,
                '动产抵押': None,
                '清算组信息': None,
                '简易注销公告': None,
                '股权冻结': None,
                '严重违法': None,
                '税务违法': None,
                '开庭公告': None,
                '司法拍卖': None,
                '被执行人': None,
                '法院公告': None,
                '立案信息': None,
                '限制高消费': None,
                '终本案件': None,
                '税务非正常户': None,
                '环保处罚': None,
                '工程异常': None,
                '欠税公告': None,
                '债券违约': None,
                '破产重整': None,
                '土地抵押': None,
                # 知识产权里面的信息
                '网站备案': None,
                '商标信息': None,
                '专利信息': None,
                '软件著作权信息': None,
                '作品著作权': None,
                # '企业发展':js_basic['data'][3]['children'],
                '融资信息': None,
                '核心成员': None,
                '企业品牌项目': None,
                '竞品信息': None,
                '投资机构': None,
                '私募基金': None,
                # '经营状况':js_basic['data'][4]['children'],
                '行政许可': None,
                '质量监督检查': None,
                '食品抽检结果': None,
                '抽查检查': None,
                '双随机抽检': None,
                '资质证书': None,
                '财务指标': None,
                '利润表': None,
                '资产负债表': None,
                '现金流量表': None,
                '微博': None,
                '微信公众号': None,
                'APP': None,
                '公司研报': None,
                '相关研报': None,
                '相关公告': None,
                '地块公示': None,
                '土地转让': None,
                '购地信息': None,
                '一般纳税人': None,
                '询价评估': None,
                '招投标': None,
                '进出口信用': None,
                '客户': None,
                '供应商': None,
                '上榜榜单': None,
                '招聘信息': None,
                '工资待遇': None,
                '债券信息': None,
                '建筑资质': None,
                '信用评级': None,
                # '数据解读':js_basic['data'][5]['children'],
                '企业图谱': None,
                '股权穿透图': None,
                '企业实力': None,
                # '新闻资讯':js_basic['data'][6]['children']
                '新闻资讯':None
            }]
        )
        # 填充数据
        for k in range(7):
            for v in js_basic['data'][k]['children']:
                name = v['name']
                # print(name)
                data_app[name] = v['total']
        # 将新爬取的数据添加到原来的数据中
        data = pd.concat([data, data_app])
        data.to_csv('data.csv')

        time.sleep(np.random.uniform(low=1,high=2)) # 随机休息1～2秒
        # 打印进度条
        # print("\r", end="")
        # print("进度: {:.2f}% \t 当前次数:{}, 总次数:{} ".format(i/len(data)*100,i,len(data)),end="")#, "▋" * (i // 2), end="")
        # sys.stdout.flush()