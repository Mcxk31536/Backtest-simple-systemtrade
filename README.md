# Backtest-simplesystemtrade-MetaTrader5
Backtest-algorithmic-trading โดยระบบนี้จะใช้ภาษา Python และ Library MetaTrader5 
ในการดึงข้อมูลราคาย้อนหลังตามจำนวนแท่งเทียนที่ระบุ สามารถดึงข้อมูลได้มากที่สุด 99,999 แท่ง ใช้คำนวณหา
Essentiail Moving Average(EMA) และ 
Price Action(PA) 
* ผู้ใช้งานควรมีความรู้เกี่ยวกับ สินค้าโภคภัณฑ์, Leverage, Contract for Differences
* Project นี้ใช้ในการทดสอบเท่านั้น (Demo)
 
ขั้นตอนการใช้งาน
1. สมัครสมาชิก Broker ที่ให้บริการเทรดใน Application MetaTrader5 ที่มีความน่าเชื่อถือ
2. ดาว์โหลด Login และกดปุ่มเปิดโหมด AutoTrade(ต้องกด manual เท่านั้น)
3. ปรับ parameter EMA 3 เส้น และกำหนดว่าจะใช้ PA รูปแบบไหนบ้าง
4. กำหนดความเสี่ยงและผลตอบแทน(Stop loss , Take profit)
5. กำหนดเงื่อนไขในกรณีมี order ใน portfolio ว่าต้องการลดหรือเพิ่มความเสียงไหม
อย่างไร (ปรับ Stop loss , Take profit)
