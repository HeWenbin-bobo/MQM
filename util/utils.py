import os
import zipfile

import pandas as pd
from sklearn.base import RegressorMixin
import subprocess


def create_directory(directory):#检查目录是否存在
    if not os.path.exists(directory):
        os.makedirs(directory) # makedirs自动创建多层目录，mkdirs创建单层目录，当上一级目录不存在将报错
        print("Directory has been created: ", directory)
    else:
        Warning("Directory has existed: ", directory)

def determine_max_fucntion_evaluation(dim):
    dim = int(dim)
    maxFE = 1E5
    if dim<=10: maxFE = 1E5
    elif 10<dim<=30: maxFE = 2E5
    elif 30<dim<=50: maxFE = 4E5
    elif 50<dim<=150: maxFE = 8E5
    else: maxFE = 1E6

    return maxFE

def extract_zip_volumes(file_path, winrar_path=None):
    """
    压缩超过指定大小的文件。
    :param file_path: 文件路径。
    """
    if not os.path.exists(file_path):
        volume_count = 1
        base_name = os.path.basename(file_path)
        file_name, _ = os.path.splitext(base_name)
        base_dir = os.path.dirname(file_path)
        archive_name = os.path.join(base_dir, file_name + '.zip')
        try:
            with zipfile.ZipFile(archive_name, 'r') as zip_ref:
                zip_ref.extractall(archive_name)
        # while True:
        #     volume_name = f'{file_name}.z0{volume_count}'
        #     print(os.path.join(base_dir, volume_name))
        #     if not os.path.exists(os.path.join(base_dir, volume_name)):
        #         break
        #     with zipfile.ZipFile(os.path.join(base_dir, volume_name), 'r') as zip_ref:
        #         zip_ref.extractall(base_dir)
        #     volume_count += 1
        except:
            if winrar_path is not None:
                try:
                    # 检查解压路径是否存在，不存在则创建
                    if not os.path.exists(base_dir):
                        os.makedirs(base_dir)

                        # 构建解压命令
                    command = [winrar_path, 'x', '-o+', archive_name, base_dir]

                    # 调用 subprocess 执行解压命令
                    subprocess.run(command, check=True)
                    print(f'Successfully extracted {archive_name} to {base_dir}')
                except subprocess.CalledProcessError as e:
                    print(f'Error occurred: {e}')

def compress_file(file_path, max_size_mb, volume_size):
    """
    压缩超过指定大小的文件。
    :param file_path: 文件路径。
    :param max_size_mb: 文件最大大小，单位为MB。
    :param volume_size: 压缩包分卷大小，单位为MB。
    """
    max_size_mb = max_size_mb * 1024 * 1024
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > max_size_mb:
            volume_size = volume_size * 1024 * 1024
            base_name = os.path.basename(file_path)
            base_dir = os.path.dirname(file_path)
            with open(file_path, 'rb') as f:
                volume_count = 1
                volume_name = f'{base_name}.z{volume_count}.zip'
                with zipfile.ZipFile(os.path.join(base_dir, volume_name), 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    while True:
                        data = f.read(volume_size)
                        if not data:
                            break
                        zip_file.writestr(f'{base_name}.part{volume_count}', data)
                        volume_count += 1
                        volume_name = f'{base_name}.z{volume_count}.zip'
                        with zipfile.ZipFile(os.path.join(base_dir, volume_name), 'w', zipfile.ZIP_DEFLATED) as next_zip:
                            next_zip.close()
                zip_file.close()
            os.remove(file_path)