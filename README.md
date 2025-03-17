# Flask 博客项目

## 项目介绍
这是一个使用 Flask 框架搭建的简单博客系统，包含文章发布、查看、删除，匿名评论，用户注册和登录等功能。

## 技术栈
### 后端
- **Flask**：用于构建 Web 应用程序。
- **SQLite**：作为数据库存储博客文章、评论和用户信息。
- **Werkzeug**：用于密码加密。

### 前端
- **HTML**：用于构建页面结构。

## 项目结构
- `app.py`：Flask 应用的主文件，包含路由和业务逻辑。
- `templates` 文件夹：存放 HTML 模板文件，用于渲染页面。
  - `index.html`：博客首页，显示所有文章列表。
  - `new.html`：发布新文章的页面。
  - `post.html`：单篇文章详情页，包含文章内容和评论列表。
  - `register.html`：用户注册页面。
  - `login.html`：用户登录页面。
- `blog.db`：SQLite 数据库文件。
- `requirements.txt`：项目依赖文件。

## 运行步骤
1. 克隆项目到本地：
```bash
git clone https://github.com/your_username/flask-blog-project.git
cd flask-blog-project

## 运行步骤
1. 克隆项目到本地：
```bash
git clone https://github.com/your_username/flask-blog-project.git
cd flask-blog-project

2、创建并激活虚拟环境：
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

安装依赖：
bash
pip install -r requirements.txt

初始化数据库：
bash
python app.py
启动项目：
bash
python app.py
打开浏览器，访问 http://127.0.0.1:5000 即可查看博客系统。
