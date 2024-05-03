def direction(deg):
    if deg <= 22.5:
        return 'ССВ'
    if deg <= 45:
        return 'СВ'
    if deg <= 67.5:
        return 'ВСВ'
    if deg <= 90:
        return 'В'
    if deg <= 112.5:
        return 'ВЮВ'
    if deg <= 135:
        return 'ЮВ'
    if deg <= 157.5:
        return 'ЮЮВ'
    if deg <= 180:
        return 'Ю'
    if deg <= 202.5:
        return 'ЮЮЗ'
    if deg <= 225:
        return 'ЮЗ'
    if deg <= 247.5:
        return 'ЗЮЗ'
    if deg <= 270:
        return 'З'
    if deg <= 292.5:
        return 'ЗСЗ'
    if deg <= 315:
        return 'СЗ'
    if deg <= 337.5:
        return 'ССЗ'
    if deg <= 360:
        return 'С'







