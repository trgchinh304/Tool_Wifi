import time, requests, json, telebot, os
import matplotlib
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta

URL_API_BINANCE= 'https://api.binance.com/api/v3'

matplotlib.use('Agg') # không dùng đồ họa trực tiếp

# Nhập tên coin
def nhap_ten_coin(danh_sach):
    while True:
        ten_coin = input("Nhập tên coin: ").strip()
        if not ten_coin:
            print("Không được để trống tên")
            continue
        ten_crypto = ten_coin.upper() + "USDT"
        if ten_crypto in danh_sach:
            return ten_crypto
        print("Tên coin không hợp lệ. Vui lòng nhập đúng tên (không bao gồm phần đuôi USDT)")     

def nhap_khoang_thoi_gian_muon_lay():
    while True:
        khoang_thoi_gian_muon_lay = int(input("Nhập khoảng thời gian: "))
        if isinstance(khoang_thoi_gian_muon_lay, int):
            if khoang_thoi_gian_muon_lay < 20 or khoang_thoi_gian_muon_lay > 400:
                print("Phạm vi trong khảng 20-400 phút")
            return khoang_thoi_gian_muon_lay
        print("Chỉ nhập số, không nhập chữ !")

def lua_chon_ghi_vao_file():
    while True:
        ghi_vao_file = input("Ghi vào file (y/n): ").strip().lower()
        if ghi_vao_file in ["y", "n"]:
            return ghi_vao_file
        print("Vui lòng nhập y hoặc n")

# Hàm lấy danh sách các đồng crypto
def lay_danh_sach_crypto():
    response = requests.get(f'{URL_API_BINANCE}/exchangeInfo')
    data = response.json()
    danh_sach = [s['symbol'] for s in data['symbols'] if s['quoteAsset'] == 'USDT']
    return danh_sach 

def lay_thong_tin_gioi_han_crypto(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, ghi_file):
    response = requests.get(f'{URL_API_BINANCE}/klines', params={
        'symbol': ten_crypto,
        'interval': '1m',  
        'startTime': timestamp_thoi_gian_muon_lay,
        'endTime': timestamp_hien_tai,
    })
    datas = response.json() 
    if datas:
        danh_sach = []
        for data in datas:
            thoi_gian = datetime.fromtimestamp(data[0] / 1000)  
            gia_mo_cua = data[1]
            gia_dong_cua = data[4]  
            gia_cao_nhat = data[2]
            gia_thap_nhat = data[3]
            khoi_luong = data[5]
            noi_dung = {
                "Thời gian": thoi_gian.strftime("%Y-%m-%d %H:%M:%S"), 
                "Giá mở cửa": gia_mo_cua,
                "Giá đóng cửa": gia_dong_cua,
                "Giá cao nhất": gia_cao_nhat,
                "Giá thấp nhất": gia_thap_nhat,
                "Khối lượng": khoi_luong
            }
            danh_sach.append(noi_dung)
        if ghi_file in ["n"]:    
            print(json.dumps(danh_sach, indent=4, ensure_ascii=False))   
            return None
        elif ghi_file in ["y"]:
            ghi_vao_file(ten_crypto, danh_sach)
            return 1
        else: 
            print("Vui lòng nhập y/n")
            return None        
        print("Hoàn thành ghi vào file !")  
    else :
        print("Không có dữ liệu theo yêu cầu")      
        return None

def ghi_vao_file(ten_crypto, danh_sach_moi):
    file_path = f'D:\\Python\\{ten_crypto.upper()}.json'
    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                danh_sach_cu = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            danh_sach_cu = []
        danh_sach_cu.extend(danh_sach_moi)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(danh_sach_cu, file, indent=4, ensure_ascii=False)
        print("Dữ liệu đã được ghi vào file!")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghi vào file: {e}")

