from datetime import time, timedelta, timezone
import os
from pathlib import Path


# 実行環境情報
CONFIG_NAME = os.getenv('FLASK_CONFIGURATION', 'development')

# S3情報
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'test')
S3_END_POINT_URL = os.getenv('S3_END_POINT_URL', None)
S3_REGION = os.getenv('S3_REGION', 'ap-northeast-1')

# SQS情報
# SQS_END_POINT_URL = os.getenv('SQS_END_POINT_URL', None)
# SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', None)
# SQS_REGION = os.getenv('SQS_REGION', 'ap-northeast-1')

# Flaskの設定一覧
FLASK_CONFIG_LIST = {
    'development': 'flask_app.config.flask.DevelopmentConfig',
}

# HTMLテンプレートで使用するClass名
FLASH_CLASS = {
    'SUCCESS': 'success-message',
    'WARNING': 'success-message',
    'ERROR': 'error-message',
}

# ライブラリ「Cerberus」で使用するメッセージ群
# 参考: https://github.com/pyeve/cerberus/blob/master/cerberus/errors.py#L426]
CERBERUS_MESSAGES = {
    'image_extension': "{field} extension not support.",
}

# 画面名(HTML対応表)
HTML_TEMPLATE_VIEW_TITLE = {
    'upload_complete.html': 'upload_complete',
    'upload.html': 'upload',
}

# # ログフォーマット
LOG_FORMAT = '[%(asctime)s] %(levelname)s - %(module)s.%(funcName)s - %(message)s'
# ログレベル
LOG_LEVEL = 'INFO'
# Logging設定
LOG_DICT_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console']
    },
}

# API処理開始ログフォーマット
LOG_METHOD_START_FORMAT = '{url} [{method}] params: {form}'
# API処理終了ログフォーマット
LOG_METHOD_END_FORMAT = 'completed'
