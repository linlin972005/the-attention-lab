from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='The Attention Lab',page_icon='◉',layout='wide',initial_sidebar_state='collapsed')
ROOT=Path(__file__).resolve().parent
@st.cache_data
def load_data():
    data=ROOT/'data'
    return (pd.read_csv(data/'instagram_posts_2026-07-25_to_2026-10-25.csv'),
            pd.read_csv(data/'instagram_follower_growth_daily.csv'),
            pd.read_csv(data/'instagram_account_totals_2026-07-25_to_2026-10-25.csv'),
            pd.read_csv(data/'instagram_audience_demographics.csv'))
p,f,t,d=load_data()
p['published_at']=pd.to_datetime(p['published_at'],errors='coerce')
p['weekday']=p['published_at'].dt.day_name()
f['date']=pd.to_datetime(f['date'],errors='coerce')
totals=dict(zip(t['metric'],pd.to_numeric(t['value'],errors='coerce')))
fmt=lambda x: f'{x:,.0f}' if pd.notna(x) else '—'
COLORS=['#77e0c4','#92aaff','#e7b9f8','#f4c47e']
PX={'template':'plotly_dark','color_discrete_sequence':COLORS}
st.markdown('''<style>
.block-container{padding-top:1.0rem;padding-bottom:1.4rem;max-width:1540px}
header[data-testid="stHeader"]{height:2rem;background:transparent}
[data-testid="stAppViewContainer"]{background:#0d121c}
h1,h2,h3{letter-spacing:-.03em}
h1{font-size:1.75rem!important;margin:0!important;padding:0!important}
h3{font-size:1.03rem!important}
[data-testid="stVerticalBlock"]{gap:.55rem}
[data-testid="stMetric"]{background:#171f2d;border:1px solid #2d3648;border-radius:12px;padding:.72rem .9rem}
[data-testid="stMetricLabel"]{font-size:.80rem}
[data-testid="stMetricValue"]{font-size:1.45rem}
[data-baseweb="tab-list"]{gap:.6rem!important;border-bottom:1px solid #344154}
[data-testid="stAppViewBlockContainer"]{padding-left:2rem;padding-right:2rem}
[data-testid="stHorizontalBlock"]{gap:.7rem}
[data-testid="stMetricDelta"]{font-size:.72rem}
[data-testid="stExpander"]{border:1px solid #293548;border-radius:10px}
[data-testid="stPlotlyChart"]{min-height:0!important}
button[data-baseweb="tab"]{padding:.45rem .9rem!important}
[data-testid="stPlotlyChart"]{border:1px solid #2a3445;border-radius:12px;overflow:hidden}
[data-testid="stCaptionContainer"]{font-size:.75rem}
hr{margin:.2rem 0!important}
</style>''',unsafe_allow_html=True)

def chart(fig,height=270):
    fig.update_layout(height=height,margin=dict(l=16,r=20,t=24,b=10),paper_bgcolor='#151d2b',plot_bgcolor='#151d2b',font=dict(size=11,color='#c5d0df'),legend=dict(orientation='h',y=-.2),hovermode='closest')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor='#2c3545',zeroline=False)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

head,sub=st.columns([2,3],vertical_alignment='center')
with head: st.title('◉ The Attention Lab')
with sub: st.markdown('<div style="text-align:right;color:#aebed0;font-size:.82rem">CREATOR INTELLIGENCE <span style="color:#64748b">/</span> JUL–OCT 2026 <span style="color:#64748b">/</span> INSTAGRAM</div>',unsafe_allow_html=True)

A,B,C,D=st.columns(4)
A.metric('Content views',fmt(totals.get('content_views')))
B.metric('Accounts reached',fmt(totals.get('accounts_reached')))
C.metric('Accounts engaged',fmt(totals.get('accounts_engaged')))
delta=int(f.iloc[-1]['follower_count']-f.iloc[0]['follower_count'])
D.metric('Follower change',f'{delta:+,}')

