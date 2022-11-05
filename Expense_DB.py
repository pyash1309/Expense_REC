import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta 
import datetime
import csv
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

with st.sidebar:
    option = option_menu("Table of Contents", ["Home", "Latest Records","Graphical Visualization"],
                         icons=['house','receipt-cutoff','graph-down'],
                         menu_icon="menu-button-wide-fill", default_index=0, 
                         styles={
                            "container": {"padding": "5!important", "background-color": "#1a1a1a"},
                            "icon": {"color": "White", "font-size": "25px"}, 
                            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#4d4d4d"},
                             "nav-link-selected": {"background-color": "#4d4d4d"},
                        }
    )
    
def Overview():
    
    filename="Hostel Expense Record.csv"
    
    d=[]
    k=[]
    y=[]
    
    with open(filename,'r') as csvfile:
        
        csvreader=csv.reader(csvfile,delimiter=',')
        
        for row in csvreader:
            d.append(float(row[3]))
            k.append(float(row[4]))
            y.append(float(row[2]))
        
    with open(filename,'r') as csvfile:
        i=0;
        csvreader=csv.reader(csvfile,delimiter=',')
        for row in csvreader :
            d[i] = d[i] + float(row[5])/3;
            k[i] = k[i] + float(row[5])/3;
            y[i] = y[i] + float(row[5])/3;
            i=i+1
            
    return d,k,y
        
def plotter():

    d_g={}
    k_g={}
    y_g={}
    
    with open("Hostel Expense Record.csv",'r') as csvfile:
        
        csvreader=csv.reader(csvfile,delimiter=',')
       
        for row in csvreader:
            if row[0] in d_g:
                d_g[row[0]]+=float(row[3]) + float(row[5])/3
            else:
                d_g[row[0]]=float(row[3])
                
            if row[0] in k_g:
                k_g[row[0]]+=float(row[4]) + float(row[5])/3
            else:
                k_g[row[0]]=float(row[4])
                
            if row[0] in y_g:
                y_g[row[0]]+=float(row[2]) + float(row[5])/3
            else:
                y_g[row[0]]=float(row[2])          
    
    return d_g,y_g,k_g

def graph_wiz(x,grph_type) :
    
    lst_key = list(x.keys())
    lst_val = list(x.values())
    
    if grph_type == 'daily' :
        
        lst_val = lst_val[-8:-1]
        lst_key = lst_key[-8:-1]
       
    elif grph_type == 'month' :
        
        lst_val = lst_val[-31:-1]
        lst_key = lst_key[-31:-1]
        
    fig, ax = plt.subplots()
    fig.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    if grph_type == 'daily' :
        ax.plot(lst_key,lst_val, color = 'white', marker = 'o',  markerfacecolor='white', markersize = 6)
        plt.grid(color = '#d8d8d8', linestyle = '-.', linewidth = '0.2')
        ax.set_xticklabels(lst_key, rotation=45)
    
    elif grph_type == 'month' :
        ax.bar(lst_key,lst_val, color = 'white')
        plt.grid(axis = 'y', color = '#d8d8d8', linestyle = '-.', linewidth = '0.2')
        ax.set_xticklabels(lst_key, rotation=45)
                
    ax.set_xticks(lst_key)
    ax.yaxis.label.set_color('#d8d8d8')
    ax.tick_params(axis = 'x', colors='#d8d8d8', labelsize = 5)
    ax.tick_params(axis = 'y', colors='#d8d8d8', labelsize = 8)
    ax.spines['bottom'].set_color('#0e1117')
    ax.spines['top'].set_color('#0e1117')
    ax.spines['left'].set_color('#0e1117')
    ax.spines['right'].set_color('#0e1117')
    plt.ylabel('Amount (in Rupees)')
    plt.xlabel('Date')
    st.pyplot(fig)

def update(da,la,e1,e2,e3,e4):
    
    filename="Hostel Expense Record.csv"
    rowlist = [da.strip('\n'),la.strip('\n'),e1,e2,e3,e4]
    with open(filename,'a',newline='') as csvfile:
        csvwriter=csv.writer(csvfile,delimiter=',')
        csvwriter.writerow(rowlist)
        

def latest_records():
    df = pd.read_csv('Hostel Expense Record.csv', delimiter=',')
    list_of_csv = [list(row) for row in df.values]
    
    return list_of_csv

def Days() :
    
    dates = latest_records()
    date_str_min = dates[0][0]
    date_str_max = dates[-1][0]

    min_date = datetime.datetime.strptime(date_str_min, '%Y-%m-%d').date()
    max_date = datetime.datetime.strptime(date_str_max, '%Y-%m-%d').date()
    
    timedelta = max_date - min_date
        
    return timedelta.days
    
