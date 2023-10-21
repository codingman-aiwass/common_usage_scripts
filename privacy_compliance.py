# 调用命令行并获取输出，根据输出内容进行相应的业务逻辑
import configparser
import getopt
import json
import os
import re
import signal
import subprocess
import platform
import sys
import threading
from configobj import ConfigObj

def prepareADB():
    # 调用命令行程序并获取输出
    command = "adb shell ip -f inet addr show wlan0"
    output = subprocess.check_output(command, shell=True).decode("utf-8")

    # 使用正则表达式提取需要的字符串
    pattern = r"inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    match = re.search(pattern, output)
    if match:
        ip_address = match.group(1)

        # 将提取的字符串写入文件
        with open("IP.txt", "w") as file:
            file.write(ip_address + ':12005')
    commands = [
        f'adb tcpip 12005',
        f'adb connect {ip_address}:12005',
        f'adb kill-server'
    ]
    for command in commands:
        subprocess.run(command, shell=True)

# 获取操作系统类型
def get_OS_type():
    sys_platform = platform.platform().lower()
    os_type = ''
    if "windows" in sys_platform:
        os_type = 'win'
    elif "darwin" in sys_platform or 'mac' in sys_platform:
        os_type = 'mac'
    elif "linux" in sys_platform:
        os_type = 'linux'
    else:
        print('Unknown OS,regard as linux...')
        os_type = 'linux'
    return os_type

# 读取ini文件的内容，并将所有内容保存在一个字典中
def get_config_settings(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    pairs = []
    for section in config.sections():
        pairs.extend(config.items(section))
    dic = {}
    for key, value in pairs:
        dic[key] = value
    return dic

# 读取并修改.ini文件和.properties文件的内容。section_name为config.ini文件中的section的名字,key_name为设置的名称
# 下面函数实现了如何读取.ini文件和.properties文件的内容，并修改其中的某个key_name的功能。
def update_ini_properties(apks):
    # Read input from the terminal
    new_apk_path = apks
    section_name = 'run_jar_settings'
    key_name = 'apk'
    # Modify the INI file
    config = configparser.ConfigParser()
    config.read(
        'config.ini')  # Replace 'config.ini' with the path to your INI file

    # Modify the 'apk' setting in the INI file
    config.set(section_name, key_name,new_apk_path)  # Replace 'section_name' with the appropriate section name in your INI file

    # Save the modified INI file
    with open('config.ini','w') as config_file:  # Replace 'config.ini' with the path to your INI file
        config.write(config_file)

    # Modify the properties file
    props = ConfigObj('Config.properties',encoding='UTF8')  # Replace 'config.properties' with the path to your properties file

    # Modify the 'apk' setting in the properties file
    props[key_name] = new_apk_path

    # Save the modified properties file
    with open('config.properties','wb') as prop_file:  # Replace 'config.properties' with the path to your properties file
        props.write(prop_file)

# 在命令行中执行命令，可以设置超时时间，达到超时时间后，可以发送终止信号(等效于ctrl+c)，以及想要该命令执行时所在的目录。
def execute_cmd_with_timeout(cmd, timeout=1800,cwd=None):
    if cwd is None:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
    else:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True,cwd=cwd)
    try:
        p.wait(timeout)
    except subprocess.TimeoutExpired:
        p.send_signal(signal.SIGINT)
        p.wait()

# 上一个命令的升级版，用于需要读取命令行程序的输入的情况
def execute_cmd_with_timeout_and_get_output(cmd, timeout=1800, cwd=None):
    if cwd is None:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, cwd=cwd)
    
    try:
        stdout, _ = p.communicate(timeout=timeout)
        output = stdout.decode('utf-8')  # 将字节流转换为字符串
        return output
    except subprocess.TimeoutExpired:
        p.send_signal(signal.SIGINT)
        p.wait()
        return "Command timed out."

# 通过给定的一个路径，判定该路径下存在多少个.apk文件，给定的这个路径中可能存在多个用;隔开的绝对路径。
def get_apks_num(apk_path):
    pathes = apk_path.split(';')
    app_set = set()
    for single_path in pathes:
        if single_path.endswith('.apk'):
            app_set.add(single_path[single_path.rindex('/') + 1:])
        elif os.path.isdir(single_path):
            files = os.listdir(single_path)
            apk_files = [apk_file for apk_file in files if apk_file.endswith('.apk')]
            app_set.update(apk_files)
    # print(app_set)
    return len(app_set)

# 使用adb命令清除给定包名的app的缓存
def clear_app_cache(app_package_name):
    print('正在清除应用包名为{}的数据。。。'.format(app_package_name))
    execute_cmd_with_timeout('adb shell pm clear {}'.format(app_package_name))
    print('清除完毕。')



# 在不删除文件夹的情况下，删除其下所有的文件
def clear_all_files_in_folder(folder):
    # 删除传入的文件夹里所有的文件
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# python像命令行程序那样，指定某些参数，例如 -c 读取配置文件
def get_command_line_like_arg():
    input_argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(input_argv, "hc:", ["config="])
    except getopt.GetoptError:
        print('run.py -c <config.ini>')
        sys.exit(2)
    if len(opts) == 0:
        # 没有指定配置文件
        pass
    else:
        # 指定了配置文件
            for opt, arg in opts:
                if opt == '-h':
                    print('run.py -c config.ini')
                # elif opt == '-c':
                elif opt in ("-c", "--config"):
                    pass
                else:
                    pass

# 在命令行执行脚本，并将日志输出到本地
def execute_command_and_get_log():
    stdout_file = 'output.log'
    stderr_file = 'error.log'
    with open(stdout_file, "w") as stdout, open(stderr_file, "w") as stderr:
        subprocess.run(["sh", "static-run.sh"], cwd='.',stdout=stdout,stderr=stderr)

# python保存字典为json，把json导入到python
def save_and_load_json():
    # 导入json
    with open('test.json','r',encoding='utf-8') as f:
        dic_1 = json.load(f)
    # 输出json
    with open('test.json','w',encoding='utf-8') as f:
        json.dump(dic_1,f,ensure_ascii=False,indent=4)

# python多线程并行
def multi_thread():
    def test(s):
        print(s)
    threads = []
    thread1 = threading.Thread(target=test,args=('Hello'))
    thread2 = threading.Thread(target=test,args=('Hello'))
    thread3 = threading.Thread(target=test,args=('Hello'))
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

# 获取config.ini中的某个section的key
def get_settings_by_section_and_name(section_name, *args):
    conf = configparser.ConfigParser()
    conf.read('config.ini', encoding='utf-8')
    if len(args) == 1:
        return conf.get(section_name, args[0])
    else:
        tmp_list = []
        for arg in args:
            tmp_list.append(conf.get(section_name, arg))
        return tmp_list


if __name__ == '__main__':
    command = "dir"
    output = execute_cmd_with_timeout_and_get_output(command)
    print(output)
