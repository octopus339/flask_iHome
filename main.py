#coding:utf-8


from flask import session

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from iHome import get_app,db
app = get_app('dev')

#创建脚本管理器
manager = Manager(app)

#在迁移时让app与db产生关联
Migrate(app,db)
#将数据库迁移的脚本、命令添加到脚本管理器中
manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    print app.url_map

    manager.run()