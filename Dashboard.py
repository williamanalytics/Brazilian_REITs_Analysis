import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

URL = 'https://www.fundsexplorer.com.br/ranking'
answer = requests.get(URL)

data = pd.read_html(answer.content)[0]

data.sort_values('Códigodo fundo', inplace=True)

data.columns = [
    'Ticker', 'Sector', 'Price', 'Daily liquidity',
    'Dividend', 'DY', '3m DY acc.', '6m DY acc.',
    '12m DY acc.', 'DY 3m', 'DY 6m', 'DY 12m',
    'DY year', 'Price Variation', 'Rent. of period', 'Rent. acc.',
    'Patrimonio_liquido', 'VPA', 'P/BV', 'DY patrimonial',
    'Variacao patrimonial', 'Rentab patrimonial no periodo',
    'Rentabilidade patrimonial acumulada', 'Vacancy', 'Vacancia financeira',
    'Qty of assets'
]

selectioned = [
  'Ticker', 'Sector', 'Price', 'Vacancy', '3m DY acc.', '6m DY acc.', '12m DY acc.', 'P/BV', 'Qty of assets', 'Daily liquidity']

data = data[selectioned]

data.isnull().sum()

setor_null = data[data['Sector'].isna()].index
data.drop(setor_null, inplace=True)

columns_floats = list(data.iloc[:, 2:-1])
data[columns_floats] = data[columns_floats].fillna(value=0)

data[columns_floats] = data[columns_floats].applymap(
    lambda x: str(x).replace('R$ ', '').replace('.0', '').replace('%', '').replace('.', '').replace(',', '.'))
data[columns_floats] = data[columns_floats].astype('float')

data['P/BV'] = data['P/BV'] / 100

metrics_sector = data.groupby('Sector').agg(['mean', 'std'])


def filtrar(data, sector, label_sector='Sector'):

    metrics_sector = data.groupby('Sector').agg(['mean', 'std'])

    df_sector = data[data[label_sector].isin([sector])]

    if sector == 'Títulos e Val. Mob.':
        filtro_ = \
            (df_sector['P/BV'] < 0.9) & \
            (df_sector['P/BV'] > .50) & \
            (df_sector['12m DY acc.'] > metrics_sector.loc[sector, ('12m DY acc.', 'mean')]) & \
            (df_sector['Daily liquidity'] >= metrics_sector.loc[sector, ('Daily liquidity', 'mean')])

    else:
        filtro_ = \
            (df_sector['Qty of assets'] > 5) & \
            (df_sector['P/BV'] < 0.9) & \
            (df_sector['P/BV'] > .50) & \
            (df_sector['12m DY acc.'] > metrics_sector.loc[sector, ('12m DY acc.', 'mean')]) & \
            (df_sector['Daily liquidity'] >= metrics_sector.loc[sector, ('Daily liquidity', 'mean')])

    return df_sector[filtro_]


data['Sector'].unique()
data['Sector'] = data['Sector'].replace({'Lajes Corporativas': 'Corporate', 'Shoppings': 'Commercial',
                                         'Logística': 'Logistics', 'Títulos e Val. Mob.': 'FOF', 'Híbrido': 'Hybrid',
                                         'Residencial': 'Residential', 'Outros': 'Others'})

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

infoType = st.sidebar.radio("Choose one of options below:", ('Home', 'Analyse by Sectors', 'Ranking of REITs', 'Strategy'))

