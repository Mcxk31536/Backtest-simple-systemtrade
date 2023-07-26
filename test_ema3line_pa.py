import MetaTrader5 as mt5
import pandas as pd
import plotly.graph_objects as go
import time
import Price_Action as pa

# open mt5
mt5.initialize()

i = ["US30Cash"]
for x in i:
        symbol = i
        symbol_info = mt5.symbol_info(x)
        print("                      ")
        print("YEAHHHHHH",x)
        point = mt5.symbol_info(x).point
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

        ##########   INPUT DATA FROM MT5   ##########

        tf = mt5.TIMEFRAME_M15
        periods_ = 0
        _periods = 1000  #จำนวน candlestick ย้อนหลังนับจากแท่งล่าสุด
        bars = mt5.copy_rates_from_pos(x, tf, periods_, _periods)
        databars = pd.DataFrame(bars)
        databars = databars[['time', 'open', 'high', 'low', 'close']]

        o = databars['open']
        h = databars['high']
        l = databars['low']
        c = databars['close']
        t = databars['time']
        #column for EMA
        databars["EMAShort"] = "NaN"
        databars["EMALong"] = "NaN"
        databars["EMALLong"] = "NaN"
        # index of column
        col_n_short = 5
        col_n_long = 6
        col_n_llong = 7

        short = 14  #EMA สั้น
        long = 60 #EMA กลาง
        llong = 200 #EMA ยาว

        # กำำหนดตัวแปร(จด)
        multikonShort = (2 / (short + 1))  # 2 ตัวคูณ
        smafirstshort = (sum(c[0:short])) / (short)  # 3 ใช้ sma ในครั้งแรกในการหา ema ตัวต่อไป
        databars.iat[short, col_n_short] = round(smafirstshort, 3)

        # calculate EMAshort
        EM = (c[short]) * multikonShort
        AShort = smafirstshort * (1 - multikonShort)
        EMAShort = EM + AShort
        # print("EMAshort -",short,"is ", EMAShort)
        for i in range(_periods - short):
            EM = (float(c[i + short])) * multikonShort
            AShort = EMAShort * (1 - multikonShort)
            EMAShort = EM + AShort
            databars.iat[short + i, col_n_short] = round(EMAShort, 3)

        multikonLong = (2 / (long + 1))  # 2 ตัวคูณ
        smafirstLong = (sum(c[0:long])) / (long)  # 3 ใช้ sma ในครั้งแรกในการหา ema ตัวต่อไป
        databars.iat[long, col_n_long] = round(smafirstLong, 3)
        # calculate EMAshort
        EM = (c[long]) * multikonLong
        ALong = smafirstLong * (1 - multikonLong)
        EMALong = EM + ALong
        # print("EMAshort -",short,"is ", EMAShort)
        for i in range(_periods - long):
            EM = (float(c[i + long])) * multikonLong
            ALong = EMALong * (1 - multikonLong)
            EMALong = EM + ALong
            databars.iat[long + i, col_n_long] = round(EMALong, 3)

        # llong
        multikonLLong = (2 / (llong + 1))  # 2 ตัวคูณ
        smafirstLLong = (sum(c[0:llong])) / (llong)  # 3 ใช้ sma ในครั้งแรกในการหา ema ตัวต่อไป
        databars.iat[llong, col_n_llong] = round(smafirstLLong, 3)
        # calculate EMAshort
        EM = (c[llong]) * multikonLLong
        ALLong = smafirstLLong * (1 - multikonLLong)
        EMALLong = EM + ALLong
        # print("EMAshort -",short,"is ", EMAShort)
        for i in range(_periods - llong):
            EM = (float(c[i + llong])) * multikonLLong
            ALLong = EMALLong * (1 - multikonLLong)
            EMALLong = EM + ALLong
            databars.iat[llong + i, col_n_llong] = round(EMALLong, 3)

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

        ########## Demo Testing & Setting ##########
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
        #print(databars)
        Balance = 25000
        for i in range(llong,_periods-3,1):
            infoCandle = databars[i:i+4]
            PA = 8 # price action
            SIG = 9 # signal
            ORP = 10 # order price
            SL  = 11# stop loss
            TP = 12
            LOT = 13
            STA = 14
            RATE = 15
            EMAShort = databars["EMAShort"]
            EMALong = databars["EMALong"]
            EMALLong = databars["EMALLong"]
            # define OHLC0,1,2 and Price Action
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

            EMAShort0 = EMAShort[i + 3]
            EMALong0 = EMALong[i + 3]
            EMALLong0 = EMALLong[i+3]

            EMAShort1 = EMAShort[i+2]
            #print(open0)
            status = databars["status"]
            signal = databars["signal"]
            ord = databars["oreder price"]
            PDSL = databars["stop loss"]
            PDTP = databars["take profit"]
            WINRATE = databars["WINRATE"]
            if  signal[i+2] == "NaN":
                print(" ")
            # create Condition trade => BUY

                if EMAShort0 > EMALong0 > EMALLong0  :
                    print("EMAShort > EMALong > EMALLong : pass")
                    if close0 > EMAShort0 and close1 > EMAShort1:
                        print("close < EMAShort          :pass")

                        openpeiceB = close0 + 5
                        stoplossB = (min(low0, low1, low2)) - 5
                        range_slB = openpeiceB - stoplossB

                        # Condition trade => price action
                        if pa.PA_BullEngulfing(open1, close1, open0, close0) == True and range_slB >= 38:
                            str = "BullEn"
                            databars.iat[i + 3, PA] = str
                            print("Price Action :pass")
                            print("range", range_slB)
                            if range_slB >= 38:
                                databars.iat[i + 3, SIG] = "Buy"
                                databars.iat[i + 3, STA] = "OPEN"
                                databars.iat[i + 3, ORP] = openpeiceB
                                databars.iat[i + 3, SL] = stoplossB
                                takeprofit = openpeiceB + (range_slB * 1)
                                databars.iat[i + 3, TP] = takeprofit
                        if pa.PA_Morning_star(open0, close0, open1, close1, open2, close2) == True and range_slB >= 38:
                            str = "Morningstar"
                            databars.iat[i + 3, PA] = str
                            print("Price Action :pass")
                            print("range", range_slB)
                            if range_slB >= 38:
                                databars.iat[i + 3, SIG] = "Buy"
                                databars.iat[i + 3, STA] = "OPEN"
                                databars.iat[i + 3, ORP] = openpeiceB
                                databars.iat[i + 3, SL] = stoplossB
                                takeprofit = openpeiceB + (range_slB * 1)
                                databars.iat[i + 3, TP] = takeprofit

                # create Condition trade => SELL

                elif EMAShort0 < EMALong0 <EMALLong0 :
                    print("EMAShort < EMALong < EMALLong : pass")
                    if close0 < EMAShort0 and close1 < EMAShort1:
                        print("close > EMAShort          :pass")
                        openpeiceS = close0 - 5
                        stoplossS = (max(high0, high1, high2)) + 5
                        range_slS = stoplossS - openpeiceS

                        # Condition trade => price action

                        if pa.PA_BearEngulfing(open1, close1, open0, close0) == True and range_slS >= 38:
                            str = "BearEn"
                            databars.iat[i + 3, PA] = str
                            print("Price Action :pass")
                            print("range", range_slS)
                            if range_slS >= 38:
                                databars.iat[i + 3, SIG] = "Sell"
                                databars.iat[i + 3, STA] = "OPEN"
                                databars.iat[i + 3, ORP] = openpeiceS
                                databars.iat[i + 3, SL] = stoplossS
                                takeprofit = openpeiceS - (range_slS * 1)
                                databars.iat[i + 3, TP] = takeprofit
                        if pa.PA_Evening_star(open0, close0, open1, close1, open2, close2) == True and range_slS >= 38:
                            str = "Eveningstar"
                            databars.iat[i + 3, PA] = str
                            print("Price Action :pass")
                            print("range", range_slS)
                            if range_slS >= 38:
                                databars.iat[i + 3, SIG] = "Sell"
                                databars.iat[i + 3, STA] = "OPEN"
                                databars.iat[i + 3, ORP] = openpeiceS
                                databars.iat[i + 3, SL] = stoplossS
                                takeprofit = openpeiceS - (range_slS * 1)
                                databars.iat[i + 3, TP] = takeprofit

            # Check status portfolio Buy/Sell/None
            elif (signal[i+2] == "Buy" or signal[i+2] == "Sell") and status[i+2] == "OPEN":
                print("")

                #Status Buy
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

                # Status Sell
                elif signal[i+2] == "Sell":
                    databars.iat[i+3,STA] = "OPEN"
                    databars.iat[i + 3, SIG] = "Sell"
                    databars.iat[i + 3, SL] = PDSL[i + 2]
                    databars.iat[i + 3, ORP] = ord[i + 2]
                    databars.iat[i + 3, TP] = PDTP[i + 2]

                    # change sl

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
            time.sleep(0.015)
        CountPA = databars.groupby(['Price Action']).count()
        CountPA = CountPA["signal"]
        print(CountPA)
        CountWL = databars.groupby(['WINRATE']).count()
        CountWL = CountWL["signal"]
        print(CountWL)




