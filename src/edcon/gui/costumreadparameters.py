class CustomReadParameters:
    def __init__(self, com):
        self.com = com

    def read_telegram(self):
        return self.com.read_pnu(3490, 0)
