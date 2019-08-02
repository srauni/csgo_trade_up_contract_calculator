from math import fabs
import random
from typing import List
import multiprocessing
import time


class CollectionWeapon(object):
    def __init__(self, _collection, _quality, _weapon, _skin, _polish_low, _polish_high):
        self.collection = _collection  # 藏品集合名字
        self.quality = _quality  # 品质等级
        self.weapon = _weapon  # 武器名称
        self.skin = _skin  # 皮肤名称
        self.polish_low = _polish_low
        self.polish_high = _polish_high


# 将商品从各地数据中读入，并填充商品所有信息
class Item:
    def __init__(self):
        self.id = 0  # 商品id
        self.name = 'N/A'  # 在网易BUFF的名字
        self.buff_price = 0  # 在网易BUFF的价格
        self.sell_num = -1  # 在网易BUFF的当前在售数量
        self.steam_price = 0  # 在Steam的价格
        self.skin = 'N/A'  # 皮肤名字
        self.weapon = 'N/A'  # 武器名字
        self.collection = 'N/A'  # 藏品集合名字
        self.quality_level = 0  # 品质等级，默认0，消费级1，工业级2，军规级3，受限4，保密5，隐秘6
        self.polish_level = 0  # 磨损等级，默认0，战痕累累1，破损不堪2，久经沙场3，略有磨损4，崭新出厂5
        self.stat_trak = None  # 此物品是否暗金
        self.polish_low = -1
        self.polish_high = -1
        self.best_collection = None  # 此物是否顶级藏品（顶级藏品无法用于炼金）

        self.real_price = -1  # 真实价格，为避免重复计算而设置

    # 判断这个Item的信息有没有完全填写
    def is_completed(self) -> bool:
        if self.id == 0 or \
                self.name == 'N/A' or \
                self.buff_price == 0 or \
                self.sell_num == -1 or \
                self.steam_price == 0 or \
                self.skin == 'N/A' or \
                self.weapon == 'N/A' or \
                self.collection == 'N/A' or \
                self.quality_level == 0 or \
                self.polish_level == 0 or \
                self.stat_trak is None or \
                self.polish_low == -1 or \
                self.polish_high == -1 or \
                self.best_collection is None:
            return False
        else:
            return True


# 用于运行时打出对象的数据
def debug_print(log_string) -> None:
    if debug_print_enable:
        print(log_string)


# 垃圾python连content都没有，还要自己判断-1，可读性极差
def content(long: str, short: str) -> bool:
    if long.find(short) == -1:
        return False
    else:
        return True


debug_print_enable = True

# 从藏品数据库获取项目
file = open('武器箱与收藏品.txt', 'r')
raw = file.readlines()
file.close()
temp = []
# 将数据读入对象
collection_list = []
temp_collection_name = ''
i = 0
while i < len(raw):
    if raw[i].strip() == '#':
        i += 1
        temp_collection_name = raw[i].strip()
    else:
        quality = raw[i].strip()
        i += 1
        weapon = raw[i].strip()
        i += 1
        skin = raw[i].strip()
        i += 1
        polish_low = float(raw[i].strip())
        i += 1
        polish_high = float(raw[i].strip())
        collection_list.append(CollectionWeapon(temp_collection_name, quality, weapon, skin, polish_low, polish_high))
    i += 1
# 检查品质等级名称是否统一
for i in collection_list:
    if content(i.quality, '消费级') or \
            content(i.quality, '工业级') or \
            content(i.quality, '军规级') or \
            content(i.quality, '受限') or \
            content(i.quality, '保密') or \
            content(i.quality, '隐秘'):
        pass
    else:
        print('皮肤' + i.skin + '的品质等级不统一，其为' + i.quality)
        exit(0)
