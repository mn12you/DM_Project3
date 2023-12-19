import my_algorithm
import time
import config
from pathlib import Path
from typing import List
import utils
import args



if __name__=="__main__":
    arg=args.parse_args()
    input_data: List[List[str]] = utils.read_file(config.IN_DIR/ arg.dataset,arg=arg)
    filename = Path(arg.dataset).stem
    data_HITS=my_algorithm.self_HITS(input_data,arg)
    data_PageRank=my_algorithm.self_PageRank(input_data,arg)
    data_SimRank=my_algorithm.self_SimRank(input_data, arg)
    if arg.visual:
        my_algorithm.show(input_data,arg)


    utils.write_file(data_HITS=data_HITS,data_PageRank=data_PageRank,data_SimRank=data_SimRank,file_path=config.OUT_DIR,file_name=arg.dataset,arg=arg)