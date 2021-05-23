from healingpaws import *

if __name__=="__main__":
    app.jinja_env.auto_reload = True #静态资源修改不需要重启
    app.run(host="0.0.0.0",debug=True,port=18091)
