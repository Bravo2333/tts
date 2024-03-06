from datetime import datetime


def string2int(string:str):
    if string in ['收藏','抢首评','转发','评论']:
        return 0
    if '万' in string:
        result  = float(string.split('万')[0])*10000

        return int(result)
    if '亿' in string:
        result  = float(string.split('亿')[0])*100000000

        return int(result)
    return int(string)
def is_within_three_days(target_date):
    # 获取当前日期（不包含时间部分）
    current_date = datetime.now().date()
    # 计算目标日期与当前日期的差异
    diff = target_date.date() - current_date
    # 检查差异是否在三天内（包括今天）
    return abs(diff.days) <= 2
def is_later_than_latest(latest,currentvideo):
    for i in range(len(latest)):
        if int(currentvideo[i])==int(latest[i]):
            continue
        if int(currentvideo[i])>int(latest[i]):

            return True
        else:
            return False