# Biểu đồ chỉ báo MA
def ve_bieu_do_nen_ma():
    with open("D:\\Python\\BTCUSDT.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:  
        print("Dữ liệu rỗng, không thể vẽ biểu đồ")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    mpf.plot(
        df,
        type='candle', 
        style='charles', 
        title="Biểu đồ giá BTC/USDT",
        ylabel="Giá (USDT)",
        volume=True,  
        ylabel_lower="Khối lượng",
        mav=(5, 10),  # Thêm MA
        savefig='D:\\Python\\bieudo_nen_ma.png'  
    )
    thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Biểu đồ nến đã được lưu lúc: {thoi_gian_hien_tai}\n")

# Biểu đồ chỉ báo BOLL 
def ve_bieu_do_nen_boll():
    with open("D:\\Python\\BTCUSDT.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:  
        print("Dữ liệu rỗng, không thể vẽ biểu đồ")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    df['MA20'] = df['Close'].rolling(window=20).mean()  # Đường trung bình 20 phiên
    df['Upper'] = df['MA20'] + 2 * df['Close'].rolling(window=20).std()  # Dải trên
    df['Lower'] = df['MA20'] - 2 * df['Close'].rolling(window=20).std()  # Dải dưới
    apds = [
        mpf.make_addplot(df['MA20'], color='blue'),
        mpf.make_addplot(df['Upper'], color='red'),
        mpf.make_addplot(df['Lower'], color='green')
    ]
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title="Biểu đồ giá BTC/USDT với Bollinger Bands",
        ylabel="Giá (USDT)",
        volume=True,
        ylabel_lower="Khối lượng",
        addplot=apds,  # Thêm Bollinger Bands
        savefig='D:\\Python\\bieudo_boll.png'
    )
    thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Biểu đồ nến đã được lưu lúc: {thoi_gian_hien_tai}\n")

def ve_bieu_do_nen_ema():
    with open("D:\\Python\\BTCUSDT.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:  
        print("Dữ liệu rỗng, không thể vẽ biểu đồ")
        return
    df = pd.DataFrame(data)
    df["Thời gian"] = pd.to_datetime(df["Thời gian"])
    df.rename(columns={
        "Thời gian": "Date",
        "Giá mở cửa": "Open",
        "Giá đóng cửa": "Close",
        "Giá cao nhất": "High",
        "Giá thấp nhất": "Low",
        "Khối lượng": "Volume"
    }, inplace=True)
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    df.set_index("Date", inplace=True)
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()  # EMA20
    apds = [
        mpf.make_addplot(df['EMA20'], color='purple', linestyle='-', title='EMA20')  # Đường liền cho EMA20
    ]
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title="Biểu đồ giá BTC/USDT với EMA",
        ylabel="Giá (USDT)",
        volume=True,
        ylabel_lower="Khối lượng",
        addplot=apds,  # Thêm EMA vào biểu đồ
        savefig='D:\\Python\\bieudo_ema.png'
    )
    thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Biểu đồ nến đã được lưu lúc: {thoi_gian_hien_tai}\n")

def main():
    try:
        danh_sach = lay_danh_sach_crypto()
        ten_crypto = nhap_ten_coin(danh_sach)
        khoang_thoi_gian_muon_lay = nhap_khoang_thoi_gian_muon_lay()
        ghi_file = lua_chon_ghi_vao_file()
        thoi_gian_hien_tai = datetime.now()
        thoi_gian_muon_lay = thoi_gian_hien_tai - timedelta(minutes=khoang_thoi_gian_muon_lay)
        timestamp_thoi_gian_muon_lay = int(thoi_gian_muon_lay.timestamp() * 1000)
        timestamp_hien_tai = int(thoi_gian_hien_tai.timestamp() * 1000)
        lua_chon = lay_thong_tin_gioi_han_crypto(ten_crypto, timestamp_thoi_gian_muon_lay, timestamp_hien_tai, ghi_file)
        if lua_chon != None :
            ve_bieu_do_nen_ma()
            ve_bieu_do_nen_boll()
            ve_bieu_do_nen_ema()
            os.remove(f'D:\\Python\\{ten_crypto.upper()}.json')    
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")        

if __name__ == "__main__":
    main()

