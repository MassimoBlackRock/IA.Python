import MetaTrader5 as mt5
import time

# Conexión a MetaTrader 5
def conectar_mt5():
    if not mt5.initialize():
        print("Error al inicializar MT5:", mt5.last_error())
        return False
    return True

# Función para desconectar de MT5
def desconectar_mt5():
    mt5.shutdown()

# Ejecutar una operación
def ejecutar_operacion(symbol, volumen, tipo_orden, stop_loss, take_profit):
    # Verificar si el símbolo está disponible
    if not mt5.symbol_select(symbol, True):
        print(f"No se puede seleccionar el símbolo: {symbol}")
        return

    # Obtener precio de mercado
    precio = mt5.symbol_info_tick(symbol).ask if tipo_orden == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

    # Crear la solicitud de operación
    solicitud = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volumen,
        "type": tipo_orden,
        "price": precio,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": 123456,
        "comment": "Ejecución automatizada desde Modulo4.py",
        "type_filling": mt5.ORDER_FILLING_IOC,  # Relleno inmediato o cancelación
        "type_time": mt5.ORDER_TIME_GTC,       # Tiempo: GTC (Good Till Cancel)
    }

    # Ejecutar la orden
    resultado = mt5.order_send(solicitud)
    
    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Error en la operación: {resultado.comment}")
    else:
        print(f"Operación ejecutada correctamente: {resultado}")

# Función de gestión de riesgos y ejecución basada en alertas
def gestionar_operaciones(alerta):
    # Parámetros básicos de la operación
    simbolo = alerta['simbolo']
    volumen = alerta['volumen']
    tipo_orden = mt5.ORDER_TYPE_BUY if alerta['tipo'] == 'compra' else mt5.ORDER_TYPE_SELL

    # Cálculo del stop-loss y take-profit basados en los datos de la alerta
    precio_entrada = alerta['precio_entrada']
    stop_loss = precio_entrada - alerta['riesgo'] if tipo_orden == mt5.ORDER_TYPE_BUY else precio_entrada + alerta['riesgo']
    take_profit = precio_entrada + alerta['beneficio'] if tipo_orden == mt5.ORDER_TYPE_BUY else precio_entrada - alerta['beneficio']

    # Ejecutar la operación
    ejecutar_operacion(simbolo, volumen, tipo_orden, stop_loss, take_profit)

# Ejemplo de alerta recibida del Módulo 3
alerta = {
    "simbolo": "EURUSD",
    "volumen": 0.1,
    "tipo": "compra",  # "compra" o "venta"
    "precio_entrada": 1.0950,
    "riesgo": 0.0010,  # Riesgo de 10 pips
    "beneficio": 0.0020  # Beneficio de 20 pips
}

# Conectar a MetaTrader 5
if conectar_mt5():
    # Gestionar la operación basada en la alerta recibida
    gestionar_operaciones(alerta)

    # Esperar un poco antes de desconectar
    time.sleep(5)
    
    # Desconectar de MetaTrader 5
    desconectar_mt5()
