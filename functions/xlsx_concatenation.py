from functions import runtimer, status_messages
from datetime import datetime
import pandas as pd
import os

def shortcut(custom_filename = "cuvee.xlsx", custom_folder = "cuvee"):
    stopwatch = runtimer.TimeKeeper()
    stopwatch.start()
    status_messages.concatenation(1, custom_folder)
    initiate_export(create_dataframe(get_xlsx_files()), custom_filename, custom_folder)
    stopwatch.show()

def initiate_export(dataframe, custom_filename, custom_folder):
    current_date = datetime.now()
    xlsx_root = os.path.join(os.path.dirname(__file__), "..")
    filename = xlsx_root + "/" + custom_folder + "/" + str(current_date.date()) + "_" + custom_filename
    if custom_folder not in os.listdir(xlsx_root):
        status_messages.status(282)
        os.mkdir(xlsx_root + "/" + custom_folder)
    dataframe_to_xlsx(filename, dataframe)

def get_xlsx_files():
    xlsx_root = os.path.join(os.path.dirname(__file__), "..")
    xlsx_folder = os.path.join(xlsx_root, "xlsx")
    xlsx_files = os.listdir(xlsx_folder)
    xlsx_files = [os.path.join(xlsx_folder, file) for file in xlsx_files]
    return xlsx_files

def create_dataframe(xlsx_files):
    dataframes = []
    for file in xlsx_files:
        status_messages.concatenation(2, file)
        # In case of table header label issue (out of sync for different stocks) select the synced ones by roughly cropping with iloc position aka columns.
        df_crop_1 = pd.read_excel(file, sheet_name=0, index_col=0).iloc[0:120]
        df_crop_2 = pd.read_excel(file, sheet_name=0, index_col=0).iloc[120:]
        df_complete = pd.concat([df_crop_1, df_crop_2], axis=0)
        dataframes.append(df_complete)
    dataframe = pd.concat(dataframes, axis=1).T
    return dataframe

def dataframe_to_xlsx(filename, dataframe):
    status_messages.concatenation(3, filename)
    with pd.ExcelWriter(filename, datetime_format='DD.MM.YYYY', engine="xlsxwriter") as writer: #pylint: disable=abstract-class-instantiated
        dataframe.to_excel(writer, sheet_name=str("Stats"))
        workbook = writer.book
        format_thousands = workbook.add_format({'num_format': '#,##0', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
        format_percentage = workbook.add_format({'num_format': '[Color 23]#,##0.00%;[RED]-#,##0.00%', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
        format_font = workbook.add_format({'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
        format_currency_int = workbook.add_format({'num_format': '#,##0', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
        format_currency_float = workbook.add_format({'num_format': '#,##0.00', 'font_name': 'Arial', 'font_size': '10', 'align': 'right', 'valign': 'vcenter'})
        format_date = workbook.add_format({'num_format': 'DD.MM.YYYY'})
        dataframe_sheet = writer.sheets[str("Stats")]
        dataframe_sheet.set_column('A:A', 20)
        dataframe_sheet.set_column('B:B', 16, format_date)
        dataframe_sheet.set_column('C:C', 9, format_font)
        dataframe_sheet.set_column('D:D', 25, format_font)
        dataframe_sheet.set_column('E:F', 15, format_currency_float)
        dataframe_sheet.set_column('G:G', 20, format_date)
        dataframe_sheet.set_column('H:I', 20, format_percentage)
        dataframe_sheet.set_column('J:J', 20, format_date)
        dataframe_sheet.set_column('K:K', 20, format_thousands)
        dataframe_sheet.set_column('L:L', 20, format_currency_float)
        dataframe_sheet.set_column('M:M', 20, format_percentage)
        dataframe_sheet.set_column('N:N', 20, format_date)
        dataframe_sheet.set_column('O:R', 20, format_currency_int)
        dataframe_sheet.set_column('S:T', 20, format_thousands)
        dataframe_sheet.set_column('U:W', 20, format_percentage)
        dataframe_sheet.set_column('X:Z', 20, format_currency_float)
        dataframe_sheet.set_column('AA:AB', 20, format_date)
        dataframe_sheet.set_column('AC:AE', 20, format_percentage)
        dataframe_sheet.set_column('AF:AH', 20, format_currency_float)
        dataframe_sheet.set_column('AI:AJ', 20, format_date)
        dataframe_sheet.set_column('AK:AM', 20, format_percentage)
        dataframe_sheet.set_column('AN:AP', 20, format_currency_float)
        dataframe_sheet.set_column('AQ:AR', 20, format_date)
        dataframe_sheet.set_column('AS:AU', 20, format_percentage)
        dataframe_sheet.set_column('AV:AX', 20, format_currency_float)
        dataframe_sheet.set_column('AY:AZ', 20, format_date)
        dataframe_sheet.set_column('BA:BC', 20, format_percentage)
        dataframe_sheet.set_column('BD:BF', 20, format_currency_float)
        dataframe_sheet.set_column('BG:BH', 20, format_date)
        dataframe_sheet.set_column('BI:BK', 20, format_percentage)
        dataframe_sheet.set_column('BL:BN', 20, format_currency_float)
        dataframe_sheet.set_column('BO:BP', 20, format_date)
        dataframe_sheet.set_column('BQ:BS', 20, format_percentage)
        dataframe_sheet.set_column('BT:BV', 20, format_currency_float)
        dataframe_sheet.set_column('BW:BX', 20, format_date)
        dataframe_sheet.set_column('BY:CA', 20, format_percentage)
        dataframe_sheet.set_column('CB:CD', 20, format_currency_float)
        dataframe_sheet.set_column('CE:CF', 20, format_date)
        dataframe_sheet.set_column('CG:CI', 20, format_percentage)
        dataframe_sheet.set_column('CJ:CL', 20, format_currency_float)
        dataframe_sheet.set_column('CM:CN', 20, format_date)
        dataframe_sheet.set_column('CO:CQ', 20, format_percentage)
        dataframe_sheet.set_column('CR:CT', 20, format_currency_float)
        dataframe_sheet.set_column('CU:CV', 20, format_date)
        dataframe_sheet.set_column('CW:FD', 20, format_font)