**6\. MANUAL DE USUARIO (DESCRIPCIÓN DEL FUNCIONAMIENTO)**

En este apartado se explica cómo interactúa un usuario con el videojuego.

Se ha capturado las pantallas del videojuego y se muestra el funcionamiento de las distintas opciones, mensajes de error, etc.

Nota: Para arrancar la aplicación es necesario elegir "Run Python File in Terminal" sobre la clase principal main.py.

**_6.1. Pantalla 1: Título y menú principal_**

**Objetivo:** punto de entrada al juego y acceso a las opciones básicas.

**Elementos en pantalla:**

- **Logo del juego:** "SPACE ESCAPE" en grande, estilo arcade, centrado.
- **Fondo animado:** planeta alienígena, estrellas, naves pasando lentamente.
- **Menú principal (lista):**
- **Jugar**
- **Créditos**
- **Instrucciones**
- **Níveles** (si está desbloqueado)
- **Salir**

**Interacción del usuario:**

- **Ratón:**
- **Arriba/abajo:** desplaza el cursor por las opciones.
- **Clica botón izquierdo:** confirma opción.
- **Salir:** Si clica en este botón sale de la aplicación.
- **Feedback visual:**
- Opción seleccionada resaltada con color, brillo o subrayado.
- Sonido corto al moverse por el menú y otro distinto al confirmar.

**_6.2. Pantalla 2: Pantalla de créditos_**

**Objetivo:** mostrar los créditos.

**Formato:**

- Ventanas con información textual sobre los autores del juego.

**Interacción del usuario:**

- Cerrar el mensaje con la mediante la acción Volver atrás.

**_6.3. Pantalla 3: Pantalla de instrucciones_**

**Objetivo:** enseñar al jugador las mecánicas del juego.

**Formato:**

- Ventanas con instrucciones textuales sobre el juego.
- Ejemplos:
- Al inicio:

"Usa ← → para moverte. Pulsa \[W\] para saltar."

- Al obtener el bláster:

"Pulsa \[Espacio\] para disparar tu bláster de energía."

- Al llegar a un teletransportador:

"Acércate y pulsa \[E\] para activar el teletransportador."

**Interacción del usuario:**

- Cerrar el mensaje con la mediante la acción Volver atrás.
- Opción en "Opciones" para activar/desactivar las instrucciones.

**_6.4. Pantalla 4: Selección de nivel_**

**Objetivo:** permitir al jugador elegir en qué zona del planeta jugar.

**Elementos en pantalla:**

- **Lista de niveles:**
- Zona de abducción
- Zona de aterrizaje
- Zonas de obras
- Laboratorio abandonado
- Base de lanzamiento alienígena
- **Indicadores de estado:**
- Icono de **bloqueado/desbloqueado**.
- Pequeño texto: "Completado", "En progreso", "Nuevo".
- **Panel de información del nivel:**
- **Descripción breve** del escenario.
- **Dificultad** (por ejemplo, 1-5 estrellas).
- **Objetivo principal** (ej.: "Encuentra la cápsula de escape").
- **Recompensas** o coleccionables encontrados / totales.

**Interacción del usuario:**

- **Arriba/abajo o izquierda/derecha:** cambiar de nivel seleccionado.
- **Raton / Click izquierdo:** iniciar el nivel seleccionado (si está desbloqueado).
- **Boton volver atras:** volver al menú principal.

**Mensajes de error / restricciones:**

- Si el jugador intenta entrar a un nivel bloqueado:
- Mensaje emergente:

"Este nivel aún está bloqueado. Completa el nivel anterior para desbloquearlo."

- Botón: "Aceptar".

**_6.5. Pantalla 5: Juego en curso (HUD in-game)_**

**Objetivo:** mostrar la acción del juego y la información mínima necesaria.

**Elementos del HUD:**

- **Barra de vida:** esquina superior izquierda.
- **Munición / energía del bláster:** icono + número o barra.
- **Iconos de mejoras temporales activas:** por ejemplo, disparo triple, escudo, con temporizador.
- **Progreso del nivel:**
- Pequeño indicador (ej.: "Gemas: 1/3" o "Objetivo: llegar al teletransportador").
- **Mensajes contextuales:**
- "Pulsa \[E\] para activar el interruptor."
- "Pulsa \[Espacio\] para doble salto."

**Interacción del usuario:**

- **Movimiento:** izquierda/derecha y teclas A y D.
- **Salto:** botón asignado fecha hacia arriba y tecla W.
- **Disparo:** botón asignado Espacio.
- **Interacción:** acción cerca de objetos (ascensores, teletransportadores).
- **Pausa:** tecla/botón específico (ej.: Esc o Start).

**Mensajes de error / feedback in-game:**

- Intentar usar un teletransportador sin energía:

