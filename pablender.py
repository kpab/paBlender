import streamlit as st
import pandas as pd

df = pd.read_csv("blender_movie.csv", encoding="utf_8")

level_list = [1, 2, 3, 4]
category_list = ["キャラクター", "建物", "アイテム", "食べ物"]
multi_list = ["初心者おすすめ", "日本語解説", "アニメーション"]

st.set_page_config( # ページの設定
    page_title="paBlender"
)

# with st.form(key='form'):
st.title("Blender 動画検索ツール ")
level = st.radio("難易度",( 1, 2, 3, 4), horizontal=True, index=None)
category = st.selectbox("カテゴリを選択してください", category_list, index=None)
keyword = st.text_input('キーワード検索')
check = st.checkbox("こだわり検索")
if check:
    begginer_check = st.toggle("初めての人におすすめ")
    explanation_check = st.toggle("解説あり")
    animation_check = st.toggle('アニメーション')
    pab_check = st.toggle('ぱぶオススメ')
submit_btn = st.button('検索')


if(submit_btn):
    result_list = [] # 結果出力用リスト初期化
    if level == None: # カテゴリ未選択の場合、全て表示
            level = level_list;
    if category == None: # カテゴリ未選択の場合、全て表示
            category = category_list
    result = df.query('Level == @level & Category == @category & Keyword.str.contains(@keyword)', engine='python') # 難易度,カテゴリソート ,キーワード検索
    if check:
        if begginer_check: # 初心者ソート
            result = result.query('Beginner == 1')
        if explanation_check: # 解説ソート
            result = result.query('Explanation == 1')
        if animation_check: # アニメーションソート
            result = result.query('Animation == 1')
        if pab_check: # ぱぶソート
            result = result.query('Pab == 1')
    if level != None:
        st.success(f"{len(result)}件見つかりました!!")
        st.balloons()
    

    for data in result.itertuples():
        st.header(data.Name, divider='rainbow')
        id = data.url[32:]
        image_link = f'http://img.youtube.com/vi/{id}/mqdefault.jpg'
        st.image(image_link, caption=f"難易度⭐︎{data.Level}")
        
        if data.Beginner == 1:
            st.caption('初めての方向け')
        if data.Explanation == 1:
            st.caption('解説あり')
        if data.Animation == 1:
            st.caption('アニメーション')
        if data.Pab == 1:
            st.caption('ぱぶオススメ')
        st.text(data.Comment)

        st.link_button('Youtube', data.url)

    back_btn = st.button('戻る')
    if back_btn:
        st.rerun()