if option=="Home":

    st.markdown("<h1 style='text-align: center; color: white;'>Expense Record</h1>", unsafe_allow_html=True)
    st.header("Introduction : ")
    st.markdown("<marquee>This project helps in identifying the daily expenses made by you and helps in maintaing the record for the same. Hello All.</marquee>", unsafe_allow_html=True)
    c1,c2=st.columns((2,1))
    
    with c1:
        
        st.header('New Entry')
        Amount_devesh=st.number_input('Expenditure - Devesh :')
        Amount_kartikey=st.number_input('Expenditure - Kartikey :')
        Amount_yash=st.number_input('Expenditure - Yash :')
        common=st.number_input('Common Expenditure :')
        date=st.date_input("Date of Expense :",datetime.datetime.now().date())
        day = str(date.strftime('%A'))
        st.write(day)
        Expense=st.text_input('Enter Expense name :') 
        date_str = date.strftime("%Y-%m-%d")
        submit_entry=st.button("Submit")
        
        if submit_entry:
            update(date_str,Expense,Amount_yash,Amount_devesh,Amount_kartikey,common)
            st.write('Sucessfully Submitted')

    with c2:
        
        c2.header('Overview:')
        choose = st.selectbox('Name : ',('Devesh','Kartikey','Yash'))
        Enter=st.button("Enter")
        
        d,k,y=Overview()
        st.write(' ')
        
        if choose=='Devesh' and Enter:
            st.write(f'Total Expense of Devesh : ₹ {round(sum(d),3)}'); 
            st.write(f'Last Spent Amount     : ₹ {round(d[len(d)-1],3)}'); 
            st.write(f'Average Daily Expense   : ₹ {round(sum(d)/Days(),3)}');
        elif choose=='Kartikey' and Enter:
            st.write(f'Total Expense of Kartikey : ₹ {round(sum(k),3)}'); 
            st.write(f'Last Spent Amount     : ₹ {round(k[len(k)-1],3)}'); 
            st.write(f'Average Daily Expense   : ₹ {round(sum(k)/Days(),3)}');
        elif choose=='Yash' and Enter:
            st.write(f'Total Expense of Yash : ₹ {round(sum(y),3)}'); 
            st.write(f'Last Spent Amount     : ₹ {round(y[len(y)-1],3)}'); 
            st.write(f'Average Daily Expense   : ₹ {round(sum(y)/Days(),3)}');

elif option=="Latest Records":                              ##-------------------------------------------------------------------------##
    
    st.markdown("<h1 style='text-align: center; color: white;'>Latest Entries</h1>", unsafe_allow_html=True)
    #st.title('Last ten Records')
    choose = st.selectbox('Name : ',('Devesh','Kartikey','Yash'))
    
    list_of_csv=latest_records()
    
    last_ten_elements_rev=list_of_csv[-10:]
    last_ten_elements=last_ten_elements_rev[::-1]
    
    for i in range(0,10):
        last_ten_elements[i][2]=round(last_ten_elements[i][5]/3 + last_ten_elements[i][2],2)
        last_ten_elements[i][3]=round(last_ten_elements[i][5]/3 + last_ten_elements[i][3],2)
        last_ten_elements[i][4]=round(last_ten_elements[i][5]/3 + last_ten_elements[i][4],2)
        
    column1,column2,column3=st.columns((1,1,1))
    
    with column1:
            st.header('Date')
            
            for i in range(0,10):
                st.write(last_ten_elements[i][0])
        
    with column2:
            st.header('Particulars')
            
            for i in range(0,10):
                st.write(last_ten_elements[i][1])
        
    if choose=='Devesh':
        
        with column3:
            st.header('Amount')
            
            for i in range(0,10):
                st.write(str(last_ten_elements[i][3]),'/-')
                
    elif choose=='Kartikey':
        
        with column3:
            st.header('Amount')
            
            for i in range(0,10):
                st.write(str(last_ten_elements[i][4]),'/-')
                
    if choose=='Yash':
        
        with column3:
            st.header('Amount')
            
            for i in range(0,10):
                st.write(str(last_ten_elements[i][2]),'/-')
        
elif option=="Graphical Visualization":                            
    
    st.markdown("<h1 style='text-align: center; color: white;'>Daily Expenditure</h1>", unsafe_allow_html=True)
    choice=st.selectbox('Name : ',('Devesh','Kartikey','Yash'))
    d_g,y_g,k_g = plotter()
    data_grph = [d_g,y_g,k_g]
    
    if choice=='Devesh':
        graph_wiz(data_grph[0],'daily')
        
    elif choice=='Kartikey':
        graph_wiz(data_grph[2],'daily')
        
    elif choice=='Yash':
        graph_wiz(data_grph[1],'daily')
        
    st.markdown("<h1 style='text-align: center; color: white;'>Monthly Expenditure</h1>", unsafe_allow_html=True)
    
    if choice=='Devesh':
        graph_wiz(data_grph[0],'month')
        
    elif choice=='Kartikey':
        graph_wiz(data_grph[2],'month')
        
    elif choice=='Yash':
        graph_wiz(data_grph[1],'month')
