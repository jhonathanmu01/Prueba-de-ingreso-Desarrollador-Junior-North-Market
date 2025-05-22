def numero_mas_frecuente(lista):
    # Verificar si la lista está vacía
    if not lista:
        print("arreglo vacío")
        return None
    
    # Crear un diccionario para contar las frecuencias
    frecuencias = {}
    
    # Contar la frecuencia de cada número
    for num in lista:
        if num in frecuencias:
            frecuencias[num] += 1
        else:
            frecuencias[num] = 1
    
    # Encontrar la máxima frecuencia
    max_frecuencia = max(frecuencias.values())
    
    # Recoger todos los números con la máxima frecuencia
    numeros_mas_frecuentes = [num for num, freq in frecuencias.items() if freq == max_frecuencia]
    
    # Si hay más de uno, devolver el menor
    if len(numeros_mas_frecuentes) > 1:
        return min(numeros_mas_frecuentes)
    else:
        return numeros_mas_frecuentes[0]

# Ejemplos de uso
print(numero_mas_frecuente([0]))               # Debe devolver 0
print(numero_mas_frecuente([-4, -4, -5, -5]))  # Debe devolver -5 (no -4 como decías en el comentario)
print(numero_mas_frecuente([1, 2, 3, 4, 5]))   # Todos con frecuencia 1, debe devolver 1 (el menor)
print(numero_mas_frecuente([2, 2, 1, 1, 3]))   # Empate entre 2 y 1, debe devolver 1
print(numero_mas_frecuente([]))                # Imprime "arreglo vacío" y devuelve None