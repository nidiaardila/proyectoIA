## Registro del ensayo de rate limit

- **Fecha:** 2026-10-27
- **Peticiones enviadas:** 10 (lote de Respuesta 0 a Respuesta 9)
- **Petición donde apareció el primer 429:** la número 6 (índice `Respuesta 5`)
- **Esperas observadas:** 2.0s–2.1s, 4.0s–4.3s (backoff exponencial con jitter, correcto)
- **Costo total del ensayo:** $0.00513 ($0.00537 acumulado total en la sesión)
- **Resultado:** 7 peticiones completadas con éxito (5 inmediatas y 2 recuperadas tras reintento) y 3 fallaron definitivamente tras agotar los 3 intentos (Respuestas 5, 7 y 8).