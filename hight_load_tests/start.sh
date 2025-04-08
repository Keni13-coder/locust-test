#! /bin/bash
docker run --network=host --name locust_test -p 8089:8089 -v $PWD:/app locustio/locust -f /app/main.py
# cli start
# locust -f locustfiles - позволяет запустить все файлы в указанном каталоге
# locust --processes 4
# ---- Распеределенный запуск по несколько машин
# locust -f my_locustfile.py --master
# locust -f - --worker --master-host <your master> --processes 4