# 将武器箱的武器名字替换为BUFF名字
for i in collection_list:
    i.weapon = i.weapon.replace('Five-SeveN', 'FN57')
    i.weapon = i.weapon.replace('R8 Revolver', 'R8 左轮手枪')
    i.weapon = i.weapon.replace('Desert Eagle', '沙漠之鹰')
    i.weapon = i.weapon.replace('Galil AR', '加利尔 AR')
    i.weapon = i.weapon.replace('FAMAS', '法玛斯')
    i.weapon = i.weapon.replace('USP-S', 'USP 消音版')
    i.weapon = i.weapon.replace('Nova', '新星')
    i.weapon = i.weapon.replace('Sawed-Off', '截短霰弹枪')
    i.weapon = i.weapon.replace('CZ75-Auto', 'CZ75 自动手枪')
    i.weapon = i.weapon.replace('Dual Berettas', '双持贝瑞塔')
    i.weapon = i.weapon.replace('PP-Bizon', 'PP-野牛')
    i.weapon = i.weapon.replace('Glock-18', '格洛克 18 型')
    i.weapon = i.weapon.replace('M4A1-S', 'M4A1 消音型')
    i.weapon = i.weapon.replace('Negev', '内格夫')
# 将武器箱的皮肤名字替换为BUFF名字
for i in collection_list:
    replace_list = {
        '奈落大名': '杀意大名',
        '火卫一': '火卫—',
        '鲭鱼': '斯康里娅',
        '铁制品': '铁之作',
        '无情喧嚣': '喧嚣杀戮',
        '冷血': '冷血杀手',
        '下好离手': '买定离手',
        '再次深入': '战火重燃',
        '下不为例': '影魔',
    }
    if i.skin in replace_list.keys():
        i.skin = replace_list[i.skin]
# 从武器箱提取名字且避免重复
collection_weapon_name_list = []
for i in range(len(collection_list)):
    if i % 3 == 1:
        if collection_list[i].weapon not in collection_weapon_name_list:
            collection_weapon_name_list.append(collection_list[i].weapon.strip())
debug_print(collection_weapon_name_list)
print('收藏品武器种类共计' + str(len(collection_weapon_name_list)))

# 从csgo_items中获取所有武器项目
file = open('csgo_items.txt', 'r')
raw = file.readlines()
file.close()
csgo_item = []
num = ''
name = ''
for i in range(len(raw)):
    if i % 3 == 0:
        num = raw[i].strip()
    if i % 3 == 1:
        name = raw[i].strip()
    if i % 3 == 2:
        link = raw[i].strip()
        item = Item()
        item.id = num
        item.name = name
        csgo_item.append(item)
# 剔除非武器项目
temp = []
for i in csgo_item:
    # 连分界线都没有的肯定不是武器
    if i.name.find('|') == -1:
        continue
    # 剔除刀和纪念品
    if content(i.name, '★') or content(i.name, '（纪念品）'):
        continue
    # 剔除非武器物品
    type_temp = i.name[:i.name.find('|')].strip()
    ban_type = [
        '印花',
        '涂鸦',
        '亲笔签名胶囊',
        '封装的涂鸦',
        '音乐盒',
        '音乐盒（StatTrak™）',
        '[Deprecated]印花'
    ]
    if type_temp in ban_type:
        continue
    # 确认是武器，识别磨损
    if content(i.name, '战痕累累'):
        i.polish_level = 1
    elif content(i.name, '破损不堪'):
        i.polish_level = 2
    elif content(i.name, '久经沙场'):
        i.polish_level = 3
    elif content(i.name, '略有磨损'):
        i.polish_level = 4
    elif content(i.name, '崭新出厂'):
        i.polish_level = 5
    else:
        print('有物品无法识别磨损，id：' + str(i.id) + '，名字：' + i.name)
        exit(0)
    # 识别是否暗金
    if content(i.name, '™'):
        i.stat_trak = True
    else:
        i.stat_trak = False
    # 识别武器名字
    if i.stat_trak:
        i.weapon = i.name[:i.name.find('（')]  # 搜索到（StatTrak™）的左括号
    else:
        i.weapon = i.name[:i.name.find('|')].strip()  # 搜索到分隔线以及去除分隔线左边的空格
    # 识别皮肤名字
    i.skin = i.name[i.name.find('|') + 1:i.name.rfind(' (')].strip()  # 分隔线右边就是皮肤名，同时要去掉右边的磨损等级
    temp.append(i)
