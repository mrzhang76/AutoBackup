#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import os
import time
import threading   
  
def get_file_md5(file_name):
    m = hashlib.md5()   
    with open(file_name,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  
    return m.hexdigest()    
      
def start_zip(zip_path,backup_path,passwd,path,size,subpackage,backup_name):
    if(subpackage==''):
        cmd = r'%s a %s.7z %s %s -mhe ' %(zip_path,backup_path,passwd,path)
    else:
        if(size /1024/1024 >=int(subpackage)):
            subpackage = subpackage+'M'  
            cmd = r'%s a %s.7z %s %s -mhe -v%s' %(zip_path,backup_path,passwd,path,subpackage)
        else:
            cmd = r'%s a %s.7z %s %s -mhe ' %(zip_path,backup_path,passwd,path)
    print(cmd)
    if(os.system(cmd)!=0):
        print('备份出现问题，请检查报错信息')
        exit(0)

def file_size(name):
    size = 0
    if(os.path.isfile(name)):
        size = os.path.getsize(name)
    if(os.path.isdir(name)):
        dir_list = os.listdir(name)
        for f in dir_list:
            file = os.path.join(name,f)
            if(os.path.getsize(file)):
                size += os.path.getsize(file)
            if(os.path.isdir(file)):
                size += file_size(file)
    return size 

def to_mb(bytesize):
    return f'{bytesize / 1024 / 1024:.2f} MB'
if __name__ == '__main__':
    backup_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    print('---------------------------------------------------')
    print('欢迎使用打包备份脚本v0.1\n')
    print('当前时间为：'+backup_time)
    print('---------------------------------------------------')
    zip_path = '7z.exe' #设定所调用压缩软件目录(推荐7z)
    
    path = input('设置需备份的目录或文件的路径：')
    backup_path = input('设置备份存储目录：')
    backup_name = input('设置备份压缩包的名称（默认为待备份文件/目录名+备份时间）：')
    passwd = input('设置备份压缩包的密码（默认为空）：')
    subpackage = input('设置分卷大小（默认不进行分卷,单位为MB）：')

    
    if(path==''): 
        print('\n---------------------------------------------------')
        print('请输入需备份的目录或文件的路径!')
        print('---------------------------------------------------')
        exit(-1)
    if(backup_path==''):
        print('\n---------------------------------------------------')
        print('请输入备份的存储目录!')
        print('---------------------------------------------------')
        exit(-1)
    print('---------------------------------------------------')
    print('所调用压缩软件目录：'+zip_path)
    print('待备份的目录为：'+path)
    print('备份存储目录为：'+backup_path)
    if(backup_name==''):
        print('备份文件的名称为：待备份目录名/文件名')
    else:
        print('备份文件的名称为：'+backup_name)
    print('备份文件的密码：'+passwd)
    print('---------------------------------------------------\n')
        
    print('获取备份目录下的内容为：')
    print('---------------------------------------------------')
    all_files = [f for f in os.listdir(path)]
    i=0
    files_size=[]
    while(i<len(all_files)):
        files_size.append(file_size(path+all_files[i]))
        print(all_files[i]+"   文件大小："+to_mb(files_size[i]))
        i=i+1
    print('---------------------------------------------------\n')   
    i=0
    
    if(passwd!=''):passwd='-p'+passwd
    

    while(True):
        a=input('是否开始备份进程？（Y/N）')
        print(a)
        if(a =="N" or a =="n"):
            print('终止备份进程')
            exit(0)
        elif(a =="Y" or a =="y"):
            break
    print('备份过程开始')
    while(i<len(all_files)):
        print(all_files[i])
        if(backup_name==''):
            start_zip(zip_path,'"'+backup_path+all_files[i]+backup_time+'"',passwd,'"'+path+all_files[i]+'"',int(files_size[i]),subpackage,'"'+backup_name+'"')
        else:
            start_zip(zip_path,'"'+backup_path+backup_name+"-"+backup_time+'-'+str(i)+'"',passwd,'"'+path+all_files[i]+'"',int(files_size[i]),subpackage,'"'+backup_name+'"')
        i=i+1
    print('---------------------------------------------------\n')   

    
    print('开始进行MD5校验计算...')
    print('---------------------------------------------------')

   
    i=0
    md5_list=['']
    all_files = [f for f in os.listdir(backup_path)]
    while(i<len(all_files)):
        file_md5 = get_file_md5(backup_path+all_files[i])
        print(all_files[i]+"的MD5校验值为："+file_md5)
        md5_list.append(all_files[i]+"的MD5校验值为："+file_md5+"\n")
        i=i+1
        
    index_file = open(backup_path+"index.md","a+",encoding="utf-8")
    index_file.write("备份日期："+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    i=0
    while(i<len(md5_list)):
        index_file.write(md5_list[i])
        i=i+1
    index_file.close()
    print('---------------------------------------------------\n')   
