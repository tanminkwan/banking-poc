def command_converter_deposit(message: dict) -> tuple[dict, str]:

    initial_param = dict(
        account = message.get('account'),
        amount = message.get('amount'),
    )

    executer = "banking.executer.deposit.Deposit"

    return initial_param, executer

def command_converter_readmessage(message: dict) -> tuple[dict, str]:

    initial_param = dict(
        account = message.get('account'),
        amount = message.get('amount'),
    )

    executer = "banking.executer.deposit.ReadMessage"

    return initial_param, executer