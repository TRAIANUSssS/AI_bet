import time


def getDate(matchDate):
    #print(matchDate)
    start = int(matchDate) // 1000
    end = int(matchDate) // 1000 - (86400 * 90)

    start = time.strftime('%Y-%m-%d', time.localtime(start))
    end = time.strftime('%Y-%m-%d', time.localtime(end))
    line = f"?startDate={end}&endDate={start}"

    # print(line)
    return line
