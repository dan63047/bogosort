import random
import datetime
import threading
import argparse
import locale
from string import Template

locale.setlocale(locale.LC_NUMERIC, ('en_EN', 'UTF-8'))
parser = argparse.ArgumentParser(description='Sorting algorithm BogoSort is very simple: it just randomly shuffle values in array, until a miracle happens and the array is sorted')
parser.add_argument("array_size", metavar="N", type=int, help="Number or values in the array to sort")
parser.add_argument("-i", action='store_true', help="During sorting, information about the elapsed time, steps and sorting speed will not be displayed")
args = parser.parse_args()

def numbers5symbols(num):
    num = int(num)
    if len(str(num)) <= 4:
        return str(num)
    elif len(str(num)) <= 5:
        num /= 10**3
        return f"{num:.{1}f}k"
    elif len(str(num)) <= 6:
        num /= 10**3
        return f"{num:.{0}f}k"
    elif len(str(num)) <= 7:
        num /= 10**6
        return f"{num:.{2}f}M"
    elif len(str(num)) <= 8:
        num /= 10**6
        return f"{num:.{1}f}M"
    elif len(str(num)) <= 9:
        num /= 10**6
        return f"{num:.{0}f}M"
    elif len(str(num)) <= 10:
        num /= 10**9
        return f"{num:.{2}f}B"
    elif len(str(num)) <= 11:
        num /= 10**9
        return f"{num:.{1}f}B"
    elif len(str(num)) <= 12:
        num /= 10**9
        return f"{num:.{0}f}B"
    elif len(str(num)) <= 13:
        num /= 10**12
        return f"{num:.{2}f}T"
    elif len(str(num)) <= 14:
        num /= 10**12
        return f"{num:.{1}f}T"
    elif len(str(num)) >= 15:
        num /= 10**12
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
    hours, rem = divmod(tdelta.seconds, 3600)
    d = {"D": tdelta.days}
    minutes, seconds = divmod(rem, 60)
    if show_days:
        d["H"] = '{:02d}'.format(hours)
        d["M"] = '{:02d}'.format(minutes)
        d["S"] = '{:02d}'.format(seconds)
        if negative:
            t = DeltaTemplate('- %D d. %H:%M:%S')
        else:
            t = DeltaTemplate('%D d. %H:%M:%S')
    else:
        hours += d["D"]*24
        d["H"] = locale.format_string('%d', hours, grouping=True)
        d["M"] = '{:02d}'.format(minutes)
        d["S"] = '{:02d}'.format(seconds)
        t = DeltaTemplate('-%H:%M:%S') if negative else DeltaTemplate('%H:%M:%S')

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
            print(f"Array with {l} values created")
        else:
            print(f"Array created: {str(self.array)}")
        self.start_time = datetime.datetime.now()
        if args.i:
            print(" [Ctrl+C чтобы прервать] Sorting...", end="\r")
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
            done_str = "Done!" if int(l) > 100 else f"Done: {str(self.array)}"
            print(done_str, end=" "*(90-len(done_str))+"\n")
            self.stats()
        except KeyboardInterrupt:
            self.end_time = datetime.datetime.now()
            print("Sorting interrupted by user", end=" "*80+"\n")
            self.stats()

    def stats(self):
        bogosort_time = self.end_time - self.start_time
        try:
            steps_for_sec = locale.format_string("%.3f", self.step/bogosort_time.total_seconds(), grouping=True)
        except Exception:
            steps_for_sec = "∞"
        print(f" {'Number of values:':25}{locale.format_string('%d', len(self.array), grouping=True)}")
        print(f" {'Start time:':25}{self.start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        print(f" {'Number of steps:':25}{locale.format_string('%d', self.step, grouping=True)}")
        print(f" {'End time:':25}{self.end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        print(f" {'Wasted time:':25}{bogosort_time}")
        print(f" {'Sorting speed:':25}{steps_for_sec} step/sec")


sorting = BogoSort()
def print_until_sorting():
    while sorting.end_time is None:
        bogosort_time = datetime.datetime.now() - sorting.start_time
        if bogosort_time.total_seconds() > 1:
            steps_for_sec = numbers5symbols(sorting.step/bogosort_time.total_seconds())
        else:
            steps_for_sec = "---"
        print(f" [Ctrl+C to interrupt] Sorting, {strfdelta(sorting.start_time, datetime.datetime.now())}, {numbers5symbols(sorting.step)} steps, {steps_for_sec} step/sec", end="  "*5+"\r") # On case, if wanna see the exact value: locale.format_string('%d', sorting.step, grouping=True)
sorting.sorting(args.array_size)
