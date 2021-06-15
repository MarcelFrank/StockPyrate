from datetime import date, timedelta
import random

def get(key):
    testdata = {}
    testdata["statistics"] = {
        'Marktkap. (im Tagesverlauf)': '223,5B', 'Unternehmenswert': '236,99B', 'Verg. P/E': '12,42', 'Erwartetes KGV': '12,06', 'PEG-Ratio (5 Jahre erwartet)': '2,34', 'Preis/Verkauf': '2,88', 'Preis/Buch': '2,80', 'Unternehmenswert/Umsatz': '3,05', 'Unternehmenswert/EBITDA': '6,84', 'Beta (5 J., monatlich)': '0,60', 'Veränderung über 52 Wochen': '-7,63%', 'S&P500 Veränderung über 52 Wochen': '41,30%', '52-Wochen-Hoch': '68,49', '52-Wochen-Tief': '43,61', 'Gleitender Durchschnitt 50 Tage': '61,09', 'Gleitender Durchschnitt 200 Tage': '55,88', 'Durchschn. Vol. (3 M.)': '31,12M', 'Durchschn. Vol. (10 Tage)': '29,15M', 'Aktien im Umlauf': '4,04B', 'Implizierte Aktien im Umlauf': 'N/A', 'Float': '4,02B', '% Beteiligung von Insidern': '0,06%', '% Beteiligung von Institutionen': '66,11%', 'Aktien (Short) (29. Apr. 2021)': '50,07M', 'Short Ratio (29. Apr. 2021)': '1,62', 'Short % / Float (29. Apr. 2021)': '1,24%', 'Short % der Aktien im Umlauf (29. Apr. 2021)': '1,24%', 'Aktien (Short, vorher. Monat 30. März 2021)': '56,96M', 'Erwartete Jahresdividendenrate': '1.39', 'Erwarteter Jahresdividendenertrag': '2,51%', 'Verg. Jahresdividendensatz': '1,34', 'Verg. Jahresdividendenertrag': '2,48%', 'Durchschnittliche Dividendenrendite über 5 Jahre': '2,53', 'Ausschüttungsquote': '30,06%', 'Datum der Dividende': '31. Mai 2021', 'Ex-Dividendendatum': '05. Mai 2021', 'Letzter Splitfaktor': '2:1', 'Letztes Split-Datum': '30. Juli 2000', 'Geschäftsjahresende': '25. Dez. 2020', 'Letztes Quartal': '26. März 2021', 'Gewinnspanne': '23,93%', 'Operative Marge': '29,05%', 'Kapitalrentabilität': '9,46%', 'Eigenkapitalrendite': '23,82%', 'Umsatz': '77,71B', 'Umsatz pro Aktie': '18,74', 'Vierteljährliches Umsatzwachstum': '-0,80%', 'Bruttoergebnis vom Umsatz': '43,61B', 'EBITDA': '34,67B', 'Auf Stammaktien entfallender Jahresüberschuss': '18,6B', 'EPS (diluted)': '4,46', 'Vierteljährliches Gewinnwachstum': '-40,60%', 'Cash (gesamt)': '22,4B', 'Cash (gesamt) pro Aktie': '5,55', 'Schulden (gesamt)': '35,88B', 'Schulden/Equity (gesamt)': '44,96', 'Aktuelles Verhältnis': '1,89', 'Buchwert je Aktie': '19,76', 'Cashflow aus betrieblichen Tätigkeiten': '34,77B', 'Freier Cashflow nach Zinsen und Dividenden': '10,43B'
        }
    testdata["weekly_prices"] = [
        [date.today() + timedelta(days=-0),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-1),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-2),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-3),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-4),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-5),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-6),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-7),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-8),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-9),  random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-10), random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-11), random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-12), random.randint(100,110)+round(random.random(), 2)],
        [date.today() + timedelta(days=-13), random.randint(100,115)+round(random.random(), 2)],
        [date.today() + timedelta(days=-14), random.randint(100,115)+round(random.random(), 2)],
        [date.today() + timedelta(days=-15), random.randint(100,115)+round(random.random(), 2)],
        [date.today() + timedelta(days=-16), random.randint(100,115)+round(random.random(), 2)],
        [date.today() + timedelta(days=-17), random.randint(100,115)+round(random.random(), 2)],
        [date.today() + timedelta(days=-18), random.randint(100,120)+round(random.random(), 2)],
        [date.today() + timedelta(days=-19), random.randint(100,120)+round(random.random(), 2)],
        [date.today() + timedelta(days=-20), random.randint(100,120)+round(random.random(), 2)],
        [date.today() + timedelta(days=-21), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-22), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-23), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-24), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-25), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-26), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-27), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-28), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-30), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-31), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-32), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-33), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-34), random.randint(100,105)+round(random.random(), 2)],
        [date.today() + timedelta(days=-35), random.randint(100,105)+round(random.random(), 2)]
        ]
    testdata["weekly_volume"] = [
        [date.today() + timedelta(days=-0),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-1),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-2),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-3),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-4),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-5),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-6),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-7),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-8),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-9),  random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-10), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-11), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-12), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-13), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-14), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-15), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-16), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-17), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-18), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-19), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-20), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-21), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-22), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-23), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-24), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-25), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-26), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-27), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-28), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-30), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-31), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-32), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-33), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-34), random.randint(1000000,2000000)],
        [date.today() + timedelta(days=-35), random.randint(1000000,2000000)]
        ]
    testdata["monthly_prices"] = [
        [date.today() + timedelta(days=-0), 150.00],
        [date.today() + timedelta(days=-2), 111.11],
        [date.today() + timedelta(days=-7), 50.00],
        [date.today() + timedelta(days=-14), 50.00],
        [date.today() + timedelta(days=-21), 25.00]
        ]
    testdata["monthly_volume"] = [
        [date.today() + timedelta(days=-0), 19126096],
        [date.today() + timedelta(days=-2), 103314100], 
        [date.today() + timedelta(days=-7), 158579400], 
        [date.today() + timedelta(days=-14), 124091600], 
        [date.today() + timedelta(days=-21), 162214400]
        ]
    testdata["yearly_prices"] = [
         [date.today() + timedelta(days=-21), 55.35],
         [date.today() + timedelta(days=-90), 50.35],
         [date.today() + timedelta(days=-180), 64.00],
         [date.today() + timedelta(days=-270), 60.00],
         [date.today() + timedelta(days=-400), 33.00]
         ]
    testdata["yearly_volume"] = [
        [date.today() + timedelta(days=-21),  1583120],
        [date.today() + timedelta(days=-90),  1596800],
        [date.today() + timedelta(days=-180), 1698700],
        [date.today() + timedelta(days=-270), 1645700],
        [date.today() + timedelta(days=-400), 1645750]
        ]
    testdata["dividends"] = [
        [date.today() + timedelta(days=-3), 2.34],
        [date.today() + timedelta(days=-90), 5.34],
        [date.today() + timedelta(days=-180), 2.31],
        [date.today() + timedelta(days=-270), 1.20],
        [date.today() + timedelta(days=-400), 3.33]
        ]
    return testdata[key]