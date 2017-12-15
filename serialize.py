
import re

def is_php_serialize(s):
    m = re.search(r"(?:b|i|d|s|a|O):[\d\.]+[:;]", s)
    if m != None:
        return True
    return False

def test_is_php_serialize():
    assert True == is_php_serialize("b:1;")
    assert True == is_php_serialize("i:1;")
    assert True == is_php_serialize("d:0.2;")
    assert True == is_php_serialize("s:4:\"test\";")
    assert True == is_php_serialize("a:3:{i:0;")
    assert True == is_php_serialize("O:8:\";")

def get_cookie(res):
    if not res:
        return []
    lines = res.split("\n")
    cookies = []
    for line in lines:
        e = line.find(":")
        if e == -1:
            continue

        key = line[:e]
        value = line[e+1:]
        if key.lower().strip() == "set-cookie":
            cookies.append(value.strip())

    return cookies

def evaluate(res):
    cookies = get_cookie(res)
    for cookie in cookies:
        if is_php_serialize(cookie):
            return True
    return False