csgo_item = temp
# BUFF市场的皇帝貌似重名了，需要删除
temp = []
for i in csgo_item:
    ban_id = [
        '769485',
        '769212',
        '769134',
        '769482',
        '769473',
        '769519',
        '769426',
        '769488',
        '769487',
        # 还需要删除重名武器极地迷彩
        '34805',
        '34807',
        '34806',
        '34808',
        '34804',

    ]
    if str(i.id) not in ban_id:
        temp.append(i)
csgo_item = temp

# 修正BUFF名字
for i in csgo_item:
    if i.skin == '城里的月光' and i.weapon == 'UMP-45':
        i.skin = '月升之时'
    if i.skin == 'Emperor' and i.weapon == 'M4A4':
        i.skin = '皇帝'
# 确认武器种类数量
buff_weapon_type = []
for i in csgo_item:
    if i.weapon not in buff_weapon_type:
        buff_weapon_type.append(i.weapon)
print('网易BUFF武器种类共计' + str(len(buff_weapon_type)))
# 检查有哪些名字不一样的武器
print('正在检查名字不一样的物资')
different_name_list = []
for i in collection_weapon_name_list:
    if i not in buff_weapon_type:
        different_name_list.append(i)
debug_print(different_name_list)
print('待替换武器种类数:' + str(len(different_name_list)))
# 从价格文件中将价格提取出来
print('正在读取价格信息')
for i in csgo_item:
    try:
        file = open('../netease_buff/price/' + str(i.id) + '.txt', 'r')
        raw = file.readlines()
        file.close()
    except FileNotFoundError:
        print('id为' + str(i.id) + '的价格文件读取失败')
        i.buff_price = 'N/A'
        i.steam_price = 'N/A'
        i.sell_num = 'N/A'
        # exit(1)
    # 验证价格文件完整性
    if len(raw) % 4 != 0:
        print('id为' + str(i.id) + '的价格文件验证失败')
        exit(1)
    # 读入数据
    i.buff_price = raw[len(raw) - 4].strip()
    i.steam_price = raw[len(raw) - 3].strip()
    i.sell_num = raw[len(raw) - 2].strip()
    if i.buff_price != 'N/A':
        i.buff_price = float(i.buff_price)
    if i.steam_price != 'N/A':
        i.steam_price = float(i.steam_price)
    if i.sell_num != 'N/A':
        i.sell_num = int(i.sell_num)
# 虽然价格缺失，但是底下往上升的时候，依然需要其计算收益率，此时缺失部分应该进行估算
"""
# 过滤价格缺失的商品
print('正在过滤价格缺失的商品')
temp = []
for i in csgo_item:
    # 必须销售正常的才能用，否则肯定缺失凑不齐10个
    if i.buff_price == 'N/A':
        continue
    if i.steam_price == 'N/A':
        continue
    if i.sell_num == 'N/A':
        continue
    temp.append(i)
csgo_item = temp
print('剩余' + str(len(csgo_item)))
"""
# 从武器中删除箱子没有的皮肤
temp = []
for i in csgo_item:
    if i.skin != '咆哮' and i.skin != '诅咒':
        temp.append(i)
csgo_item = temp
# 从藏品数据库里搜索武器的品质等级以及集合名字
print('正在从藏品数据库搜索品质等级以及集合名字')
for i in csgo_item:
    for x in collection_list:
        if i.skin == x.skin and i.weapon == x.weapon:
            if x.quality == '消费级':
                i.quality_level = 1
            elif x.quality == '工业级':
                i.quality_level = 2
            elif x.quality == '军规级':
                i.quality_level = 3
            elif x.quality == '受限':
                i.quality_level = 4
            elif x.quality == '保密':
                i.quality_level = 5
            elif x.quality == '隐秘':
                i.quality_level = 6
            else:
                print('皮肤' + i.skin + '武器' + i.weapon + '名字中无法读取质量等级')
                debug_print(i.__dict__)
                exit(0)
            i.collection = x.collection
            i.polish_low = x.polish_low
            i.polish_high = x.polish_high
            break
    else:
        print('皮肤' + i.skin + '武器' + i.weapon + '无法搜索到对应的武器箱')
        debug_print(i.__dict__)
        exit(0)
