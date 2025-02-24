#!/bin/bash

echo "开始部署华容道项目..."

# 1. 确保在正确的目录
if [ ! -f "manage.py" ]; then
    echo "错误：请在项目根目录（包含manage.py的目录）运行此脚本"
    exit 1
fi

# 2. 创建必要的目录
echo "创建静态文件目录..."
mkdir -p static
mkdir -p staticfiles

# 3. 设置目录权限
echo "设置目录权限..."
chmod -R 755 static
chmod -R 755 staticfiles

# 4. 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 5. 检查数据库
echo "执行数据库迁移..."
python manage.py migrate

# 6. 检查项目配置
echo "检查项目配置..."
if ! grep -q "STATIC_ROOT" settings.py; then
    echo "警告：settings.py 中可能缺少 STATIC_ROOT 配置"
fi

if ! grep -q "ALLOWED_HOSTS" settings.py; then
    echo "警告：settings.py 中可能缺少 ALLOWED_HOSTS 配置"
fi

# 7. 显示部署信息
echo "
部署信息：
- 项目目录: $(pwd)
- Python版本: $(python --version)
- Django版本: $(python -c "import django; print(django.get_version())")
- 静态文件目录: $(pwd)/staticfiles
"

# 8. 提示下一步操作
echo "
部署完成！接下来请：
1. 确认 PythonAnywhere Web 配置：
   - Source code: $(pwd)
   - Working directory: $(pwd)
   - WSGI configuration file: /var/www/hnjueeray_pythonanywhere_com_wsgi.py
   - Static files URL: /static/
   - Static files directory: $(pwd)/staticfiles

2. 在 Web 页面点击 'Reload' 按钮

3. 访问 https://hnjueeray.pythonanywhere.com 测试网站

如果遇到问题：
- 检查错误日志: /var/log/hnjueeray.pythonanywhere.com.error.log
- 确认所有路径配置正确
- 确认静态文件已正确收集
" 