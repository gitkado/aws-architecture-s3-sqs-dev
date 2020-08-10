from datetime import datetime
from sqlalchemy.sql.functions import current_timestamp

from . import db


class Image(db.Model):
    """画像管理モデル

    Attributes:
        id (int): 主キー
        name (str): ファイル名
        s3_path (str): ファイルパス
        comments (str): コメント
        created_at (datetime): 作成時刻
        updated_at (datetime): 更新時刻
    """
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    s3_path = db.Column(db.String(255), nullable=False)
    comments = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, server_default=current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '<Image id={self.id} name={self.name} s3_path={self.s3_path}>'.format(self=self)
