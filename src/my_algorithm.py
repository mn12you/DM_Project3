import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt 
import time
import args
# np.set_printoptions(precision=3,suppress=True)

class vertex:
    '''
    節點類型
    提供圖的最基礎架構
    包括節點名稱
    子節點名稱 ()
    父節點名稱 ()
    '''
    def __init__(self,name) -> None:
        self.name=name
        self.children_v={}
        self.parent_v={}

class DAG:
    '''
    圖類型

    '''

    def __init__(self) -> None:
        '''    
        透過 add_vertex 方法 將 input data 存成圖
        並同步以 networkx 方式存有向圖以供視覺化
        '''
        self.vertex_list={}
        self.G=nx.DiGraph()

    def add_vertex(self,name):
        '''    
        透過 add_vertex 方法 將 input data 存成圖
        並同步以 networkx 方式存有向圖以供視覺化
        '''
        self.vertex_list[name]=vertex(name)

    def add_edge(self,parent,children):
        '''
        輸入起終點便能建立邊：
        在起點的子節點中加入終點，終點的父節點中加入起點。
        '''
        self.G.add_edge(parent,children)
        if parent not in self.vertex_list.keys():
            self.add_vertex(parent)
        if children not in self.vertex_list.keys():
            self.add_vertex(children)
        self.vertex_list[parent].children_v[children]=1
        self.vertex_list[children].parent_v[parent]=1

    def visualize(self):
        '''
        使用 networkx 視覺化有向圖
        '''
        pos=nx.circular_layout(self.G)
        nx.draw_networkx(self.G,pos) 
        plt.show() 

    def visual_table(self):
        '''
        列出所有邊
        '''
        
        for ind in self.vertex_name():
            for ind2 in self.vertex_list[ind].children_v.keys():
                print("[",ind,",",ind2,"]")
    def vertex_num(self):
        '''
        回傳圖中點數量
        '''
        return len(self.vertex_list.keys())
    def vertex_name(self):
        '''
        回傳排序好的圖的節點編號
        '''
        myKeys = list(self.vertex_list.keys())
        myKeys.sort()
        return myKeys
    
def Adjacent_matrix(graph:DAG):
    '''
    將已存成 DAG 類型的圖存成鄰接矩陣
    '''
    length=graph.vertex_num()
    A_M=np.zeros([length,length])
    ind_dict={}#將圖的點編號以 dictionary 對應到矩陣 index，例如有 [1,2,4,5] 四個點， ind_dict 會等於 {1:0, 2:1, 4:2, 5:3} 
    # 將排序後的圖得節點編號對應到矩陣的　ｉｎｄｅｘ　
    for ind,name in enumerate(graph.vertex_name()):
        ind_dict[name]=ind
    #有 a 到 b 的邊的話，將鄰接矩陣 A_M 的 [a,b] 設為 1
    for ind in graph.vertex_name():
            for ind2 in graph.vertex_list[ind].children_v.keys():
                A_M[ind_dict[ind]][ind_dict[ind2]]+=1
    return A_M

def to_graph(input_data):
    '''
    將輸入資料存成 DAG類型
    '''
    graph=DAG()
    for i in input_data:
        graph.add_edge(i[0],i[1])
    return graph


def self_HITS(input_data,arg):
    '''
    實作 HITS 演算法
    '''
    start_time=time.time()
    #前處理###################################
    graph_1=to_graph(input_data)
    A_M=Adjacent_matrix(graph_1)
    #########################################
    
    G_length=graph_1.vertex_num()#取得 N
    au=np.ones([G_length])#初始化 authority 矩陣為 1
    hu=np.ones([G_length])#初始化 hub 矩陣為 1
    
    for itr in range(arg.itr):
        au=np.matmul(A_M.T,hu)#a_t=(A^T)(h_t-1)
        hu=np.matmul(A_M,au)#h_t=A(a_t-1)
        au=au/np.sum(au)#normalized
        hu=hu/np.sum(hu)#normalized
    end_time=time.time()
    if arg.print_result:#如果要印出 result 可以將  --print_result 設為 True 
        print("Authority:",au)
        print("Hub:",hu)
    if arg.show_time:#如果要印出 計算時間 可以將  --show_time 設為 True 
        print("HITS_Computation_time:",end_time-start_time)
    return au,hu

