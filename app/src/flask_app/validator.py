import imghdr
from cerberus import Validator
from cerberus.errors import BasicErrorHandler

from .consts import CERBERUS_MESSAGES


class CustomErrorHandler(BasicErrorHandler):
    """Validatorのエラーメッセージを上書きして日本語化"""
    def __init__(self, tree=None):
        super().__init__(tree)
        self.messages = {**self.messages, **CERBERUS_MESSAGES}


class CustomValidator(Validator):
    def __init__(self, schema, **kwargs):
        super().__init__(schema, error_handler=CustomErrorHandler())

    def _validate_image_extension(self, image_extension, field, buffer):
        """画像拡張子が正しいか検証する関数
        Example:
            schema {'image_extension': true}

        Args:
            field (str): 検証する項目名
            files (BufferedReader): 検証するデータ

        The rule's arguments are validated against this schema: {'type': 'boolean'}
        """
        if imghdr.what(None, h=buffer) is None:
            self._error('', CERBERUS_MESSAGES['image_extension'].format(field=field))
