import streamlit as st
import os

# 定位脚本所在目录，确保路径绝对正确
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

#大标题
st.title("The first title")
st.header("Teh first header")
st.subheader("The second title")

#写入文字
st.write("疾风本名克莱尔·安·拜尔斯，是极限运动选手，脊椎重伤后接受哈夫克集团机械改造。植入的辅助脊椎重塑了她的行动能力，代价是永远受制于这套机械义体，昔日追风的冒险者，最终成为哈夫克执行高危任务的突击尖刀")
st.write("疾风拥有极强的机动突击能力，战术翻滚灵活拉扯枪线，辅助脊椎受到战火刺激便可获得移速增益。专属电刺能够穿透墙体，隔墙眩晕、缴械掩体后方的敌人，专门克制固守点位的架枪对手，轻松撕开敌方防线。")
st.write("紧急回避锚点是疾风的核心底牌。她可以大胆前压突进，身陷险境时瞬间回溯至锚点位置，倒地状态下亦能依靠技能争取自救机会。灵活突进、进退自如，是擅长打乱敌方阵型的侵略型突击干员。")
#图片
st.image(os.path.join(SCRIPT_DIR, "resources", "疾风2.jpg"), width=400)
#音频
st.audio(os.path.join(SCRIPT_DIR, "resources", "i'm waiting.mp3"))
#视频
video_path = os.path.join(SCRIPT_DIR, "resources", "xg.mp4")
st.video(video_path, format="video/mp4")
#logo
st.logo("./resources/logo.jpg")
#表格
ganyuan_data = {

}