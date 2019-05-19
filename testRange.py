import datetime


startA = 2018
endA = 2018

startB = 2016
endB = 2018


def check_Overlap(startA, endA, startB, endB):
    if (startA==startB) or (startA>startB and startA<=endB):
        return True
    else:
        return False


print check_Overlap(startA, endA, startB, endB)




