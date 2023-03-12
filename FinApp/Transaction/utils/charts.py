# util/charts.py

months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
colorPalette = ['#D1D3C4' ,'#fab1a0', '#55efc4', '#81ecec', '#a29bfe', '#ffeaa7', '#ff7675', '#fd79a8',  '2E0F15']
colorPrimary, colorSuccess, colorDanger = '#79aec8', colorPalette[0], colorPalette[5]


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        print("COLOR" + colorPalette[i])
        
        if i == len(colorPalette) and len(palette) < amount:
            i = 0
        i += 1
    return palette

def generate_color_palette_2(i):

    if i < len(colorPalette):
       return colorPalette[i]
    
    else:
       return colorPalette[i%len(colorPalette)]
    