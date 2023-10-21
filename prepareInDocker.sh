# /bin/bash
# 该脚本在宿主机运行python run_docker.py之后，在进入docker容器后使用
IP=$(cat /app/IP.txt)
adb connect $IP;
frida_server_running=$(adb shell ps -e | grep frida15)

if [[ -n $frida_server_running ]]; then
  echo "frida-server is running. Killing..."
  adb shell su -c killall frida15
  echo "Starting..."
  adb shell su -c ./data/local/tmp/frida15 &
else
  echo "frida-server is not running. Starting..."
  adb shell su -c ./data/local/tmp/frida15 &
fi
# 更改换行符格式
sed -i 's/\r$//' ./Privacy-compliance-detection-2.1/core/static-run.sh
#sed -i 's/\r$//' ./AppUIAutomator2Navigation/run.sh
exit
#该脚本运行结束以后就可以在docker中运行python3 run.py了