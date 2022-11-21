import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta 
import datetime
import csv
from streamlit_option_menu import option_menu
import base64

st.set_page_config(layout="wide")

with st.sidebar:
    option = option_menu("Table of Contents", ["Home", "Latest Records","Graphical Visualization","Documentation"],
                         icons=['house','receipt-cutoff','graph-down','file-text'],
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
            d.append(float(row[4]))
            k.append(float(row[5]))
            y.append(float(row[3]))
        
    with open(filename,'r') as csvfile:
        i=0;
        csvreader=csv.reader(csvfile,delimiter=',')
        for row in csvreader :
            d[i] = d[i] + float(row[6])/3;
            k[i] = k[i] + float(row[6])/3;
            y[i] = y[i] + float(row[6])/3;
            i=i+1
            
    return d,k,y
        
def plotter():

    d_g={}
    k_g={}
    y_g={}
    
    month_d={}
    month_k={}
    month_y={}
    
    with open("Hostel Expense Record.csv",'r') as csvfile:
        
        csvreader=csv.reader(csvfile,delimiter=',')
       
        for row in csvreader:
            if row[0] in d_g:
                d_g[row[0]]+=float(row[4]) + float(row[6])/3
            else:
                d_g[row[0]]=float(row[4]) + float(row[6])/3
                
            if row[0] in k_g:
                k_g[row[0]]+=float(row[5]) + float(row[6])/3
            else:
                k_g[row[0]]=float(row[5]) + float(row[6])/3
                
            if row[0] in y_g:
                y_g[row[0]]+=float(row[3]) + float(row[6])/3
            else:
                y_g[row[0]]=float(row[3]) + float(row[6])/3
                
            month=row[0][:7]
            
            if month in month_d:
                month_d[month]+=float(row[4]) + float(row[6])/3
            else:
                month_d[month]=float(row[4]) + float(row[6])/3
                
            if month in month_k:
                month_k[month]+=float(row[5]) + float(row[6])/3
            else:
                month_k[month]=float(row[5]) + float(row[6])/3
                
            if month in month_y:
                month_y[month]+=float(row[3]) + float(row[6])/3
            else:
                month_y[month]=float(row[3]) + float(row[6])/3              
    
    return d_g,y_g,k_g,month_d,month_y,month_k

def graph_wiz(x,grph_type) :
    
    lst_key = list(x.keys())
    lst_val = list(x.values())
    
    if grph_type == 'daily-7' :
        
        lst_val = lst_val[-7:]
        lst_key = lst_key[-7:]
       
    elif grph_type == 'daily-30' :
        
        lst_val = lst_val[-30:]
        lst_key = lst_key[-30:]
        
    fig, ax = plt.subplots()
    fig.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    if grph_type == 'daily-7' :
        ax.plot(lst_key,lst_val, color = 'white', marker = 'o',  markerfacecolor='white', markersize = 6)
        plt.grid(color = '#d8d8d8', linestyle = '-.', linewidth = '0.2')
        ax.set_xticklabels(lst_key, rotation=45)
    
    elif grph_type == 'daily-30' :
        ax.bar(lst_key,lst_val, color = 'white')
        plt.grid(axis = 'y', color = '#d8d8d8', linestyle = '-.', linewidth = '0.2')
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
    st.pyplot(fig)

def update(da,day,la,e1,e2,e3,e4):
    
    filename="Hostel Expense Record.csv"
    rowlist = [da.strip('\n'),day.strip('\n'),la.strip('\n'),e1,e2,e3,e4]
    with open(filename,'a',newline='') as csvfile:
        csvwriter=csv.writer(csvfile,delimiter=',')
        csvwriter.writerow(rowlist)

def latest_records():
    df = pd.read_csv('Hostel Expense Record.csv', delimiter=',')
    list_of_csv = [list(row) for row in df.values]
    
    last_ten_elements_rev=list_of_csv[-10:]
    last_ten_elements=last_ten_elements_rev[::-1]
    
    for i in range(0,10):
        last_ten_elements[i][3]=round(last_ten_elements[i][6]/3 + last_ten_elements[i][3],2)
        last_ten_elements[i][4]=round(last_ten_elements[i][6]/3 + last_ten_elements[i][4],2)
        last_ten_elements[i][5]=round(last_ten_elements[i][6]/3 + last_ten_elements[i][5],2)
    
    return last_ten_elements 

def Days() :
    
    df = pd.read_csv('Hostel Expense Record.csv', delimiter=',')
    dates = [list(row) for row in df.values]
 
    date_str_min = dates[0][0]
    date_str_max = dates[-1][0]

    min_date = datetime.datetime.strptime(date_str_min, '%Y-%m-%d').date()
    max_date = datetime.datetime.strptime(date_str_max, '%Y-%m-%d').date()
    
    timedelta = max_date - min_date
        
    return timedelta.days

def display_pdf(pdf_file):
    with open(pdf_file,'rb') as f:
        base64_pdf=base64.b64encode(f.read()).decode('utf-8')
    
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="1000" height="800" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

##--------------------------------       Function Definition Ends      -------------------------------------#


if option=="Home":

    st.markdown("<h1 style='text-align: center; color: white;'>Expense Record Data Base</h1>", unsafe_allow_html=True)
    st.markdown("<marquee>A one stop point to have a record and correctly monitor all your expenses !! </marquee>", unsafe_allow_html=True)
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
            update(date_str,day,Expense,Amount_yash,Amount_devesh,Amount_kartikey,common)
            st.write('Sucessfully Submitted')

    with c2:
        
        c2.header('Overview:')
        choose = st.selectbox('Name : ',('Devesh','Kartikey','Yash'))
        Enter=st.button("Enter")
        
        d,k,y=Overview()
        st.write(' ')
        
        record = latest_records()
        
        if choose=='Devesh' and Enter:
            st.write(f'Total Expense of Devesh : ₹ {round(sum(d),3)}'); 
            st.write(f'Last Spent Amount     : ₹ {round(d[len(d)-1],3)}'); 
            st.write(f'Average Daily Expense   : ₹ {round(sum(d)/Days(),3)}');
            st.write(f'Last Expense Name : {record[0][2]}')
        elif choose=='Kartikey' and Enter:
            st.write(f'Total Expense of Kartikey : ₹ {round(sum(k),3)}'); 
            st.write(f'Last Spent Amount     : ₹ {round(k[len(k)-1],3)}'); 
            st.write(f'Average Daily Expense   : ₹ {round(sum(k)/Days(),3)}');
            st.write(f'Last Expense Name : {record[0][2]}')
        elif choose=='Yash' and Enter:
            st.write(f'Total Expense of Yash : ₹ {round(sum(y),3)}'); 
            st.write(f'Last Spent Amount     : ₹ {round(y[len(y)-1],3)}'); 
            st.write(f'Average Daily Expense   : ₹ {round(sum(y)/Days(),3)}');
            st.write(f'Last Expense Name : {record[0][2]}')
            
        if Enter:
            
            d,k,y=Overview()

            labels = 'Devesh', 'Kartikey', 'Yash'
            sizes = [sum(d),sum(k),sum(y)]

            fig, ax1 = plt.subplots()
            fig.set_facecolor('#0e1117')
            ax1.set_facecolor('#0e1117')
            ax1.pie(sizes, autopct='%1.1f%%', wedgeprops={'linewidth': 3.0, 'edgecolor': '#0e1117'}, shadow=False, startangle=90)
            ax1.axis('equal')  
            plt.legend(labels, )
            plt.title("Overall Analysis Chart", color = 'white', fontdict={'fontsize': 17})
            st.pyplot(fig)

elif option=="Latest Records":                              ##-------------------------------------------------------------------------##
    
    st.markdown("<h1 style='text-align: center; color: white;'>Latest Entries</h1>", unsafe_allow_html=True)
    choose = st.selectbox('Name : ',('Devesh','Kartikey','Yash'))
        
    column1,column2,column3,column4=st.columns((1,1,1,1))
    
    record = latest_records()

    with column1:
        st.header('Date')
            
        for i in range(0,10):
            st.write(record[i][0])
        
    with column2:
        st.header('Day')
            
        for i in range(0,10):
            st.write(record[i][1])
      
    with column3:
        st.header('Particulars')
            
        for i in range(0,10):
            st.write(record[i][2])
        
    with column4: 
        st.header('Expense')
            
        for i in range(0,10):
            if(choose == 'Devesh') :
                st.write('Rs. ',str(record[i][4]))
                
            elif(choose == 'Kartikey') :
                st.write('Rs. ',str(record[i][5]))
                
            elif(choose == 'Yash') :
                st.write('Rs. ',str(record[i][3]))
            
        
elif option=="Graphical Visualization":                            
    
    n_choice=st.selectbox('Please Enter the Name : ',('Devesh','Kartikey','Yash'))
    gr_choice=st.selectbox('Please select the way to visualize the expenses : ',('Last 7 days','Last 30 days','Monthwise Record'))
    
    d_g,y_g,k_g,dm_g,km_g,ym_g = plotter()
    
    data_grph = [d_g,y_g,k_g]
    data_month_graph=[dm_g,km_g,ym_g]
    
    if gr_choice == 'Last 7 days' :
        
        st.markdown("<h1 style='text-align: center; color: white;'>Expenditure : Last 7 Days</h1>", unsafe_allow_html=True)
        
        if n_choice=='Devesh':
            graph_wiz(data_grph[0],'daily-7')
        
        elif n_choice=='Kartikey':
            graph_wiz(data_grph[2],'daily-7')
        
        elif n_choice=='Yash':
            graph_wiz(data_grph[1],'daily-7')
        
    elif gr_choice == 'Last 30 days' :
        
        st.markdown("<h1 style='text-align: center; color: white;'>Expenditure : Last 30 Days</h1>", unsafe_allow_html=True)
        
        if n_choice=='Devesh':
            graph_wiz(data_grph[0],'daily-30')
        
        elif n_choice=='Kartikey':
            graph_wiz(data_grph[2],'daily-30')
        
        elif n_choice=='Yash':
            graph_wiz(data_grph[1],'daily-30')
            
    elif gr_choice == 'Monthwise Record' :
        
        st.markdown("<h1 style='text-align: center; color: white;'>Expenditure : Monthwise Record</h1>", unsafe_allow_html=True)
        
        if n_choice=='Devesh':
            graph_wiz(data_month_graph[0],'month')
        
        elif n_choice=='Kartikey':
            graph_wiz(data_month_graph[2],'month')
        
        elif n_choice=='Yash':
            graph_wiz(data_month_graph[1],'month')
        
elif option=="Documentation":
    
    st.title('Documentation : ')
    display_pdf("ADMM1.pdf")
