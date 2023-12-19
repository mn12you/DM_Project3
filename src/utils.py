import time
from pathlib import Path
from typing import Any, List, Tuple, Union
import numpy as np
import os


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running {func.__name__} ...", end='\r')
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} Done in {end - start:.2f} seconds")
        return result
    return wrapper


@timer
def read_file(filename: Union[str, Path],arg) -> List[List[int]]:
    """read_file

    Args:
        filename (Union[str, Path]): The filename to read
        arg: parameter for input: dataset,decay,damp 

    Returns:
        List[List[int]]: The data in the file
    """
    if arg.dataset=='ibm-5000.txt': # 如果輸入是 ibm-5000 的資料處理方式不同
        #逐行讀入資料
        file_temp=[
            [x for x in line.split()]
            for line in Path(filename).read_text().splitlines()]
        result=[]
        #每行包含三個數字 例如第一行 line 就會等於 ['1', '1', '307']
        for line in file_temp:
            temp=[]
            num=0
            for word in line:
                if num!=1:# 三個數字只取頭尾兩個為邊的起終點
                    temp.append(int(word))#將編號轉為 integer 方便之後對節點做排序
                num+=1
            result.append(temp.copy())#回傳資料 (邊的資訊，且為 integer 的 list List[List[int])
                
    else:# ibm之外的資料處理方式
        #逐行讀入資料
        file_temp=[
            [x for x in line.split()]
            for line in Path(filename).read_text().splitlines()]
        result=[]
        for line in file_temp: # 每行資料為一個字串陣列 例如 graph_1 第一行['1,2']
            temp=[]
            word_temp=""#暫放數字的變數
            for list_line in line:#list_line 是字串，因為 line 是字串陣列，例如 graph_1 第一行的 line 是 ['1,2'] list_line 是 '1,2'
                #收集數字, 以 ',' 為分界，讀到 ',' 就將 world_temp 的字串轉為 integer 
                for word in list_line:
                    if word ==',':
                        temp.append(int(word_temp))#將編號轉為 integer 方便之後對節點做排序
                        word_temp=""
                        
                    else:
                    #若為十位數字以上就會以字串形式收集在 word_temp中，例如 307 就會以 '3' '30' '307'  歷經三個迴圏被讀入
                        word_temp=word_temp+word
                temp.append(int(word_temp))#終點後沒有 ',', 所以需要再 append 一次
                result.append(temp.copy())#回傳資料 (邊的資訊，且為 integer 的 list List[List[int])
    return result.copy()
    

@timer
def write_file(data_HITS: List[Tuple[Any]],data_PageRank: List[Tuple[Any]],data_SimRank: List[Tuple[Any]], file_path: Union[str, Path],file_name:str,arg) -> None:
    """write_file writes the data to a txt file 

    Args:
        data (List[Tuple[Any]]): The data to write to the file
        filename (Union[str, Path]): The filename to write to
    """
    if arg.dataset=="graph_6.txt" or arg.dataset=="ibm-5000.txt":
        Page=file_name[0:-4]+"_PageRank.txt"
        Hit_a=file_name[0:-4]+"_HITS_authority.txt"
        Hit_h=file_name[0:-4]+"_HITS_hub.txt"
        file_path=file_path/file_name[0:-4]

        file_name_temp=file_path/Page
        data_PageRank=data_PageRank.reshape([1,data_PageRank.shape[0]])
        np.savetxt(file_name_temp, data_PageRank, delimiter=' ',fmt='%1.3f')

        file_name_temp=file_path/Hit_a
        data_HITS_a=data_HITS[0]
        data_HITS_a=data_HITS_a.reshape([1,data_HITS_a.shape[0]])
        np.savetxt(file_name_temp, data_HITS_a, delimiter=' ',fmt='%1.3f') 
        
        file_name_temp=file_path/Hit_h
        data_HITS_h=data_HITS[1]
        data_HITS_h=data_HITS_h.reshape([1,data_HITS_h.shape[0]])
        np.savetxt(file_name_temp, data_HITS_h, delimiter=' ',fmt='%1.3f') 


    else:
        Page=file_name[0:-4]+"_PageRank.txt"
        Sim=file_name[0:-4]+"_SimRank.txt"
        Hit_a=file_name[0:-4]+"_HITS_authority.txt"
        Hit_h=file_name[0:-4]+"_HITS_hub.txt"
        file_path=file_path/file_name[0:-4]
        if not file_path.exists():
            os.mkdir(file_path)

        file_name_temp=file_path/Page
        data_PageRank=data_PageRank.reshape([1,data_PageRank.shape[0]])
        np.savetxt(file_name_temp, data_PageRank, delimiter=' ',fmt='%1.3f')

        file_name_temp=file_path/Hit_a
        data_HITS_a=data_HITS[0]
        data_HITS_a=data_HITS_a.reshape([1,data_HITS_a.shape[0]])
        np.savetxt(file_name_temp, data_HITS_a, delimiter=' ',fmt='%1.3f') 
        
        file_name_temp=file_path/Hit_h
        data_HITS_h=data_HITS[1]
        data_HITS_h=data_HITS_h.reshape([1,data_HITS_h.shape[0]])
        np.savetxt(file_name_temp, data_HITS_h, delimiter=' ',fmt='%1.3f') 

        file_name_temp=file_path/Sim
        np.savetxt(file_name_temp, data_SimRank, delimiter=' ',fmt='%1.3f') 


