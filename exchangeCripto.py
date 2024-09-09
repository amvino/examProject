from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

# Словари кодов валют и их полных названий
crypto_cur = {
    "BTC" : ["Bitcoin", "bitcoin"], # btc
    "ETH" : ["Ethereum", "ethereum"], # eth
    "XRP" : ["XRP", "ripple"], # xrp
    "TON" : ["Toncoin", "the-open-network"], # ton
    "SOL" : ["Solana", "solana"] # sol
}
currencies = {
    "RUB": "Российский рубль",
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CNY": "Китайский юань"
}

# Получаем полное название криптовалюты из словаря и обновляем метку
def update_base_label(event):
    base_code = base_combobox.get()
    base_name = crypto_cur[base_code][0]
    base_label.config(text=base_name)


# Получаем полное название валюты из словаря и обновляем метку
def update_target_label(event):
    target_code = target_combobox.get()
    target_name = currencies[target_code]
    target_label.config(text=target_name)


# Функция обработки запроса API
def exchange():
    base_code = base_combobox.get()
    target_code = target_combobox.get()

    if base_code and target_code:
        base_code_id = crypto_cur[base_code][1]
        target_code_id = target_code.lower()

        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={base_code_id}&vs_currencies={target_code_id}')
            response.raise_for_status()
            data = response.json()

            exchange_rate = data[base_code_id][target_code_id]
            base_name = crypto_cur[base_code][0]
            target_name = currencies[target_code]

            mb.showinfo("Курс обмена", f"Текущий курс: {exchange_rate:.1f} {target_name} за 1 {base_name}")

        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание" ,"Код валюты не выбран")


# Создание графического интерфейса
window = Tk()
window.title("Курс обмена криптовалюты")
window.geometry("360x300")

Label(text="Выберите криптовалюту:").pack(padx=10, pady=10)
base_combobox = ttk.Combobox(values=list(crypto_cur.keys()), state="readonly")
base_combobox.pack(padx=10, pady=2)
base_combobox.bind("<<ComboboxSelected>>", update_base_label)

base_label = ttk.Label()
base_label.pack(padx=10, pady=10)

Label(text="Выберите валюту:").pack(padx=10, pady=10)
target_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")
target_combobox.pack(padx=10, pady=2)
target_combobox.bind("<<ComboboxSelected>>", update_target_label)

target_label = ttk.Label()
target_label.pack(padx=10, pady=10)

Button(text="Показать курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()