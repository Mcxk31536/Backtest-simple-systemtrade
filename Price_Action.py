#1
def PA_BullEngulfing(open1,close1,open0,close0):
    Ratio_redgreen = (close0 - open0) / (open1 - close1)
    if close1 < open1 and close0 > open0 and  Ratio_redgreen <= 4 and Ratio_redgreen >= 1:
        return  True
    else:
        return False

#2
def PA_BearEngulfing(open1,close1,open0,close0):
    Ratio_redgreen = ( open0 - close0 ) / (close1 - open1)
    if close1 > open1 and close0 < open0 and  Ratio_redgreen <= 4 and Ratio_redgreen >= 1 :
        return  True
    else:
        return False
#Bull
#3
def PA_Hammer(open0,high0,low0,close0):
    sticklow = (open0 - low0) / (high0 - low0)
    headhammer = (close0 - open0)/(high0 - low0)
    if sticklow >= 0.5 and headhammer < 0.5 and headhammer > 0 :
        return  True
    else:
        return False

#4
def PA_Inverse_hammer(open0,high0,low0,close0):
    stickhigh = (high0 - close0) / (high0 - low0)
    buttomhammer = (close0 - open0 ) / (high0 - low0)
    if stickhigh >= 0.5 and buttomhammer < 0.5 and buttomhammer > 0 :
        return  True
    else:
        return False

#Bear
#5
def PA_Hanging_man(open0,high0,low0,close0):
    sticklow = (close0 - low0) / (high0 - low0)
    headhammer = (open0 - close0) / (high0 - low0)
    if sticklow >= 0.5 and headhammer < 0.5 and headhammer > 0:
        return True
    else:
        return False

#6
def PA_Shooting_star(open0,high0,low0,close0):
    stickhigh = (high0 - close0) / (high0 - low0)
    buttomhammer = (open0 - close0) / (high0 - low0)
    if stickhigh >= 0.5 and buttomhammer < 0.5 and buttomhammer > 0:
        return True
    else:
        return False

#7
def PA_Evening_star(open0, close0,open1, close1,open2, close2):
    candle_2 = close2 - open2 #green
    candle_1 = close1 - open1 #green
    can1r2 = abs(candle_1/candle_2)
    candle_0 = open0 - close0 #red
    can0r2 = candle_0/candle_2
    if candle_2 > 0 and candle_1 > 0 and can1r2 <= 0.4 and can1r2 > 0 and candle_0 > 0 and can0r2 >= 0.5 and can0r2 < 4 and can0r2 > 0 :
        return True
    else:
        return False

#bull
#8
def PA_Morning_star(open0, close0,open1,close1,open2,close2):
    candle_2 = open2 - close2 #red
    candle_1 = open1 - close1 #red
    can1r2 = abs(candle_2/candle_1)
    candle_0 = close0 - open0 #green
    can0r2 = candle_0/candle_2
    if candle_2 > 0 and candle_1 > 0 and can1r2 <= 0.4 and can1r2 > 0 and candle_0 > 0 and can0r2 >= 0.5 and can0r2 < 4 and can0r2 > 0 :
        return True
    else:
        return False

# Secret All price action
def Secret_AllPA(open0, high0, low0, close0,open1, close1,open2, close2):
    Morningstar = PA_Morning_star(open0, close0,open1, close1,open2, close2)
    Hammer = PA_Hammer(open0,high0,low0,close0)
    Eveningstar = PA_Evening_star(open0, close0,open1, close1,open2, close2)
    Shootingstar = PA_Shooting_star(open0,high0,low0,close0)
    Inversehammer = PA_Inverse_hammer(open0,high0,low0,close0)
    BearEn = PA_BearEngulfing(open1,close1,open0,close0)
    BullEn= PA_BullEngulfing(open1,close1,open0,close0)
    Hangingman= PA_Hanging_man(open0,high0,low0,close0)

    if Morningstar == True or Hammer == True or Eveningstar == True or Shootingstar == True or \
        Inversehammer == True or BullEn == True or BearEn == True or Hangingman == True :
        return True

# Secret SOME price action

def Secret_SOMEPA(Morningstar= False,Hammer= False,Eveningstar= False,Shootingstar= False,Inversehammer= False,BearEn= False,BullEn= False,Hangingman= False,
                  open0 = 0, high0 = 0, low0 = 0, close0 = 0,open1 = 0, close1 = 0,open2 =0, close2 = 0 ):
    MS = Morningstar
    H = Hammer
    ES = Eveningstar
    SS = Shootingstar
    IH = Inversehammer
    Be_En = BearEn
    Bu_En = BullEn
    HM = Hangingman

    if MS == True:
        MS = PA_Morning_star(open0, close0,open1, close1,open2, close2)
        return MS
    if H == True:
        H = PA_Hammer(open0,high0,low0,close0)
        if H == True :
            return H
    if ES == True:
        ES = PA_Evening_star(open0, close0,open1, close1,open2, close2)
        if ES == True :
            return ES
    if SS == True:
        SS = PA_Shooting_star(open0,high0,low0,close0)
        if SS == True :
            return SS
    if IH == True:
        IH = PA_Inverse_hammer(open0,high0,low0,close0)
        if IH == True :
            return IH
    if Be_En == True:
        Be_En = PA_BearEngulfing(open1,close1,open0,close0)
        if Be_En == True :
            return Be_En
    if Bu_En == True:
        Bu_En = PA_BullEngulfing(open1,close1,open0,close0)
        if Bu_En == True:
            return Bu_En
    if HM == True:
        HM = PA_Hanging_man(open0,high0,low0,close0)
        if HM == True:
            return HM





