import euler
import os
import numpy as np

def xmp_data(in_path,out_path,filename,index,transfrom):
    with open(fr'{in_path}{filename}.rmx','r',encoding='UTF-16') as f:
        line = f.read().splitlines()

    np.set_printoptions(suppress=True,precision=8,floatmode='fixed')

    x = np.array([float(tok) for tok in line[5].split()])
    #print(line[5])
    x = x/1000
    x = x.tolist()
    hou = np.array([float(tok) for tok in line[8].split()])
    if 0 == hou[2]:
        RW_roll = float(line[11])
    else:
        RW_roll = float(line[11])* hou[2]
    
    trans_matrixs = np.array([
        [[0,-1,0],[0,0,-1],[1,0,0]],    #右
        [[1,0,0],[0,0,-1],[0,1,0]],    #後
        [[0,1,0],[0,0,-1],[-1,0,0]],    #左
        [[-1,0,0],[0,0,-1],[0,-1,0]],   #前
        [[1,0,0],[0,1,0],[0,0,1]],     #上
        [[-0.70710678,-0.70710678,0],[0.5,-0.5,-0.70710678],[0.5,-0.5,0.70710678]],  #左後上
        [[-0.70710678,0.70710678,0],[-0.5,-0.5,-0.70710678],[-0.5,-0.5,0.70710678]],  #左前上
        [[0.70710678,0.70710678,0],[-0.5,0.5,-0.70710678],[-0.5,0.5,0.70710678]],  #右前上
        [[0.70710678,-0.70710678,0],[0.5,0.5,-0.70710678],[0.5,0.5,0.70710678]], #右後上
        [[-0.70710678,-0.70710678,0],[-0.1830127,0.1830127,-0.96592583],[0.6830127,-0.6830127,-0.25881905]],  #左後下
        [[-0.70710678,0.70710678,0],[0.1830127,0.1830127,-0.96592583],[-0.6830127,-0.6830127,-0.25881905]],  #左前下
        [[0.70710678,0.70710678,0],[0.1830127,-0.1830127,-0.96592583],[-0.6830127,0.6830127,-0.25881905]],  #右前下
        [[0.70710678,-0.70710678,0],[-0.1830127,-0.1830127,-0.96592583],[0.6830127,0.6830127,-0.25881905]]  #右後下
                            ])

    
    trans_matrix = trans_matrixs[index]

    #print([index,trans_matrix])
    
    np.set_printoptions(suppress=True)

    f = open(fr'{out_path}output_{filename}_{index}.xmp','w',encoding='UTF-8')
    f.writelines(f'<x:xmpmeta xmlns:x="adobe:ns:meta/">\n')
    f.writelines(f'  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n')
    #写真情報の精度（固定するかなど）<coordinates:absolute or relative>
    #f.writelines(f'     <rdf:Description xcr:Version="3" xcr:PosePrior="locked" xcr:Coordinates="absolute"\n')
    #f.writelines(f'     <rdf:Description xcr:Version="3" xcr:PosePrior="exact" xcr:Coordinates="absolute"\n')
    f.writelines(f'     <rdf:Description xcr:Version="3" xcr:PosePrior="initial" xcr:Coordinates="absolute"\n')

    #写真の位置・回転情報
    f.writelines(f'      xcr:Rotation="{trans_matrix[0][0]} {trans_matrix[0][1]} {trans_matrix[0][2]} {trans_matrix[1][0]} {trans_matrix[1][1]} {trans_matrix[1][2]} {trans_matrix[2][0]} {trans_matrix[2][1]} {trans_matrix[2][2]}"\n')
    f.writelines(f'      xcr:Position="{x[0]} {x[1]} {x[2]}"\n')
    f.writelines(f'       xcr:DistortionModel="brown3" xcr:FocalLength35mm="18"\n')
    f.writelines(f'       xcr:PrincipalPointV="0" xcr:CalibrationPrior="exact"\n')
    f.writelines(f'       xcr:CalibrationGroup="-1" xcr:DistortionGroup="-1" xcr:InTexturing="1"\n')
    f.writelines(f'       xcr:InMeshing="0" xmlns:xcr="http://www.capturingreality.com/ns/xcr/1.1#">\n')

    #別カッコで数値を指定すると数値が確定してしまって変更されない
    #f.writelines(f'      <xcr:Rotation>{trans_matrix[0][0]} {trans_matrix[0][1]} {trans_matrix[0][2]} {trans_matrix[1][0]} {trans_matrix[1][1]} {trans_matrix[1][2]} {trans_matrix[2][0]} {trans_matrix[2][1]} {trans_matrix[2][2]}</xcr:Rotation>\n')
    f.writelines(f'      <xcr:Position>{x[0]} {x[1]} {x[2]}</xcr:Position>\n')
    #f.writelines(f'      <xcr:DistortionCoeficients>0 0 0 0 0 0</xcr:DistortionCoeficients>\n')
    #f.writelines(f'    </rdf:Description>\n')
    f.writelines(f'  </rdf:RDF>\n')
    f.writelines(f'</x:xmpmeta>\n')
    f.close()

    return np.degrees(RW_roll)
