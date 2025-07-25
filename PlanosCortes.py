import pulp
import numpy as np

class ModeloPL:
    def __init__(self):
        self.problema = None
        self.variables = []
        self.num_variables = 0
        self.num_restricciones = 0
        self.tipo_optimizacion = None
        self.matriz_restricciones = []
        self.vector_lado_derecho = []
        self.coef_objetivo = []

    def solicitar_numero(self, mensaje, tipo=float, minimo=0):
        while True:
            try:
                valor = tipo(input(mensaje))
                if valor < minimo:
                    print(f"Debe ser un número mayor o igual a {minimo}.")
                else:
                    return valor
            except ValueError:
                print("Entrada inválida. Intente nuevamente.")

    def solicitar_datos(self):
        print("¿Qué tipo de problema desea resolver?")
        print("1. Maximizar")
        print("2. Minimizar")
        while True:
            opcion = input("Seleccione (1/2): ").strip()
            if opcion == '1':
                self.tipo_optimizacion = pulp.LpMaximize
                break
            elif opcion == '2':
                self.tipo_optimizacion = pulp.LpMinimize
                break
            else:
                print("Opción inválida. Escriba 1 o 2.")

        self.num_variables = self.solicitar_numero("Ingrese el número de variables (mínimo 1): ", int, 1)
        self.num_restricciones = self.solicitar_numero("Ingrese el número de restricciones (mínimo 1): ", int, 1)

        print("\nIngrese los coeficientes de la función objetivo:")
        for i in range(self.num_variables):
            coef = self.solicitar_numero(f"Coeficiente de x{i+1}: ")
            self.coef_objetivo.append(coef)

        print("\nIngrese los coeficientes y lado derecho de cada restricción (de la forma ≤):")
        for r in range(self.num_restricciones):
            fila = []
            for i in range(self.num_variables):
                coef = self.solicitar_numero(f"Coef x{i+1} en restricción {r+1}: ")
                fila.append(coef)
            self.matriz_restricciones.append(fila)
            lado_derecho = self.solicitar_numero(f"Lado derecho de restricción {r+1}: ")
            self.vector_lado_derecho.append(lado_derecho)

    def construir_modelo(self):
        self.problema = pulp.LpProblem("Problema_Cortes_Gomory", self.tipo_optimizacion)
        self.variables = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(self.num_variables)]
        self.problema += pulp.lpSum([self.coef_objetivo[i] * self.variables[i] for i in range(self.num_variables)]), "Función Objetivo"

        for i in range(self.num_restricciones):
            restriccion = pulp.lpSum([self.matriz_restricciones[i][j] * self.variables[j] for j in range(self.num_variables)])
            self.problema += restriccion <= self.vector_lado_derecho[i], f"Restriccion_{i+1}"

    def imprimir_modelo(self):
        print("\n📋 Modelo ingresado:")
        objetivo = "Maximizar" if self.tipo_optimizacion == pulp.LpMaximize else "Minimizar"
        print(f"{objetivo}: ", end="")
        print(" + ".join(f"{self.coef_objetivo[i]}*x{i+1}" for i in range(self.num_variables)))

        print("Sujeto a:")
        for i in range(self.num_restricciones):
            izquierda = " + ".join(f"{self.matriz_restricciones[i][j]}*x{j+1}" for j in range(self.num_variables))
            print(f"{izquierda} ≤ {self.vector_lado_derecho[i]}")
        print("Y todas las variables ≥ 0")

    def mostrar_solucion(self):
        print(f"\n🧮 Estado: {pulp.LpStatus[self.problema.status]}")
        for var in self.variables:
            print(f"{var.name} = {round(var.varValue, 4)}")

    def obtener_tableau_simulado(self):
        tableau = []
        for i in range(self.num_restricciones):
            fila = self.matriz_restricciones[i] + [self.vector_lado_derecho[i]]
            tableau.append(fila)
        return np.array(tableau)

    def agregar_corte_gomory(self, tableau):
        filas, columnas = tableau.shape
        for i in range(filas):
            if not np.isclose(tableau[i, -1], np.floor(tableau[i, -1])):
                corte = np.floor(tableau[i, -1]) - tableau[i, -1]
                for j in range(columnas - 1):
                    if not np.isclose(tableau[i, j], 0):
                        corte += (tableau[i, j] - np.floor(tableau[i, j])) * self.variables[j]
                self.problema += corte <= 0, f"Corte_Gomory_{i}"
                print(f"➕ Corte de Gomory agregado a partir de la fila {i+1}")
                return True
        return False

    def resolver_con_cortes(self):
        self.problema.solve(pulp.PULP_CBC_CMD(msg=False))
        self.mostrar_solucion()
        tableau = self.obtener_tableau_simulado()

        while True:
            if not self.agregar_corte_gomory(tableau):
                break
            self.problema.solve(pulp.PULP_CBC_CMD(msg=False))
            self.mostrar_solucion()

if __name__ == "__main__":
    modelo = ModeloPL()
    modelo.solicitar_datos()
    modelo.construir_modelo()
    modelo.imprimir_modelo()
    modelo.resolver_con_cortes()
