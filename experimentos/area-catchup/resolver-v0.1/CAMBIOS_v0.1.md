# Cambios v0.1

- Agregado resolver puro y determinista para timers, meters lineales y eventos programados absolutos.
- Agregada validación estricta mediante descriptores propios, con rechazo de accessors, campos extra, estructuras heredadas y arrays dispersos.
- Agregada aritmética BigInt para saturación segura de meters dentro del rango de enteros seguros.
- Agregados fixtures, 101 pruebas y stress reproducible con oracle independiente, cinco seeds y digest SHA-256.
- La salida usa orden canónico y no ejecuta eventos ni integra otros laboratorios.
