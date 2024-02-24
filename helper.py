import re
from urlextract import URLExtract

from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
# from emot.emo_unicode import UNICODE_EMO
# from emot.emoticons import EMOTICONS, EMOTICONS_EMO
# import emot

# text_with_emoticons = "Feeling happy :-) 😊"
# emoticons = emot.emoticons(text_with_emoticons)
# print(emoticons)
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # fetch number of messages
    num_messages = df.shape[0]
    words = []
    
    # number of words
    for message in df['message']:
        words.extend(message.split())
    
    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # fetch number of link messages
    # pattern = 'https:.+'
    links = []
    extractor = URLExtract()
    for message in df['message']:
        # entry = re.findall(pattern,message)
        links.extend(extractor.find_urls(message))
    # print(links)
    return num_messages, len(words), num_media_messages, len(links)
        

def most_busy_users(df):
    # busy user
    users = df['user'].value_counts().head()

    # perctage of messages
    users_percent = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index': "name", 'user': 'percent'})
    # print(users_percent)
    return users, users_percent
    # print(users)


def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
 
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    # Removing 'media omitted' and 'message deleted'
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'This message was deleted\n']
        
    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
    df['message'] = df['message'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white', random_state=42)
    # .generate_from_frequencies(df['message'])
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc



def most_used_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    words = []

    df = df[df['message'] != 'This message was deleted\n']

    for messages in df['message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)
    words = pd.DataFrame(Counter(words).most_common(20))

    # print(words)
    return words


def emoji(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # emojis = []
    # for message in df['message']:
    #     emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    # print(emoji)
    # emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df = []

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Monthly timeline
    df["month_num"] = df['date'].dt.month
    timeline = df.groupby(['year', "month_num",'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Daily timeline
    timeline = df.groupby('only_date').count()['message'].reset_index()

    return timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity = df.pivot_table(index='day_name',columns='period', values='message',aggfunc='count').fillna(0)
    return activity