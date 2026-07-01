def decor(fun):
    def inner():
        ret = fun()
        return ret+10
    return inner
    

def add10():
    return 5

decor_ret = decor(add10)
print(decor_ret())