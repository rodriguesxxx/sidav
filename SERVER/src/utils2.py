from libs import Dict, Any, ArgumentParser
from exceptions import NullArgsException

def parse_arguments(argp: ArgumentParser) -> Dict[str, Any]:
    
    if argp is None: raise NullArgsException("error >>> O argumento de análise não pode ser null.")
    
    argp.add_argument("-v", "--video",
        help="path to the (optional) video file")
    
    argp.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    
    return vars(argp.parse_args())