from hulk.hulk import hulk_compile_str

def hulk_compile():

    f = open('main.hulk')
    p = f.read()
    f.close()

    hulk_compile_str(p)

hulk_compile()
