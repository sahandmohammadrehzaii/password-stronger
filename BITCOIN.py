import locale
from pycoingecko import CoinGeckoAPI
import tkinter as tk
from tkinter import ttk, simpledialog
import threading
import webbrowser

# تنظیمات محلی برای استفاده از جداکننده‌های هزارگان
locale.setlocale(locale.LC_ALL, '')

def get_crypto_prices(coins):
    cg = CoinGeckoAPI()
    prices = cg.get_price(ids=','.join(coins), vs_currencies='usd')
    return prices

def format_number(number):
    return locale.format_string("%d", number, grouping=True)

def convert_to_toman(amount_usd, rate):
    return format_number(amount_usd * rate)

def convert_from_toman(amount_toman, rate, price_usd):
    converted_amount = amount_toman / rate / price_usd
    return "{:.6f}".format(converted_amount)  # برای نمایش دقیق‌تر اعداد با اعشار

def update_prices(labels, coins, rate):
    prices = get_crypto_prices(coins)
    for coin in coins:
        if coin in prices:
            price_usd = prices[coin]['usd']
            price_toman = convert_to_toman(price_usd, rate)
            labels[coin].config(text=f"{coin.capitalize()}: ${price_usd} / {price_toman} تومان")
        else:
            labels[coin].config(text=f"{coin.capitalize()}: مشکلی هنگام پردازش قیمت به مشکلی به وجود آمد")

def display_prices(rate):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    labels = {}
    coins =  [
    "bitcoin",
]
    
    #  "ethereum", "litecoin", "ripple", "cardano",
    # "dogecoin", "polkadot", "binancecoin", "solana", "uniswap",
    # "chainlink", "stellar", "bitcoin-cash", "usd-coin", "cosmos",
    # "monero", "tron", "iota", "neo", "tezos", "aave", "algorand", 
    # "vechain", "terra-luna", "axie-infinity"

    for coin in coins:
        labels[coin] = tk.Label(canvas_frame, text=f"{coin.capitalize()}: در حال بارگذاری", font=("Arial", 14))
        labels[coin].pack()

    threading.Thread(target=update_prices, args=(labels, coins, rate), daemon=True).start()

def ask_amount_and_convert(selected_coin, rate, prices, output_text, to_toman):
    if to_toman:
        amount_crypto = simpledialog.askfloat("تبدیل", f"مقدار {selected_coin.upper()} را وارد کنید:", minvalue=0.0)
        if amount_crypto is not None and selected_coin in prices:
            price_usd = prices[selected_coin]['usd']
            converted_amount = convert_to_toman(amount_crypto * price_usd, rate)
            output_text.insert(tk.END, f"تبدیل {amount_crypto:.6f} {selected_coin.upper()} به تومان:\n{converted_amount} تومان\n\n")
    else:
        amount_toman = simpledialog.askfloat("تبدیل", "مبلغ به تومان را وارد کنید:", minvalue=0.0)
        if amount_toman is not None and selected_coin in prices:
            price_usd = prices[selected_coin]['usd']
            converted_amount = convert_from_toman(amount_toman, rate, price_usd)
            output_text.insert(tk.END, f"تبدیل {amount_toman} تومان به {selected_coin.upper()}:\n{converted_amount} {selected_coin.upper()}\n\n")

def open_link(url):
    webbrowser.open_new(url)

window = tk.Tk()
window.title("تکلیف سید سهیل موسوی به استاد صابری")
window.geometry("500x700")

usd_to_toman_rate = 42075  # نرخ تبدیل تومان به دلار

link = tk.Label(window, text="تکلیف سید سهیل موسوی به استاد صابری", font=("Arial", 10), fg="blue", cursor="hand2")
link.pack(side="top", fill="x")


canvas = tk.Canvas(window)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

coins =  [
        "بیت کوین", 
    ]

# "اتریوم", "لایت کوین", "ریپل", "کاردونو",
#         "دوج کوین", "پولکادات", "باینس کوین", "سولانا", "یونی سو اپ",
#         "چین لینک", "استلار", "بیت کوین - کش", "یو اس دی کوین", "کازماس",
#         "مونرو", "ترون", "یوتا", "نئو", "تزوس", "آوه", "الگروند", 
#         "ویچین", "ترالونا", "اکسی اینفینیتی"

prices = get_crypto_prices(coins)

conversion_frame = tk.Frame(window)
conversion_frame.pack(pady=10)

select_label = tk.Label(conversion_frame, text="ارزتان را انتخاب کنید:", font=("Arial", 12))
select_label.pack(side=tk.LEFT)

coin_var = tk.StringVar(window)
coin_var.set(coins[0])  # انتخاب اولیه

coin_menu = tk.OptionMenu(conversion_frame, coin_var, *coins)
coin_menu.pack(side=tk.LEFT)

output_text = tk.Text(window, height=10, width=50)
output_text.pack(pady=10)

convert_to_toman_button = tk.Button(conversion_frame, text="تبدیل ارز دیجیتال به تومان", command=lambda: ask_amount_and_convert(coin_var.get(), usd_to_toman_rate, prices, output_text, True), font=("Arial", 12))
convert_to_toman_button.pack(side=tk.LEFT)

convert_from_toman_button = tk.Button(conversion_frame, text="تبدیل تومان به ارز دیجیتال", command=lambda: ask_amount_and_convert(coin_var.get(), usd_to_toman_rate, prices, output_text, False), font=("Arial", 12))
convert_from_toman_button.pack(side=tk.LEFT)

display_prices_button = tk.Button(window, text="نمایش قیمت‌ها", command=lambda: display_prices(usd_to_toman_rate), font=("Arial", 12))
display_prices_button.pack(pady=10)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

canvas_frame = scrollable_frame

watermark = tk.Label(window, text="تکلیف سید سهیل موسوی به استاد صابری", font=("Arial", 10), fg="gray")
watermark.pack(side="bottom", fill="x")

window.mainloop()
