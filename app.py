import streamlit as st
import mainfunc
import matplotlib.pyplot as plt


# st.sidebar.title("Analysis")
st.title('WhatsApp Chat Analyzer')
file = st.file_uploader("Choose a file")



if file:
    df = mainfunc.generateDataFrame(file)
    try:
        dayfirst = st.radio("Select Date Format in text file:", ('dd-mm-yy', 'mm-dd-yy'))
        if dayfirst == 'dd-mm-yy':
            dayfirst = True
        else:
            dayfirst = False
        users = mainfunc.getUsers(df)
        users_s = st.sidebar.selectbox("Select User to View Analysis", users)
        selected_user = ""
        if st.sidebar.button("Show Analysis"):
            selected_user = users_s

            st.title("Showing Results for : " + selected_user)
            df = mainfunc.PreProcess(df,dayfirst)
            if selected_user != "Everyone":
                df = df[df['User'] == selected_user]
            df, media_cnt, deleted_msgs_cnt, links_cnt, word_count, msg_count = mainfunc.getStats(df)
            st.title("Chat Statistics")
            stats_c = ["Total Messages", "Total Words", "Media Shared", "Links Shared", "Messages Deleted"]
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.subheader(stats_c[0])
                st.title(msg_count)
            with c2:
                st.subheader(stats_c[1])
                st.title(word_count)
            with c3:
                st.subheader(stats_c[2])
                st.title(media_cnt)
            with c4:
                st.subheader(stats_c[3])
                st.title(links_cnt)
            with c5:
                st.subheader(stats_c[4])
                st.title(deleted_msgs_cnt)
            if file is not None:
                bytes_data = file.getvalue()
                data = bytes_data.decode("utf-8")
                # st.text(data)+
                # User Activity Count
                if selected_user == 'Everyone':
                    x = df['User'].value_counts().head()
                    name = x.index
                    count = x.values
                    st.title("Messaging Frequency")
                    st.subheader('Messaging Percentage Count of Users')
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
                            columns={'User': 'name', 'count': 'percent'}))
                    with col2:
                        fig, ax = plt.subplots()
                        ax.bar(name, count)
                        ax.set_xlabel("Users")
                        ax.set_ylabel("Message Sent")
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)

                
                emojiDF = mainfunc.getEmoji(df)
                st.title("Emoji Analysis")
                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(emojiDF)
                with col2:
                    fig, ax = plt.subplots()
                    ax.pie(emojiDF[1].head(), labels=emojiDF[0].head(), autopct="%0.2f", shadow=True)
                    plt.legend()
                    st.pyplot(fig)


                sentiment_scores = mainfunc.perform_sentiment_analysis(df['Message'])
                df['Sentiment'] = [score['compound'] for score in sentiment_scores]


                negative_responses = df[df['Sentiment'] < 0]
                positive_responses = df[df['Sentiment'] > 0]
                neutral_response = df[df['Sentiment'] == 0.0]

                st.subheader("User with Negative Response")
                if negative_responses.empty:
                    st.write("No negative responses")
                else:
                    negative_user = negative_responses['User'].iloc[0]
                    st.write(negative_user)

                st.subheader("Total Negative Responses")
                st.write(len(negative_responses))

                st.subheader("Total Neutral Responses")
                st.write(len(neutral_response))

                st.subheader("Total Positive Responses")
                st.write(len(positive_responses))

    except Exception as e:
        st.subheader("Unable to Process Your Request")



