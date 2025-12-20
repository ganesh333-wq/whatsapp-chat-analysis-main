import re
import pandas as pd

def preprocess(data):

    # Pattern supports both 24h and 12h AM/PM WhatsApp formats
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # ---------------- DATE + TIME PARSING ----------------
    # Try 24-hour format first, fallback to 12-hour AM/PM format
    try:
        df['message_date'] = pd.to_datetime(
            df['message_date'],
            format='%d/%m/%Y, %H:%M - '
        )
    except ValueError:
        df['message_date'] = pd.to_datetime(
            df['message_date'],
            format='%d/%m/%Y, %I:%M %p - '
        )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # ---------------- SPLIT USER & MESSAGE ----------------
    users = []
    msgs = []

    for message in df['user_message']:
        # Split into: username : message
        entry = re.split(r'([\w\W]+?):\s', message)

        if entry[1:]:
            users.append(entry[1])
            msgs.append(" ".join(entry[2:]))
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_message'], inplace=True)

    # ---------------- DATE COMPONENTS ----------------
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # ---------------- 12-HOUR TIME DISPLAY ----------------
    df['time_12hr'] = df['date'].dt.strftime("%I:%M %p")

    # ---------------- PERIOD COLUMN (12-HOUR FORMAT) ----------------
    period = []
    for hour in df['hour']:
        start = pd.to_datetime(str(hour), format="%H").strftime("%I %p")
        end = pd.to_datetime(str((hour + 1) % 24), format="%H").strftime("%I %p")
        period.append(f"{start} - {end}")

    df['period'] = period

    return df
