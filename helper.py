from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

# ------------------------ BASIC STATS ------------------------
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    # Count words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Count media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Count links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


# ------------------------ BUSIEST USERS ------------------------
def most_busy_users(df):
    x = df['user'].value_counts().head()

    df_percent = (
        (df['user'].value_counts() / df.shape[0]) * 100
    ).round(2)

    df_percent = df_percent.reset_index()
    df_percent.columns = ['name', 'percent']

    return x, df_percent


# ------------------------ WORDCLOUD ------------------------
def create_wordcloud(selected_user, df):

    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        clean_words = []
        for word in message.lower().split():
            if word not in stop_words:
                clean_words.append(word)
        return " ".join(clean_words)

    temp['message'] = temp['message'].apply(remove_stop_words)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    return wc.generate(temp['message'].str.cat(sep=" "))


# ------------------------ MOST COMMON WORDS ------------------------
def most_common_words(selected_user, df):

    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[
        (df['user'] != 'group_notification') &
        (df['message'] != '<Media omitted>\n')
    ]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    word_count = Counter(words).most_common(20)

    return pd.DataFrame(word_count, columns=['word', 'count'])


# ------------------------ EMOJI ANALYSIS ------------------------
def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Prevent crash when no emojis found
    if len(emojis) == 0:
        return pd.DataFrame(columns=['emoji', 'count'])

    emoji_counts = Counter(emojis)

    emoji_df = pd.DataFrame(
        emoji_counts.items(),
        columns=['emoji', 'count']
    ).sort_values(by='count', ascending=False)

    return emoji_df


# ------------------------ MONTHLY TIMELINE ------------------------
def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline


# ------------------------ DAILY TIMELINE ------------------------
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date').count()['message'].reset_index()


# ------------------------ ACTIVITY MAP ------------------------
def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


# ------------------------ HEATMAP ------------------------
def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)
