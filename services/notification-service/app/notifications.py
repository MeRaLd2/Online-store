import schemas

def basket_upload(
        message: schemas.Notification
) -> str:
    products_info = ""
    for product in message.products:
        product_info = (
            f'Товар: {product.name}\n'
            f'Описание: {product.description}\n'
            f'Цена: {product.price}\n\n'
        )
        products_info += product_info

    msg = f'Вы совершили покупку:\n{products_info}'

    return msg