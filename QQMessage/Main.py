# encoding=utf-8
print("模块加载中，请稍后…")
import codecs
import time
import re
import matplotlib.pyplot as plt
import jieba
from collections import Counter
import warnings
import os
import easygui


warnings.filterwarnings("ignore")
# 解决matplotlib显示中文的问题
import matplotlib as mpl
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams['axes.unicode_minus'] = False

# 获取24个时间段----->periods
# 用于之后时间的分段
def get_periods():
    periods = []
    for i in range(0, 24):
        # 这里的判断用于将类似的‘8’ 转化为 ‘08’ 便于和导出数据匹配
        if i < 10:
            i = '0' + str(i)
        else:
            i = str(i)
        periods.append(i)
    return periods

# 对每一个时间段进行计数
def classification(times, period):
    num = 0
    for tim in times:
        try:
            timm = int(tim)
        except:
            tim = tim.replace(":", "")
            tim = "0" + tim
        if tim == period:
            num += 1
    period_time.append([period, num])
    # print(period, '--->', num)


# 作图

def plot_time(period_time, name):
    time = []
    num = []
    for i in period_time:
        time.append(i[0])
        num.append(i[1])
    time = time[6:24] + time[0:6]
    num = num[6:24] + num[0:6]
    # print(time,'\n',num)
    labels = time
    x = [i for i in range(0, 24)]
    plt.plot(num, 'g')
    num_max = max(num)
    plt.xticks(x, labels)
    plt.axis([00, 24, 0, num_max * (1.2)])
    plt.grid(True)
    plt.title(name)
    plt.ylabel('发言量')
    plt.xlabel('时间')
    plt.show()


def get_person_data(filename, name):
    person_data = {'date': [], 'time': [], 'word': []}
    with open(filename, encoding='utf-8') as f:
        s = f.read()
        # 正则，跨行匹配
        pa = re.compile(r'^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}|\d:\d{2}:\d{2}) ' + name  + '\n(.*?)\n$',
                        re.DOTALL + re.MULTILINE)
        ma = re.findall(pa, s)
        # print(len(ma))
        for i in range(len(ma)):
            # print(ma[i][0])
            date = ma[i][0]
            time = ma[i][1]
            word = ma[i][2]
            person_data['date'].append(date)
            person_data['time'].append(time[0:2])
            person_data['word'].append(word)
    return person_data

def fuhao(text):
    while 1 == 1:
        try:
            lists.remove(text)
        except:
            break

########################################################
script_name = "QQ聊天记录"

#s = easygui.enterbox(msg='请输入聊天记录的文件名(无后缀)', title=' ', default='', strip=True, image=None, root=None)+  '.txt'
file1=easygui.fileopenbox(default="*.txt")

filepath = file1
# 读取文件
try:
    fp = codecs.open(filepath, 'r', 'utf-8')
except:
    easygui.msgbox('文件读取异常:(')
    exit()
txt = fp.read()
fp.close()
mode = easygui.ccbox(msg='请选择读取方式', title='  ', choices=('读取指定人', '全部读取'), image=None)

if mode == 0:
    name1 = file1.strip('.txt')
    name_sp = name1.split('\\')
    name = name_sp[-1]
    name2 = '(.*?)'
else:
    name = easygui.enterbox(msg='请输入要提取人的备注', title=' ', default='', strip=True, image=None, root=None)
    name2 = name

file2= name+'Arrange.txt'
if mode != 0:
    # 整理后的记录
    log_format = ''
    # 开始整理
    contentlist = get_person_data(file1,name2)
    contentli = contentlist["word"]
    fp = codecs.open(file2, 'w', 'utf-8')
    for i in contentli:
        fp.write(i)
        fp.write("\n")
    fp.close()
else:
    re_pat = r'20[\d-]{8}\s[\d:]{7,8}\s+[^\n]+[^\n]'
    log_title_arr = re.findall(re_pat, txt)  # 记录头数组['2016-06-24 15:42:52  张某(40**21)',…]
    log_content_arr = re.split(re_pat, txt)  # 记录内容数组['\n', '\n选修的\n\n', '\n就怕这次…]
    log_content_arr.pop(0)  # 剔除掉第一个（分割造成的冗余部分）
    l1 = len(log_title_arr)
    log_format = ''
    for i in range(0, l1):
        content = log_content_arr[i].strip()  # 删记录内容首尾空白字符
        content = content.replace('\r\n', '\n')  # 记录中的'\n'，替换为'\r\n'
        content = content.replace('\n', '\r\n')
        log_format += content + '\r\n'  # 拼接合成记录
    fp = codecs.open(file2, 'w', 'utf-8')
    fp.write(log_format)
    fp.close()
###########
filepath2 = file2
fp2 = codecs.open(filepath2, 'r', 'utf-8')

lines = fp2.readlines()
fp2.close()
list_length = len(lines)
lists = []
easygui.msgbox('结…巴…正…在…分…析…')
try:
    fp = codecs.open(filepath, 'r', 'utf-8')
    for line in lines:
        seg_list = jieba.lcut(line)
        lists += seg_list
except:
    easygui.msgbox('结巴分词异常:(')
    exit()
############################
fuhaolist = ["\n",'\r\n',',','。','[',']','【','】','图片','表情','…',':','_','-','´','(',')','<','>','д','`','ノ','=',
                                                                        '你','她','他','我',' ','就','我们','在','好',
                                                     'ヽ','｀','...','？','￣','！','，','/','ㅍ','┍','┑','Д','~',
                                                                '的','了','是','啊','不','都','吧','有','要','说']
for fuh in fuhaolist:
    fuhao(fuh)


##########################

count = Counter(lists).most_common()

file3 = open('output.txt','w',encoding='UTF-8')
for x in count:
    c1 = list(x)
    lineee = ''.join(str(c1[0]))+'=>'+''.join(str(c1[1]))+'\n'
    file3.write(lineee)

###############
file3.close()
period_time = []
person_data = get_person_data(file1, name2)
times = person_data['time']

periods = get_periods()
for period in periods:
    classification(times, period)
plot_time(period_time, name)
# print(person_data['word'])
file4 = open('output.txt','r',encoding='UTF-8')
os.system('notepad output.txt')


time.sleep(10)