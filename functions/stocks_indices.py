indices = {
    0:  "undefined",
    1:  "dow",
    2:  "nasdaq",
    3:  "nyse",
    4:  "dax",
    5:  "mdax",
    6:  "sdax",
    7:  "scale",
    8:  "ftse",
    9:  "cac",
    10: "ibex",
    11: "shorties",
    12: "",
    13: "asianstockexchanges",
    14: "",
    15: "europeanstockexchanges"
    }

def get(code, indices=indices):
    return indices[code]