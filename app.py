from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='@linsvideodiary | Instagram Insights',page_icon='◉',layout='wide',initial_sidebar_state='collapsed')
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
COLORS=['#635bdb','#40a9a0','#dc9d4b','#9a7ad4']
PX={'template':'plotly_white','color_discrete_sequence':COLORS}
st.markdown('''<style>
.block-container{padding:2.5rem 2.4rem 1.4rem;max-width:none}
[data-testid="stAppViewContainer"]{background:#f7f8fc;color:#202637}
header[data-testid="stHeader"]{background:transparent}
h1,h2,h3{letter-spacing:-.035em}
h1{font-size:clamp(1.5rem,2.3vw,2.15rem)!important;padding:0!important;line-height:1.35!important}
[data-testid="stVerticalBlock"]{gap:.7rem}
[data-testid="stMetric"]{background:white;border:1px solid #e4e7f0;border-radius:14px;padding:1rem 1.2rem;min-height:106px;box-shadow:0 3px 12px #20263704}
[data-testid="stMetricLabel"]{color:#637087;font-size:.85rem}
[data-testid="stMetricValue"]{font-size:1.85rem;font-weight:650;letter-spacing:-.04em;color:#202637}
[data-baseweb="tab-list"]{gap:1.3rem!important;border-bottom:1px solid #e1e5ee;margin:.3rem 0 .6rem}
button[data-baseweb="tab"]{padding:.5rem .15rem!important;font-size:.9rem}
button[data-baseweb="tab"][aria-selected="true"]{color:#635bdb}
[data-testid="stHorizontalBlock"]{gap:1rem}
[data-testid="stExpander"]{background:white;border:1px solid #e4e7f0;border-radius:12px}
[data-testid="stPlotlyChart"]{background:white;border:1px solid #e4e7f0;border-radius:14px;overflow:hidden}
[data-testid="stCaptionContainer"]{color:#66738a;font-size:.8rem}
.eyebrow{font-size:.72rem;letter-spacing:.14em;color:#635bdb;font-weight:700;margin-bottom:.4rem}
.subtitle{color:#66738a;font-size:.95rem;margin:.35rem 0 .85rem}
.insight{background:#eeecfb;border:1px solid #dedaf7;padding:.8rem 1rem;border-radius:12px;color:#49417e;font-size:.88rem}
@media(max-width:760px){.block-container{padding:2rem 1rem}h1{font-size:1.45rem!important}[data-testid="stMetricValue"]{font-size:1.5rem}}
</style>''',unsafe_allow_html=True)

def chart(fig,height=270):
    fig.update_layout(height=height,margin=dict(l=24,r=24,t=24,b=42),paper_bgcolor='#ffffff',plot_bgcolor='#ffffff',font=dict(size=12,color='#637087'),legend=dict(orientation='h',y=-.2),hovermode='closest')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor='#edf0f6',zeroline=False)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

st.markdown('<div class="eyebrow">CREATOR ANALYTICS · JUL 25 – OCT 25, 2026</div>',unsafe_allow_html=True)
st.markdown('<h1><span style="white-space:nowrap">@linsvideodiary</span> | Instagram Insights</h1>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">A closer look at content, audience and growth</div>',unsafe_allow_html=True)

A,B,C,D=st.columns(4)
A.metric('Content views',fmt(totals.get('content_views')))
B.metric('Accounts reached',fmt(totals.get('accounts_reached')))
C.metric('Accounts engaged',fmt(totals.get('accounts_engaged')))
delta=int(f.iloc[-1]['follower_count']-f.iloc[0]['follower_count'])
D.metric('Follower change',f'{delta:+,}')

nav=st.tabs(['Overview','Content','Audience','Methods & SQL'])
with nav[0]:
    c1,c2=st.columns([1,1],gap='medium')
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
    st.markdown(f'<div class="insight"><b>Growth snapshot</b> · Followers grew from {fmt(f.iloc[0]["follower_count"])} to {fmt(f.iloc[-1]["follower_count"])} ({delta / f.iloc[0]["follower_count"]:.1%}) across the observed history. Publishing patterns below are descriptive, not evidence of causation.</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    a.metric('Reels in export',fmt(len(p)))
    b.metric('Total Reel likes',fmt(p['likes'].sum()))
    c.metric('Total Reel comments',fmt(p['comments'].sum()))
    with st.expander('Metric definitions and data coverage'):
        st.caption('Follower change is last minus first observed total (13,162 − 5,695 = 7,467). Summing daily net changes gives 7,470 because July 25 includes +3 versus the preceding day outside the observed totals. Account totals are separate from Reel metrics. Follower history ends Oct 24; exported account totals end Oct 25. No per-post reach or views available.')
with nav[1]:
    x,y=st.columns([1,1],gap='medium')
    with x:
        st.markdown('**Reel interaction signals**')
        scatter=px.scatter(p,x='likes',y='comments',hover_data=['published_at'],labels={'likes':'Likes','comments':'Comments'},**PX)
        st.caption('Likes and comments at retrieval · one point per Reel')
        chart(scatter,285)
    with y:
        st.markdown('**Publishing day patterns**')
        order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        cadence=p.groupby('weekday',as_index=False).agg(posts=('post_id','size'),avg_likes=('likes','mean'))
        cadence['weekday']=pd.Categorical(cadence['weekday'],categories=order,ordered=True)
        cadence=cadence.sort_values('weekday')
        metric=st.radio('Compare',options=['Posts','Average likes'],horizontal=True,label_visibility='collapsed')
        key='posts' if metric=='Posts' else 'avg_likes'
        fig=px.bar(cadence,x='weekday',y=key,labels={'weekday':'','posts':'Reels','avg_likes':'Avg likes'},**PX)
        fig.update_traces(marker_color=COLORS[0])
        chart(fig,285)
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
    with st.expander('Read the SQL analysis'):
        st.code((ROOT / 'analysis.sql').read_text(), language='sql')
    with st.expander('Data completeness audit',expanded=False):
        audit=p.notna().sum().to_frame('Posts with data');audit['Coverage (%)']=(audit['Posts with data']/len(p)*100).round(1)
        st.dataframe(audit,use_container_width=True,height=260)
    st.caption('Data retrieved Oct 25, 2026. Reel publications July 29–Oct 23; follower history July 25–Oct 24; account totals July 25–Oct 25.')
