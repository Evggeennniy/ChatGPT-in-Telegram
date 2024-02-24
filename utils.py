import datetime


def logging(message: str, label: str = 'info') -> None:
    """
    Using for logging actions
    """
    labels = {
        'error': '\033[91m {} \033[0m',
        'ok': '\033[92m {} \033[0m',
        'warning': '\033[93m {} \033[0m',
        'info': '\033[94m {} \033[0m',
    }
    current_time = datetime.datetime.now()
    current_time = current_time.strftime("[ %d.%m.%Y | %H:%M ]")
    formatted_message = labels.get(label).format(message)
    formatted_message = str(current_time) + formatted_message

    print(formatted_message)
