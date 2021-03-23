import math
from functools import lru_cache

from django import template

from .format_class import NumToVnStr

register = template.Library()

text_list = [" không ", " một ", " hai ", " ba ", " bốn ", " năm ", " sáu ", " bảy ", " tám ", " chín "]
num_list = ["", " nghìn", " triệu", " tỷ", " nghìn tỷ", " triệu tỷ"]


def check_money_length(money: float) -> int:
    return len(str(money))


def format_short_money(money: float) -> str:
    result = ""
    hundreds = int(money / 100)
    dozens = int((money % 100) / 10)
    basics = int(money % 10)

    if hundreds == 0 and dozens == 0 and basics == 0:
        return result

    if hundreds != 0:
        result += text_list[hundreds] + " trăm"
        if dozens == 0 and basics != 0:
            result += " linh "

    if dozens != 0 and dozens != 1:
        result += text_list[dozens] + " mươi"
        if dozens == 0 and basics != 0:
            result += " linh "

    if dozens == 1:
        result += ' mười'

    if basics == 1:
        if dozens != 0 and dozens != 1:
            result += " mốt "
        else:
            result += text_list[basics]
    elif basics == 5:
        if dozens == 0:
            result += text_list[basics]
        else:
            result += " lăm "
    else:
        if basics != 0:
            result += text_list[basics]

    return result


@lru_cache()
def format_money_vn(money: float) -> str:
    money = float(money)
    if money == 0:
        return "Không đồng"
    if money < 0:
        raise ValueError("Số tiền âm")
    if money > 8999999999999999:
        raise ValueError("Số tiền quá lớn")

    pos = [0] * 6
    pos[5] = math.floor(money / 1000000000000000)
    money = money - pos[5] * 1000000000000000

    pos[4] = math.floor(money / 1000000000000)
    money = money - pos[4] * 1000000000000

    pos[3] = math.floor(money / 1000000000)
    money = money - pos[3] * 1000000000

    pos[2] = int(money / 1000000)
    pos[1] = int((money % 1000000) / 1000)
    pos[0] = int(money % 1000)

    count = 0
    if pos[5] > 0:
        count = 5
    elif pos[4] > 0:
        count = 4
    elif pos[3] > 0:
        count = 3
    elif pos[2] > 0:
        count = 2
    elif pos[1] > 0:
        count = 1
    tmp = ''
    result = ''
    for i in range(count, 0, -1):
        tmp = str(format_short_money(pos[i]))
        result += tmp
        if pos[i] > 0:
            result += num_list[i]
        if i > 0 and len(tmp) > 0:
            result += ','
    result_length = len(result)
    if result[result_length - 1] == ',':
        result = result[0:result_length - 1]
    return result.replace('  ', ' ')


@register.filter
def text_money(money: float) -> str:
    return format_money_vn(money)


custom_converter = NumToVnStr(is_empty=True, linh='lẻ', tu='bốn', nghin='ngàn', hang_chuc=False, ty='tỉ', nam='năm')
