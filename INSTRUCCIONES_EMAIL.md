# 🚀 Guía de Envío de Correos Masivos - Automatika

Ya tenés todo listo en esta carpeta para enviar correos masivos personalizados con la máxima seguridad anti-spam.

---

## 📁 Archivos creados:

1. **`contactos.csv`**: Tu base de datos de clientes. Podés abrirla con **Excel** o el Bloc de Notas.
   * Tiene 3 columnas: `Nombre`, `Empresa`, `Email`.
   * Simplemente pegás tus contactos ahí respetando las columnas.

2. **`enviar_campana.py`**: El script de Python que automatiza los envíos:
   * Personaliza el asunto y cuerpo con el nombre de cada persona y empresa.
   * Envía en formato profesional HTML con botón directo a WhatsApp y enlace a la web.
   * Espera entre 15 y 30 segundos entre cada envío para que Gmail lo procese como un humano normal y no caiga en Spam.
   * Viene con **MODO PRUEBA activado** para que te envíes primero un mail a vos mismo.

---

## 🔑 El único requisito de Google (Contraseña de Aplicación):

Para que un script envíe correos desde tu cuenta de Gmail (`automatika.corp@gmail.com`), Google no te pide tu clave personal, sino una **Contraseña de Aplicación** segura (16 letras):

1. Entrá a tu cuenta de Google: [myaccount.google.com/security](https://myaccount.google.com/security).
2. Asegurate de tener activada la **Verificación en 2 pasos**.
3. En la barra de búsqueda superior de Google escribí: **Contraseñas de aplicaciones** (o entrá a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)).
4. En nombre escribí: `Automatika` y hacé clic en **Crear**.
5. Te va a mostrar un código amarillo de 16 letras (ejemplo: `abcd efgh ijkl mnop`).
6. Copiás ese código y lo pegás en la línea 17 del archivo `enviar_campana.py`.

---

## 🧪 Paso a Paso para enviar:

### Paso 1: Enviar correo de prueba a vos mismo
1. Abrí la terminal en esta carpeta.
2. Ejecutá:
   ```bash
   python enviar_campana.py
   ```
3. Te llegará a `automatika.corp@gmail.com` el correo de prueba para que veas cómo luce.

### Paso 2: Enviar a tus clientes reales
1. Cargá tu lista de clientes en `contactos.csv`.
2. En `enviar_campana.py`, cambiás:
   ```python
   MODO_PRUEBA = False
   ```
3. Volvés a ejecutar `python enviar_campana.py` y el script irá enviando a cada cliente uno a uno.
