import json
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='Multi-view Data · CDWorld',page_icon='🎬',layout='wide')
ROOT=Path(__file__).parent
@st.cache_data
def load(name):
    return json.loads((ROOT/name).read_text(encoding='utf8'))
manifest=load('samples.json')
public_base=load('site_base.json')['base_url'] if (ROOT/'site_base.json').exists() else manifest['public_base_url']
def url(name):
    p=ROOT/name
    return str(p) if p.exists() else public_base+name

st.title('Multi-view Data Gallery')
st.caption('GTA replay · GTA anime · DL3DV | 3 samples per domain | Training input & evidence')
group=st.sidebar.radio('数据来源',['GTA replay','GTA anime','DL3DV'])
options=[s for s in manifest['samples'] if s['group']==group]
sid=st.sidebar.selectbox('选择样本',[s['id'] for s in options],format_func=lambda x:next(s['title'] for s in options if s['id']==x))
s=next(s for s in options if s['id']==sid)
c=load(s['camera']);poses=np.asarray(c['c2w']);K=np.asarray(c['K'])
st.sidebar.info('展示包共 9 条。指标取自已有交付和实测记录；此页不改变训练准入状态。')
st.sidebar.caption('视频为有损、缩小的展示预览。左 A / view0；右 B / view1。')
st.subheader(s['title'])
st.caption('Source: '+s['source_id'])
a,b,d,e=st.columns(4)
a.metric('原交付尺寸',f"{s['width']} × {s['height']}")
b.metric('帧 / FPS',f"{s['frames']} / {s['fps']}")
d.metric('首末 PTS 跨度',f"{s['pts_span_s']} s")
e.metric('LTX latent 时刻',str(s['latent_frames']))
st.video(url(s['video']))
st.caption('左右已合成为同一视频，确保两路播放同步。下方几何帧由滑块单独选择，不自动跟随播放器。')
tabs=st.tabs(['相机与时间','训练条件','数值证据'])
with tabs[0]:
    if len(poses)<s['frames']:
        st.warning(f'本地交付仅有 {len(poses)} 个相机关键帧。只展示实测点，不补齐或插值成逐帧相机。')
    j=st.select_slider('几何帧 / 视频 PTS',options=list(range(len(poses))),format_func=lambda n:f"frame {c['frame_indices'][n]} · {c['video_seconds'][n]:.3f}s",value=0)
    fig=go.Figure()
    allpos=poses[:,:,:3,3];span=max(float(np.ptp(allpos.reshape(-1,3),axis=0).max()),1.)
    axislen=span*.12
    for vi,color in enumerate(['#22b8cf','#ff922b']):
        p=allpos[:,vi];fig.add_trace(go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode='lines+markers' if len(p)<10 else 'lines',name=['A / view0','B / view1'][vi],line=dict(color=color,width=5)))
        m=poses[j,vi];o=m[:3,3]
        fig.add_trace(go.Scatter3d(x=[o[0]],y=[o[1]],z=[o[2]],mode='markers',marker=dict(color=color,size=6),name=f'current {vi}'))
        for ax,clr in enumerate(['#ff4b4b','#2ecc71','#4287ff']):
            end=o+m[:3,ax]*axislen
            fig.add_trace(go.Scatter3d(x=[o[0],end[0]],y=[o[1],end[1]],z=[o[2],end[2]],mode='lines',line=dict(color=clr,width=6),showlegend=False))
        # Image-plane frustum based on the actual output-pixel K.
        corners=np.array([[0,0,1],[s['width'],0,1],[s['width'],s['height'],1],[0,s['height'],1]])
        rays=corners@np.linalg.inv(K[j,vi]).T
        q=(rays*axislen*1.4)@m[:3,:3].T+o
        for n in range(4):
            seg=np.array([o,q[n],q[(n+1)%4]])
            fig.add_trace(go.Scatter3d(x=seg[:,0],y=seg[:,1],z=seg[:,2],mode='lines',line=dict(color=color,width=2),showlegend=False))
    fig.update_layout(height=460,margin=dict(l=0,r=0,t=10,b=0),scene=dict(aspectmode='data',xaxis_title='World X',yaxis_title='World Y',zaxis_title='World Z'),legend=dict(orientation='h'))
    st.plotly_chart(fig,use_container_width=True)
    st.caption('RGB 分别为相机 X右 / Y下 / Z前。相机轨迹及视锥直接使用导出坐标；可拖动旋转三维视图。')
    st.write('**坐标与尺度：** '+c['axes']+' · '+c['units'])
    st.caption('Reference: '+c['reference']+' | '+c['scope'])
    if c.get('world_seconds') is not None:
        w=np.asarray(c['world_seconds']);tf=go.Figure()
        for vi,color in enumerate(['#22b8cf','#ff922b']):
            tf.add_trace(go.Scatter(x=c['video_seconds'],y=w[:,vi],name=f'world time {vi}',mode='markers' if len(w)<10 else 'lines',line=dict(color=color)))
        tf.update_layout(height=240,xaxis_title='Video PTS (s)',yaxis_title='Declared world time (s)',margin=dict(l=5,r=5,t=10,b=5))
        st.plotly_chart(tf,use_container_width=True)
    with st.expander('当前帧两路 c2w / K 与相机数据下载'):
        for vi in range(2):
            st.write(f'View {vi} · c2w');st.dataframe(poses[j,vi]);st.write('K');st.dataframe(K[j,vi])
        st.link_button('打开全部相机 JSON ↗',public_base+s['camera'])
with tabs[1]:
    st.write('**消费协议：** `'+manifest['training_contract']+'`')
    st.caption('241=8×30+1 → 31 latent 时刻；图像底部复制 padding 到32倍数。当前标准预处理宽640；GTA旧交付960×544尚需按正式路径重新绑定转换与验证。')
    st.table([{'训练条件':k,'现有证据 / 状态':v} for k,v in s['conditions'].items()])
    st.warning(s['training_admission'])
    for note in s['notes']:st.write('• '+note)
    st.caption('GTA 动画字典或画面中的动作不等于已编译的主体控制标注。未知字段不会自动填成零；派生相机数值检查通过也不等于像素标定通过。')
with tabs[2]:
    st.write('已有审核、几何与 loader 证据（不同域的检查方法不可直接比较成一个准确率）')
    st.json(s['qc'])
    st.caption('无自动生成的全绿结论；缺失项保持未知。9个展示样本不构成全库质量或准确率认证。')
st.divider()
st.caption('CDWorld · Demonstration snapshot 2026-10-17 · No training is started by this page')