max_quality = {}  # 以收藏品名字做键，以最高品质做值，搜索收藏品最高品质的数字
for i in csgo_item:
    if i.collection not in max_quality:
        max_quality[i.collection] = 0
    if i.quality_level > max_quality[i.collection]:
        max_quality[i.collection] = i.quality_level
# 填充item的beast_collection字段
for i in csgo_item:
    if max_quality[i.collection] == i.quality_level:
        i.best_collection = True
    else:
        i.best_collection = False
# 修正MAC10 渐变之色的磨损区间为0~0.08
for i in csgo_item:
    if i.weapon == 'MAC-10' and i.skin == '渐变之色':
        i.polish_low = 0
        i.polish_high = 0.08

# 极地迷彩特别烦，干脆删除办公室收藏品，反正这绝版东西贵的一P，根本不能炼金
temp = []
for i in csgo_item:
    if i.collection != '办公室收藏品':
        temp.append(i)
csgo_item = temp

# 验证数据完整性
print('正在验证数据完整性')
for i in csgo_item:
    if not i.is_completed():
        print(i.name + '数据不完整')
        print(i.__dict__)
        exit(0)

# 虽然无法炼金，但底下的还是要通过炼金升上来，以计算收益，所以还是要保留
"""
# 开始剔除无法参与炼金的物品
print('正在剔除无法参与炼金的物品')
best_quality = {}
for i in csgo_item:
    # 搜索各个藏品品质最高的皮肤
    if i.collection in best_quality:
        if i.quality_level > best_quality[i.collection]:
            best_quality[i.collection] = i.quality_level
    else:
        best_quality[i.collection] = i.quality_level
temp = []
for i in csgo_item:
    # 删除各个藏品品质最高的皮肤
    if i.quality_level == best_quality[i.collection]:
        continue
    else:
        temp.append(i)
csgo_item = temp
print('剩余' + str(len(csgo_item)))
"""


# 使用商品的steam价格以及buff价格计算出其真实steam价格（因提现困难，频繁充钱不可取，故主要使用Steam元购买）
def get_real_price(_item: Item):
    if _item.steam_price != 'N/A':
        return _item.steam_price
    if _item.steam_price == 'N/A' and _item.buff_price != 'N/A':
        return _item.buff_price * 1.7  # 一般情况下，从BUFF->Steam都会翻1.7倍，故此计算
    if _item.steam_price == 'N/A' and _item.buff_price == 'N/A':
        return -1  # 均为空的情况下，此商品无价格，以-1计


# 拿上面那个函数计算真实价格
for i in csgo_item:
    i.real_price = get_real_price(i)


# 用来获取某个数值是属于什么磨损等级
def check_polish(polish: float) -> int:
    if 0 <= polish < 0.07:
        return 5
    elif 0.07 <= polish < 0.15:
        return 4
    elif 0.15 <= polish < 0.38:
        return 3
    elif 0.38 <= polish < 0.45:
        return 2
    elif 0.45 <= polish <= 1:
        return 1
    else:
        raise Exception('磨损度超出范围，数据错误' + str(polish))


# 用来获取某个磨损等级是什么磨损区间
def get_polish_wide(polish_level: int) -> (float, float):
    if polish_level == 5:
        return 0, 0.07
    elif polish_level == 4:
        return 0.07, 0.15
    elif polish_level == 3:
        return 0.15, 0.38
    elif polish_level == 2:
        return 0.38, 0.45
    elif polish_level == 1:
        return 0.45, 1
    else:
        raise Exception('磨损区间超出范围，数据错误' + str(polish_level))


# 用来计算某个物品的某个磨损等级的百分比排位是多少磨损
def cal_polish(_item: Item, _percent: float, polish_level: int) -> float:
    # 获取该等级的磨损区间
    low, high = get_polish_wide(polish_level)
    item_low = _item.polish_low
    item_high = _item.polish_high
    # 如果该物品限定磨损区间更小，则替换为限定磨损区间
    if item_low > low:
        low = item_low
    if item_high < high:
        high = item_high
    # 计算磨损并返回
    wide = high - low
    return low + wide * (_percent / 100)


