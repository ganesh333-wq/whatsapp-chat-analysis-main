import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

st.sidebar.title("WhatsApp Chat Analyzer")

# Upload file (.txt or .zip)
uploaded_file = st.sidebar.file_uploader(
    "Upload WhatsApp chat (.txt or .zip)",
    type=["txt", "zip"]
)

if uploaded_file is not None:

    # Handle ZIP chats
    if uploaded_file.name.endswith(".zip"):
        with zipfile.ZipFile(uploaded_file, "r") as z:
            txt_files = [f for f in z.namelist() if f.endswith(".txt")]

            if not txt_files:
                st.error("ZIP does not contain any .txt file")
                st.stop()

            data = z.read(txt_files[0]).decode("utf-8")

    else:
        data = uploaded_file.getvalue().decode("utf-8")

    df = preprocessor.preprocess(data)

    # Prepare users
    user_list = df['user'].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyze", user_list)

    if st.sidebar.button("Show Analysis"):

        # ---------- TOP STATS ----------
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media", num_media)
        col4.metric("Links", num_links)

        # ---------- MONTHLY TIMELINE ----------
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # ---------- DAILY TIMELINE ----------
        st.title("Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily["only_date"], daily["message"], color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # ---------- ACTIVITY ----------
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Busy Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color="purple")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.subheader("Busy Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # ---------- HEATMAP ----------
        st.title("Weekly Activity Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(heatmap, ax=ax)
        st.pyplot(fig)

        # ---------- BUSIEST USERS ----------
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # ---------- WORDCLOUD ----------
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # ---------- MOST COMMON WORDS ----------
        st.title("Most Common Words")
        common = helper.most_common_words(selected_user, df)

        if not common.empty:
            fig, ax = plt.subplots()
            ax.barh(common["word"], common["count"])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        else:
            st.write("No common words found.")

        # ---------- EMOJI ANALYSIS ----------
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            if not emoji_df.empty:
                ax.pie(
                    emoji_df["count"].head(),
                    labels=emoji_df["emoji"].head(),
                    autopct="%0.2f"
                )
            else:
                ax.text(0.5, 0.5, "No Emojis Found", ha="center", va="center")
            st.pyplot(fig)
