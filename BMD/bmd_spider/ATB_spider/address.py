import re

target = '<tr><th>地址：</th><td><a href="/Companys/s-p26/">四川</a> - <a href="/Companys/s-p26-s568/">成都</a> - <a href="/Companys/s-p26-s568-q2171/">青白江</a> \xa0 中国（四川）自由贸易试验区成都市青白江区清泉大道一段716号（成都万贯五金机电配送大市场（一期）66栋2单<span class="size88">代大富(http://www.atobo.com)</span>元1-3层4号</td></tr>'


# </a> \xa0 中国（四川）自由贸易试验区成都市青白江区清泉大道一段716号（成都万贯五金机电配送大市场（一期）66栋2单<span class="size88">

def find_address(target):
    b = re.compile('\xa0.*?</td>', re.S)

    # c=  中国（四川）自由贸易试验区成都市青白江区清泉大道一段716号（成都万贯五金机电配送大市场（一期）66栋2单<span class="size88">代大富(http://www.atobo.com)</span>元1-3层4号</td>

    c = b.findall(target)[0].strip()
    g = c.replace('</td>', '')
    d = re.compile('<.+>', re.S)

    # e=  '<span class="size88">代大富(http://www.atobo.com)</span>'
    e = d.findall(g)[0]

    f = c.replace(e, '')
    h = f.replace('</td>', '')
    return h
