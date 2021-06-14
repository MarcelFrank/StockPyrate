from datetime import datetime
import pandas as pd

def to_date_object(dates):
    date_objects = []
    mapping = [
        ["Dez.", "12"],
        ["Nov.", "11"],
        ["Okt.", "10"],
        ["Sept.", "09"],
        ["Aug.", "08"],
        ["Juli", "07"],
        ["Juni", "06"],
        ["Mai", "05"],
        ["Apr.", "04"],
        ["März", "03"],
        ["Feb.", "02"],
        ["Jan.", "01"]
        ]
    for date in dates:
        for item in mapping:
            if item[0] in date:
                date = date.replace(item[0], item[1]).replace(".", "")
        date_converted = datetime.strptime(date, "%d %m %Y").date()             
        date_objects.append(date_converted)
    return date_objects

def to_float(s):
    counter_comma = s.count(",")
    counter_dot = s.count(".")
    counter_total = counter_comma + counter_dot
    if counter_total == 1:
        s = s.replace(",", ".")
        if int(s[:s.find(".")]) > 4 and len(s[s.find(".")+1:]) == 3:
            s = float(s)*1000
        else:
            s = float(s)
    elif counter_total == 0:
        s = float(s)
    elif counter_comma >= 2 or counter_dot >= 2:
        s = float(s.replace(",", "").replace(".", ""))
    elif counter_comma >= 1 and counter_dot >= 1:
        s = float(s.replace(",", ".").replace(".", "", counter_total-1))
    return s

def parsed_stock_data_list_to_dataframe(list, column_name_for_values="missing_column_name"):
    column_dates  = [datetime.combine(date, datetime.min.time()) for date, value in list]
    column_values = [value for date, value in list]
    dataframe_index = pd.DatetimeIndex(column_dates)
    dataframe_one_column_of_stock_data = pd.DataFrame(data=column_values, index=dataframe_index, columns=[column_name_for_values])
    return dataframe_one_column_of_stock_data

def apply_yahoo_fix_to_dataframes_of_parsed_stock_data(df1, df2, df3):
    # Only up to ~90 lines of prices/volumes data retrievable in one html request, hence the limited daily, weekly and quarterly quotes are blended together.
    # Outcome: Accuracy for the last ~4 months will be daily, then frequency changes to weekly for around two years, then to quarterly for historical quotes. 
    dataframe_blended_time_series = pd.concat([df1, df2[df2.index<df1.index[-1]]])
    dataframe_blended_time_series = pd.concat([dataframe_blended_time_series, df3[df3.index<df2.index[-1]]])
    return dataframe_blended_time_series

def create_time_series_dataframe_based_on_parsed_stock_data(stock_object_current):
    dataframe_prices_daily = parsed_stock_data_list_to_dataframe(stock_object_current.prices_daily, "Close")
    dataframe_prices_weekly = parsed_stock_data_list_to_dataframe(stock_object_current.prices_weekly, "Close")
    dataframe_prices_quarterly = parsed_stock_data_list_to_dataframe(stock_object_current.prices_quarterly, "Close")
    dataframe_volumes_daily = parsed_stock_data_list_to_dataframe(stock_object_current.volumes_daily, "Volume")
    dataframe_volumes_weekly = parsed_stock_data_list_to_dataframe(stock_object_current.volumes_weekly, "Volume")
    dataframe_volumes_quarterly = parsed_stock_data_list_to_dataframe(stock_object_current.volumes_quarterly, "Volume")
    dataframe_dividends = parsed_stock_data_list_to_dataframe(stock_object_current.dividend_history, "Dividend")
    dataframe_prices = apply_yahoo_fix_to_dataframes_of_parsed_stock_data(dataframe_prices_daily, dataframe_prices_weekly, dataframe_prices_quarterly)
    dataframe_volumes = apply_yahoo_fix_to_dataframes_of_parsed_stock_data(dataframe_volumes_daily, dataframe_volumes_weekly, dataframe_volumes_quarterly)
    time_series_dataframe_based_on_parsed_stock_data = pd.concat([dataframe_prices, dataframe_volumes, dataframe_dividends], axis=1)
    time_series_dataframe_based_on_parsed_stock_data.fillna(value={"Dividend":int(0)}, inplace=True)
    return time_series_dataframe_based_on_parsed_stock_data