def self_PageRank(input_data,arg):
    '''
    PageRank 實作
    '''
    start_time=time.time()
    #前處理###################################
    graph_1=to_graph(input_data)
    A_M=Adjacent_matrix(graph_1)
    #########################################
    
    G_length=graph_1.vertex_num()#取得 N
    d=arg.damp#取得 damp d

    temp=np.array([np.sum(A_M,axis=1)]).T #取得每一節點的出度
    temp[temp==0]=1#不能造成除以零的狀況 (出度為零的話那一格 row 也都是零，所以維持一樣就好) 
    M_M=A_M/temp#做出 row normalized 鄰接矩陣 (每條邊標示成 1/父節點出度)
    pr=np.ones([G_length])*1/G_length#初始化 pagerank 為 1/N
    temp=np.matmul(M_M.T,pr)
    for itr in range(arg.itr):
        temp=np.matmul(M_M.T,pr)
        #參照老師 PPT 版本定義改寫 wiki 公式為 PR(t+1)=(1-d)MPR(t)+d/N, 其中，如果 j 點連到 i 點，則 M_ij= 1/j的出度 否則為 0，所以M 就是 M_M.T
        pr=(d)/G_length+(1-d)*temp
    end_time=time.time()
    if arg.print_result:#如果要印出 result 可以將  --print_result 設為 True 
        print("PageRank:",pr)
    if arg.show_time:#如果要印出 計算時間 可以將  --show_time 設為 True 
        print("PageRank_Computation_time:",end_time-start_time)
    
    return pr

def max_matrix(a_M,b_M):
    '''
    設立 caonstrant: S(a,b)在 [0,1]，S(a,a)=1
    '''
    temp_M=np.zeros(a_M.shape)
    for i in range(a_M.shape[0]):
        for j in range(b_M.shape[1]):
            if a_M[i][j]>b_M[i][j]:
                temp_M[i][j]=a_M[i][j]
            else:
                temp_M[i][j]=b_M[i][j]
    return temp_M

def self_SimRank(input_data,arg):
    '''
    SimRank 演算法的實作
    '''
    start_time=time.time()
    #前處理###################################
    graph_1=to_graph(input_data)
    A_M=Adjacent_matrix(graph_1)
    #########################################
    
    G_length=graph_1.vertex_num()#取得 N
    c=arg.decay#取得 decay c
    temp=np.array([np.sum(A_M,axis=0)])#取得各點入度
    temp[temp==0]=1#不能造成除以零的狀況 (出度為零的話那一格 column 也都是零，所以維持一樣就好) 
    M_M=A_M/temp# column normalized 矩陣 (每條邊標示成 1/子節點入度)
    Id=np.identity(G_length)# 單位矩陣
    sim=np.identity(G_length)# 以單位矩陣初始化 SimRank
    for itr in range(arg.itr):
        #M_M.T dot Sim dot M_M 就會是 S(I(a),I(b))/|I(a)||I(b)|　之後乘上 decay c  就能將老師 PPT 上的公式實作出來 
          sim=max_matrix(np.dot(c,np.dot(np.dot(M_M.T,sim),M_M)),Id)
    end_time=time.time()
    if arg.print_result:#如果要印出 result 可以將  --print_result 設為 True 
        print("SimRank:")
        print(sim)
    if arg.show_time:#如果要印出 計算時間 可以將  --show_time 設為 True 
        print("SimRank_Computation_time:",end_time-start_time)
    return sim

def show(input_data,arg):
    graph_1=to_graph(input_data)
    A_M=Adjacent_matrix(graph_1)
    graph_1.visualize()



