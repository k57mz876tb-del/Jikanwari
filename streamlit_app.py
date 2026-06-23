from datetime import datetime
now = datetime.now()
print(now)

import time
alarm_time = "11:40"

#while True:
#    now = datetime.now().strftime("%H:%M")

    #if now == alarm_time:
        #print("時間")
        #break

today = datetime.now()
w_number = today.weekday()

print(w_number)
days = ["月","火","水","木","金","土","日",]
print({days[w_number]})

import subprocess
import sys
subprocess.check_call([sys.executable,"-m","pip","install","jpholiday"])

import jpholiday
from datetime import date, timedelta

members = ["高見","内村","堀川","力石","松村","塩見","谷口","編塚"]

# =========================
# 芸術鑑賞の日を決める
# =========================

year = 2026

art_day = date(year, 5, 28)

# 土曜=5 日曜=6
while art_day.weekday() >= 5:
    art_day += timedelta(days=1)

print("芸術鑑賞の日:", art_day)

# =========================
# 中間テスト期間
# 芸術鑑賞の前の登校日4日間
# =========================

midterm_days = []

current = art_day - timedelta(days=1)

while len(midterm_days) < 4:

    # 土日を除外
    is_weekend = current.weekday() >= 5

    # 祝日を除外
    is_holiday = jpholiday.is_holiday(current)

    if not is_weekend and not is_holiday:
        midterm_days.append(current)

    current -= timedelta(days=1)

# 古い順に並べ替え
midterm_days.reverse()

print("\n1学期中間テスト")

for d in midterm_days:
    print(d)

# =========================
# 期末テスト
# 7月第一週の月〜木
# =========================

current = date(year, 7, 1)

# 最初の月曜まで進める
while current.weekday() != 0:
    current += timedelta(days=1)

final_exam_days = []

for i in range(4):
    final_exam_days.append(current + timedelta(days=i))

print("\n1学期期末テスト")

for d in final_exam_days:
    print(d)

def get_duty_person(target_date):
    if target_date.weekday() >= 5 or jpholiday.is_holiday(target_date):
        return None

    base_date = date(2026,4,1)
    current_date = base_date
    workday_count = 0

    while current_date < target_date.date():
        if current_date.weekday() <5 and not jpholiday.is_holiday(current_date) and not today ==art_day and today != midterm_days :
            workday_count +=1
        current_date += timedelta(days=1)

    return members[workday_count % 8]

person = get_duty_person(today)

if person:
    print("日直:",person)

#from datetime import datetime, timedelta
#import time
import winsound

# =========================
# 設定
# =========================

CLASS_TIME = 50
BREAK_TIME = 10

FIRST_START = datetime.strptime("08:40", "%H:%M")
LUNCH_END = datetime.strptime("13:15", "%H:%M")

# 月=0 火=1 水=2 木=3 金=4 土=5 日=6
today_weekday = datetime.now().weekday()
#today_weekday = 3

# 水曜だけ6限
if today_weekday == 2:
    max_period = 6
elif today_weekday == 3:
        max_period = 6
else:
    max_period = 7

# =========================
# 時間割生成
# =========================

schedule = []

current = FIRST_START

for period in range(1, max_period + 1):

    # 5限は昼休み後
    if period == 5:
        start = LUNCH_END
    else:
        start = current

    end = start + timedelta(minutes=CLASS_TIME)

    schedule.append({
        "name": f"{period}時間目",
        "start": start.strftime("%H:%M"),
        "end": end.strftime("%H:%M")
    })

    # 次の時間へ
    if period == 4:
        current = LUNCH_END
    else:
        current = end + timedelta(minutes=BREAK_TIME)

# =========================
# SHR / LHR
# =========================

last_end = end

after_break = last_end + timedelta(minutes=10)

# 木曜だけLHR
if today_weekday == 3:

    lhr_end = after_break + timedelta(minutes=50)

    schedule.append({
        "name": "LHR",
        "start": after_break.strftime("%H:%M"),
        "end": lhr_end.strftime("%H:%M")
    })

else:

    shr_end = after_break + timedelta(minutes=10)

    schedule.append({
        "name": "SHR",
        "start": after_break.strftime("%H:%M"),
        "end": shr_end.strftime("%H:%M")
    })

# =========================
# 今日の予定表示
# =========================

print("===== 今日の予定 =====")

for item in schedule:
    print(f"{item['name']} : {item['start']} ～ {item['end']}")

print("=====================")

# =========================
# 通知済み管理
# =========================

already_done = set()

# =========================
# メインループ
# =========================

while True:
    kazuto = 0
#while kazuto == 1:
    now = datetime.now().strftime("%H:%M")
    #now = "14:12"
    kazuto = 1
    # -----------------
    # 昼休み予鈴
    # -----------------
    if now == "13:10" and "lunch_warning" not in already_done:

        print("あと5分で5時間目が始まります！")

        already_done.add("lunch_warning")

    # -----------------
    # 日直面談
    # -----------------
    if now == "12:55" and "nichoku" not in already_done:

        print("日直面談の時間です！")

        already_done.add("nichoku")

    # -----------------
    # 授業通知
    # -----------------
    for item in schedule:

        start_key = item["name"] + "_start"
        end_key = item["name"] + "_end"

        # 開始3分前
        notify_time = (
            datetime.strptime(item["start"], "%H:%M")
            - timedelta(minutes=3)
        ).strftime("%H:%M")

        # 3分前通知
        if now == notify_time and start_key not in already_done:

            print(f"あと3分で {item['name']} が始まります！")
            winsound.Beep(1000,1000)

            already_done.add(start_key)

        # 終了通知
        if now == item["end"] and end_key not in already_done:

            print(f"{item['name']} が終わりました！")

            already_done.add(end_key)


    now = datetime.now().strftime("%H:%M")
    state = "放課後です"

    for item in schedule:

        start = datetime.strptime(item["start"], "%H:%M")
        end = datetime.strptime(item["end"], "%H:%M")

        if item["start"] <= now <= item["end"]:
            state = f"{item['name']}の授業中です"
            break

    print(state)

    time.sleep(60)
