import tweepy
from datetime import datetime,timezone
import pytz
import pandas as pd
import streamlit as st

api_key = 'CiFuUOBj3omKqno4oCRlxV7nA'
api_secret = 'iMQ1K2T7eymc41L0PzvhFNlDlVlwoCFRYjJ4HSmG3LgFCgNDvn'
access_key = '1341737879291060231-ntyoRZ9fNzmM9CDEBgGPi1UjK6QtFB'
access_secret = 'mzPaS8mnhiTAYRqL6x1JBGkGx5qEdjJzLPNoNE6PjkK19'

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

st.title("キレイパスtwitterアカウント")

answer = st.button('データ取得')
searchkey = '"キレイパス"'
item_num = 900

# tweets = tweepy.Cursor(api.search,q=searchkey,lang='ja').items(item_num)


if answer == True:
    # @st.cache
    def test():
        tweets = tweepy.Cursor(api.search,q=searchkey,lang='ja').items(item_num)
        return tweets
    tweets = test()


    def change_time_JST(u_time):
        #イギリスのtimezoneを設定するために再定義する
        utc_time = datetime(u_time.year, u_time.month,u_time.day, \
        u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
        #タイムゾーンを日本時刻に変換
        jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
        # 文字列で返す
        str_time = jst_time.strftime("%Y-%m-%d")
        return str_time

    tweet_data = []
    for tweet in tweets:
        #ツイート時刻とユーザのアカウント作成時刻を日本時刻にする
        tweet_time = change_time_JST(tweet.created_at)
        create_account_time = change_time_JST(tweet.user.created_at)
        #tweet_dataの配列に取得したい情報を入れていく
        tweet_data.append([
            tweet.id,
            tweet_time,
            tweet.text,
            tweet.favorite_count, 
            tweet.retweet_count, 
            tweet.user.id, 
            tweet.user.screen_name,
            tweet.user.name,
            tweet.user.description,
            tweet.user.friends_count,
            tweet.user.followers_count,
            create_account_time,
            tweet.user.following,
    #         tweet.user.profile_image_url,
    #         tweet.user.profile_background_image_url,
    #         tweet.user.url
                        ])

    labels=[
        'ツイートID',
        'ツイート時刻',
        'ツイート内容',
        'いいね数',
        'リツイート数',
        'ID',
        'ユーザID',
        'アカウント名',
        '自己紹介文',
        'フォロー数',
        'フォロワー数',
        'アカウント作成日時',
        '自分がフォローしているか？',
    #     'アイコン画像URL',
    #     'ヘッダー画像URL',
    #     'WEBサイト'
        ]

    df = pd.DataFrame(tweet_data,columns=labels)

    df = df[~df['ユーザID'].str.contains('kireipas')]
    # df = df[~df['ツイート内容'].str.contains('RT')]
    # 特定のユーザーを除く

    dfa = df[["ツイート時刻","ユーザID","アカウント名","ツイート内容"]]

    # dfa = dfa.set_index("ツイート時刻")

    # file_name='tweet_data.csv'
    # dfa.to_csv(file_name,encoding='utf-8-sig',index=False)

    dfs = df[["ツイート時刻","ツイートID"]]
    dfs = dfs.groupby('ツイート時刻').count()
    dfs = dfs.rename(columns={'ツイートID': 'ツイート数'})
    dfs = dfs.sort_values('ツイート時刻',ascending=False)
    # dfs
    st.bar_chart(dfs)



    st.table(dfa)

