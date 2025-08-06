import re
from datetime import datetime
import pandas as pd

def preprocess(data):
    # Define pattern to match datetime, user, and message
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2})\u202F?(AM|PM) - (.*?): (.*)'

    messages = []
    dates = []
    users = []

    lines = data.split('\n')
    current_message = ''
    current_date = None
    current_user = None

    for line in lines:
        match = re.match(pattern, line)
        if match:
            # If there's a previous message, save it
            if current_date is not None:
                dates.append(current_date)
                users.append(current_user)
                messages.append(current_message.strip())

            # Extract new message
            date_str = f"{match.group(1)}, {match.group(2)} {match.group(3)}"
            try:
                current_date = datetime.strptime(date_str, '%m/%d/%y, %I:%M %p')
            except:
                current_date = None

            current_user = match.group(4)
            current_message = match.group(5)
        else:
            # Continuation of previous message
            current_message += '\n' + line

    # Save last message
    if current_date is not None:
        dates.append(current_date)
        users.append(current_user)
        messages.append(current_message.strip())

    # Create DataFrame
    df = pd.DataFrame({'user': users, 'message': messages, 'date': dates})
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
