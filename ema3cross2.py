import MetaTrader5 as mt5
import pandas as pd
import plotly.graph_objects as go
import time
import Price_Action as pa

# open mt5
mt5.initialize()
login = 66637082
password = "/?65^a#425,M#$T"
server = "XMGlobal-MT5 2"
mt5.login(login,password,server)

i = ["US30Cash"]
for x in i:
        symbol = i
        symbol_info = mt5.symbol_info(x)
        print("                      ")
        print("YEAHHHHHH",x)
        # point = mt5.symbol_info(x).point
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()
            quit()
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", x)
                mt5.shutdown()
                quit()

        ##########   INPUT DATA # requesting historical data  ##########

        tf = mt5.TIMEFRAME_M5
        periods_ = 0
        _periods = 1000
        bars = mt5.copy_rates_from_pos(x, tf, periods_, _periods)
        databars = pd.DataFrame(bars)
        databars = databars[['time', 'open', 'high', 'low', 'close']]

        o = databars['open']
        h = databars['high']
        l = databars['low']
        c = databars['close']
        t = databars['time']
        databars["EMAShort"] = "NaN"
        databars["EMALong"] = "NaN"
        databars["EMALLong"] = "NaN"

        col_n_short = 5
        col_n_long = 6
        col_n_llong = 7
        # create sma long and short H1

        short = 14
        long = 28
        llong = 200

        # กำำหนดตัวแปร EMAshort
        multikonShort = (2 / (short+1))  # 2 ตัวคูณ
        smafirstshort = (sum (c[0:short]) ) / (short)  # 3 ใช้ sma ในครั้งแรกในการหา ema ตัวต่อไป
        databars.iat[short, col_n_short] = round(smafirstshort, 3)

        # calculate EMAshort *สั้น
        EM = (c[short]) * multikonShort
        AShort = smafirstshort * (1 - multikonShort)
        EMAShort = EM + AShort
        for i in range(_periods - short):
            EM = (float(c[i + short])) * multikonShort
            AShort = EMAShort * (1 - multikonShort)
            EMAShort = EM + AShort
            databars.iat[short + i, col_n_short] = round(EMAShort, 3)


        # กำำหนดตัวแปร EMALong
        multikonLong = (2 / (long + 1))  # 2 ตัวคูณ
        smafirstLong = (sum(c[0:long])) / (long)  # 3 ใช้ sma ในครั้งแรกในการหา ema ตัวต่อไป
        databars.iat[long, col_n_long] = round(smafirstLong, 3)
        # calculate EMALong *เส้นกลาง
        EM = (c[long]) * multikonLong
        ALong = smafirstLong * (1 - multikonLong)
        EMALong = EM + ALong
        for i in range(_periods - long):
            EM = (float(c[i + long])) * multikonLong
            ALong = EMALong * (1 - multikonLong)
            EMALong = EM + ALong
            databars.iat[long + i, col_n_long] = round(EMALong, 3)

        # # กำำหนดตัวแปร EMAllong *เส้นยาวสุด
        multikonLLong = (2 / (llong + 1))  # 2 ตัวคูณ
        smafirstLLong = (sum(c[0:llong])) / (llong)  # 3 ใช้ sma ในครั้งแรกในการหา ema ตัวต่อไป
        databars.iat[llong, col_n_llong] = round(smafirstLLong, 3)
        # calculate EMAllong
        EM = (c[llong]) * multikonLLong
        ALLong = smafirstLLong * (1 - multikonLLong)
        EMALLong = EM + ALLong
        for i in range(_periods - llong):
            EM = (float(c[i + llong])) * multikonLLong
            ALLong = EMALLong * (1 - multikonLLong)
            EMALLong = EM + ALLong
            databars.iat[llong + i, col_n_llong] = round(EMALLong, 3)

        ############# Graph candlestick , Graph Line EMA ###################

        A = go.Figure(data=[
            go.Candlestick(x=databars['time'], open=databars['open'], high=databars['high'], low=databars['low'],
                           close=databars['close'])])

        A.add_trace(
            go.Scatter(
                x=databars['time'],
                y=databars['EMAShort'],
                name='EMAShort'
            ))
        A.add_trace(
            go.Scatter(
                x=databars['time'],
                y=databars['EMALong'],
                name='EMALong'
            ))
        A.add_trace(
            go.Scatter(
                x=databars['time'],
                y=databars['EMALLong'],
                name='EMALLong'
            ))
        #A.show()

        ########## Success[INPUT DATA] ##########

        ########## สร้างตารางดูผลการเทรดDemo ##########
        balance = 25000
        databars["Price Action"] = "NaN"
        databars["signal"] = "NaN"
        databars["oreder price"] = "NaN"
        databars["stop loss"] = "NaN"
        databars["take profit"] = "NaN"
        databars["lot"] = "NaN"
        databars["status"] = "NaN"
        databars["WINRATE"] = "NaN"

        pd.set_option('display.max_columns',None)

        Balance = 25000   ##### กำหนดจำนวนเงิน
        for i in range(llong,_periods-3,1):
            infoCandle = databars[i:i+4]
            PA = 8 # price action
            SIG = 9 # signal
            ORP = 10 # order price
            SL  = 11 # stop loss
            TP = 12 # take profit
            LOT = 13 # lot size
            STA = 14 # status BUY/SELL/NONE
            RATE = 15 # winrate

            # define OPEN HIGH LOW CL0SE,1,2

            open0 = o[i+3]
            high0 = h[i+3]
            low0 = l[i+3]
            close0 =c[i+3]

            open1 = o[i+2]
            high1 = h[i+2]
            low1 = l[i+2]
            close1 = c[i+2]

            open2 = o[i+1]
            high2 = h[i+1]
            low2 = l[i+1]
            close2 = c[i+1]

            EMAShort = databars["EMAShort"]
            EMALong = databars["EMALong"]
            EMALLong = databars["EMALLong"]

            EMAShort0 = EMAShort[i+3]
            EMALong0 = EMALong[i+3]
            EMALLong0 = EMALLong[i+3]

            EMAShort1 = EMAShort[i+2]
            EMALong1 = EMALong[i + 2]
            EMALLong1 = EMALLong[i + 2]

            status = databars["status"]
            signal = databars["signal"]
            ord = databars["oreder price"]
            PDSL = databars["stop loss"]
            PDTP = databars["take profit"]
            WINRATE = databars["WINRATE"]
            if  signal[i+2] == "NaN":
                print(" ")
            # create condition BUY/SELL

                if EMALong0 > EMALLong0 and  EMAShort0 > EMALong0 and EMAShort1 > EMALong1 :
                    print("EMAShort > EMALong > EMALLong : pass")
                    if  EMAShort1 > EMALong1 and close0 > EMAShort0 :
                        print("close < EMAShort          :pass")

                        openpeiceB = close0 + 5
                        stoplossB = (min(low0, low1, low2)) - 5
                        range_slB = openpeiceB - stoplossB

                        ######### กำหนด Price Action ที่จะใช้และบันทึกการ Status การเทรด ########
                        if  EMAShort0 > EMAShort1 :
                            #pa.PA_BullEngulfing(open1, close1, open0, close0) == True and range_slB >= 38:
                            #str = "BullEn"
                            #databars.iat[i + 3, PA] = str
                            #print("Price Action :pass")
                            print("range", range_slB)
                            if range_slB >= 0.38:
                                databars.iat[i + 3, SIG] = "Buy"
                                databars.iat[i + 3, STA] = "OPEN"
                                databars.iat[i + 3, ORP] = openpeiceB
                                databars.iat[i + 3, SL] = stoplossB
                                takeprofit = openpeiceB + (range_slB * 2)
                                databars.iat[i + 3, TP] = takeprofit

                        #if pa.PA_Hammer(open0,high0,low0,close0) == True:
                            #str = "Hammer"
                            #databars.iat[i + 3, PA] = str
                            #print("Price Action :pass")
                            #print("range", range_slB)
                            #if range_slB >= 38:
                            #    databars.iat[i + 3, SIG] = "Buy"
                            #    databars.iat[i + 3, ORP] = openpeiceB
                            #    databars.iat[i + 3, SL] = stoplossB
                        #if pa.PA_Inverse_hammer(open0,high0,low0,close0) == True:
                            #str = "Inverse Hammer"
                            #databars.iat[i + 3, PA] = str
                            #print("Price Action :pass")
                            #print("range", range_slB)
                            #if range_slB >= 38:
                            #    databars.iat[i + 3, SIG] = "Buy"
                            #    databars.iat[i + 3, ORP] = openpeiceB
                            #    databars.iat[i + 3, SL] = stoplossB

                elif  EMALong0 <EMALLong0 and  EMAShort0 < EMALong0 and EMAShort1 > EMALong1:
                    print("EMAShort < EMALong < EMALLong : pass")
                    if  EMAShort1 < EMALong1 and close0 < EMAShort0:
                        print("close > EMAShort          :pass")
                        openpeiceS = close0 - 5
                        stoplossS = (max(high0, high1, high2)) + 5
                        range_slS = stoplossS - openpeiceS

                        ######### กำหนด Price Action ที่จะใช้และบันทึกการ Status การเทรด ########
                        if  EMAShort1 > EMALong1:
                             #   pa.PA_BearEngulfing(open1, close1, open0, close0) == True and range_slS >= 38:
                            #str = "BearEn"
                            #databars.iat[i + 3, PA] = str
                           # print("Price Action :pass")
                            print("range", range_slS)
                            if range_slS >= 0.38:
                                databars.iat[i + 3, SIG] = "Sell"
                                databars.iat[i + 3, STA] = "OPEN"
                                databars.iat[i + 3, ORP] = openpeiceS
                                databars.iat[i + 3, SL] =  stoplossS
                                takeprofit = openpeiceS - (range_slS * 2)
                                databars.iat[i + 3, TP] = takeprofit

                        #if pa.PA_Hanging_man(open0,high0,low0,close0) == True:
                        #    str = "Hanging_man"
                        #    databars.iat[i + 3, PA] = str
                        #    print("Price Action :pass")
                        #    print("range", range_slS)
                        #    if range_slS >= 38:
                        #        databars.iat[i + 3, SIG] = "Sell"
                        #        databars.iat[i + 3, ORP] = openpeiceS
                        #        databars.iat[i + 3, SL] = stoplossS
                        #if pa.PA_Shooting_star(open0,high0,low0,close0) == True:
                        #    str = "Shooting_star"
                        #    databars.iat[i + 3, PA] = str
                        #    print("Price Action :pass")
                        #    print("range", range_slS)
                        #    if range_slS >= 38:
                        #        databars.iat[i + 3, SIG] = "Sell"
                        #        databars.iat[i + 3, ORP] = openpeiceS
                        #        databars.iat[i + 3, SL] = stoplossS

            ########## Check Status    เช็ค status เพื่อปรับ SL
            elif status[i+2] == "OPEN":
                print("")
                if signal[i+2] == "Buy" :
                    databars.iat[i+3,STA] = "OPEN"
                    databars.iat[i + 3, SIG] = "Buy"
                    databars.iat[i + 3,SL] = PDSL[i+2]
                    databars.iat[i + 3, ORP] = ord[i + 2]
                    databars.iat[i+3,TP] = PDTP[i+2]

                    #change sl
                    range_TP = PDTP[i+3] - ord[i+3]
                    rangeFopenP =  (open0- ord[i+3])/range_TP *100
                    rangeFhighP = (high0 - ord[i + 3])/range_TP *100
                    rangeFlowP = (low0 - ord[i + 3])/range_TP *100
                    rangeFcloseP = (close0 - ord[i + 3])/range_TP *100
                    if high0 >= PDTP[i + 3] and low0 > PDSL[i + 3]:
                        databars.iat[i + 3, STA] = "CLOSE"
                        databars.iat[i + 3, RATE] = "WIN"
                    elif low0 <= PDSL[i + 3] and ord[i + 3] > PDSL[i + 3]:
                        databars.iat[i + 3, STA] = "CLOSE"
                        databars.iat[i + 3, RATE] = "LOSE"
                    if rangeFopenP > 38 or rangeFhighP > 38 or rangeFlowP > 38 or rangeFcloseP > 38:
                        databars.iat[i + 3, SL] = ord[i + 3] + 5
                    elif low0 <= PDSL[i + 3] and ord[i + 3] < PDSL[i + 3]:
                        databars.iat[i + 3, STA] = "CLOSE"
                        databars.iat[i + 3, RATE] = "win"
                elif signal[i+2] == "Sell":
                    databars.iat[i+3,STA] = "OPEN"
                    databars.iat[i + 3, SIG] = "Sell"
                    databars.iat[i + 3, SL] = PDSL[i + 2]
                    databars.iat[i + 3, ORP] = ord[i + 2]
                    databars.iat[i + 3, TP] = PDTP[i + 2]

                    range_TP = - PDTP[i + 3] + ord[i + 3]
                    rangeFopenP = (- open0 + ord[i + 3]) / range_TP *100
                    rangeFhighP = (- high0 + ord[i + 3]) / range_TP * 100
                    rangeFlowP = (- low0 + ord[i + 3]) / range_TP *100
                    rangeFcloseP = (- close0 + ord[i + 3]) / range_TP *100
                    if low0 <= PDTP[i + 3] and high0 < PDSL[i + 3]:
                        databars.iat[i + 3, STA] = "CLOSE"
                        databars.iat[i + 3, RATE] = "WIN"
                    elif high0 >= PDSL[i + 3] and ord[i + 3] < PDSL[i + 3]:
                        databars.iat[i + 3, STA] = "CLOSE"
                        databars.iat[i + 3, RATE] = "LOSE"
                    if rangeFopenP > 38 or rangeFhighP > 38 or rangeFlowP > 38 or rangeFcloseP > 38:
                        databars.iat[i + 3, SL] = ord[i + 3] - 5
                    elif high0 >= PDSL[i + 3] and ord[i + 3] > PDSL[i + 3]:
                        databars.iat[i + 3, STA] = "CLOSE"
                        databars.iat[i + 3, RATE] = "win"

            print(infoCandle)
            time.sleep(0.01)
        CountPA = databars.groupby(['Price Action']).count()
        CountPA = CountPA["signal"]
        print(CountPA)
        CountWL = databars.groupby(['WINRATE']).count()
        CountWL = CountWL["signal"]
        print(CountWL)
        STAT = CountWL