# 某个物品+平均磨损能炼出啥玩意 新皮肤磨损值=（新皮肤理论最大磨损 - 新皮肤理论最小磨损）*10把素材皮肤平均磨损 + 新皮肤理论最小磨损
def get_upper(_item: Item, polish: float) -> List[Item]:
    # 搜索与其同藏品，且品质+1的所有物品
    _upper = database[_item.stat_trak][_item.collection][_item.quality_level + 1].values()
    # 逐个搜索磨损区间并计算，再返回其应该会出货的商品
    res: List[Item] = []
    for up in _upper:  # upper是列表，储存一个品质的所有物品集合，up就是某个特定物品，其储存该物品所有磨损
        # 获取新枪物品磨损区间
        low = list(up.values())[0].polish_low
        high = list(up.values())[0].polish_high
        new_polish = (high - low) * polish + low  # 计算新枪磨损
        new_polish_level = check_polish(new_polish)  # 获得新枪的磨损等级
        res.append(up[new_polish_level])  # 返回该物品特定磨损等级的物品
    return res


# 按照藏品->品质->物品(weapon+skin)->磨损 的方式建立字典索引
database = {}
for i in csgo_item:
    # 建立对暗金的索引
    if i.stat_trak not in database:
        database[i.stat_trak] = {}
    # 建立对藏品的索引
    if i.collection not in database[i.stat_trak]:
        database[i.stat_trak][i.collection] = {}
    # 建立对品质的索引
    if i.quality_level not in database[i.stat_trak][i.collection]:
        database[i.stat_trak][i.collection][i.quality_level] = {}
    # 建立对物品的索引
    if i.weapon + i.skin not in database[i.stat_trak][i.collection][i.quality_level]:
        database[i.stat_trak][i.collection][i.quality_level][i.weapon + i.skin] = {}
    # 建立对磨损的索引
    if i.polish_level not in database[i.stat_trak][i.collection][i.quality_level][i.weapon + i.skin]:
        database[i.stat_trak][i.collection][i.quality_level][i.weapon + i.skin][i.polish_level] = i

# 随缘炼金大乱炖法
not_best_collection_list = [i for i in csgo_item if i.best_collection is False]  # 过滤掉顶级物品的名单
# 按照品质分类好的物品（非暗金）
quality_classify = {1: [i for i in not_best_collection_list if i.quality_level == 1 and not i.stat_trak],
                    2: [i for i in not_best_collection_list if i.quality_level == 2 and not i.stat_trak],
                    3: [i for i in not_best_collection_list if i.quality_level == 3 and not i.stat_trak],
                    4: [i for i in not_best_collection_list if i.quality_level == 4 and not i.stat_trak],
                    5: [i for i in not_best_collection_list if i.quality_level == 5 and not i.stat_trak]}
# 按照品质分类好的物品（暗金）
quality_classify_trak = {1: [i for i in not_best_collection_list if i.quality_level == 1 and i.stat_trak],
                         2: [i for i in not_best_collection_list if i.quality_level == 2 and i.stat_trak],
                         3: [i for i in not_best_collection_list if i.quality_level == 3 and i.stat_trak],
                         4: [i for i in not_best_collection_list if i.quality_level == 4 and i.stat_trak],
                         5: [i for i in not_best_collection_list if i.quality_level == 5 and i.stat_trak]}


# 返回实际收益
def real_receive(buy_list, upper):
    # 计算炼金收益
    spend = cal_value(buy_list)
    receive = cal_value(upper)
    receive *= 0.85
    receive /= len(upper)
    return receive - spend


# 计算一批货的价值
def cal_value(items):
    res = 0
    for _i in items:
        res += get_real_price(_i)
    return res


# 按比例混合两件商品
def mix_item(item1, item2, percent):
    res = []
    for _i in range(percent):
        res.append(item1)
    for _i in range(10 - percent):
        res.append(item2)
    if len(res) != 10:
        print('混合器有误，混合总数不为10')
        exit(1)
    return res


