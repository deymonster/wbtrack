import hashlib
import hmac

class HashCheck:
    def __init__(self, data, secret):
        self.hash = data['hash']
        self.secret_key = secret
        self.data = {k: v for k, v in data.items() if k != 'hash'}

    def data_check_string(self):
        print(f"Data for hashing: {self.data}")
        items = sorted(self.data.items())  # Сортировка по ключам
        print(f"Sorted items: {items}")
        # Формируем строку в формате "key=value", добавляя все поля
        return '\n'.join(f"{k}={v}" for k, v in items)

    def calc_hash(self):
        msg = self.data_check_string().encode('utf-8')
        print(f"String to hash: {msg}")
        calculated_hash = hmac.new(self.secret_key, msg=msg, digestmod=hashlib.sha256).hexdigest()
        print(f"Calculated hash: {calculated_hash}")  # Для отладки
        return calculated_hash

    def check_hash(self):
        print(f"Received hash: {self.hash}")  # Для отладки
        return self.calc_hash() == self.hash
