def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # fetch number of messages
        num_messages = df.shape[0]
        # number of words
        words = []
        for message in df['message']:
            words.extend(message.split())
        return num_messages, len(words)
    else :
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]
        # number of words
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        return num_messages, len(words)
        