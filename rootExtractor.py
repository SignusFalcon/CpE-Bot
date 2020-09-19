import sympy as sp
import re


def extract_root(func: str, debug: bool = False) -> list:
    def function_cleaner(func: str, dbg: bool = False) -> sp.Function:
        try:
            if "^" in func:
                raise SyntaxError
            else:
                return sp.parse_expr(func)
        except SyntaxError or TypeError:
            pass

        func_dict = {'^': '**', 'e': 'E'}
        trans_table = func.maketrans(func_dict)

        translated = func.translate(trans_table)
        if translated[0] != "+" and translated[0] != "-":
            translated = "+" + translated
        monomialsToBeConverted = re.findall(r"[+|\-][0-9]+[a-z]", translated)

        if dbg:
            print(monomialsToBeConverted)

        def multiply_var(mono: list) -> list:
            joined = list()
            for x in mono:
                variables = re.search(r"[a-z]", x)
                if not variables:
                    joined.append(x)
                else:
                    joined.append(x[:variables.start()] + "*" + x[variables.start():])
            return joined

        replacementTerms = multiply_var(monomialsToBeConverted)

        if dbg:
            print(replacementTerms)

        for monomial in range(len(monomialsToBeConverted)):
            translated = translated.replace(monomialsToBeConverted[monomial], replacementTerms[monomial])

        if dbg:
            print(translated)

        return sp.parse_expr(translated)

    x = sp.Symbol('x')
    function = function_cleaner(func, debug)
    if debug:
        print(function)
    dict_result = sp.solve(function, dict=True)
    list_result = list()

    for val in dict_result:
        list_result.append(val[x].evalf())

    return list_result


#function_sample = "-x^2+x"
#print(extract_root(function_sample, debug=True))
