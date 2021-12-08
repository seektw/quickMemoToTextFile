# Copyright 2021 seektw. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Follow the next work flow
# step 1 : Copy your target file (.lqm) to '/target' 
# step 2 : Unzip target file to temp directory
# step 3 : Convert contents to text and create result file in '/result'
# step 4 : remove temp directory


import os
from os import walk, getcwd
import zipfile
import json
import shutil
from datetime import datetime

print("start")


def unzip_file(target_file, result_dir):
    """Unzip target_file to result_dir."""    
    # file check
    with zipfile.ZipFile(target_file) as unzip:
        unzip.extractall(result_dir)

def convert_to_text(target_file, result_dir, result_file):
    """Extract content text from jlqm(json type) file And Create txt file"""
    # file check
    try:
        with open(target_file, 'r', encoding="UTF-8") as json_file:
            json_data = json.load(json_file)
            # Extract create datetime of contend
            c_time = str(json_data["Memo"]["CreatedTime"])[0:10]
            m_time = str(json_data["Memo"]["ModifiedTime"])[0:10]
            created_datetime = datetime.utcfromtimestamp(int(c_time)).strftime("%Y-%m-%d %H:%M")
            modified_datetime = datetime.utcfromtimestamp(int(m_time)).strftime("%Y-%m-%d %H:%M")
            result_file_name = result_dir + '/' + created_datetime[0:10]+'_'+result_file

            f = open(result_file_name,'w',encoding="UTF-8")            
            j_mem = json_data["MemoObjectList"]
            for i in range(len(j_mem)):
                mem_dict = json_data["MemoObjectList"][i]
                if 'DescRaw' in mem_dict.keys():
                    j_mem = json_data["MemoObjectList"][i]["DescRaw"]
                    f.write(j_mem+'\n')
                else:
                    continue
            f.write('\ncreated: ' + created_datetime + '    modified: ' + modified_datetime + '\n')
            f.close()
    except:
        print(f"file convert error : {result_file}")


# step 1 : Copy your target file (.lqm) to '/target' 
target_dir = "./target"
result_dir = "./result"

for (dirpath, dirnames, filenames) in walk(target_dir):
    print(f"dirpath : {dirpath}")
    print(f"filenames : {filenames}")

    for filename in filenames:
        if '.lqm' in filename:            
            #print(f"filename : {filename}")
            temp_dir = dirpath + '/temp'  

            # step 2 : Unzip target file to temp directory
            unzip_file(dirpath + '/' + filename, temp_dir)
            
            # remove extension            
            filename = filename.split('.')[0]
            result_file_name = filename + '.txt'

            # step 3 : Convert contents to text
            convert_to_text(temp_dir + '/memoinfo.jlqm', result_dir, result_file_name)

            # step 4 : remove temp directory
            shutil.rmtree(temp_dir)  
