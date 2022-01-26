import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime, pytz

def data(data):
    data = pd.read_csv(data)
    return data


def download_data(data, label):
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    current_time = "{}.{}-{}-{}".format(current_time.date(), current_time.hour, current_time.minute, current_time.second)
    export_data = st.download_button(
                        label="Download {} data as CSV".format(label),
                        data=data.to_csv(),
                        file_name='{}{}.csv'.format(label, current_time),
                        mime='text/csv',
                        help = "When You Click On Download Button You can download your {} CSV File".format(label)
                    )
    return export_data


def describe(data):
    global num_category
    num_category = [feature for feature in data.columns if data[feature].dtypes != "O"]
    str_category = [feature for feature in data.columns if data[feature].dtypes == "O"]
    return data.describe(), data.shape, data.columns, num_category, str_category, data.isnull().sum(),data.dtypes.astype("str"), data.nunique()


def outliers(data):
    plt.figure(figsize=(6,2))
    flierprops = dict(marker='o', markerfacecolor='purple', markersize=6,
                    linestyle='none', markeredgecolor='black')
    
    path_list = []
    for i in range(len(data.columns)):
        if data.columns[i] in num_category:
            plt.xlim(min(data[data.columns[i]]), max(data[data.columns[i]])) 
            plt.title("Checking Outliers for {} Column".format(data.columns[i]))
            plot = sns.boxplot(x=data.columns[i], flierprops=flierprops, data=data)
            fig = plot.get_figure()
            path = 'temp/pic{}.png'.format(i)
            fig.savefig(path)
            path_list.append(path)
    return path_list



def drop_items(data, selected_name):
    droped = data.drop(selected_name, axis = 1)
    return droped


def filter_data(data, selected_column, selected_name):
    if selected_name == []:
        filtered_data = data
    else:
        filtered_data = data[~ data[selected_column].isin(selected_name)]
    return filtered_data


def num_filter_data(data, start_value, end_value, column, param):
    if param == "Delete data inside the range":
        if column in num_category:
            num_filtered_data = data[~data[column].isin(range(int(start_value), int(end_value)+1))]
    else:
        if column in num_category:
            num_filtered_data = data[data[column].isin(range(int(start_value), int(end_value)+1))]
    
    return num_filtered_data