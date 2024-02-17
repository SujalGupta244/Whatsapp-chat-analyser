import re
from urlextract import URLExtract


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
        