from django import template

register = template.Library()


@register.filter(name='makerange')
def makerange_(num):
    return range(num)


@register.filter(name='checkpayment')
def checkpayment_(num):
    return num > 0
    

@register.filter(name='checkstring')
def checkstring_(str_):
    str_ = str(str_)
    return "reachable" in str_

@register.filter(name='checkloginstring')
def checkloginstring_(str_):
    str_ = str(str_)
    return "Account was created" in str_


@register.filter(name='orderbydate')
def orderbydate_(list_):
    print(list_)
    return reversed(list_)
    # return list_


@register.filter(name='checklength')
def orderbydate_(some):
    return len(some)


@register.filter(name='logsignpass')
def logsignpass_(validatoins):
    list__ = [
        '/signup/',
        '/login/',
        '/request_reset_email/',
        '/set_new_password/'
    ]
    if validatoins in list__:
        return True
    else:
        return False
