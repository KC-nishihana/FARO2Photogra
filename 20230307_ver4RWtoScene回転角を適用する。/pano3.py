import PySimpleGUI as sg
import subprocess
import os
import glob
import pano_geo
import concurrent.futures
import time
import numpy as np

deployData = "230220"
print("pc_uploader. deploy : ", deployData)

# プロセス数を決定する関数
def determine_max_workers():
    import psutil
    # PCのCPU数を取得
    cpu_count = psutil.cpu_count(logical=True)
    # 使用可能なCPUの数を取得
    available_cpu_count = len(psutil.Process().cpu_affinity())
    # CPU使用率が80%になるようにプロセス数を決定
    max_workers = int(available_cpu_count * 0.3)
    # 最低でも1プロセスは起動する
    print(max_workers)
    return max(1, max_workers)

path = sg.popup_get_folder("フォルダを選択")
#path = fr'D:\realitycapture\test'
path = path + '\\'
print(path)

# 出力フォルダ、なければ作る
output_path = fr'{path}img' + '\\'
os.makedirs(output_path, exist_ok=True)

# 視点リスト(yaw,pitch,roll)
transforms = (
    ( 180,   0,0),  #1右
    (  90,   0,0),  #2前
    (   0,   0,0),  #3左
    ( -90,   0,0),  #4後
    (  90,  90,0),  #上

    #(-135,  45,0),  #1左後上
    #( -45,  45,0),  #2左前上
    #(  45,  45,0),  #3右前上
    #( 135,  45,0),  #4右後上

    #(-135, -15,0),  #1左後下
    #( -45, -15,0),  #2左前下
    #(  45, -15,0),  #3右前下
    #( 135, -15,0),  #4右後下
    )

# 画像切り出しのフレームレート、撮影時の移動スピードをみて調節
fps = 1

files = glob.glob(fr'{path}*.png')

def process_file(file):
    for index, transform in enumerate(transforms):
        filename = os.path.basename(file)
        filename_name = os.path.splitext(filename)[0]
        output_file_path=fr'{output_path}output_{filename_name}_{index}.jpg'

        RW_rote = pano_geo.xmp_data(path,output_path,filename_name,index,transform)
        sc_path = path + filename_name + '.txt'
        scene_rote = 0
        if os.path.isfile(sc_path):
            scene = open(sc_path,'r')
            #scene_rote = float(scene.read())
            scene_rote = np.array(scene.read().split(','))
            #print(scene_rote)
        else:
            scene_rote = np.array([0,0,0])

        yaw = transform[0] - (360 - RW_rote + float(scene_rote[2]))
        #yaw = transform[0] - RW_rote - float(scene_rote[2])
        pitch = transform[1] + float(scene_rote[1])
        roll = transform[2] + float(scene_rote[0])
        #print([filename_name,scene_rote[1],scene_rote[0]])
        
        if yaw < -180:
            yaw = yaw + 360
        elif yaw > 180:
            yaw = yaw - 360

        if pitch < -180:
            pitch = yaw + 360
        elif pitch > 180:
            pitch = yaw - 360

        if roll < -180:
            roll = yaw + 360
        elif roll > 180:
            roll = yaw - 360

        #print(pitch,roll)
        print([filename,yaw,pitch,roll])
        
        #print(yaw)
        # v360ライブラリのオプション
        v360_options = ':'.join([
            'input=e', # Equirectangular projection.
            'output=rectilinear', # Regular video.
            'h_fov=90',
            'v_fov=90',
            'w=5072',
            'h=5072',
            # 'interp=gauss',
            f'yaw={yaw}',
            f'pitch={pitch}',
            f'roll={roll}'
            ])

        # コマンドをつくる
        command = f'ffmpeg -i "{file}" -vf v360={v360_options} "{output_file_path}"'
        # ffmpegを実行
        print(command)
        subprocess.run(command, shell=True)
        #subprocess.run(command)

max_workers = determine_max_workers()

with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor:
#with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as executor:

    futures = [executor.submit(process_file, file) for file in files]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(e)