"El teletransportador no tiene energía suficiente."

- Intentar abrir puerta sin llave:

"Necesitas una llave para abrir esta puerta."

- Vida baja:
- Parpadeo de la barra de vida y mensaje breve:

"¡Peligro! Vida crítica."

**_6.6. Pantalla 6: Game Over_**

**Objetivo:** informar que el jugador ha perdido y ofrecer opciones de reintentar nivel o volver al menú principal del juego, escoger otra fase, etc.

**Elementos:**

- Texto central grande: **"GAME OVER"**.
- Subtexto: "Has perdido toda tu vida."
- Estadísticas rápidas:
- Tiempo jugado.
- Enemigos derrotados.
- Coleccionables obtenidos (gemas de salud).
- Opciones:
- **Reintentar nivel**
- **Volver al menú principal o de niveles.**

**Interacción del usuario:**

- Arriba/abajo para seleccionar con ratón.
- Clicar botón izquierdo ratón para confirmar.

**_6.7. Pantalla 7: Pantalla de victoria / fin de nivel_**

**Objetivo:** celebrar la victoria del jugador, mostrar progresos y resultados.

**Elementos:**

- Texto: **"Nivel final completado"** o, al final, **"Has escapado del planeta"**.
- Cinemática breve o imagen estática del personaje en la cápsula de escape.
- Estadísticas:
- Tiempo que ha tardado en completar el nivel.
- Porcentaje de coleccionables (gemas, por ejemplo).
- Daño recibido (si ha perdido algo de vida).
- Botones:
- **Repetir nivel final**.
- **Volver al menú principal o de niveles**.

**_6.8. Pantalla 8: Mensajes de error del sistema / carga_**

**Situaciones típicas:**

- **Error al cargar partida:**

"No se ha podido cargar la partida. El archivo está dañado." Botón: "Aceptar".

- **Error al guardar:**

"Error al guardar el progreso. Comprueba el espacio disponible." Botones: "Reintentar / Continuar sin guardar".

- **Pantalla de carga:**
- Barra de progreso.
- Texto: "Cargando zona: Fábrica abandonada…"
- Consejos de juego ("Tip: Usa el doble salto para alcanzar plataformas altas.").

**_6.9. Pantalla 9: Opciones / Configuración_**

**Objetivo:** ajustar parámetros del juego.

**Secciones típicas:**

- **Audio:**
- Volumen general.
- Volumen música.
- Volumen efectos.
- **Vídeo (si aplica):**
- Pantalla completa / ventana.
- Brillo.
- **Controles:**
- Mapeo de teclas/botones.
- Sensibilidad (si hay apuntado).
- **Juego:**
- Idioma.
- Activar/desactivar tutoriales.
- Nivel de dificultad (Fácil / Normal / Difícil).

**Interacción del usuario:**

- Navegación por pestañas o lista.
- Ajuste de valores con izquierda/derecha.
- Confirmar con Enter / A.
- Volver con Esc / B.

**Mensajes de error / validación:**

- Si se intenta asignar la misma tecla a dos acciones críticas:

"Esta tecla ya está asignada a otra acción. ¿Deseas sobrescribirla?" Opciones: **Sí / No**.

**_6.10. Pantalla 10: Menú de pausa_**

**Objetivo:** permitir al jugador detener la acción y acceder a opciones rápidas.

**Elementos:**

- Fondo del juego **congelado** y oscurecido.
- Menú central con opciones:
- **Reanudar**
- **Reiniciar nivel**
- **Opciones**
- **Volver al menú principal**

**Interacción del usuario:**

- Navegar con arriba/abajo.
- Confirmar con Enter / A.
- Reanudar también con la tecla/botón de pausa.

**Mensajes de confirmación:**

- Al elegir "Reiniciar nivel":

"¿Seguro que deseas reiniciar el nivel? Perderás el progreso actual." Opciones: **Sí / No**.

- Al elegir "Volver al menú principal":

"¿Salir al menú principal? El progreso no guardado se perderá." Opciones: **Sí / No**.

**_6.11. Pantalla 11: Pantallas de tutorial / ayuda contextual_**

**Objetivo:** enseñar al jugador las mecánicas sin romper el ritmo.

**Formato:**

- Pequeñas ventanas semitransparentes sobre el juego.
- Ejemplos:
- Al inicio:

"Usa ← → para moverte. Pulsa \[Espacio\] para saltar."

- Al obtener el bláster:

"Pulsa \[Ctrl\] para disparar tu bláster de energía."

- Al llegar a un teletransportador:

"Acércate y pulsa \[E\] para activar el teletransportador."

**Interacción del usuario:**

- Cerrar el mensaje con la tecla de acción o automáticamente tras unos segundos (según diseño).
- Opción en "Opciones" para activar/desactivar tutoriales.