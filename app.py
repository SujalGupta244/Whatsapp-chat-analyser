import streamlit as st
import preprocessor, helper
# st.write("Hello world")
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocessor.preprocess(data)
    # Removing group notifications
    df = df[df['user'] != 'group_notification']
    

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()

    # if "group_notification" in user_list:
    # user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        
        # Stats Area
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("links Shared")
            st.title(links)

        
        # Finding the busiest users in the group(Group Level)
        if(selected_user == 'Overall'):
            busy_users, user_percents = helper.most_busy_users(df)
            fig,ax = plt.subplots(figsize=(8,6)) 
            
            st.title("Most Busy Users")

            col1, col2 = st.columns(2)
    
            with col1:
                names = busy_users.index
                count = busy_users.values
                ax.bar(names,count)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(user_percents)

        # WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
                
            
        # Most Used Word
        st.title("Most Used Words")
        # Removing media omitted
        df = df[df['message'] != '<Media omitted>\n']
        most_used_words = helper.most_used_words(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.barh(most_used_words[0], most_used_words[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        # st.dataframe(most_used_words)

        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji(selected_user, df)
        st.dataframe(emoji_df)