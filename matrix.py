import time
import requests

url = "https://api.okdream.tcl.zendo.cloud/api/v1/register"
url_auf = "https://api.okdream.tcl.zendo.cloud/api/v1/login"
url_acc = "https://api.okdream.tcl.zendo.cloud/api/v1/user/finance/accounts"
url_money_up = "https://api.okdream.tcl.zendo.cloud/api/v1/admin/finance/operations/user-transfer"
url_game_activation= "https://api.okdream.tcl.zendo.cloud/api/v1/buy/game-activation"

inviter = "avtotest"
admin_login = "admin"
password_admin = "Xeb2Liv8Fym7Pit8Zaf9"


password = "123456"
headers =  register_headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, /'
        }

# Шаг 1. Создаем пользователя.
class UserGenerator:  # Гениратор пользователей. Нужно настраивать
    def generate_login(self, index):
        return "avtotest" + str(7026 + index) #настрой окончание  логина

    def generate_users(self, count):
        for i in range(count):
            login = self.generate_login(i)
            self.create_user(login)

    def create_user(self, login):
        data = {
            "password": "123456",
            "username": login,
            "sponsor_username": inviter,
            'password_confirmation':"123456",
            "email": login + "@gmail.com",
            "agreement": "true",
            "has_sponsor": 1
        }
        print("шаг 1 Создание пользователя")
        response = requests.post(url=url, headers=register_headers, json=data)
        if response.status_code == 201:
            print(response.status_code)
            print(f"User--- {login} ---created successfully")
        else:
            print(f"Failed to create user {login}")
            print(response.status_code)
# Шаг 2. Авторизация клиентом.
        body_1 = {

            "login": login,
            "password": password
        }

        print("Шаг 2.  Авторизация клиентом")
        print("____________________________________________________________________________________________")
        post_1 = requests.post(url=url_auf, headers=register_headers, json=body_1)
        assert 200 == post_1.status_code
        if post_1.status_code == 200:
            print("статус код =", post_1.status_code)
            print("------------")
        else:
            print("case is not working")
        token_1 = post_1.json()['data']['token']
        register_headers_2 = \
            {
                'Authorization': f'Bearer {token_1}',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, /'
            }
        print("Узнаем аккаунт пользователя")
        get_1 = requests.get(url=url_acc, headers=register_headers_2)
        assert 200 == post_1.status_code
        if get_1.status_code == 200:
            get_1 = get_1.json()
        account_main = None
        for account in get_1['data']:
            if account['name'] == "Основной счет OGC":
                account_main = account['id']  # account_ustd_main  это переменная которую система использует как номер счета
                break
        print("Аккаунт для пополнения основного счета = id ", account_main)
        print("--------------------------")
        print("Теперь админом кидаем деньги на основной счет пользователю")
        print("Авторизация админом")

        auf_hed_admin = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, /'
        }
        body_admin = {

            "login": admin_login,
            "password": password_admin
        }
        post_admin = requests.post(url=url_auf, headers=auf_hed_admin, json=body_admin)
        print(post_admin.status_code)
        assert 200 == post_admin.status_code
        if post_admin.status_code == 200:
            print("Токен админа получил.")
        else:
            print("чтото посло не так")
        token_admin = post_admin.json()['data']['token']
        register_admin = \
            {
                'Authorization': f'Bearer {token_admin}',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, /'
            }
        post_body = {
            "credit_account_id": "9",
            "debit_account_id": account_main,
            "amount": "100"
            }
        post_money = requests.post(url=url_money_up, headers=register_admin, json=post_body)
        print(post_money.json())
        assert 202 == post_money.status_code
        if post_money.status_code == 202:
            print("Статус код", post_money.status_code)
            print("Баблишко на счету")
            print("----------")
        else:
            print(post_money.json())
            print(post_money.status_code, "чет натупилось")

        print("Приступаем к активации матрици")
        post_body_2 = {
            "main_ogc_selected": "1",
             "financial_password": password
        }
        time.sleep(5)
        post_3 = requests.post(url=url_game_activation, headers=register_headers_2, json=post_body_2)
        assert 200 == post_3.status_code
        if post_3.status_code == 200:
            print(post_3.status_code)
            print(post_3.json(), 'пользователь в игре')
            print("--------------------------------------------------------------")
            time.sleep(3)
            print("Перекурчик 3 сек")
        else:
            print("Чтото посло не так")
            print(post_3.status_code)
            print(post_3.json(), 'пользователь в игре')
            time.sleep(3)
            print("Перекурчик 3 сек")





# Использование класса UserGenerator для создания 10 пользователей
generator = UserGenerator()
generator.generate_users(5000)





