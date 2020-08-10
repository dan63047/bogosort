import random
import datetime
import time


class BogoSort:
    def __init__(self, l):
        array = list(range(int(l)))
        random.shuffle(array)
        print(f"Array created: {str(array)}\nSorting... (Ctrl+C to interrupt)")
        start_time = time.time()
        step = 0
        try:
            while any(x > y for x, y in zip(array, array[1:])):
                random.shuffle(array)
                step += 1
            end_time = time.time()
            print(f"Done: {str(array)}")
            self.stats(end_time, start_time, l, step)
        except KeyboardInterrupt:
            end_time = time.time()
            print("Sorting interrupted by user")
            self.stats(end_time, start_time, l, step)

    def stats(self, end_time, start_time, l, step):
        bogosort_time = end_time - start_time
        try:
            steps_for_sec = step / bogosort_time
        except Exception:
            steps_for_sec = "∞"
        time_d = int(bogosort_time) / (3600 * 24)
        time_h = int(bogosort_time) / 3600 - int(time_d) * 24
        time_min = int(bogosort_time) / 60 - int(time_h) * \
            60 - int(time_d) * 24 * 60
        time_sec = int(bogosort_time) - int(time_min) * 60 - \
            int(time_h) * 3600 - int(time_d) * 24 * 60 * 60
        time_msec = (bogosort_time - int(bogosort_time))*1000
        str_up_time = '%01d:%02d:%02d:%02d.%03d' % (
            time_d, time_h, time_min, time_sec, time_msec)
        datetime_start_time = datetime.datetime.fromtimestamp(start_time)
        datetime_end_time = datetime.datetime.fromtimestamp(end_time)
        print(f" {'Number of values:':25}{l}\n {'Start time:':25}{datetime_start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n {'Number of steps:':25}{step}\n {'End time:':25}{datetime_end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n {'Wasted time:':25}{str_up_time}\n {'Sorting speed:':25}{steps_for_sec} step/sec")


print("Sorting algorithm BogoSort is very simple: it just randomly shuffle values in array, until a miracle happens and the array is sorted\nHow many values should there be in the array to sort?")
BogoSort(input(">"))
