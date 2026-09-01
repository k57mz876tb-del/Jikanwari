from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
st.markdown(
    """
    <meta http-equiv="refresh" content="60">
    """,
    unsafe_allow_html=True,
)

now = datetime.now(ZoneInfo("Asia/Tokyo")).time()

st.write(now)

import time
alarm_time = "11:40"



today = datetime.now(ZoneInfo("Asia/Tokyo"))
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

# =========================
# 現在の状態を判定
# =========================

now = datetime.now(ZoneInfo("Asia/Tokyo")).time()

state = "放課後です"

for i, item in enumerate(schedule):

    start = datetime.strptime(item["start"], "%H:%M").time()
    end = datetime.strptime(item["end"], "%H:%M").time()

    # 授業中
    if start <= now < end:
        state = f"{item['name']}の授業中です"
        break

    # 休み時間
    if i < len(schedule) - 1:

        next_start = datetime.strptime(
            schedule[i + 1]["start"], "%H:%M"
        ).time()

        if end <= now < next_start:
            state = "休み時間です"
            break


# =========================
# 色を決める
# =========================

if "授業中" in state:
    bg_color = "#dff5e1"
    text_color = "#267a35"

elif "休み時間" in state:
    bg_color = "#dcecff"
    text_color = "#2864a8"

elif "昼休み" in state:
    bg_color = "#fff1cc"
    text_color = "#9a6800"

else:
    bg_color = "#eeeeee"
    text_color = "#555555"


# =========================
# 大きく表示
# =========================

st.markdown(
    f"""
    <div style="
        background-color: {bg_color};
        color: {text_color};
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 45px;
        font-weight: bold;
    ">
        {state}
    </div>
    """,
    unsafe_allow_html=True
)
