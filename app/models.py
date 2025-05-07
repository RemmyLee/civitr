from datetime import datetime
from app import db

class Creator(db.Model):
    __tablename__ = 'creators'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    image = db.Column(db.String(255))
    
    models = db.relationship('Model', backref='creator', lazy='dynamic')
    
    def __repr__(self):
        return f'<Creator {self.username}>'

class Model(db.Model):
    __tablename__ = 'models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    allow_no_credit = db.Column(db.Boolean, default=False, name='allowNoCredit')
    allow_derivatives = db.Column(db.Boolean, default=False, name='allowDerivatives')
    allow_different_license = db.Column(db.Boolean, default=False, name='allowDifferentLicense')
    type = db.Column(db.String(50))
    minor = db.Column(db.Boolean, default=False)
    sfw_only = db.Column(db.Boolean, default=True, name='sfwOnly')
    poi = db.Column(db.Boolean, default=False)
    nsfw = db.Column(db.Boolean, default=False)
    nsfw_level = db.Column(db.Integer, default=0, name='nsfwLevel')
    availability = db.Column(db.String(50))
    cosmetic = db.Column(db.String(255))
    supports_generation = db.Column(db.Boolean, default=False, name='supportsGeneration')
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'))
    download_count = db.Column(db.Integer, default=0, name='downloadCount')
    
    versions = db.relationship('ModelVersion', backref='model', lazy='dynamic')
    tags = db.relationship('Tag', backref='model', lazy='dynamic')
    
    def __repr__(self):
        return f'<Model {self.name}>'

class ModelVersion(db.Model):
    __tablename__ = 'modelVersions'
    
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    index_in_model = db.Column(db.Integer, name='index_in_model')
    name = db.Column(db.String(255))
    base_model = db.Column(db.String(100), name='baseModel')
    base_model_type = db.Column(db.String(100), name='baseModelType')
    published_at = db.Column(db.String(), name='publishedAt')
    availability = db.Column(db.String(50))
    nsfw_level = db.Column(db.Integer, default=0, name='nsfwLevel')
    description = db.Column(db.Text)
    supports_generation = db.Column(db.Boolean, default=False, name='supportsGeneration')
    download_url = db.Column(db.String(255), name='downloadUrl')
    download_count = db.Column(db.Integer, default=0, name='downloadCount')
    
    files = db.relationship('File', backref='model_version', lazy='dynamic')
    images = db.relationship('Image', backref='model_version', lazy='dynamic')
    
    def __repr__(self):
        return f'<ModelVersion {self.name}>'

class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    size_kb = db.Column(db.Float, name='sizeKB')
    name = db.Column(db.String(255))
    type = db.Column(db.String(50))
    pickle_scan_result = db.Column(db.String(50), name='pickleScanResult')
    pickle_scan_message = db.Column(db.Text, name='pickleScanMessage')
    virus_scan_result = db.Column(db.String(50), name='virusScanResult')
    virus_scan_message = db.Column(db.Text, name='virusScanMessage')
    scanned_at = db.Column(db.String(), name='scannedAt')
    format = db.Column(db.String(50))
    model_version_id = db.Column(db.Integer, db.ForeignKey('modelVersions.id'), name='modelVersion_id')
    sha256 = db.Column(db.String(64))
    autov1 = db.Column(db.String(255))
    autov2 = db.Column(db.String(255))
    autov3 = db.Column(db.String(255))
    crc32 = db.Column(db.String(8))
    blake3 = db.Column(db.String(64))
    download_url = db.Column(db.String(255), name='downloadUrl')
    primary_file = db.Column(db.Boolean, default=False, name='primaryFile')
    
    def __repr__(self):
        return f'<File {self.name}>'

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    nsfw_level = db.Column(db.Integer, default=0, name='nsfwLevel')
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    hash = db.Column(db.String(64))
    model_version_id = db.Column(db.Integer, db.ForeignKey('modelVersions.id'), name='modelVersion_id')
    
    def __repr__(self):
        return f'<Image {self.id}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    tag = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Tag {self.tag}>'