# 使用前先使用 sed -i 's/\r$//' build_image.sh 替换换行符，以防因为换行符问题无法在unix-like os 运行
cp ~/.android/adbkey ./adbkey
docker build -t privacy_compliance_image .