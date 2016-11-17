


def containsStr(A,B):
    if B in A:
        return True
    else:
        return False


SHELL=['android','iphone','ipad','windows phone','touch','metasr','maxthon','qqbrowser','4399box','360se','2345Explorer','bidubrowser','theworld','youxihe','woshihoney','lbbrowser','tencenttraveler','opera']
def parseUserAgent(useragent):
    useragent=useragent.lower()
    type=''

    skip=True



    for char in SHELL:
        if containsStr(useragent,char):
            type=char
            break
        if SHELL[-1]==char:
            skip=False

    if(skip==False) :
        if 'windows nt 5.1'in useragent or 'windows nt 5.2'in useragent:
            if 'msie 6.0' in useragent:
                type='winxp+ie6'
            elif 'msie 7.0' in useragent:
                type='winxp+ie7'
            elif 'msie 8.0' in useragent:
                type='winxp+ie8'
            elif 'chrome'in useragent:
                type='winxp+chrome'
            elif 'firefox' in useragent:
                type='winxp+firefox'
            else:
                type='winxp+unknown'

        elif 'windows nt 6.0' in useragent:
            if 'msie 7.0' in useragent:
                type='winvista+ie7'
            elif 'msie 8.0' in useragent:
                type='winvista+ie8'
            elif 'msie 9.0' in useragent:
                type='winvista+ie9'
            elif 'chrome'in useragent:
                type='winvista+chrome'
            elif 'firefox' in useragent:
                type='winvista+firefox'
            else:
                type='winvista+unknown'
        elif 'windows nt 6.1' in useragent:
            if 'msie 7.0' in useragent:
                type='win7+ie7'
            elif 'msie 8.0' in useragent:
                type='win7+ie8'
            elif 'msie 9.0' in useragent:
                type='win7+ie9'
            elif 'msie 10.0' in useragent:
                type='win7+ie10'
            elif 'chrome'in useragent:
                type='win7+chrome'
            elif 'firefox' in useragent:
                type='win7+firefox'
            else:
                type='win7+unknown'
        elif 'windows nt 6.2' in useragent:
            if 'msie 7.0' in useragent:
                type='win8+ie7'
            elif 'msie 9.0' in useragent:
                type='win8+ie9'
            elif 'msie 10.0' in useragent:
                type='win8+ie10'
            elif 'chrome'in useragent:
                type='win8+chrome'
            elif 'firefox' in useragent:
                type='win8+firefox'
            else:
                type='win8+unknown'
        elif 'macintosh' in useragent:
            if 'chrome' in useragent:
                type='mac+chrome'
            elif 'safari' in useragent:
                type='mac+safari'
            else:
                type='mac+others'
        elif 'linux' in useragent:
            if 'chrome' in useragent:
                type='linux+chrome'
            elif 'firefox' in useragent:
                type='linux+firefox'
            else:
                type='linux+others'
        elif 'windows nt 5.0' in useragent:
            type='win2k+ie6'
        else:
            type='unrecognised'

    return type