if infoType == 'Home':

    kpi1, kpi2, kpi3 = st.columns(3)

    dropdown = st.sidebar.selectbox('', pd.unique(data['Ticker']))

    with kpi1:
        st.subheader("**Price (R$)**")
        data1 = pd.DataFrame(data)
        data1 = data1[data1['Ticker'] == dropdown]
        data1 = float(data1[data1.columns[data1.columns != 'Ticker']].reset_index().iloc[:, -8])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data1}</h1>", unsafe_allow_html=True)

    with kpi2:
        st.subheader("**Vacancy (%)**")
        data2 = pd.DataFrame(data)
        data2 = data2[data2['Ticker'] == dropdown]
        data2 = float(data2[data2.columns[data2.columns != 'Ticker']].reset_index().iloc[:, -7])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data2}</h1>", unsafe_allow_html=True)

    with kpi3:
        st.subheader("**Sector**")
        data3 = pd.DataFrame(data)
        data3 = data3[data3['Ticker'] == dropdown]
        data3 = data3[data3.columns[data3.columns != 'Ticker']].reset_index().iloc[:, -9].astype('str')
        data3 = (data3.str.cat(sep='\n'))
        st.caption(f"<h1 style='text-align: left; color: #428ADE;'>{data3}</h1>", unsafe_allow_html=True)
        pass

    kpi01, kpi02, kpi03 = st.columns(3)

    with kpi01:
        st.subheader("**3m DY acc. (%)**")
        data4 = pd.DataFrame(data)
        data4 = data4[data4['Ticker'] == dropdown]
        data4 = float(data4[data4.columns[data4.columns != 'Ticker']].reset_index().iloc[:, -6])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data4}</h1>", unsafe_allow_html=True)

    with kpi02:
        st.subheader("**6m DY acc. (%)**")
        data5 = pd.DataFrame(data)
        data5 = data5[data5['Ticker'] == dropdown]
        data5 = float(data5[data5.columns[data5.columns != 'Ticker']].reset_index().iloc[:, -5])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data5}</h1>", unsafe_allow_html=True)

    with kpi03:
        st.subheader("**12m DY  acc. (%)**")
        data6 = pd.DataFrame(data)
        data6 = data6[data6['Ticker'] == dropdown]
        data6 = float(data6[data6.columns[data6.columns != 'Ticker']].reset_index().iloc[:, -4])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data6}</h1>", unsafe_allow_html=True)

    kpi001, kpi002, kpi003 = st.columns(3)

    with kpi001:
        st.subheader("**Price per Book Value (%)**")
        data7 = pd.DataFrame(data)
        data7 = data7[data7['Ticker'] == dropdown]
        data7 = float(data7[data7.columns[data7.columns != 'Ticker']].reset_index().iloc[:, -3])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data7}</h1>", unsafe_allow_html=True)

    with kpi002:
        st.subheader("**Quantity of fund's assets**")
        data8 = pd.DataFrame(data)
        data8 = data8[data8['Ticker'] == dropdown]
        data8 = int(data8[data8.columns[data8.columns != 'Ticker']].reset_index().iloc[:, -2])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data8}</h1>", unsafe_allow_html=True)

    with kpi003:
        st.subheader("**Quantity of trades realized**")
        data9 = pd.DataFrame(data)
        data9 = data9[data9['Ticker'] == dropdown]
        data9 = int(data9[data9.columns[data9.columns != 'Ticker']].reset_index().iloc[:, -1])
        st.write(f"<h1 style='text-align: left; color: #428ADE;'>{data9}</h1>", unsafe_allow_html=True)

elif infoType == 'Analyse by Sectors':

    dropdown1 = st.selectbox('Chose the Setor:', pd.unique(data['Sector']))

    dropdown2 = st.selectbox('Chose the metric you wish ?',
                                 ['Price', 'Daily liquidity', '3m DY acc.', '6m DY acc.', '12m DY acc.', 'P/BV',
                                  'Vacancy', 'Qty of assets'])

    values = pd.DataFrame(data)

    values = data[data['Sector'] == dropdown1][[dropdown2]].sort_values(dropdown2, ascending=True)

    values = pd.merge(data['Ticker'], values, left_index=True, right_index=True).astype('string')

    visual = st.checkbox('Check out the display')

    if visual:
        st.table(values)

