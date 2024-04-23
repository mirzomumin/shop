import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from src.orders.schemas import OrderSchemaList
from src.orders.repository import OrdersRepository
from src.celeryapp import app
from src.configs.config import settings
from src.database import get_db


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    # TEMPLATE_FOLDER='./templates/email'
)


async def send_mail(order_id: int) -> None:
    idb = get_db()
    db = await anext(idb)

    order = await OrdersRepository.get(id=order_id, db=db)
    anext(idb)
    subject = f"Order nr. {order.id}"
    body = (
        f"Dear {order.first_name},\n\n"
        f"You have successfully placed an order. "
        f"Your order ID is {order.id}"
    )

    order_data = OrderSchemaList.from_db(order=order).model_dump()

    message = MessageSchema(
        subject=subject,
        recipients=[order_data["email"]],
        body=body,
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


@app.task
def sync_send_mail(order_id: int) -> None:
    asyncio.run(send_mail(order_id=order_id))
