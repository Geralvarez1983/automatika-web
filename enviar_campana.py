import csv
import smtplib
import time
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ==============================================================================
# CONFIGURACIÓN DE LA CAMPAÑA
# ==============================================================================

# Tu correo de envío (debe ser el correo de Gmail)
REMITENTE_EMAIL = "automatika.corp@gmail.com"
REMITENTE_NOMBRE = "Equipo de Automatika"

# Contraseña de Aplicación de 16 caracteres generada en Google Account
# (NO es tu contraseña normal de Gmail, es la "Contraseña de aplicación" para scripts)
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "TU_CONTRASENA_DE_APLICACION_AQUI")

# MODO DE PRUEBA:
# True: Envía un único correo a EMAIL_DE_PRUEBA para que veas cómo queda antes de mandarlo a clientes reales.
# False: Envía a toda la lista de contactos.csv
MODO_PRUEBA = True
EMAIL_DE_PRUEBA = "automatika.corp@gmail.com"

# Archivo con los contactos (con columnas: Nombre, Empresa, Email)
ARCHIVO_CONTACTOS = "contactos.csv"

# Intervalo aleatorio en segundos entre envíos para no alertar a los filtros de Gmail
SEGUNDOS_MIN = 15
SEGUNDOS_MAX = 30

# ==============================================================================
# PLANTILLA DEL CORREO
# ==============================================================================

def generar_asunto(empresa):
    if empresa and empresa.strip():
        return f"Ahorro de tiempo en tareas manuales para {empresa.strip()}"
    return "Ahorro de tiempo en tareas manuales para tu empresa"

