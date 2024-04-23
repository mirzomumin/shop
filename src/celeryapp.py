from celery import Celery

app = Celery("tasks", include=["src.categories.tasks", "src.orders.tasks"])
app.config_from_object("src.configs.celeryconfig")


@app.task
def add(x, y):
    return x + y


@app.task
def get_order_list():
    return "TASK RUN"
    # orders = await OrdersRepository.list(db=db)
    # print(orders)
