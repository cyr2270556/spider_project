import execjs


def get_sign(target):
    with open("first.js","r",encoding="utf-8") as f:
        js=execjs.compile(f.read())
    sign=js.call("e",str(target))
    return sign

