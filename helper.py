import re
from urlextract import URLExtract

from wordcloud import WordCloud
from collections import Counter
import pandas as pd



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

    print(words)
    return words