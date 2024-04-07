import json

from flask import Flask, request, jsonify
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.errors import error_proxy
from Src.Logics.report_factory import report_factory
from Src.Logics.start_factory import start_factory
from datetime import datetime
from Src.Logics.storage_service import storage_service
from Src.Models.nomenclature_model import nomenclature_model
from Src.Logics.nomenclature_service import nomenclature_service


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Сформировать начальный набор данных
options = settings_manager() 
start = start_factory(options.settings)
start.create()

nomenclature_service_instance = nomenclature_service(start.storage.data)


@app.route("/api/report/<storage_key>", methods = ["GET"])
def get_report(storage_key: str):
    """
        Сформировать отчет
    Args:
        storage_key (str): Ключ - тип данных: номенклатура, группы и т.д.
    """
    
    keys = storage.storage_keys( start.storage )
    if storage_key == "" or  storage_key not in keys:
        return error_proxy.create_error_response(app, f"Некорректный передан запрос! Необходимо передать: /api/report/<storage_key>. Список ключей (storage_key): {keys}.", 400)
    
    # Создаем фабрику
    report = report_factory()
    data = start.storage.data
    
    # Формируем результат
    try:
        result = report.create_response( options.settings.report_mode, data, storage_key, app )  
        return result
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/storage/turns", methods = ["GET"] )
def get_turns():
    # Получить параметры
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
        
    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
    
    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
          
    source_data = start.storage.data[  storage.storage_transaction_key()   ]      
    data = storage_service( source_data   ).create_turns( start_date, stop_date )      
    result = storage_service.create_response( data, app )
    return result
      
@app.route("/api/storage/<nomenclature_id>/turns", methods = ["GET"] )
def get_turns_nomenclature(nomenclature_id):
    
    # Получить параметры
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")

    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")

    try:
        start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
        stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
    except:
        return error_proxy.create_error_response(app, "Некорректно перпеданы параметры: start_period, stop_period")    

    transactions_data = start.storage.data[  storage.storage_transaction_key()   ]   
    nomenclature_data =  start.storage.data[  storage.nomenclature_key()   ]   
    
    nomenclatures =  nomenclature_model.create_dictionary( nomenclature_data )
    ids = [item.id for item in nomenclatures.values()]
    if nomenclature_id not in ids:
        return error_proxy.create_error_response(app, "Некорректно передан код номенклатуры!")
    
    nomenclature = nomenclatures[nomenclature_id]
      
    data = storage_service( transactions_data  ).create_turns_by_nomenclature( start_date, stop_date, nomenclature )      
    result = storage_service.create_response( data, app )
    return result

@app.route("/api/nomenclature/<nomenclature_id>", methods=["DELETE"])
def delete_nomenclature(nomenclature_id):
    try:
        if nomenclature_service_instance.delete_nomenclature(nomenclature_id):
            start.storage.save()
            return storage_service.create_response(app, "ok")
        else:
            return error_proxy.create_error_response(app, "Nomenclature not found", 404)
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Error processing: {ex}", 500)

@app.route("/api/report/<storage_key>", methods=["GET"])
def get_report(storage_key: str):
    keys = storage_service.storage_keys(start.storage)
    if storage_key == "" or storage_key not in keys:
        return error_proxy.create_error_response(app,
            f"Некорректный запрос! Необходимо передать: /api/report/<storage_key>. Список ключей (storage_key): {keys}.",
            400)

    report = report_factory()
    data = start.storage.data

    try:
        result = report.create_response(options.settings.report_mode, data, storage_key, app)
        return result
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/storage/turns", methods=["GET"])
def get_turns():
    args = request.args
    if "start_period" not in args.keys() or "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")

    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")

    source_data = start.storage.data[storage_service.storage_transaction_key()]
    data = storage_service(source_data).create_turns(start_date, stop_date)
    result = storage_service.create_response(data, app)
    return result

@app.route("/api/storage/<nomenclature_id>/turns", methods=["GET"])
def get_turns_nomenclature(nomenclature_id):
    args = request.args
    if "start_period" not in args.keys() or "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!",
                                                 400)

    try:
        start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
        stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
    except:
        return error_proxy.create_error_response(app, "Некорректно переданы параметры: start_period, stop_period",
                                                 400)

    transactions_data = start.storage.data[storage_service.storage_transaction_key()]
    nomenclature_data = start.storage.data[storage_service.nomenclature_key()]

    nomenclatures = nomenclature_model.create_dictionary(nomenclature_data)
    ids = [item.id for item in nomenclatures.values()]
    if nomenclature_id not in ids:
        return error_proxy.create_error_response(app, "Некорректно передан код номенклатуры!", 400)

    nomenclature = nomenclatures[nomenclature_id]

    data = storage_service(transactions_data).create_turns_by_nomenclature(start_date, stop_date, nomenclature)
    result = storage_service.create_response(data, app)
    return result

@app.route("/api/change_block_period", methods=["GET"])
def change_block_period():
    block_period = request.args.get("block_period")
    if block_period:
        try:
            block_date = datetime.strptime(block_period, "%Y-%m-%d")
            options.settings.block_period = block_date
            options.save()
            response_data = {"status": "success", "message": "Block period uodated successfully!",
                             "block_period": options.settings.block_period.strftime("%Y-%m-%d")}
            return json.dumps(response_data), 200
        except Exception as ex:
            return error_proxy.create_error_response(app, f"Ошибка запроса {ex}", 400)
    else:
        return error_proxy.create_error_response(app, "Параметр 'block_period' не найден!", 400)


@app. route("/api/system/mode", methods = ["GET"])
def set_work_mode():
    args = request.args
    if "first start" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: first_start")
    try:
        options.settings.is_first_start = args["first_start"]
        start.storage. save()
        return jsonify({"ok"})
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка обработки: (ex)", 500)


if __name__ == "__main__":
    app.run(debug = True)