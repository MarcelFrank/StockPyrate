from functions import converter, status_messages
from datetime import datetime, timedelta
import pandas as pd
import os

class StockObject():

    def __init__(self, name):
        self.name = name
        self.index = ""
        self.symbol = ""
        self.id = int(0)
        self.overview_key_facts = {}
        self.overview_yahoo_statistics = {}
        self.overview_shares_freefloat = int(0)
        self.overview_shares_total = int(0)
        self.overview_ex_date = []
        self.prices_daily = []
        self.prices_weekly = []
        self.prices_quarterly = []
        self.dividend_history = []
        self.dividend_rate = float(0)
        self.dividend_rate_hypothetic = float(0)
        self.dividend_race_to_recover = {}
        self.volumes_daily = []
        self.volumes_weekly = []
        self.volumes_quarterly = []
        self.volumes_transaction_daily = []
        self.volumes_transaction_quarterly = []
        self.volumes_transaction_20_days = float(0)
        self.volumes_transaction_one_year = []
        self.volumes_transaction_one_year_sum = float(0)
        self.market_capitalization_daily = []
        self.market_capitalization_20_days = int(0)
        self.market_capitalization_quarterly = []
        self.prices_with_delta_by_timestamp = {}
        self.prices_with_delta_by_row = {}
        self.dataframes_for_xlsx_export = {}
        
    def write_raw_dictionary_data_to_stock_object(self, share):
        status_messages.status(211)
        self.id = share["id"]
        status_messages.status(212)
        self.symbol = share["symbol"] 
        status_messages.status(213)
        self.index = share["index"]
        status_messages.status(214)
        self.prices_daily = share["stock_price_weeks"]
        status_messages.status(215)
        self.prices_weekly = share["stock_price_months"]
        status_messages.status(216)
        self.prices_quarterly = share["stock_price_years"]
        status_messages.status(218)
        self.dividend_history = share["dividends"]
        status_messages.status(219)
        self.overview_yahoo_statistics = share["statistics"]
        status_messages.status(217)
        self.volumes_daily = share["stock_volume_weeks"]
        status_messages.status(220)
        self.volumes_weekly = share["stock_volume_months"]
        status_messages.status(221)
        self.volumes_quarterly = share["stock_volume_years"]
        status_messages.status(222) 
    
    def assign_overview_shares_total(self):
        if self.overview_yahoo_statistics["Aktien im Umlauf"] != "N/A":
            if str(self.overview_yahoo_statistics["Aktien im Umlauf"])[-1] == "M":
                status_messages.status(231)
                self.overview_shares_total = int(float(str(self.overview_yahoo_statistics["Aktien im Umlauf"]).replace("M", "").replace(",", "."))*1000000)
            elif str(self.overview_yahoo_statistics["Aktien im Umlauf"])[-1] == "B":
                status_messages.status(231)
                self.overview_shares_total = int(float(str(self.overview_yahoo_statistics["Aktien im Umlauf"]).replace("B", "").replace(",", "."))*1000000000)
        else:
            status_messages.status(232)
            self.overview_shares_total = int(1)

    def assign_overview_shares_freefloat(self):
        if self.overview_yahoo_statistics["Float"] != "N/A":
            if str(self.overview_yahoo_statistics["Float"])[-1] == "M":
                status_messages.status(233)
                self.overview_shares_freefloat = int(float(str(self.overview_yahoo_statistics["Float"]).replace("M", "").replace(",", "."))*1000000)
            elif str(self.overview_yahoo_statistics["Float"])[-1] == "B":
                status_messages.status(234)
                self.overview_shares_freefloat = int(float(str(self.overview_yahoo_statistics["Float"]).replace("B", "").replace(",", "."))*1000000000)
            elif self.overview_yahoo_statistics["Aktien im Umlauf"] != "N/A":
                status_messages.status(235)
                self.overview_shares_freefloat = self.overview_shares_total
        else:
            status_messages.status(236)
            self.overview_shares_freefloat = self.overview_shares_total + 1

    def assign_overview_key_facts(self):
        status_messages.status(291)
        
        self.overview_key_facts = {
            "Abruf": datetime.now().date(),
            "Index": str(self.index).upper(),
            "Kurs": self.prices_daily[0][1],
            "Dividende": self.dividend_history[0][1],
            "Abschlagsdatum": self.dividend_history[0][0],
            "Dividendenrendite": self.dividend_rate,
            "Div.r. hypot.": self.dividend_rate_hypothetic,
            "Dividende/Ex-Tag erholt am": self.dividend_race_to_recover["recovery_date"],
            "Tage für Erholung (0 = fail)": self.dividend_race_to_recover["recovery_timedelta"],
            "Kurs nach Erholung": self.dividend_race_to_recover["recovery_price"],
            "Delta nach Erholung": self.dividend_race_to_recover["recovery_pricedelta"],
            "Ex-Tag (YStats)": self.overview_ex_date,
            "Marktkapitalisierung": self.market_capitalization_daily[0][1],
            "Marktkapita. 20T": self.market_capitalization_20_days,
            "Börsenumsatz 12M": self.volumes_transaction_one_year_sum,
            "Börsenumsatz 20T": self.volumes_transaction_20_days,
            "Freefloat-Aktien": self.overview_shares_freefloat,
            "Aktien im Umlauf": self.overview_shares_total
            }

    def compute_race_to_recuperate_dividend(self):
        # This comparison is based on weekly price table (daily table is not availabe for a full years), this lowers accuracy slightly.
        dividend = self.dividend_history[0][1]
        dividend_date = self.dividend_history[0][0]
        if self.dividend_history[0][0].year == datetime.now().year:                        
            for line in self.prices_weekly[::-1]:
                competitive_price = line[1]
                if line[0] >= dividend_date:
                    break
            for line in self.prices_weekly[::-1]:
                if line[0].year >= datetime.now().year and line[0] > dividend_date and line[1] > float(dividend + competitive_price):
                    race_won_date = line[0]
                    race_won_price = line[1]
                    time_passed = (race_won_date - dividend_date).days
                    break
                else:
                    race_won_date = datetime.strptime("01.01.1980", "%d.%m.%Y").date()
                    race_won_price = 0
                    time_passed = 0
        else:
            race_won_date = datetime.strptime("01.01.1980", "%d.%m.%Y").date()
            race_won_price = 0
            time_passed = 0
        self.dividend_race_to_recover["recovery_date"] = race_won_date
        self.dividend_race_to_recover["recovery_price"] = race_won_price
        self.dividend_race_to_recover["recovery_timedelta"] = int(time_passed)
        if time_passed > 0:
            self.dividend_race_to_recover["recovery_pricedelta"] = float((race_won_price/competitive_price)-1)
        else:
            self.dividend_race_to_recover["recovery_pricedelta"] = float(0)

    def assign_overview_ex_date(self):
        if self.overview_yahoo_statistics["Ex-Dividendendatum"] != "N/A":
            status_messages.status(241)
            self.overview_ex_date = [str(self.overview_yahoo_statistics["Ex-Dividendendatum"])]
        else:
            status_messages.status(242)
            self.overview_ex_date = ["01. Jan. 1980"]
        self.overview_ex_date = converter.to_date_object(self.overview_ex_date)[0]

    def compute_dividend_rate(self):
        status_messages.status(243)
        year_of_last_dividend_payment = self.dividend_history[0][0].year
        if datetime.now().year == year_of_last_dividend_payment:
            if self.dividend_history[0][1] > 0:
                if self.index in ["dow", "nasdaq", "nyse"]:
                    dividend_last_amount = self.dividend_history[0][1]*4
                    if self.name == "realtyincome":
                        dividend_last_amount = dividend_last_amount*3
                    elif self.name in ["euronav", "frontline"]:
                        dividend_last_amount = self.dividend_history[0][1] + self.dividend_history[1][1]
                    elif self.name in ["tangerfactoryoutlet", "macys", "macerich", "simonpropertygroup", "meredith", "ford", "carnival"]:
                        dividend_last_amount = self.dividend_history[0][1]
                elif self.index in ["ibex", "ftse"]:
                    dividend_last_amount = self.dividend_history[0][1]*2 # IBEX/FTSE stocks will be dealt with as if paying dividends half-yearly (does not fit to all 35 components; better solution requires additional stock information about yearly no. of ex dates [e. g. 1, 2, 4, 12] in stocks_userlist.py)
                    if self.name == "imperialbrands":
                        dividend_last_amount = self.dividend_history[0][1] + self.dividend_history[1][1] + self.dividend_history[2][1] + self.dividend_history[3][1]
                    elif self.name in ["bp", "royaldutchshella", "royaldutchshellb"]:
                        dividend_last_amount = self.dividend_history[0][1]*4
                elif self.index in ["dax", "mdax", "sdax", "scale", "cac"]:
                    dividend_last_amount = self.dividend_history[0][1]
                self.dividend_rate = float(dividend_last_amount/self.prices_daily[0][1])
                self.dividend_rate_hypothetic = float(dividend_last_amount/self.prices_daily[0][1])
            else:
                status_messages.status(244)
                self.dividend_rate = float(0)
        else:
            status_messages.status(245)
            self.dividend_rate = float(0)
            self.dividend_rate_hypothetic = float(self.dividend_history[0][1]/self.prices_daily[0][1])

    def compute_volume_transaction_daily(self):
        status_messages.status(251)
        for i in range(0, len(self.prices_daily)):
            if self.prices_daily[i][0] == self.volumes_daily[i][0]:
                transaction_sum = int(self.prices_daily[i][1]*self.volumes_daily[i][1])
                if transaction_sum == 0:
                    transaction_sum += 1
                self.volumes_transaction_daily += [[self.prices_daily[i][0], transaction_sum]]
            else:
                status_messages.status(259)
        
        amount_total = int(0)
        for amount_daily in self.volumes_transaction_daily[0:20]:
            amount_total += amount_daily[1]
        self.volumes_transaction_20_days = amount_total

    def compute_volume_transaction_quarterly(self):
        status_messages.status(252)
        for i in range(0, len(self.prices_quarterly)):
            if self.prices_quarterly[i][0] == self.volumes_quarterly[i][0]:
                transaction_sum = int(self.prices_quarterly[i][1]*self.volumes_quarterly[i][1])
                if transaction_sum == 0:
                    transaction_sum += 1
                self.volumes_transaction_quarterly += [[self.prices_quarterly[i][0], transaction_sum]]
            else:
                status_messages.status(259)
        self.volumes_transaction_quarterly = self.volumes_transaction_quarterly[2:]

    def compute_volume_transaction_one_year(self):
        status_messages.status(253)

        datetime_object_one_year_ago = self.prices_weekly[0][0] + timedelta(days=-365)
        set_position_to_one_year_ago = 0
        for i in range(0, len(self.prices_weekly)):
            if self.prices_weekly[i][0] < datetime_object_one_year_ago:
                set_position_to_one_year_ago = i
                break

        prices_weekly_one_year = self.prices_weekly[0:set_position_to_one_year_ago+1]
        volumes_weekly_one_year = self.volumes_weekly[0:set_position_to_one_year_ago+1]
        for i in range(0, len(prices_weekly_one_year)):
            if prices_weekly_one_year[i][0] == volumes_weekly_one_year[i][0]:
                transaction_sum = int(prices_weekly_one_year[i][1]*volumes_weekly_one_year[i][1])
                if transaction_sum == 0:
                    transaction_sum += 1
                self.volumes_transaction_one_year += [[prices_weekly_one_year[i][0], transaction_sum]]
            else:
                status_messages.status(259)
        self.volumes_transaction_one_year = self.volumes_transaction_one_year[2:]
        
        amount_total = int(0)
        for amount_daily in self.volumes_transaction_one_year:
            amount_total += amount_daily[1]
        self.volumes_transaction_one_year_sum = amount_total
    
    def compute_market_capitalization_daily(self):
        if self.overview_shares_freefloat > 2:
            for i in range(0, len(self.prices_daily)):
                self.market_capitalization_daily += [[self.prices_daily[i][0], int(self.prices_daily[i][1]*self.overview_shares_freefloat)]]
            amount_total = float(0)
            for amount_daily in self.market_capitalization_daily[0:20]:
                amount_total += amount_daily[1]
            self.market_capitalization_20_days = int(float(amount_total/20))
            
        elif str(self.overview_yahoo_statistics["Marktkap. (im Tagesverlauf)"][-1]) == "M":
            self.market_capitalization_daily = [[self.prices_daily[0][0], int(float(str(self.overview_yahoo_statistics["Marktkap. (im Tagesverlauf)"]).replace("M", "").replace(",", "."))*1000000+1)]]
            self.market_capitalization_20_days = int(self.market_capitalization_daily[0][1])

        elif str(self.overview_yahoo_statistics["Marktkap. (im Tagesverlauf)"][-1]) == "B":
            self.market_capitalization_daily = [[self.prices_daily[0][0], int(float(str(self.overview_yahoo_statistics["Marktkap. (im Tagesverlauf)"]).replace("B", "").replace(",", "."))*1000000000+1)]]
            self.market_capitalization_20_days = int(self.market_capitalization_daily[0][1])

        else:
            status_messages.status(258)
            self.market_capitalization_daily = [[self.prices_daily[0][0], int(1)]]
            self.market_capitalization_20_days = int(1)

    def compute_market_capitalization_quarterly(self):
        for i in range(0, len(self.prices_quarterly)):
            self.market_capitalization_quarterly += [[self.prices_quarterly[i][0], int(self.prices_quarterly[i][1]*self.overview_shares_freefloat)]]
        self.market_capitalization_quarterly = self.market_capitalization_quarterly[1:]

    def compute_prices_with_delta_by_timestamp(self): 
        status_messages.status(261)

        prices = {}
        prices["daily"] = self.prices_daily[::-1]
        prices["weekly"] = self.prices_weekly[::-1]
        prices["quarterly"] = self.prices_quarterly[::-1]
        prices["daily_dataframe"] = pd.DataFrame(prices["daily"], columns=["Datum", "Kurs"])
        prices["weekly_dataframe"] = pd.DataFrame(prices["weekly"], columns=["Datum", "Kurs"])
        prices["quarterly_dataframe"] = pd.DataFrame(prices["quarterly"], columns=["Datum", "Kurs"])
        lexikon = {}
        lexikon[7]    = " 1 Woche - "
        lexikon[14]   = " 2 Wochen - "
        lexikon[31]   = " 1 Monat - "
        lexikon[90]   = " 3 Monate - "
        lexikon[180]  = " 6 Monate - "
        lexikon[365]  = " 1 Jahr - "
        lexikon[1095] = " 3 Jahre - "
        lexikon[1825] = " 5 Jahre - "
        lexikon[3650] = "10 Jahre - "
        lexikon[5475] = "15 Jahre - "

        def calculate_delta_template(prices_dataframe, days_back, lexikon):
            start = lambda number_of_days_gone: (datetime.now().date() + timedelta(days=-number_of_days_gone))
            end = (datetime.now().date() + timedelta(days=-1))
            df = prices_dataframe
            df = df.set_index(pd.to_datetime(df['Datum']))
            price_lowest = df[start(days_back):end]['Kurs'].min()
            price_average = df[start(days_back):end]['Kurs'].mean()
            price_highest = df[start(days_back):end]['Kurs'].max()
            df = df.reset_index(drop=True)
            price_lowest_position = df.index[df['Kurs'] == price_lowest][-1]
            price_highest_position = df.index[df['Kurs'] == price_highest][-1]
            price_lowest_date = df.iloc[price_lowest_position, 0]
            price_highest_date = df.iloc[price_highest_position, 0]
            price_dict = {}
            price_dict[lexikon[days_back]+"Hoch Delta"] = (self.prices_daily[0][1]-price_highest)/price_highest
            price_dict[lexikon[days_back]+"Durchschnitt Delta"] = (self.prices_daily[0][1]-price_average)/price_average
            price_dict[lexikon[days_back]+"Tief Delta"] = (self.prices_daily[0][1]-price_lowest)/price_lowest
            price_dict[lexikon[days_back]+"Hoch Preis"] = price_highest
            price_dict[lexikon[days_back]+"Durchschnitt Preis"] = price_average
            price_dict[lexikon[days_back]+"Tief Preis"] = price_lowest
            price_dict[lexikon[days_back]+"Hoch Datum"] = price_highest_date
            price_dict[lexikon[days_back]+"Tief Datum"] = price_lowest_date
            return price_dict
        
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["daily_dataframe"], 7, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["daily_dataframe"], 14, lexikon))        
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["daily_dataframe"], 31, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["daily_dataframe"], 90, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["weekly_dataframe"], 180, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["weekly_dataframe"], 365, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["quarterly_dataframe"], 1095, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["quarterly_dataframe"], 1825, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["quarterly_dataframe"], 3650, lexikon))
        self.prices_with_delta_by_timestamp.update(calculate_delta_template(prices["quarterly_dataframe"], 5475, lexikon))

    def compute_prices_with_delta_by_row(self):
        stock_dividend_history_with_row_delta = []
        if self.dividend_history[0][0] != datetime.strptime("01.01.1980", "%d.%m.%Y").date():
            for i in range(0, len(self.dividend_history)):
                if i < len(self.dividend_history)-1:
                    stock_dividend_history_with_row_delta += [[self.dividend_history[i][0], self.dividend_history[i][1], float((self.dividend_history[i][1]/self.dividend_history[i+1][1])-1), float((self.dividend_history[i][1]/self.dividend_history[0][1])-1)]]
                elif i == len(self.dividend_history)-1:
                    stock_dividend_history_with_row_delta += [[self.dividend_history[i][0], self.dividend_history[i][1], float(0), float((self.dividend_history[i][1]/self.dividend_history[0][1])-1)]]
                    break
        else:
            stock_dividend_history_with_row_delta += [[self.dividend_history[0][0], float(0), float(0), float(0)]]

        def get_delta(current_list):
            current_list_with_delta = []
            for i in range(0, len(current_list)):
                if i < len(current_list)-1:
                    current_list_with_delta += [[current_list[i][0], current_list[i][1], float((current_list[i][1]/current_list[i+1][1])-1), float((current_list[i][1]/current_list[0][1])-1)]]
                elif i == len(current_list)-1:
                    current_list_with_delta += [[current_list[i][0], current_list[i][1], float(0), float((current_list[i][1]/current_list[0][1])-1)]]
                    break
            return current_list_with_delta
                   
        self.prices_with_delta_by_row["tageskurse"] = get_delta(self.prices_daily)
        self.prices_with_delta_by_row["wochenkurse"] = get_delta(self.prices_weekly)
        self.prices_with_delta_by_row["historischekurse"] = get_delta(self.prices_quarterly)
        self.prices_with_delta_by_row["dividendenhistorie"] = stock_dividend_history_with_row_delta
        self.prices_with_delta_by_row["handelsumsatz_12monate"] = get_delta(self.volumes_transaction_one_year)
        self.prices_with_delta_by_row["handelsumsatz_historisch"] = get_delta(self.volumes_transaction_quarterly)
        self.prices_with_delta_by_row["marktkapitalisierungfreefloat_historisch"] = get_delta(self.market_capitalization_quarterly)

    def create_pandas_dataframes(self):
        status_messages.status(271)
        dataframe_key_facts = pd.DataFrame([self.overview_key_facts], index=[str(self.name)])
        dataframe_highlowdelta = pd.DataFrame([self.prices_with_delta_by_timestamp], index=[str(self.name)])
        dataframe_statistics = pd.DataFrame([self.overview_yahoo_statistics], index=[str(self.name)])
        self.dataframes_for_xlsx_export["stock_first_sheet_overview"] = pd.concat([dataframe_key_facts, dataframe_highlowdelta, dataframe_statistics], axis=1).T

        self.dataframes_for_xlsx_export["stock_price_daily"] = pd.DataFrame(self.prices_with_delta_by_row["tageskurse"], columns=["Datum", "Tageskurs", "+/-", "Delta"]).sort_index(ascending=False)
        self.dataframes_for_xlsx_export["stock_price_weekly"] = pd.DataFrame(self.prices_with_delta_by_row["wochenkurse"], columns=["Datum", "Wochenkurs", "+/-", "Delta"]).sort_index(ascending=False)
        self.dataframes_for_xlsx_export["stock_price_quarterly"] = pd.DataFrame(self.prices_with_delta_by_row["historischekurse"], columns=["Datum", "Quartalskurs", "+/-", "Delta"]).sort_index(ascending=False)
        self.dataframes_for_xlsx_export["stock_dividend_history"] = pd.DataFrame(self.prices_with_delta_by_row["dividendenhistorie"], columns=["Datum", "Dividende", "+/-", "Delta"]).sort_index(ascending=False)
        self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"] = pd.DataFrame(self.prices_with_delta_by_row["handelsumsatz_12monate"], columns=["Datum", "Handelsumsatz", "+/-", "Delta"]).sort_index(ascending=False)
        self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"] = pd.DataFrame(self.prices_with_delta_by_row["handelsumsatz_historisch"], columns=["Datum", "Handelsumsatz", "+/-", "Delta"]).sort_index(ascending=False)
        self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"] = pd.DataFrame(self.prices_with_delta_by_row["marktkapitalisierungfreefloat_historisch"], columns=["Datum", "Marktkapitalisierung", "+/-", "Delta"]).sort_index(ascending=False)
        
        self.dataframes_for_xlsx_export["stock_price_daily_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_price_daily"].index)+1)       
        self.dataframes_for_xlsx_export["stock_price_weekly_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_price_weekly"].index)+1)
        self.dataframes_for_xlsx_export["stock_price_quarterly_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_price_quarterly"].index)+1)       
        self.dataframes_for_xlsx_export["stock_dividend_history_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_dividend_history"].index)+1)
        self.dataframes_for_xlsx_export["stock_volume_transaction_one_year_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"].index)+1)
        self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"].index)+1)
        self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly_row_count"] = str(len(self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"].index)+1)

    def create_xlsx(self):
        current_date = datetime.now()
        current_id = str(self.id)
        while len(current_id) < 3:
            current_id = "0"+current_id
        xlsx_filename = str(self.index).upper()+"_ID_"+current_id+"_"+str(current_date.date())+"_"+str(self.name)+".xlsx"
        xlsx_root = os.path.join(os.path.dirname(__file__), "..")
        if "xlsx" not in os.listdir(xlsx_root):
            status_messages.status(281)
            os.mkdir(xlsx_root + "/" + "xlsx")
        xlsx_filepath = xlsx_root + "/xlsx/" + xlsx_filename
        status_messages.xlsx(xlsx_filename)
      
        with pd.ExcelWriter(xlsx_filepath, date_format="DD.MM.YYYY", datetime_format="DD.MM.YYYY", engine="xlsxwriter") as writer: #pylint: disable=abstract-class-instantiated
            self.dataframes_for_xlsx_export["stock_first_sheet_overview"].to_excel(writer, sheet_name=str(self.name).upper())
            self.dataframes_for_xlsx_export["stock_price_daily"].to_excel(writer, sheet_name="Daily Stock Prices")
            self.dataframes_for_xlsx_export["stock_price_weekly"].to_excel(writer, sheet_name="Weekly Stock Prices")
            self.dataframes_for_xlsx_export["stock_price_quarterly"].to_excel(writer, sheet_name="Quarterly Stock Prices")
            self.dataframes_for_xlsx_export["stock_dividend_history"].to_excel(writer, sheet_name="Dividends History")
            self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"].to_excel(writer, sheet_name="Transaction Volume 12 Months")
            self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"].to_excel(writer, sheet_name="Transaction Volume History")
            self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"].to_excel(writer, sheet_name="Market Capitalization")
            
            workbook = writer.book
            format_thousands = workbook.add_format({'num_format': '#,##0', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
            format_percentage = workbook.add_format({'num_format': '[Color 23]#,##0.00%;[RED]-#,##0.00%', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
            format_font = workbook.add_format({'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
            if self.index in ["dax", "mdax", "sdax", "xetra", "germany", "scale", "ibex", "cac"]:
                format_currency_int = workbook.add_format({'num_format': '#,##0 [$€-407]', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
                format_currency_float = workbook.add_format({'num_format': '#,##0.00 [$€-407]', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
            elif self.index in ["dow", "nasdaq", "nyse"]:
                format_currency_int = workbook.add_format({'num_format': '#,##0 [$$-409]', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
                format_currency_float = workbook.add_format({'num_format': '#,##0.00 [$$-409]', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
            elif self.index in ["ftse"]:
                format_currency_int = workbook.add_format({'num_format': '#,##0 [$£-809]', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
                format_currency_float = workbook.add_format({'num_format': '#,##0.00 [$£-809]', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
           
            def draw_sheet_overview(sheet_name):
                sheet = writer.sheets[sheet_name]
                sheet.set_column('A:A', 50)
                sheet.set_column('B:B', 20, format_font)
                sheet.conditional_format('B4:B5', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B7:B8', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})
                sheet.conditional_format('B10', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_thousands})
                sheet.conditional_format('B11', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_currency_float})
                sheet.conditional_format('B12', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})
                sheet.conditional_format('B13:B16', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_int})
                sheet.conditional_format('B17:B19', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_thousands})
                sheet.conditional_format('B20:B22', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B23:B25', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B28:B30', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B31:B33', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B36:B38', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B39:B41', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B44:B46', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B47:B49', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B52:B54', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B55:B57', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B60:B62', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B63:B65', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B68:B70', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B71:B73', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B76:B78', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B79:B81', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B84:B86', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B87:B89', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})
                sheet.conditional_format('B92:B94', {'type': 'cell', 'criteria': 'between', 'minimum': -1, 'maximum': 100, 'format': format_percentage})          
                sheet.conditional_format('B95:B97', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': format_currency_float})

            def draw_sheet(sheet_name, column_name, chart_type, chart_title, row_count, format_type, y_axis_min, y_axis_max):
                sheet = writer.sheets[sheet_name]
                sheet.set_column('B:B', 10)
                sheet.set_column('C:C', 20, format_type)
                sheet.set_column('D:D', 10, format_percentage)
                sheet.set_column('E:E', 80, format_percentage)
                sheet.conditional_format("C2:C"+row_count, {'type': '3_color_scale'})
                sheet.conditional_format("D2:D"+row_count, {'type': 'icon_set', 'icon_style': '3_arrows', 'icons': [{'criteria': '>=', 'type': 'number', 'value': 0.00001}, {'criteria': '<=', 'type': 'number', 'value': -0.00001}]})
                sheet.conditional_format("E2:E"+row_count, {'type': 'data_bar', 'data_bar_2010': True, 'bar_axis_position': 'middle', 'min_value': -1, 'max_value': 1})
                chart = workbook.add_chart({'type': chart_type})
                chart.set_title ({'name': chart_title})
                chart.set_style(2)
                chart.set_size({'width': 1280, 'height': 720})
                chart.set_x_axis({'name': 'Datum', 'name_font': {'size': 12, 'bold': True}})
                chart.set_y_axis({'min': y_axis_min, 'max': y_axis_max, 'name': column_name, 'name_font': {'size': 12, 'bold': True}})
                chart.add_series({'values': "="+"'"+sheet_name+"'"+"!$C2:$C"+row_count, 'categories': "="+"'"+sheet_name+"'"+"!$B2:$B"+row_count, 'name': "="+"'"+sheet_name+"'"+"!$C$1"})
                sheet.insert_chart('G2', chart)
            
            draw_sheet_overview(str(self.name).upper())
            draw_sheet("Daily Stock Prices",
                "Kurs", "line", "Tageskurse der letzten 12 Monate",
                self.dataframes_for_xlsx_export["stock_price_daily_row_count"], format_currency_float,
                int(self.dataframes_for_xlsx_export["stock_price_daily"]['Tageskurs'].min()*0.95),
                int(self.dataframes_for_xlsx_export["stock_price_daily"]['Tageskurs'].max()*1.05)
                )
            draw_sheet("Weekly Stock Prices",
                "Kurs", "line", "Wochenkurse der letzten zwei Jahre",
                self.dataframes_for_xlsx_export["stock_price_weekly_row_count"], format_currency_float,
                int(self.dataframes_for_xlsx_export["stock_price_weekly"]['Wochenkurs'].min()*0.95),
                int(self.dataframes_for_xlsx_export["stock_price_weekly"]['Wochenkurs'].max()*1.05)
                )
            draw_sheet("Quarterly Stock Prices",
                "Kurs", "line", "Quartalskurse der letzten Jahre",
                self.dataframes_for_xlsx_export["stock_price_quarterly_row_count"], format_currency_float,
                int(self.dataframes_for_xlsx_export["stock_price_quarterly"]['Quartalskurs'].min()*0.95),
                int(self.dataframes_for_xlsx_export["stock_price_quarterly"]['Quartalskurs'].max()*1.05)
                )
            draw_sheet("Dividends History",
                "Dividende", "column", "Dividendenhistorie der letzten Jahre",
                self.dataframes_for_xlsx_export["stock_dividend_history_row_count"], format_currency_float,
                int(self.dataframes_for_xlsx_export["stock_dividend_history"]['Dividende'].min()),
                int(self.dataframes_for_xlsx_export["stock_dividend_history"]['Dividende'].max())
                )
            draw_sheet("Transaction Volume 12 Months",
                "Handelsumsatz", "line", "Handelsumsätze der letzten 12 Monate",
                self.dataframes_for_xlsx_export["stock_volume_transaction_one_year_row_count"], format_currency_int,
                round(int(self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"]['Handelsumsatz'].min()), -len(str(int(self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"]['Handelsumsatz'].min())))+1),
                round(int(self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"]['Handelsumsatz'].max()), -len(str(int(self.dataframes_for_xlsx_export["stock_volume_transaction_one_year"]['Handelsumsatz'].max())))+1)
                )
            draw_sheet("Transaction Volume History",
                "Handelsumsatz", "line", "Historischer Handelsumsatz",
                self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly_row_count"], format_currency_int,
                round(int(self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"]['Handelsumsatz'].min()), -len(str(int(self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"]['Handelsumsatz'].min())))+1),
                round(int(self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"]['Handelsumsatz'].max()), -len(str(int(self.dataframes_for_xlsx_export["stock_volume_transaction_quarterly"]['Handelsumsatz'].max())))+1)
                )
            draw_sheet("Market Capitalization",
                "Marktkapitalisierung", "line", "Historische Marktkapitalisierung (Free Float)",
                self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly_row_count"], format_currency_int,
                round(int(self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"]['Marktkapitalisierung'].min()), -len(str(int(self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"]['Marktkapitalisierung'].min())))+1),
                round(int(self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"]['Marktkapitalisierung'].max()), -len(str(int(self.dataframes_for_xlsx_export["stock_market_capitalization_free_float_quarterly"]['Marktkapitalisierung'].max())))+1)
                )
            status_messages.sneak_preview(self.dataframes_for_xlsx_export)
