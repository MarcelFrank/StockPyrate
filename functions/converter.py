from datetime import datetime

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

def to_float(s): #*
    counter_comma = s.count(",")
    counter_dot = s.count(".")
    counter_total = counter_comma + counter_dot
    if counter_total == 1:
        s = s.replace(",", ".")
        if int(s[:s.find(".")]) > 4 and len(s[s.find(".")+1:]) == 3: #**
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