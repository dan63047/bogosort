import random
import datetime
import time


class BogoSort:
    def __init__(self, l):
        array = list(range(int(l)))
        random.shuffle(array)
        if int(l) > 100:
            print(f"Создан массив со {l} значениями\nСортировка... (Ctrl+C чтобы прервать)")
        else:
            print(f"Создан массив: {str(array)}\nСортировка... (Ctrl+C чтобы прервать)")
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
                print("Готово!")
            else:
                print(f"Готово: {str(array)}")
            self.stats(end_time, start_time, l, step)
        except KeyboardInterrupt:
            end_time = datetime.datetime.now()
            print("Сортировка прервана пользователем")
            self.stats(end_time, start_time, l, step)

    def stats(self, end_time, start_time, l, step):
        bogosort_time = end_time - start_time
        try:
            steps_for_sec = round(step / bogosort_time.total_seconds(), 3)
        except Exception:
            steps_for_sec = "∞"
        print(f" {'Кол-во элементов:':25}{l}\n {'Время старта:':25}{start_time.strftime('%d.%m.%Y %H:%M:%S.%f')}\n {'Кол-во шагов:':25}{step}\n {'Время завершения:':25}{end_time.strftime('%d.%m.%Y %H:%M:%S.%f')}\n {'Потрачено времени:':25}{bogosort_time}\n {'Скорость сортировки:':25}{steps_for_sec} шаг/сек")


print("Алгоритм сортировки BogoSort очень прост: он просто передвигает значения в массиве в рандомные места, пока не случится чудо и массив не отсортируется\nСколько элементов должно быть в массиве для сортировки?")
BogoSort(input(">"))
