import random
import datetime
import time


class BogoSort:
    def __init__(self, l):
        array = list(range(int(l)))
        random.shuffle(array)
        if int(l) > 100:
            print(
                f"Array with {l} values created\nSorting... (Ctrl+C to interrupt)")
        else:
            print(
                f"Array created: {str(array)}\nSorting... (Ctrl+C to interrupt)")
        start_time = datetime.datetime.now()
        step = 0
        try:
            while any(x > y for x, y in zip(array, array[1:])):
                x = random.randint(0, int(l)-1)
                y = random.randint(0, int(l)-1)
                array[x], array[y] = array[y], array[x]
                step += 1
            end_time = datetime.datetime.now()
            if int(l) > 100:
                print("Done!")
            else:
                print(f"Done: {str(array)}")
            self.stats(end_time, start_time, l, step)
        except KeyboardInterrupt:
            end_time = datetime.datetime.now()
            print("Sorting interrupted by user")
            self.stats(end_time, start_time, l, step)

    def stats(self, end_time, start_time, l, step):
        bogosort_time = end_time - start_time
        try:
            steps_for_sec = round(step / bogosort_time.total_seconds(), 3)
        except Exception:
            steps_for_sec = "∞"
        print(f" {'Number of values:':25}{l}\n {'Start time:':25}{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n {'Number of steps:':25}{step}\n {'End time:':25}{end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n {'Wasted time:':25}{bogosort_time}\n {'Sorting speed:':25}{steps_for_sec} step/sec")


print("Sorting algorithm BogoSort is very simple: it just randomly shuffle values in array, until a miracle happens and the array is sorted\nHow many values should there be in the array to sort?")
BogoSort(input(">"))
