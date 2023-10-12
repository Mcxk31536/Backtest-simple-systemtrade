# Backtest-simplesystemtrade-MetaTrader5
Backtest-algorithmic-trading โดยระบบนี้จะใช้ภาษา Python 3.11 และ Library MetaTrader5 
ในการดึงข้อมูลราคาย้อนหลังตามจำนวนแท่งเทียนที่ระบุ สามารถดึงข้อมูลได้มากที่สุด 99,999 แท่ง ใช้คำนวณหา
Essentiail Moving Average(EMA) และ 
Price Action(PA) 
* ผู้ใช้งานควรมีความรู้เกี่ยวกับ สินค้าโภคภัณฑ์, Leverage, Contract for Differences
* Project นี้ใช้ในการทดสอบเท่านั้น (Demo)
 
ขั้นตอนการใช้งาน

0. Install Package          

certifi          2023.5.7
distlib          0.3.6
filelock         3.12.0
MetaTrader5      5.0.45
numpy            1.24.3
packaging        23.1
pandas           2.0.1
pip              23.2.1
pipenv           2023.4.29
platformdirs     3.5.0
plotly           5.15.0
python-dateutil  2.8.2
pytz             2023.3
setuptools       68.0.0
six              1.16.0
tenacity         8.2.2
tzdata           2023.3
virtualenv       20.23.0
virtualenv-clone 0.5.7

1. สมัครสมาชิก Broker ที่ให้บริการเทรดใน Application MetaTrader5 ที่มีความน่าเชื่อถือ
2. ดาว์โหลด Login และกดปุ่มเปิดโหมด AutoTrade(ต้องกด manual เท่านั้น)
3. ปรับ parameter EMA 3 เส้น และกำหนดว่าจะใช้ PA รูปแบบไหนบ้าง
4. กำหนดความเสี่ยงและผลตอบแทน(Stop loss , Take profit)
5. กำหนดเงื่อนไขในกรณีมี order ใน portfolio ว่าต้องการลดหรือเพิ่มความเสียงไหม
อย่างไร (ปรับ Stop loss , Take profit)
