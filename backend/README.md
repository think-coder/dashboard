# CDC 境外升学案例系统手册
## 一、部署方式
```
1、该目录下打开终端terminal
2、安装依赖包，执行命令： "pip3 install -y -r requirements.txt"
3、启动服务，执行命令： "python3 main.py"
```
## 二、目录结构
### 2.1 app
```
应用目录；记录着服务主业务逻辑及API的定义
```
### 2.2 config
```
配置目录；记录着数据库连接的配置
```
### 2.3 const
```
常量目录；记录着程序中用到的全局变量及常量
```
### 2.4 csv
```
数据文件目录；记录着程序所用到的数据源
```
### 2.5 database
```
数据库目录；记录着数据库连接，及ORM定义
```
### 2.6 scripts
```
脚本目录；记录着项目中用到的功能脚本
```
### 2.7 static
```
静态文件目录；记录着 css、js、ttf、woff、img 等静态文件
```
### 2.8 templates
```
模板目录；记录着页端展示所用的模板
```
### 2.9 main.py
```
服务启动的入口文件，启动函数
```
### 2.10 requirements.txt
```
记录着项目的依赖项及软件包
```