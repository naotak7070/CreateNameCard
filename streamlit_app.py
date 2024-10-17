import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from io import BytesIO

# CSVファイルの読み込み
df = pd.read_csv('dummy_data.csv')

# 顧客リストをデータフレームとして表示
st.title("顧客リスト")

# チェックボックスの状態を保存するための辞書
selected_customers = {}

# 各行ごとにデータとチェックボックスを表示
for index, row in df.iterrows():
    selected_customers[index] = st.checkbox(
        label=f"{row['顧客番号']} - {row['氏名']} - {row['会社名']}",
        key=f"checkbox_{index}"
    )

# 「カード作成」ボタン
if st.button("選択した顧客のカードを生成"):
    # 選択された顧客をフィルタリング
    selected_data = df.loc[[index for index, selected in selected_customers.items() if selected]]
    
    if not selected_data.empty:
        st.write(f"{len(selected_data)}件のカードを表示中...")

        for _, row in selected_data.iterrows():
            # QRコードの生成
            qr = qrcode.make(row['顧客番号'])
            qr_image = qr.get_image().resize((150, 150))
            qr_image_buffer = BytesIO()
            qr_image.save(qr_image_buffer, format='PNG')
            qr_image_buffer.seek(0)
            
            # 顧客情報とQRコードを表示
            st.image(qr_image_buffer, caption=f"QRコード - {row['顧客番号']}")
            st.write(f"**会社名**: {row['会社名']}")
            st.write(f"**氏名**: {row['氏名']}")
            st.write(f"**カテゴリ**: {row['カテゴリ']}")
            st.write("---")
    else:
        st.write("選択された顧客がありません。")
