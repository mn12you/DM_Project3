import argparse


def parse_args():
    args_custom = argparse.ArgumentParser()

    def add_arg(*args, **kwargs):
        args_custom.add_argument(*args, **kwargs)

    add_arg('--dataset', type=str, default='graph_1.txt', help='Dataset to use, please include the extension')
    add_arg('--itr', type=int, default=100, help='How many times you should repeat')
    add_arg('--damp', type=float, default=0.1, help='The damping factor')
    add_arg('--decay', type=float, default=0.7, help='The decay factor')
    add_arg('--print_result', type=bool, default=False, help='Print out the result or not')
    add_arg('--show_time', type=bool, default=False, help='Print the computation time')
    add_arg('--visual', type=bool, default=False, help='Plot out  the graph')


    return args_custom.parse_args()