from locust import HttpUser, task, tag, FastHttpUser, LoadTestShape
from random import randint
import json
import logging
from locust import events

# для более удобного запуска упарвления используеться тег
# например через опцию --tags home, будут запущенны только таски где указан тег home

@events.quitting.add_listener
def _(environment, **kw):
    '''
    Более 1% запросов не были выполнены

    Среднее время отклика составляет более 200 мс.

    95-й процентиль времени отклика превышает 800 мс.'''
    
    
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0



class HelloWorldUser(FastHttpUser):
    
    @tag("home")
    @task(1)
    def hello_world(self):
        # почему то не отображается в консоли
        with self.client.get("/", catch_response=True) as response:
            pass
        #     if "Hello World" not in response.text:
        #         response.failure("Got wrong response")
        #     elif response.elapsed.total_seconds() > 0.5:
        #         response.failure("Request took too long")
        
    
    # @tag("item", "home")
    # @task(2)
    # def get_item(self):
    #     self.client.get(f"/items/{randint(1, 10000)}", name="/items/")


# class BasckedUser(HttpUser):
#     '''Описываем таски для корзины.
#     Является класом для пути клиента под корзину
#     '''
#     @task
#     def create_basket(self):
#         self.client.post("/basket")
        
#     @task
#     def get_basket(self):
#         self.client.get("/basket")
        
#     @task
#     def create_order_from_basket(self):
#         '''Тут описан сценарий создания заказа из корзины'''
#         self.client.put("/basket")
#         self.client.post("/notify/user/", json={'id': 1})
#         self.client.post("/create_order/", json={'id': 1})


class StagesShapeWithCustomUsers(LoadTestShape):
    
    '''
    Note:
        идут по наростающей последовательности
        в первые 10 секунд создаст 10 пользователей
        в следующие 20 секунд создаст 40 пользователей,
        таким образом за длительность 30 мы получим общее количество 50 пользователей,
        так как за первые 10 секунд были созданы 10 пользлователей
        
        duration: Время (в секундах) от начала теста, до которого действует стадия.
        users: Общее количество пользователей.
        spawn_rate: Скорость добавления пользователей в секунду.
        user_classes: Классы пользователей, активные на этой стадии.
    '''
    stages = [
        {"duration": 10, "users": 10, "spawn_rate": 10, "user_classes": [HelloWorldUser]}, # 0-10
        {"duration": 30, "users": 50, "spawn_rate": 10, "user_classes": [HelloWorldUser, HelloWorldUser]},# 10-30
        {"duration": 60, "users": 100, "spawn_rate": 10, "user_classes": [HelloWorldUser]},# 30-60
        {"duration": 120, "users": 100, "spawn_rate": 10, "user_classes": [HelloWorldUser,HelloWorldUser]},# 60-120
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
    