def generar_cuerpo_html(nombre, empresa):
    nombre_txt = nombre.strip() if nombre and nombre.strip() else ""
    empresa_txt = f"<b>{empresa.strip()}</b>" if empresa and empresa.strip() else "su empresa"
    
    saludo = f"Hola {nombre_txt}," if nombre_txt else "Hola,"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #222222; font-size: 15px; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
            p {{ margin-bottom: 16px; }}
            ul {{ margin-top: 8px; margin-bottom: 20px; padding-left: 20px; }}
            li {{ margin-bottom: 10px; }}
            .highlight {{ color: #0284c7; font-weight: 600; }}
            .btn-cta {{ display: inline-block; background-color: #2563eb; color: #ffffff !important; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; margin: 15px 0; }}
            .signature {{ margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 16px; color: #475569; font-size: 14px; }}
            .signature strong {{ color: #0f172a; font-size: 15px; }}
            a {{ color: #2563eb; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>{saludo} esperamos que te encuentres muy bien.</p>
            
            <p>Te escribimos desde el equipo de <strong>Automatika</strong>.</p>
            
            <p>Nuestro objetivo es ayudar a empresas como {empresa_txt} a <strong>optimizar tiempo y dinero</strong>, transformando tareas administrativas y operativas manuales en flujos digitales autónomos y software a medida.</p>
            
            <p>Entre las soluciones que implementamos frecuentemente para nuestros clientes se encuentran:</p>
            
            <ul>
                <li><strong>Software y portales para Recursos Humanos:</strong> Gestión digital de solicitudes de vacaciones, control de ausentismo, licencias y turnos de personal (eliminando el desorden de planillas Excel cruzadas).</li>
                <li><strong>Eliminación de la doble carga operativa:</strong> Conexión directa entre plataformas de venta, facturación fiscal y sistemas contables.</li>
                <li><strong>Procesamiento inteligente de documentos con IA:</strong> Lectura automática de facturas de proveedores (OCR) para ingreso inmediato al sistema contable.</li>
                <li><strong>Desarrollos y automatizaciones a medida:</strong> Diseñamos la integración exacta que tu equipo necesita para ahorrar horas de trabajo repetitivo.</li>
            </ul>
            
            <p>Para que puedan evaluar el impacto real y el ahorro de horas en su estructura sin ningún compromiso, ponemos a disposición de {empresa_txt} una <strong>sesión de diagnóstico sin costo</strong>, donde analizamos sus circuitos actuales e identificamos oportunidades de mejora inmediata.</p>
            
            <p>Pueden ver nuestros casos de uso y metodología en nuestra web:<br>
            👉 <a href="https://automatika-one.vercel.app">automatika-one.vercel.app</a></p>
            
            <p>Si les parece de interés, <strong>¿qué día les resultaría conveniente esta semana para coordinar una breve llamada virtual de 15 minutos?</strong></p>
            
            <p>
                <a href="https://wa.me/5491136826065?text=Hola%20equipo%20de%20Automatika%2C%20recibimos%20su%20correo%20y%20nos%20gustar%C3%ADa%20hacerles%20una%20consulta." class="btn-cta">
                    Conversar por WhatsApp (+54 9 11 3682-6065)
                </a>
            </p>
            
            <div class="signature">
                <p>Saludos cordiales,<br>
                <strong>Equipo de Automatika</strong><br>
                Automatización Inteligente de Procesos Administrativos<br>
                Email: <a href="mailto:automatika.corp@gmail.com">automatika.corp@gmail.com</a> | Web: <a href="https://automatika-one.vercel.app">automatika-one.vercel.app</a><br>
                WhatsApp directo: +54 9 11 3682-6065</p>
            </div>
        </div>
    </body>
    </html>
    """

def generar_cuerpo_texto(nombre, empresa):
    nombre_txt = nombre.strip() if nombre and nombre.strip() else ""
    empresa_txt = empresa.strip() if empresa and empresa.strip() else "su empresa"
    saludo = f"Hola {nombre_txt}," if nombre_txt else "Hola,"

    return f"""{saludo} esperamos que te encuentres muy bien.

Te escribimos desde el equipo de Automatika.

Nuestro objetivo es ayudar a empresas como {empresa_txt} a optimizar tiempo y dinero, transformando tareas administrativas y operativas manuales en flujos digitales autónomos y software a medida.

Entre las soluciones que implementamos frecuentemente para nuestros clientes se encuentran:

* Software y portales para Recursos Humanos: Gestión digital de solicitudes de vacaciones, control de ausentismo, licencias y turnos de personal (eliminando el desorden de planillas Excel cruzadas).
* Eliminación de la doble carga operativa: Conexión directa entre plataformas de venta, facturación fiscal y sistemas contables.
* Procesamiento inteligente de documentos con IA: Lectura automática de facturas de proveedores (OCR) para ingreso inmediato al sistema contable.
* Desarrollos y automatizaciones a medida: Diseñamos la integración exacta que tu equipo necesita para ahorrar horas de trabajo repetitivo.

Para que puedan evaluar el impacto real y el ahorro de horas en su estructura sin ningún compromiso, ponemos a disposición de {empresa_txt} una sesión de diagnóstico sin costo, donde analizamos sus circuitos actuales e identificamos oportunidades de mejora inmediata.

Pueden ver nuestros casos de uso y metodología en nuestra web:
👉 https://automatika-one.vercel.app

Si les parece de interés, ¿qué día les resultaría conveniente esta semana para coordinar una breve llamada virtual de 15 minutos?

También pueden escribirnos directamente por WhatsApp:
📲 https://wa.me/5491136826065

Saludos cordiales,
Equipo de Automatika
Automatización Inteligente de Procesos Administrativos
Email: automatika.corp@gmail.com | WhatsApp: +54 9 11 3682-6065
Web: https://automatika-one.vercel.app
"""

# ==============================================================================
# LÓGICA DE ENVÍO
# ==============================================================================

def detectar_delimitador(ruta_archivo):
    """Detecta si el archivo CSV usa coma (,) o punto y coma (;) común en Excel español."""
    with open(ruta_archivo, "r", encoding="utf-8-sig") as f:
        primera_linea = f.readline()
        if ";" in primera_linea and "," not in primera_linea:
            return ";"
        return ","

def cargar_contactos(ruta_archivo):
    contactos = []
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: No se encontró el archivo {ruta_archivo}")
        return []
    
    delimitador = detectar_delimitador(ruta_archivo)
    with open(ruta_archivo, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=delimitador)
        for fila in reader:
            # Limpiar claves de posibles espacios en blanco
            fila_limpia = {k.strip().capitalize(): v.strip() for k, v in fila.items() if k}
            contactos.append(fila_limpia)
    return contactos

def enviar_correo(servidor, destinatario, nombre, empresa):
    asunto = generar_asunto(empresa)
    cuerpo_html = generar_cuerpo_html(nombre, empresa)
    cuerpo_texto = generar_cuerpo_texto(nombre, empresa)

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = f"{REMITENTE_NOMBRE} <{REMITENTE_EMAIL}>"
    mensaje["To"] = destinatario
    mensaje["Reply-To"] = REMITENTE_EMAIL

    mensaje.attach(MIMEText(cuerpo_texto, "plain", "utf-8"))
    mensaje.attach(MIMEText(cuerpo_html, "html", "utf-8"))

    servidor.sendmail(REMITENTE_EMAIL, destinatario, mensaje.as_string())

def main():
    print("=" * 60)
    print("  🚀 AUTOMATIKA - SISTEMA DE ENVÍO DE EMAIL CAMPAIGNS")
    print("=" * 60)

    if GMAIL_APP_PASSWORD == "TU_CONTRASENA_DE_APLICACION_AQUI" or not GMAIL_APP_PASSWORD:
        print("\n⚠️  ATENCIÓN:")
        print("Para enviar correos mediante Gmail necesitas configurar tu 'Contraseña de aplicación'.")
        print("1. Entra a tu Cuenta de Google (Seguridad -> Verificación en 2 pasos -> Contraseñas de aplicaciones)")
        print("2. Genera una contraseña llamada 'Automatika' (16 letras).")
        print("3. Pégala en la variable GMAIL_APP_PASSWORD dentro de 'enviar_campana.py'.\n")
        return

    contactos = cargar_contactos(ARCHIVO_CONTACTOS)
    if not contactos:
        print("❌ No se pudieron cargar los contactos. Revisa el archivo contactos.csv.")
        return

    print(f"📋 Contactos detectados en {ARCHIVO_CONTACTOS}: {len(contactos)}")

    try:
        print("\n🔌 Conectando con los servidores de Gmail SMTP...")
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(REMITENTE_EMAIL, GMAIL_APP_PASSWORD)
        print("✅ Autenticación exitosa en Gmail.\n")
    except Exception as e:
        print(f"❌ Error al conectar con Gmail: {e}")
        return

    try:
        if MODO_PRUEBA:
            print("🧪 --- MODO DE PRUEBA ACTIVADO ---")
            print(f"Enviando correo de prueba a tu propia casilla: {EMAIL_DE_PRUEBA}")
            primer_contacto = contactos[0] if contactos else {"Nombre": "German", "Empresa": "Mi Empresa"}
            nombre = primer_contacto.get("Nombre", "German")
            empresa = primer_contacto.get("Empresa", "Mi Empresa")
            
            enviar_correo(servidor, EMAIL_DE_PRUEBA, nombre, empresa)
            print(f"✅ ¡Correo de prueba enviado con éxito a {EMAIL_DE_PRUEBA}!")
            print(f"👉 Asunto enviado: {generar_asunto(empresa)}")
            print("Revisa tu casilla de correo para ver cómo quedó el diseño y el texto.")
            print("Cuando estés listo para enviar a todos, cambia MODO_PRUEBA = False en el script.")
        else:
            print("🚀 --- INICIANDO ENVÍO A CLIENTES REALES ---")
            total = len(contactos)
            enviados = 0

            for i, c in enumerate(contactos, start=1):
                destinatario = c.get("Email")
                nombre = c.get("Nombre", "")
                empresa = c.get("Empresa", "")

                if not destinatario or "@" not in destinatario:
                    print(f"⚠️ [{i}/{total}] Saltando fila sin email válido: {c}")
                    continue

                print(f"📧 [{i}/{total}] Enviando a: {destinatario} ({empresa or 'Sin empresa'})...")
                try:
                    enviar_correo(servidor, destinatario, nombre, empresa)
                    enviados += 1
                    print(f"   ✅ Enviado correctamente.")
                except Exception as err:
                    print(f"   ❌ Error al enviar a {destinatario}: {err}")

                # Pausa aleatoria para evitar detección de spam
                if i < total:
                    espera = random.randint(SEGUNDOS_MIN, SEGUNDOS_MAX)
                    print(f"   ⏳ Esperando {espera}s antes del siguiente envío...")
                    time.sleep(espera)

            print("\n" + "=" * 60)
            print(f"🎉 Campaña finalizada. Total enviados con éxito: {enviados}/{total}")
            print("=" * 60)

    finally:
        servidor.quit()

if __name__ == "__main__":
    main()
