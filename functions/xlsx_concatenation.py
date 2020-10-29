from functions import status_messages
from datetime import datetime
import pandas as pd
import os

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
        df_crop_1 = pd.read_excel(file, sheet_name=0, index_col=0).iloc[0:120]
        df_crop_2 = pd.read_excel(file, sheet_name=0, index_col=0).iloc[125:]
        df_complete = pd.concat([df_crop_1, df_crop_2], axis=0)        
        dataframes.append(df_complete)
    dataframe = pd.concat(dataframes, axis=1).T
    return dataframe

def initiate_export(dataframe, custom_filename, custom_folder):
    current_date = datetime.now()
    xlsx_root = os.path.join(os.path.dirname(__file__), "..")
    filename = xlsx_root + "/" + custom_folder + "/" + str(current_date.date()) + "_" + custom_filename
    if custom_folder not in os.listdir(xlsx_root):
        status_messages.status(282)
        os.mkdir(xlsx_root + "/" + custom_folder)
    dataframe_to_xlsx(filename, dataframe)

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
        dataframe_sheet.set_column('D:E', 15, format_currency_float)
        dataframe_sheet.set_column('F:F', 20, format_date)
        dataframe_sheet.set_column('G:H', 20, format_percentage)
        dataframe_sheet.set_column('I:I', 20, format_date)
        dataframe_sheet.set_column('J:J', 20, format_thousands)
        dataframe_sheet.set_column('K:K', 20, format_currency_float)
        dataframe_sheet.set_column('L:L', 20, format_percentage)
        dataframe_sheet.set_column('M:M', 20, format_date)
        dataframe_sheet.set_column('N:Q', 20, format_currency_int)
        dataframe_sheet.set_column('R:S', 20, format_thousands)
        
        dataframe_sheet.set_column('T:V', 20, format_percentage)
        dataframe_sheet.set_column('W:Y', 20, format_currency_float)
        dataframe_sheet.set_column('Z:AA', 20, format_date)

        dataframe_sheet.set_column('AB:AD', 20, format_percentage)
        dataframe_sheet.set_column('AE:AG', 20, format_currency_float)
        dataframe_sheet.set_column('AH:AI', 20, format_date)

        dataframe_sheet.set_column('AJ:AL', 20, format_percentage)
        dataframe_sheet.set_column('AM:AO', 20, format_currency_float)
        dataframe_sheet.set_column('AP:AQ', 20, format_date)

        dataframe_sheet.set_column('AR:AT', 20, format_percentage)
        dataframe_sheet.set_column('AU:AW', 20, format_currency_float)
        dataframe_sheet.set_column('AX:AY', 20, format_date)

        dataframe_sheet.set_column('AZ:BB', 20, format_percentage)
        dataframe_sheet.set_column('BC:BE', 20, format_currency_float)
        dataframe_sheet.set_column('BF:BG', 20, format_date)

        dataframe_sheet.set_column('BH:BJ', 20, format_percentage)
        dataframe_sheet.set_column('BK:BM', 20, format_currency_float)
        dataframe_sheet.set_column('BN:BO', 20, format_date)

        dataframe_sheet.set_column('BP:BR', 20, format_percentage)
        dataframe_sheet.set_column('BS:BU', 20, format_currency_float)
        dataframe_sheet.set_column('BV:BW', 20, format_date)

        dataframe_sheet.set_column('BX:BZ', 20, format_percentage)
        dataframe_sheet.set_column('CA:CC', 20, format_currency_float)
        dataframe_sheet.set_column('CD:CE', 20, format_date)

        dataframe_sheet.set_column('CF:CH', 20, format_percentage)
        dataframe_sheet.set_column('CI:CK', 20, format_currency_float)
        dataframe_sheet.set_column('CL:CM', 20, format_date)

        dataframe_sheet.set_column('CN:CP', 20, format_percentage)
        dataframe_sheet.set_column('CQ:CS', 20, format_currency_float)
        dataframe_sheet.set_column('CT:CU', 20, format_date)

        dataframe_sheet.set_column('CV:FB', 20, format_font)

def shortcut(custom_filename = "cuvee.xlsx", custom_folder = "cuvee"):
    status_messages.concatenation(1, custom_folder)
    initiate_export(create_dataframe(get_xlsx_files()), custom_filename, custom_folder)
