from razomy.python.id import id_lib
from razomy.python.logging import logger


class KeyMessageCodeError:
    def __init__(self, code, key, message=None, context=None):
        self.code = code
        self.error_id = id_lib.create_id_short()
        self.key = key
        self.message = message or key
        self.context = context


def copy(self: KeyMessageCodeError, context):
    key_message_copy = KeyMessageCodeError(
        code=self.code,
        key=self.key,
        message=self.message,
        context=context or self.context,
    )
    return key_message_copy


def to_json(self: KeyMessageCodeError):
    return {
        'code': self.code,
        'message': self.message,
        'key': self.key,
        'error_id': self.error_id,
        'context': self.context
    }


def to_string(self: KeyMessageCodeError):
    return f"code:{self.code}, message:{self.message}, key:{self.key}, error_id:{self.error_id}, context:{self.context}"


def to_public_json_and_code(self: KeyMessageCodeError, private_context=None, public_context=None):
    key_message_copy = copy(self, context=public_context)
    logger.error(KeyMessageCodeError.__name__, to_string(key_message_copy), private_context)
    return to_json(key_message_copy), self.code


def to_public_json(self: KeyMessageCodeError, private_context=None, public_context=None):
    key_message_copy = copy(self, context=public_context)
    logger.error(KeyMessageCodeError.__name__, to_string(key_message_copy), private_context)
    return to_json(key_message_copy)


INVALID_REQUEST_ERROR = KeyMessageCodeError(400, 'invalid_request')
