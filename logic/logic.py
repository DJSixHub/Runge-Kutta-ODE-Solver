from astAL import Expression
from lexer import Lexer, TOKEN_PATTERNS, CONSTANTS, Token
from parser import Parser
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from error import *
from matplotlib.quiver import Quiver


class RungeKutta:
    def __init__(self, x0: int, y0: int, xf: int, h: float, function: str):
        try:
            self.x0: float = float(x0)
            self.y0: float = float(y0)
            self.h: float = float(h)
            self.xf: float = float(xf)

            self.lexer: Lexer = Lexer(TOKEN_PATTERNS, CONSTANTS)
            self.tokens: list[Token] = self.lexer.tokenize(function)
            self.parser: Parser = Parser()
            self.ast: Expression = self.parser.make_ast(self.tokens)
        except ValueError as e:
            raise ValueError("introduzca valores válidos.")
        except Parentesis_Error as e:
            raise Parentesis_Error()

    def edo(self, vars: dict) -> float:

        variables = {"e": 2.718281828459045, "pi": 3.141592653589793}
        for key, value in vars.items():
            variables[key] = value
        return self.ast.eval(variables)

    def solver(self) -> Tuple[List[float], List[float]]:
        try:
            X_right = np.arange(self.x0, self.xf, self.h)

            y_right = np.zeros(len(X_right))

            y_right[0] = self.y0
            #### Runge-Kutta
            for i in range(len(X_right) - 1):
                k1 = self.edo({"x": X_right[i], "y": y_right[i]})
                k2 = self.edo({"x": X_right[i] + self.h / 2, "y": y_right[i] + k1 / 2})
                k3 = self.edo({"x": X_right[i] + self.h / 2, "y": y_right[i] + k2 / 2})
                k4 = self.edo({"x": X_right[i] + self.h, "y": y_right[i] + k3})
                y_right[i + 1] = y_right[i] + self.h * (
                    k1 / 6 + k2 / 3 + k3 / 3 + k4 / 6
                )
            if any(np.isinf(y_right)) or any(np.isnan(y_right)):
                raise Inf()
            return X_right, y_right
        except:
            raise RK_Error()

    def isoclinas(self, x_min, x_max, y_min, y_max):
        x_values = np.linspace(x_min, x_max, 25)  
        y_values = np.linspace(y_min, y_max, 25)
        X, Y = np.meshgrid(x_values, y_values)
        U = np.ones_like(X)
        V = self.edo({"x": X, "y": Y})  
        aux = V.copy().flatten()
        if any(np.isinf(aux)) or any(np.isnan(aux)):
            raise Inf()
        return X.flatten().tolist(), Y.flatten().tolist(), U.flatten().tolist(), V.flatten().tolist()


