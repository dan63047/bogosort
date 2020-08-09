import random
import datetime
import time


def bogosort(l):
    array = list(range(int(l)))
    random.shuffle(array)
    print(f"Создан массив: {str(array)}\nСортировка...")
    start_time = time.time()
    step = 0
    while any(x > y for x, y in zip(array, array[1:])):
        random.shuffle(array)
        step += 1
    end_time = time.time()
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
    print(f"Готово: {str(array)}\n {'Кол-во элементов:':25}{l}\n {'Время старта:':25}{datetime_start_time.strftime('%d.%m.%Y %H:%M:%S.%f')}\n {'Кол-во шагов:':25}{step}\n {'Время завершения:':25}{datetime_end_time.strftime('%d.%m.%Y %H:%M:%S.%f')}\n {'Потрачено времени:':25}{str_up_time}\n {'Скорость сортировки:':25}{steps_for_sec} шаг/сек")


print("Алгоритм сортировки BogoSort очень прост: он просто передвигает значения в массиве в рандомные места, пока не случится чудо и массив не отсортируется\nСколько элементов должно быть в массиве для сортировки?")
bogosort(input(">"))
