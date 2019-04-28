import datetime

class FourDigitYearConverter:
    regex = r'\d{4}'  # regex는 regular express의 약자(정규표현식)

    def to_python(self, value):
        if 2010 <= int(value) <= datetime.datetime.now().year:
            return int(value)
        else:
            return None

    def to_url(self, value):
        return '{%04d}'.format(value)  # 모자르는 값은 0으로 채움