nav=st.tabs(['Overview','Content','Audience','Methods & SQL'])
with nav[0]:
    c1,c2=st.columns([1.65,1],gap='medium')
    with c1:
        st.markdown('**Follower trajectory**')
        fig=px.line(f,x='date',y='follower_count',labels={'date':'','follower_count':'Followers'},**PX)
        fig.update_traces(line_color=COLORS[0],line_width=2.5)
        chart(fig,285)
    with c2:
        st.markdown('**Daily net growth**')
        fig=px.bar(f,x='date',y='net_follower_change',labels={'date':'','net_follower_change':'Net follows'},**PX)
        fig.update_traces(marker_color=COLORS[1])
        chart(fig,285)
    a,b,c=st.columns(3)
    a.metric('Reels in export',fmt(len(p)))
    b.metric('Total Reel likes',fmt(p['likes'].sum()))
    c.metric('Total Reel comments',fmt(p['comments'].sum()))
    with st.expander('Metric definitions and data coverage'):
        st.caption('Account totals are separate from Reel metrics. Follower history ends Oct 24; exported account totals end Oct 25. No per-post reach or views available.')
with nav[1]:
    x,y=st.columns([1,1],gap='medium')
    with x:
        st.markdown('**Reel interaction signals**')
        scatter=px.scatter(p,x='likes',y='comments',hover_data=['caption','published_at'],labels={'likes':'Likes','comments':'Comments'},**PX)
        chart(scatter,285)
    with y:
        st.markdown('**Publishing day patterns**')
        order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        cadence=p.groupby('weekday',as_index=False).agg(posts=('post_id','size'),avg_likes=('likes','mean'))
        cadence['weekday']=pd.Categorical(cadence['weekday'],categories=order,ordered=True)
        cadence=cadence.sort_values('weekday')
        metric=st.segmented_control('Compare',options=['Posts','Average likes'],default='Posts',label_visibility='collapsed')
        key='posts' if metric=='Posts' else 'avg_likes'
        fig=px.bar(cadence,x='weekday',y=key,labels={'weekday':'','posts':'Reels','avg_likes':'Avg likes'},**PX)
        fig.update_traces(marker_color=COLORS[0])
        chart(fig,253)
    with st.expander('Explore individual Reels',expanded=False):
        q=st.text_input('Filter captions',placeholder='Search text…')
        view=p[p['caption'].fillna('').str.contains(q,case=False,regex=False)].sort_values('likes',ascending=False)
        st.dataframe(view[['published_at','caption','likes','comments','url']],hide_index=True,use_container_width=True,height=300)
    st.caption('Reel-level views, reach, shares, saves, and watch time are unavailable. Like counts are not engagement rates; these are descriptive comparisons only.')
with nav[2]:
    left,right=st.columns([1,2],gap='medium')
    with left:
        st.markdown('**Audience segments**')
        dimension=st.radio('Breakdown',options=['age','gender','country','city'],horizontal=False,label_visibility='collapsed')
        st.caption('Snapshot dated Oct 25, 2026, not historical averages.')
    with right:
        dd=d[d['dimension']==dimension].sort_values('follower_count',ascending=False)
        if dimension in ('city','country'): dd=dd.head(12)
        fig=px.bar(dd,x='follower_count',y='category',orientation='h',labels={'follower_count':'Followers','category':''},**PX)
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        fig.update_traces(marker_color=COLORS[1])
        chart(fig,max(295,min(420,len(dd)*27+70)))
    st.caption('Demographic categories may include unknown values. City/country view shows top categories only.')
with nav[3]:
    st.markdown('**Research integrity & experiment design**')
    m1,m2=st.columns(2,gap='large')
    with m1:
        st.markdown('**Available data**')
        st.markdown('- Account-wide views, reach, and engaged accounts\n- Daily follower totals and net changes\n- Individual Reel likes and comments\n- Audience demographics snapshot')
        st.markdown('**Important limitations**')
        st.markdown('- No post-level views, reach, saves, shares, watch time or follows\n- No valid Reel engagement rate or retention calculation\n- Correlation in posting activity is not causation')
    with m2:
        st.markdown('**Proposed experiment (not yet conducted)**')
        st.write('Compare curiosity-based versus straightforward informational hooks using randomly assigned future Reels. Pre-register one primary metric such as shares per 1,000 reached **once reach becomes available**; control for posting times and set an observation window.')
        st.markdown('**SQL portfolio evidence**')
        st.write('The included `analysis.sql` demonstrates aggregations, a JOIN, CTEs and window functions. Inspect and run it before claiming proficiency.')
    with st.expander('Data completeness audit',expanded=False):
        audit=p.notna().sum().to_frame('Posts with data');audit['Coverage (%)']=(audit['Posts with data']/len(p)*100).round(1)
        st.dataframe(audit,use_container_width=True,height=260)
    st.caption('Data retrieved Oct 25, 2026. Reel publications July 29–Oct 23; follower history July 25–Oct 24; account totals July 25–Oct 25.')
