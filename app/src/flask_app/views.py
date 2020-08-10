from datetime import datetime
from functools import wraps
from io import BufferedReader

from flask import request, redirect, url_for

from . import app, db
from .helper import Helper as h
from .models import Image
from .consts import (
    LOG_METHOD_START_FORMAT, LOG_METHOD_END_FORMAT
)


def logger_exception(f):
    """例外時のログを出力するデコレータ"""
    @wraps(f)
    def decorated_view(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.exception(e)
    return decorated_view


@app.before_request
def request_log():
    app.logger.info(
        LOG_METHOD_START_FORMAT.format(
            url=request.url,
            method=request.method,
            form={**request.form, **request.form}
        )
    )


@app.after_request
def response_log(response):
    app.logger.info(LOG_METHOD_END_FORMAT)

    return response


@app.route('/')
@logger_exception
def root_access():
    return redirect('/upload')


@app.route('/upload', methods=['GET'])
@logger_exception
def upload():
    """
    # TODO
    # 選択した画像を表示
    """
    return h.render_template('upload.html')


@app.route('/upload', methods=['POST'])
@logger_exception
def upload_submit():
    schema = {
        'image': {
            'required': True,
            'image_extension': True
        },
        'comments': {
            'type': 'string',
            'maxlength': 255
        }
    }
    request_form = request.form.to_dict()
    for field, file in request.files.to_dict().items():
        request_form['name'] = file.filename
        request_form[field] = BufferedReader(file).read()

    if h.verify_parameters(schema, request_form) is False:
        return redirect('upload')

    s3_path = h.upload_image(request_form['image'])
    h.sqs_send({'path': s3_path})
    image = Image(name=request_form['name'], s3_path=s3_path, comments=request_form['comments'])
    db.session.add(image)

    db.session.commit()
    h.success_flash('Image uploaded!')

    return redirect('/images')


@app.route('/images', methods=['GET'])
@logger_exception
def images():
    """
    # TODO
    # S3画像表示
    """
    images = Image.query.all()
    return h.render_template('images.html', images=images)