elif infoType == 'Ranking of REITs':

        st.header('Brazilian REITs with more than 5 assets')

        infotype2 = st.radio("", ('Price per Book Value', '3m DY acc.', '6m DY acc.', '12m DY acc.'))

        Ranking_REITS = data[data['Qty of assets'] >= 5]

        if infotype2 == 'Price per Book Value':

            graph1A = Ranking_REITS.sort_values('P/BV', ascending=False)

            graph1A = graph1A.head(20)

            y1 = graph1A['P/BV']

            x1 = graph1A['Ticker']

            fig1 = plt.figure(figsize=(12, 7))

            plt.barh(x1, y1, color='#428ADE', edgecolor='limegreen', linewidth=.2)
            plt.ylabel('TICKER', fontsize=12)
            plt.xlabel('Price per Book Value', fontsize=12)
            plt.rcParams.update({'font.size': 10})
            plt.style.use('ggplot')
            st.pyplot(fig1)

            graph1B = Ranking_REITS.sort_values('P/BV', ascending=True)

            graph1B = graph1B.head(20)

            y1 = graph1B['P/BV']

            x1 = graph1B['Ticker']

            fig2 = plt.figure(figsize=(12, 7))

            plt.barh(x1, y1, color='red', edgecolor='limegreen', linewidth=.2)
            plt.ylabel('TICKER', fontsize=12)
            plt.xlabel('Price per Book Value', fontsize=12)
            plt.rcParams.update({'font.size': 10})
            plt.style.use('ggplot')
            st.pyplot(fig2)

        elif infotype2 == '3m DY acc.':

            graph2A = Ranking_REITS.sort_values('3m DY acc.', ascending=False)

            graph2A = graph2A.head(20)

            y2 = graph2A['3m DY acc.']

            x2 = graph2A['Ticker']

            fig3 = plt.figure(figsize=(12, 7))

            plt.barh(x2, y2, color='#428ADE', edgecolor='limegreen', linewidth=.5)
            plt.ylabel('TICKER', fontsize=10)
            plt.xlabel('% DY', fontsize=10)
            plt.rcParams.update({'font.size': 8})
            plt.style.use('ggplot')
            st.pyplot(fig3)

            graph2B = Ranking_REITS.sort_values('3m DY acc.', ascending=True)

            graph2B = graph2B.head(20)

            y2 = graph2B['3m DY acc.']

            x2 = graph2B['Ticker']

            fig4 = plt.figure(figsize=(12, 7))

            plt.barh(x2, y2, color='red', edgecolor='limegreen', linewidth=.5)
            plt.ylabel('TICKER', fontsize=10)
            plt.xlabel('% DY', fontsize=10)
            plt.rcParams.update({'font.size': 8})
            plt.style.use('ggplot')
            st.pyplot(fig4)

        if infotype2 == '6m DY acc.':

            graph3A = Ranking_REITS.sort_values('6m DY acc.', ascending=False)

            graph3A = graph3A.head(20)

            y1 = graph3A['6m DY acc.']

            x1 = graph3A['Ticker']

            fig5 = plt.figure(figsize=(12, 7))

            plt.barh(x1, y1, color='#428ADE', edgecolor='limegreen', linewidth=.2)
            plt.ylabel('TICKER', fontsize=12)
            plt.xlabel('% DY', fontsize=12)
            plt.rcParams.update({'font.size': 10})
            plt.style.use('ggplot')
            st.pyplot(fig5)

            graph3B = Ranking_REITS.sort_values('6m DY acc.', ascending=True)

            graph3B = graph3B.head(20)

            y1 = graph3B['6m DY acc.']

            x1 = graph3B['Ticker']

            fig6 = plt.figure(figsize=(12, 7))

            plt.barh(x1, y1, color='red', edgecolor='limegreen', linewidth=.2)
            plt.ylabel('TICKER', fontsize=12)
            plt.xlabel('% DY', fontsize=12)
            plt.rcParams.update({'font.size': 10})
            plt.style.use('ggplot')
            st.pyplot(fig6)

        elif infotype2 == '12m DY acc.':

            graph4A = Ranking_REITS.sort_values('12m DY acc.', ascending=False)

            graph4A = graph4A.head(20)

            y2 = graph4A['12m DY acc.']

            x2 = graph4A['Ticker']

            fig7 = plt.figure(figsize=(12, 7))

            plt.barh(x2, y2, color='#428ADE', edgecolor='limegreen', linewidth=.5)
            plt.ylabel('TICKER', fontsize=10)
            plt.xlabel('% DY', fontsize=10)
            plt.rcParams.update({'font.size': 8})
            plt.style.use('ggplot')
            st.pyplot(fig7)

            graph4B = Ranking_REITS.sort_values('12m DY acc.', ascending=True)

            graph4B = graph4B.head(20)

            y2 = graph4B['12m DY acc.']

            x2 = graph4B['Ticker']

            fig8 = plt.figure(figsize=(12, 7))

            plt.barh(x2, y2, color='red', edgecolor='limegreen', linewidth=.5)
            plt.ylabel('TICKER', fontsize=10)
            plt.xlabel('% DY', fontsize=10)
            plt.rcParams.update({'font.size': 8})
            plt.style.use('ggplot')
            st.pyplot(fig8)

elif infoType == 'Strategy':

    filtro_lajes = filtrar(data, sector='Corporate')
    filtro_lajes.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_shopping = filtrar(data, sector='Commercial')
    filtro_shopping.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_logistica = filtrar(data, sector='Logistics')
    filtro_logistica.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_valores = filtrar(data, sector='FOF')
    filtro_valores.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_hibrido = filtrar(data, sector='Hybrid')
    filtro_hibrido.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_hospital = filtrar(data, sector='Hospital')
    filtro_hospital.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_hotel = filtrar(data, sector='Hotel')
    filtro_hotel.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_residencial = filtrar(data, sector='Residential')
    filtro_residencial.sort_values('12m DY acc.', ascending=False, inplace=True)

    filtro_Outros = filtrar(data, sector='Others')
    filtro_Outros.sort_values('12m DY acc.', ascending=False, inplace=True)

    with st.expander("Explanation"):
        st.markdown("**Quantity of assets**: Greater than 5 assets.")
        st.markdown("**Price per Book Value**:Between 0.9 e 0.50.")
        st.markdown("**6m and 12m DY acc.**: Greater than the mean sector.")
        st.markdown("**Trade's number realized**: Greater equal than the mean sector.")
    st.subheader("**Corporate**")
    st.table(filtro_lajes)
    st.subheader("**Commercial**")
    st.table(filtro_shopping)
    st.subheader("**Logistics**")
    st.table(filtro_logistica)
    st.subheader("**Fund of funds**")
    st.table(filtro_valores)
    st.subheader("**Hybrid**")
    st.table(filtro_hibrido)
    st.subheader("**Hospital**")
    st.table(filtro_hospital)
    st.subheader("**Hotel**")
    st.table(filtro_hotel)
    st.subheader("**Residential**")
    st.table(filtro_residencial)
