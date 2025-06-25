from datetime import datetime

weekdays = ["понедельник", "вторник", "среда",
            "четверг", "пятница", "суббота", "воскресенье"]


def get_current_datetime_info() -> str:
    now = datetime.now()
    nows = now.strftime("%d.%m.%Y %H:%M")
    weekday_num = now.weekday()
    return f"Текущая дата, время и день недели: {nows}, {weekdays[weekday_num]}"
