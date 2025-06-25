import streamlit as st
import re

# タイトル
st.title("汎用3C分析プロンプト生成ツール")

# ユーザー入力
service_name = st.text_input("サービス名を入力してください", "サービスA")
market_name = st.text_input("市場名を入力してください", "サービスAの市場")

# ファイルアップロード
ds_file = st.file_uploader("DSインサイト：時系列キーワード（CSV）", type=["csv"])
statistics_file = st.file_uploader("Dockpit：サイトサマリ（statistics.txt）", type=["txt"])
referral_file = st.file_uploader("Dockpit：集客構造（referralType.txt）", type=["txt"])
funnel_self = st.file_uploader("KnownsBIZ：自社ファネル構造（任意・PNG）", type=["png"])
funnel_competitor = st.file_uploader("KnownsBIZ：競合ファネル構造（任意・PNG）", type=["png"])
opinions_self = st.file_uploader("KnownsBIZ：自社商品への意見（任意・CSV）", type=["csv"])
opinions_competitor = st.file_uploader("KnownsBIZ：競合商品への意見（任意・CSV）", type=["csv"])

# テンプレート読み込み
import os

base_path = os.path.dirname(__file__)
template_path = os.path.join(base_path, "Template_3c.txt")

with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

# テキスト置換
replacements = {
    "[[サービス名]]": service_name,
    "[[市場名]]": market_name,
    "[[DSファイル]]": ds_file.name if ds_file else "未アップロード",
    "[[サイトサマリ]]": statistics_file.name if statistics_file else "未アップロード",
    "[[集客構造]]": referral_file.name if referral_file else "未アップロード",
    "[[ファネル自社]]": funnel_self.name if funnel_self else "未使用",
    "[[ファネル競合]]": funnel_competitor.name if funnel_competitor else "未使用",
    "[[意見自社]]": opinions_self.name if opinions_self else "未使用",
    "[[意見競合]]": opinions_competitor.name if opinions_competitor else "未使用",
}

for key, value in replacements.items():
    template_text = template_text.replace(key, value)

# カスタマーセクションの有無
if not (funnel_self and funnel_competitor and opinions_self and opinions_competitor):
    pattern = r"\[\[CUSTOMER_START\]\](.*?)\[\[CUSTOMER_END\]\]"
    template_text = re.sub(pattern, "", template_text, flags=re.DOTALL)
    st.warning("KnownsBIZのデータが未アップロードのため、カスタマー分析セクションは省略されました。")

# 出力
st.subheader("出力プロンプト")
st.download_button("ダウンロード", template_text, file_name="3C_analysis_prompt.txt")
st.text_area("プレビュー", template_text, height=800)
