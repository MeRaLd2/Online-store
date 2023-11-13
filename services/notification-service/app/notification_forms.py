import schemas

def reservation_notification_message(
        message: schemas.Notification
) -> str:
    msg = (f'Совершена покупка {message.products[0].name} \n'\
           f'{message.products[0].description} \n'\
           f'За {message.products[0].price} \n')

    return msg