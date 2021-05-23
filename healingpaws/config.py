import os

class DatabaseSecretConfig(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    userimgdir = os.path.join(basedir, 'user-img')
    house_mgdir = os.path.join(basedir,"html/img/pic")
    cssdir=os.path.join(basedir,'html/css')
    jsdir=os.path.join(basedir,'html/javascript')
    imgdir = os.path.join(basedir,'html/img')
    homedir = os.path.join(basedir,'html/homepage')
    # static_folder = os.path.join(basedir,"html")
    SECRET_KEY = 'group-10-is-the-best'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False