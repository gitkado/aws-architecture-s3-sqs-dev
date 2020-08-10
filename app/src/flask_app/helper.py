import imghdr
import json
import itertools
import mimetypes
from os import path
import uuid

import imghdr
from io import BufferedReader

import boto3
from flask import flash, render_template

from . import app
from .validator import CustomValidator
from .consts import (
    FLASH_CLASS, HTML_TEMPLATE_VIEW_TITLE,
    S3_BUCKET_NAME, S3_END_POINT_URL, S3_REGION,
    SQS_END_POINT_URL, SQS_QUEUE_URL, SQS_REGION,
)


class Helper:
    @classmethod
    def verify_parameters(cls, schema, params):
        """リクエストパラメータを検証する関数
        エラーメッセージはFlashメッセージに設定する

        Args:
            schema (dict): チェック項目のスキーマ
            dict (dict): 検証するリクエストパラメータ

        Returns:
            True: リクエストパラメータが想定する値
            False: リクエストパラメータが不正な値
        """
        v = CustomValidator(schema)
        v.allow_unknown = True
        if v.validate(params) is False:
            # パラメータ不正の場合
            for message in itertools.chain.from_iterable(v.errors.values()):
                cls.error_flash(str(message))

            return False

        return True

    @classmethod
    def render_template(cls, template_name, **context):
        """flask.render_template実行前にtitleパラメータを追加
        https://flask.palletsprojects.com/en/1.1.x/api/#flask.render_template

        Args:
            template_name (str): 描画するHTMLファイル名
        """
        context['title'] = HTML_TEMPLATE_VIEW_TITLE[template_name]

        return render_template(template_name, **context)

    @classmethod
    def success_flash(cls, message):
        flash(message, FLASH_CLASS['SUCCESS'])

    @classmethod
    def error_flash(cls, message):
        flash(message, FLASH_CLASS['ERROR'])
        
    @classmethod
    def s3_client(cls):
        return boto3.client('s3', region_name=S3_REGION, endpoint_url=S3_END_POINT_URL)

    @classmethod
    def upload_image(cls, buffer):
        client = cls.s3_client()

        image_url = path.join(
            S3_BUCKET_NAME, '{}.{}'.format(
                str(uuid.uuid4()),
                imghdr.what(None, h=buffer)
            )
        )

        bucket = image_url.split('/')[0]
        key = '/'.join(image_url.split('/')[1:])
        content_type = mimetypes.guess_type(image_url)[0]
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=buffer,
            ContentType=content_type
        )

        return image_url

    @classmethod
    def sqs_client(cls):
        return boto3.client('sqs', region_name=SQS_REGION, endpoint_url=SQS_END_POINT_URL)

    @classmethod
    def sqs_send(cls, message_dict):
        client = cls.sqs_client()
        client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message_dict)
        )
