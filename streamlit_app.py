from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
now = datetime.now(ZoneInfo("Asia/Tokyo")).time()

st.write(now)

import time
alarm_time = "11:40"



today = datetime.now(ZoneInfo("Asia/Tokyo")).time()
w_number = today.weekday()

st.write(w_number)
days = ["月","火","水","木","金","土","日",]
st.write({days[w_number]})


from datetime import date, timedelta

year = 2026


# =========================
# 設定
# =========================

CLASS_TIME = 50
BREAK_TIME = 10

FIRST_START = datetime.strptime("08:40", "%H:%M")
LUNCH_END = datetime.strptime("13:15", "%H:%M")

# 月=0 火=1 水=2 木=3 金=4 土=5 日=6
today_weekday = datetime.now(ZoneInfo("Asia/Tokyo")).weekday()
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
st.write("===== 今日の予定 =====")

for item in schedule:
    st.write(f"{item['name']} : {item['start']} ～ {item['end']}")

st.write("=====================")

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
    now = datetime.now(ZoneInfo("Asia/Tokyo")).time().strftime("%H:%M")
    #now = "14:12"
    kazuto = 1
    # -----------------
    # 昼休み予鈴
    # -----------------
    if now == "13:10" and "lunch_warning" not in already_done:

        st.write("あと5分で5時間目が始まります！")

        already_done.add("lunch_warning")

    # -----------------
    # 日直面談
    # -----------------
    if now == "12:55" and "nichoku" not in already_done:

        st.write("日直面談の時間です！")

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

            st.write(f"あと3分で {item['name']} が始まります！")

            already_done.add(start_key)

        # 終了通知
        if now == item["end"] and end_key not in already_done:

            st.write(f"{item['name']} が終わりました！")

            already_done.add(end_key)


    now = datetime.now(ZoneInfo("Asia/Tokyo")).time()
    state = "放課後です"

    for i, item in enumerate(schedule):

        start = datetime.strptime(item["start"], "%H:%M").time()
        end = datetime.strptime(item["end"], "%H:%M").time()

        if start <= now <= end:
            state = f"{item['name']}の授業中です"
            break
        if i < len(schedule)-1:
            next_start = datetime.strptime(schedule[i+1]["start"],"%H:%M").time()
            if end < now < next_start:
                state = "休み時間です"
                break

    st.write(state)

    time.sleep(60)
