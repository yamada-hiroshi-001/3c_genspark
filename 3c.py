import streamlit as st
import re

# タイトル
st.title("GenSpark用3C分析プロンプト生成ツール")
st.markdown("""
ツールには下記のデータが必要です：

- **DSインサイト時系列キーワード**（調べたいサービス名）
- **Dockpit サイトサマリ**（Dockpitで調査した競合のサイトサマリ）
- **Dockpit 集客構造**（Dockpitで調査した集客構造）
- **KnownsBIZ ファネル構造**（KnownsBIZで調査した自社と競合のファネル）
- **KnownsBIZ 商品・サービスへの意見**（KnownsBIZで調査した自社と競合のユーザーの意見）

⚠️ 上記以外の形式や文字コードで読み込むとエラーが出ることがあります。  
すべて入力後にページ下部にGenSparkでの利用を想定したプロンプトが出ます。
GenSparkのＡＩスライドに上記のファイルをアップの上、プロンプトを張り付けることにより、まぁまぁ精度の高い３Ｃ分析ファイルが出来上がる（はず）です。
GenSparkのＡＩスライドはＰＰＴでＤＬできますので、細かい修正はＰＰＴ上で行ってください。
自分でテキスト書くよりは早いと思います。
事前に内容・形式を確認の上でご利用ください。
""")

# ユーザー入力
service_name = st.text_input("サービス名を入力してください", "サービスA")
service_url = st.text_input("サービス名のURLを入力してください", "URL")
market_name = st.text_input("市場名を入力してください", "サービスAの市場")

# ファイルアップロード
ds_file = st.file_uploader("DSインサイト：時系列キーワード（CSV）DSインサイトで対象のサービス名での時系列KWのCSVファイル", type=["csv"])
statistics_file = st.file_uploader("Dockpit：サイトサマリ（statistics.txt）DockPitのサイトサマリ（競合含むユーザー数・セッション数などの基本情報）のTXTファイル", type=["txt"])
referral_file = st.file_uploader("Dockpit：集客構造（referralType.txt）DockPitの集客構造サマリ（競合含む自然検索経由・検索広告経由の流入などの集客構造）のTXTファイル", type=["txt"])
funnel_self = st.file_uploader("KnownsBIZ：自社ファネル構造（任意・PNG）KnownsBizからファネル構造の画像ファイルをDLしてアップ", type=["png"])
funnel_competitor = st.file_uploader("KnownsBIZ：競合ファネル構造（任意・PNG）KnownsBizからファネル構造の画像ファイルをDLしてアップ", type=["png"])
opinions_self = st.file_uploader("KnownsBIZ：自社商品への意見（任意・CSV）KnownsBizから対象ブランドの顧客の意見のCSVをDLしてアップ", type=["csv"])
opinions_competitor = st.file_uploader("KnownsBIZ：競合商品への意見（任意・CSV）KnownsBizからベンチマークブランドの顧客の意見のCSVをDLしてアップ", type=["csv"])

# テンプレート読み込み
with open("Template_3c.txt", "r", encoding="utf-8") as f:
    template_text = f.read()

# テキスト置換
replacements = {
    "[[サービス名]]": service_name,
    "[[市場名]]": market_name,
    "[[URL]]": service_url,
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