# 计算一个配方能收多少钱
def cal_method(buy_list, percent) -> float:
    if len(buy_list) != 10:
        print('放入的配方不够10个！')
        exit(1)
    avg_polish = 0  # 计算平均磨损
    for _i in buy_list:
        avg_polish += cal_polish(_i, percent, _i.polish_level)
        # print('cal_polish' + str(cal_polish(i, percent, i.polish_level)))
    avg_polish /= 10
    # 开始计算炼金结果啦
    upper = []  # 储存能炼出来的东西
    for _i in buy_list:
        upper += get_upper(_i, avg_polish)
    # 如果炼出来的东西，在BUFF在售小于10，则取消重炼
    flag = False
    for _i in upper:
        if _i.sell_num <= 10:
            flag = True
            break
    if flag:
        return -1
    money = real_receive(buy_list, upper)
    return money


def print_method(buy_list, money, percent):
    if money > 1 and cal_value(buy_list) < 1000:
        avg_polish = 0  # 计算平均磨损
        for _i in buy_list:
            avg_polish += cal_polish(_i, percent, _i.polish_level)
            # print('cal_polish' + str(cal_polish(i, percent, i.polish_level)))
        avg_polish /= 10
        # 开始计算炼金结果啦
        upper = []  # 储存能炼出来的东西
        for _i in buy_list:
            upper += get_upper(_i, avg_polish)
        print('-----------------------------------------------')
        print('收益：' + str(money) + '成本：' + str(cal_value(buy_list)))
        # 将配方简化
        _temp = {}
        for _i in buy_list:
            if _i.name not in _temp:
                _temp[_i.name] = 1
            else:
                _temp[_i.name] += 1
        print('配方：' + str(_temp))
        _temp = {}
        for _i in buy_list:
            if _i.name not in _temp:
                _temp[_i.name] = cal_polish(_i, percent, _i.polish_level)
        print('配方磨损：' + str(_temp))
        _temp = {}
        for _i in buy_list:
            if _i.name not in _temp:
                _temp[_i.name] = _i.real_price
        print('配方价格：' + str(_temp))
        # 输出成品数量以及价格
        _temp = {}
        for _i in upper:
            if _i.name not in _temp:
                _temp[_i.name] = 1
            else:
                _temp[_i.name] += 1
        print('成品数量：' + str(_temp))
        _temp = {}
        for _i in upper:
            if _i.name not in _temp:
                _temp[_i.name] = _i.real_price
        print('成品价格：' + str(_temp))
        print('===============================================')


def worker():
    while True:
        percent = 75  # 磨损度取区间80%，便于购买
        _quality = random.randint(1, 5)  # 决定抽出的品质
        stat = random.randint(0, 1)  # 决定抽暗金
        # 随机决定要不要抽暗金
        if stat:
            can_buy_list = quality_classify_trak[_quality]
        else:
            can_buy_list = quality_classify[_quality]
        # 从名单里随便抽
        if len(can_buy_list) == 0:
            # 低品质的枪没暗金，就跳过吧
            continue
            # print('quality'+str(quality))
            # print('stat'+str(stat))

        weapon1 = can_buy_list[random.randint(0, len(can_buy_list) - 1)]  # 随机俩物品
        weapon2 = can_buy_list[random.randint(0, len(can_buy_list) - 1)]

        # 要是随机出的物品，在BUFF在售不够10个，就重新挑选
        if weapon1.sell_num <= 5 or weapon2.sell_num <= 5:
            continue

        # # 混合后塞进购买列表当中
        # buy_list = mix_item(weapon1, weapon2, 5)
        # # 计算收益
        # money = cal_method(buy_list, percent)
        # if money > 0:

        # 收入大于0，说明有戏，应当改变配方比例，寻求最大利润
        high_money = -1
        high_method = []
        for _i in range(11):
            temp_method = mix_item(weapon1, weapon2, _i)
            temp_money = cal_method(temp_method, percent)
            if temp_money > high_money:
                high_money = temp_money
                high_method = temp_method
        # 打印出最终结果
        # print(money_list)
        print_method(high_method, high_money, percent)


print('开始随机大乱炖模式')
# 创建3个进程同时刷
p1 = multiprocessing.Process(target=worker)
p2 = multiprocessing.Process(target=worker)
p3 = multiprocessing.Process(target=worker)
p1.start()
time.sleep(1)
#p2.start()
time.sleep(1)
#p3.start()


