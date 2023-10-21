# 包含文件复制和docker镜像构建
Copy-Item -Path $env:USERPROFILE\.android\adbkey -Destination .\adbkey
docker build -t privacy_compliance_image .