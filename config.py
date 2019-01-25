# -*- coding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__)) #返回脚本所在目录

class Config:
	#设置秘钥，web表单防止CSRF攻击
	SECRET_KEY = 'hard to guess string'	
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True	#请求后数据库的改动会自动提交
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_RECORD_QUERIES =True
	FLASKY_SLOW_DB_QUERY_TIME = 1  #缓慢查询的阈值
	#邮件通用设置
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'		#邮件主题前缀
	FLASKY_MAIL_SENDER = '1286759028@qq.com'	#发送端
	FLASKY_ADMIN = '1286759028@qq.com'	#接收端
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 50
	FLASKY_COMMENTS_PER_PAGE = 30

	
	@staticmethod
	def init_app(app):
		pass
		
class DevelopmentConfig(Config):
	DEBUG = True	
	MAIL_SERVER = 'smtp.qq.com'	#smtp服务器
	MAIL_PORT = 465	#服务器端口
	MAIL_USE_SSL = True	#使用SSL加密
	MAIL_USERNAME = '1286759028@qq.com'	#发送端
	MAIL_PASSWORD = 'pkjvktjxunyjgied'	#授权码
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
		
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
		
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')
		
config = {                           # config字典
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	
	'default': DevelopmentConfig
	}