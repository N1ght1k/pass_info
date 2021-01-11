import serial
import config
import traceback
from datetime import timedelta, datetime

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
is_BP = False
BP_time = datetime.today()
cur_BP = ''
while True:
    data = ser.readline().decode('utf-8')
    if is_BP and datetime.today() - BP_time > timedelta(seconds=30):
        is_BP = False
        route = cur_BP[30:36].strip()
        airline = cur_BP[36:39].strip()
        flight = cur_BP[39:44].strip()
        for char in flight:
            if char == '0':
                flight = flight[1:]
            else:
                break
        connection = config.get_connection()
        sql_query = 'INSERT INTO %s (route, airline, flight, shop) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');' \
                    % (config.table, route, airline, flight, config.shop)
        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            connection.commit()
        except Exception:
            print('Ошибка:\n', traceback.format_exc())
        connection.close()
    if data and data.find('&n') != -1 and data.find('&fp') != -1:
        if is_BP:
            index_start = data.find('&fp')
            index_end = data.find('&n')
            fn = data[index_start+4:index_end]
            route = cur_BP[30:36].strip()
            airline = cur_BP[36:39].strip()
            flight = cur_BP[39:44].strip()
            for char in flight:
                if char == '0':
                    flight = flight[1:]
                else:
                    break
            connection = config.get_connection()
            sql_query = 'INSERT INTO %s (route, airline, flight, shop, fiscal_sign) VALUES ' \
                        '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' \
                        % (config.table, route, airline, flight, config.shop, fn)
            try:
                cursor = connection.cursor()
                cursor.execute(sql_query)
                connection.commit()
            except Exception:
                print('Ошибка:\n', traceback.format_exc())
            connection.close()
            is_BP = False
    elif data and len(data) > 44:
        print(data)
        cur_BP = data
        is_BP = True
        BP_time = datetime.today()

