'''
# 找零兑换问题：递归解法改进代码
'''



def recDC(coinValueList, change, knowResults):
    minCoins = change
    if change in coinValueList:
        knowResults[change] =1
        return 1
    elif knowResults[change] > 0:
        return knowResults[change]
    else:
        for i in [c for c in coinValueList if c < change]:
            numCoins = 1 + recDC(coinValueList, change - i, knowResults)
            if numCoins < minCoins:
                minCoins = numCoins
                knowResults[change] = minCoins
    return minCoins
print([0]*64)
print(recDC([1,5,10,25],63,[0]*64))