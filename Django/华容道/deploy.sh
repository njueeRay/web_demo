#!/bin/bash

echo "开始部署华容道项目..."

# 1. 确保在正确的目录
if [ ! -f "manage.py" ]; then
    echo "错误：请在项目根目录（包含manage.py的目录）运行此脚本"
    exit 1
fi

# 2. 设置Django环境变量
export DJANGO_SETTINGS_MODULE="settings"
echo "设置环境变量 DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"

# 3. 显示当前配置
echo "当前配置信息："
echo "- 当前目录: $(pwd)"
echo "- Python路径: $(which python)"
echo "- Django版本: $(python -c "import django; print(django.get_version())")"

# 4. 创建必要的目录
echo "创建静态文件目录..."
mkdir -p static
mkdir -p staticfiles
echo "- static目录: $(pwd)/static"
echo "- staticfiles目录: $(pwd)/staticfiles"

# 5. 设置目录权限
echo "设置目录权限..."
chmod -R 755 static
chmod -R 755 staticfiles

# 6. 检查并更新settings.py配置
echo "检查并更新Django配置..."
if ! grep -q "STATIC_ROOT.*=.*staticfiles" settings.py; then
    echo "更新 STATIC_ROOT 配置..."
    echo "STATIC_ROOT = str(BASE_DIR / 'staticfiles')" >> settings.py
fi

if ! grep -q "STATICFILES_DIRS.*=.*\[.*static" settings.py; then
    echo "更新 STATICFILES_DIRS 配置..."
    echo "STATICFILES_DIRS = [str(BASE_DIR / 'static')]" >> settings.py
fi

# 7. 检查Django配置
echo "验证Django配置..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
from django.conf import settings
print('BASE_DIR:', settings.BASE_DIR)
print('STATIC_ROOT:', settings.STATIC_ROOT)
print('STATICFILES_DIRS:', settings.STATICFILES_DIRS)
"

# 8. 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput -v 2

# 9. 检查数据库
echo "执行数据库迁移..."
python manage.py migrate

# 10. 检查项目配置
echo "检查项目配置..."
if ! grep -q "ALLOWED_HOSTS" settings.py; then
    echo "警告：settings.py 中可能缺少 ALLOWED_HOSTS 配置"
fi

# 11. 显示部署信息
echo "
部署信息：
- 项目目录: $(pwd)
- Python版本: $(python --version)
- Django版本: $(python -c "import django; print(django.get_version())")
- 静态文件目录: $(pwd)/staticfiles
"

# 12. 提示下一步操作
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