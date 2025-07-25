# Optimizador Entero con Cortes de Gomory

Este proyecto es un programa interactivo en Python para resolver **problemas de Programación Lineal Entera (PLE)** utilizando el **método de planos de corte de Gomory**. Permite al usuario ingresar manualmente un modelo de optimización, aplicar cortes iterativos, y obtener una solución entera óptima (si existe).

---

## 🚀 Características principales

* 🧮 Permite **maximizar o minimizar** una función objetivo.
* 🔢 Acepta restricciones con **desigualdades (≤, ≥, =)**.
* 🧠 Implementa el método de **cortes de Gomory simulados**.
* 📄 Permite **guardar la solución** en un archivo `.txt`.

---

## 📦 Requisitos

Este programa fue desarrollado en **Python 3.10+** y requiere las siguientes librerías:

* [`pulp`](https://pypi.org/project/PuLP/) — Para modelar y resolver problemas de optimización lineal.
* [`numpy`](https://pypi.org/project/numpy/) — Para manipulación básica de matrices y cálculo de partes fraccionarias.

### 📥 Instalación

Puedes instalar las dependencias necesarias con:

```bash
pip install pulp numpy
```

---

## ▶️ Cómo usar el programa

1. Ejecuta el script desde la terminal o tu editor:

```bash
python PlanosCortes.py
```

2. Ingresa el tipo de optimización (`Maximizar` o `Minimizar`).
3. Introduce la función objetivo y las restricciones.
4. El programa resolverá el problema y, si encuentra soluciones fraccionarias, aplicará automáticamente **cortes de Gomory**.
5. Podrás guardar los resultados en un archivo `.txt` al finalizar.

---

## 📝 Ejemplo rápido

```
Tipo de problema: Maximizar
Función objetivo: Z = 3x1 + 2x2
Restricciones:
  2x1 + 3x2 ≤ 17
  4x1 + x2 ≤ 15
```

El programa resolverá el problema, detectará si hay variables fraccionarias y aplicará cortes hasta alcanzar una solución entera o agotar el número de cortes permitidos.

---

## ❌ Advertencia

Este programa es un **prototipo educativo**. No se recomienda para problemas reales complejos o de gran escala, ya que:

* No implementa una lectura real del tableau Simplex.
* Los cortes son simulados con base en valores de entrada, no del solver.
* Puede no encontrar soluciones enteras si los datos no lo permiten.

---

## 💡 Aportes futuros

* Lectura real del tableau del solver.
* Interfaz gráfica para ingreso de datos.
* Soporte para variables enteras mixtas.

---

🚀 Hecho con fines académicos y de aprendizaje. ¡Explora y mejora libremente!
