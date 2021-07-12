import random
import datetime
import threading
import argparse
import locale
from string import Template

locale.setlocale(locale.LC_NUMERIC, ('ru_RU', 'UTF-8'))
parser = argparse.ArgumentParser(description='Алгоритм сортировки BogoSort очень прост: он просто передвигает значения в массиве в рандомные места, пока не случится чудо и массив не отсортируется')
parser.add_argument("array_size", metavar="N", type=int, help="Количество элементов в массиве для сортировки")
parser.add_argument("-i", action='store_true', help="Во время сортировки не будет выводится информация о потраченном времени, шагах и скорости сортировки")
args = parser.parse_args()

def numbers5symbols(num):
    num = int(num)
    if len(str(num)) <= 4:
        return str(num)
    elif len(str(num)) <= 5:
        num = num/10**3
        return f"{num:.{1}f}k"
    elif len(str(num)) <= 6:
        num = num/10**3
        return f"{num:.{0}f}k"
    elif len(str(num)) <= 7:
        num = num/10**6
        return f"{num:.{2}f}M"
    elif len(str(num)) <= 8:
        num = num/10**6
        return f"{num:.{1}f}M"
    elif len(str(num)) <= 9:
        num = num/10**6
        return f"{num:.{0}f}M"
    elif len(str(num)) <= 10:
        num = num/10**9
        return f"{num:.{2}f}B"
    elif len(str(num)) <= 11:
        num = num/10**9
        return f"{num:.{1}f}B"
    elif len(str(num)) <= 12:
        num = num/10**9
        return f"{num:.{0}f}B"
    elif len(str(num)) <= 13:
        num = num/10**12
        return f"{num:.{2}f}T"
    elif len(str(num)) <= 14:
        num = num/10**12
        return f"{num:.{1}f}T"
    elif len(str(num)) >= 15:
        num = num/10**12
        return f"{num:.{0}f}T"

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(dtfrom:datetime.datetime, zero:datetime.datetime) -> str:
    if zero < dtfrom:
        tdelta = dtfrom - zero
        negative = True
    else:
        tdelta = zero - dtfrom
        negative = False
    show_days = True
    if tdelta.days == 0: show_days = False
    if show_days:
        d = {"D": tdelta.days}
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        d["H"] = '{:02d}'.format(hours)
        d["M"] = '{:02d}'.format(minutes)
        d["S"] = '{:02d}'.format(seconds)
        if negative:
            t = DeltaTemplate('- %D дн. %H:%M:%S')
        else:
            t = DeltaTemplate('%D дн. %H:%M:%S')
        return t.substitute(**d)
    else:
        d = {"D": tdelta.days}
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        hours += d["D"]*24
        d["H"] = locale.format_string('%d', hours, grouping=True)
        d["M"] = '{:02d}'.format(minutes)
        d["S"] = '{:02d}'.format(seconds)
        if negative:
            t = DeltaTemplate('-%H:%M:%S')
        else:
            t = DeltaTemplate('%H:%M:%S')
        return t.substitute(**d)

class BogoSort:
    def __init__(self):
        self.step = 0
        self.start_time = None
        self.end_time = None
        self.array = None

    def sorting(self, l):
        self.array = list(range(int(l)))
        random.shuffle(self.array)
        if int(l) > 100:
            print(f"Создан массив со {l} значениями")
        else:
            print(f"Создан массив: {str(self.array)}")
        self.start_time = datetime.datetime.now()
        if args.i:
            print(" [Ctrl+C чтобы прервать] Сортировка...", end="\r")
        else:
            printing = threading.Thread(target=print_until_sorting, name=print_until_sorting, daemon=True)
            printing.start()
        try:
            while any(x > y for x, y in zip(self.array, self.array[1:])):
                x = random.randint(0, int(l)-1)
                y = random.randint(0, int(l)-1)
                self.array[x], self.array[y] = self.array[y], self.array[x]
                self.step += 1
            self.end_time = datetime.datetime.now()
            if int(l) > 100:
                done_str = "Готово!"
            else:
                done_str = f"Готово: {str(self.array)}"
            print(done_str, end=" "*(90-len(done_str))+"\n")
            self.stats()
        except KeyboardInterrupt:
            self.end_time = datetime.datetime.now()
            print("Сортировка прервана пользователем", end=" "*80+"\n")
            self.stats()

    def stats(self):
        bogosort_time = self.end_time - self.start_time
        try:
            steps_for_sec = locale.format_string("%.3f", self.step/bogosort_time.total_seconds(), grouping=True)
        except Exception:
            steps_for_sec = "∞"
        print(f" {'Кол-во элементов:':25}{locale.format_string('%d', len(self.array), grouping=True)}")
        print(f" {'Время старта:':25}{self.start_time.strftime('%d.%m.%Y %H:%M:%S.%f')}")
        print(f" {'Кол-во шагов:':25}{locale.format_string('%d', self.step, grouping=True)}")
        print(f" {'Время завершения:':25}{self.end_time.strftime('%d.%m.%Y %H:%M:%S.%f')}")
        print(f" {'Потрачено времени:':25}{bogosort_time}")
        print(f" {'Скорость сортировки:':25}{steps_for_sec} шаг/сек")


sorting = BogoSort()
def print_until_sorting():
    while sorting.end_time is None:
        bogosort_time = datetime.datetime.now() - sorting.start_time
        if bogosort_time.total_seconds() > 1:
            steps_for_sec = numbers5symbols(sorting.step/bogosort_time.total_seconds())
        else:
            steps_for_sec = "---"
        print(f" [Ctrl+C чтобы прервать] Сортировка, {strfdelta(sorting.start_time, datetime.datetime.now())}, {numbers5symbols(sorting.step)} шагов, {steps_for_sec} шаг/сек", end="  "*5+"\r") # На случай, если захочется видеть точную цифру: locale.format_string('%d', sorting.step, grouping=True)
sorting.sorting(args.array_size)