# """
# # 开始搜索单集合、单物品藏品配方
# print('开始搜索单集合藏品')
# collection_index = {}  # 按藏品建立索引
# for i in csgo_item:
#     if i.collection not in collection_index:
#         collection_index[i.collection] = []
#     collection_index[i.collection].append(i)
# # 找出适合购入的商品，其相同藏品、相同品质、相同磨损、相同暗金下，价格最低
# buy_list = []
# for col in collection_index.values():
#     for quality in range(1, 6):
#         for polish in range(1, 6):
#             for stat_trak in range(2):
#                 low_price: float = -1
#                 low_item: Item = None
#                 for i in col:
#                     if i.quality_level == quality and i.polish_level == polish and i.stat_trak == stat_trak:
#                         # 初始状态下直接放
#                         if low_price == -1:
#                             low_price = get_real_price(i)
#                             low_item = i
#                         # 非初始状态下，判断价格读取成功才放
#                         elif get_real_price(i) != -1 and get_real_price(i) < low_price:
#                             low_price = get_real_price(i)
#                             low_item = i
#                 if low_price != -1:
#                     buy_list.append(low_item)
# print([i.name for i in buy_list])
# exit(0)
# # 从适合购入的商品当中，剔除掉在他的环境下，位于顶端的物品
# max_quality = {}    # 以收藏品名字做键，以最高品质做值，搜索收藏品最高品质的数字
# for i in csgo_item:
#     if i.collection not in max_quality:
#         max_quality[i.collection] = 0
#     if i.quality_level > max_quality[i.collection]:
#         max_quality[i.collection] = i.quality_level
# temp = []
# for i in buy_list:
#     # 搜索品质与最高相同的，将其剔除
#     if i.quality_level != max_quality[i.collection]:
#         temp.append(i)
# buy_list = temp
# res = []
# # 开始遍历适合购买名单中，单买10个的利润情况
# for i in buy_list:
#     # 搜索其同一藏品下，品质+1的物品集合
#     upper_list = []
#     for x in csgo_item:
#         if x.collection == i.collection and x.quality_level == i.quality_level + 1:
#             upper_list.append(x)
#     # 去除品质+1的物品集合中，暗金情况不同的
#     temp = []
#     for x in upper_list:
#         if x.stat_trak != i.stat_trak:
#             pass
#         else:
#             temp.append(x)
#     upper_list = temp
#     # 将品质+1的物品集合按名字做整合
#     upper_name_dict = {}
#     for x in upper_list:
#         if x.skin+x.weapon not in upper_name_dict:
#             upper_name_dict[x.skin+x.weapon] = []
#         upper_name_dict[x.skin+x.weapon].append(x)
#
#     # 在品质+1的物品集合中，仅保留与购买物品相同的物品。若没有相同的，则优先保留接近的
#     temp = []
#     for x in upper_name_dict.values():
#         # 注意x是一个物品下所有磨损的集合
#         # 判断是否有-1的磨损
#         for z in x:
#             if i.polish_level - 1 == z.polish_level:
#                 temp.append(z)
#                 break
#         else:
#             # 没找到一样的，找abs与-1最小的
#             least_abs = 99
#             least_item = None
#             for z in x:
#                 if least_abs > fabs(i.polish_level - 1 - z.polish_level):
#                     least_abs = fabs(i.polish_level - 1 - z.polish_level)
#                     least_item = z
#             if least_abs == 99:
#                 print('居然没找到abs最小的，程序有问题')
#                 print(x)
#                 exit(0)
#             # 保留最接近的
#             temp.append(least_item)
#     upper_list = temp
#     # 已经有由上面的最接近算法替代
#     '''
#     # 去除品质+1的物品集合中，磨损度比购买物品还低的
#     temp = []
#     for x in upper_list:
#         if x.polish_level < i.polish_level:
#             pass
#         else:
#             temp.append(x)
#     upper_list = temp
#
#     # 只保留磨损度最低的同类物品
#     lower_polish = {}   # 储存每个皮肤+枪支磨损度最低的情况
#     for x in upper_list:
#         if x.skin+x.weapon not in lower_polish:
#             lower_polish[x.skin+x.weapon] = 99
#         if x.polish_level < lower_polish[x.skin+x.weapon]:
#             lower_polish[x.skin+x.weapon] = x.polish_level
#     temp = []
#     for x in upper_list:
#         if x.polish_level == lower_polish[x.skin+x.weapon]:
#             temp.append(x)
#     upper_list = temp
#     '''
#     # 计算利润并放入结果中
#     spend_price = get_real_price(i) * 10
#     receive_price = 0
#     for x in upper_list:
#         receive_price += get_real_price(x)
#     if len(upper_list) != 0:
#         receive_price /= len(upper_list)
#         receive_price *= 0.85
#         # 将upper的名字生成为列表
#         upper_name_list = []
#         for x in upper_list:
#             upper_name_list.append((x.name, get_real_price(x)))
#         res.append((i, receive_price - spend_price, upper_name_list, upper_list))
# res = sorted(res, key=lambda x: x[1], reverse=True)
# # 如果自身以及升级品在buff sell num <= 10, then delete it
# temp = []
# for i in res:
#     if i[0].sell_num <= 20:
#         continue
#     flag = False
#     for x in i[3]:
#         if x.sell_num <= 20:
#             flag = True
#             break
#     if flag:
#         continue
#     temp.append(i)
# res = temp
#
# file = open('res.txt', 'a')
# for i in res:
#     if get_real_price(i[0]) <= 99999999:
#
#         print(i[0].name + '  ' + str(get_real_price(i[0])) + '  ' + str(i[0].quality_level) + '  ' + str(i[1]) + '  ' + str(i[2]))
#         file.write(i[0].name + '  ' + str(get_real_price(i[0])) + '  ' + str(i[0].quality_level) + '  ' + str(i[1]) + '  ' + str(i[2]) + '\n')
# file.close()
# '''
# # 按藏品逐个遍历
# res = {}
# for col in collection_index.values():
#     # 按藏品内品质遍历
#     for quality in range(1, 4):
#         # 按品质下磨损遍历
#         for polish in range(1, 6):
#             # 找出该品质及磨损下，价格最低的物品
#             low_price: float = -1
#             low_price_item: Item = None
#             for x in col:
#                 if x.quality_level == quality and x.polish_level == polish:
#                     if low_price == -1:
#                         low_price = get_real_price(x)
#                         low_price_item = x
#                     elif get_real_price(x) < low_price:
#                         low_price = get_real_price(x)
#                         low_price_item = x
#             if low_price != -1:
#                 # 计算其+1品质下，所有物品的均价
#                 avg_price: int = 0
#                 avg_count: int = 0
#                 search_quality = low_price_item.quality_level + 1
#                 while True:
#                     for x in col:
#                         # 找到是其品质+1的
#                         if x.quality_level == low_price_item.quality_level + 1:
#
#                         if x.quality_level == low_price_item.quality_level + 1 and low_price_item.polish_level == polish:
#                             avg_price += get_real_price(x)
#                             avg_count += 1
#                     if avg_count != 0:
#                         avg_price /= avg_count
#                         # 计算其利润，并放入字典
#                         res[x] = avg_price - get_real_price(x) * 10
#                         break
#                     else:
#                         # 如果
#                         pass
# # 将字典读出，并排序
# res = sorted(res.items(), key=lambda x: x[1], reverse=True)
# for i in res:
#     print(i[0].name + '  ' + str(i[0].quality_level) + '  ' + str(i[1]))
# """
# '''
# # TODO: 大致工作就是，将价格也读进去，然后将藏品集合名字、品质等级也一起读进去，然后验证数据完整性，剔除掉没价格之类的物品
# # TODO: 然后就可以根据微信里的搜索方法，自动化搜索
# # 非跨藏品炼金搜索
#
# # 暴力遍历策略：直接多线程全速遍历所有可能性，找出最高价值配方。若耗时为指数级，则此法无效。若为平方级，则可考虑优化（包括代码及语言）
# # 略优化的便利策略：也许在一个物品中添加另一个物品可以提高价值，
# # 炼金随机搜索策略：每个品质依次搜索10把武器，进行炼金期望判断
# '''
