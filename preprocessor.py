import re
import pandas as pd


def preprocessor(data):
    patterns = '\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\u202f?[apmAPM]{2}\s-\s'
    messages = re.split(patterns, data)[1:]
    dates = re.findall(patterns, data)

    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    # convert messages_data type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)


    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        print(entry)
        if(entry[1:]): # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
