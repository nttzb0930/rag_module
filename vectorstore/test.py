from .build_vectorstore import (
    load_or_build_lsd_vectorstore,
    load_or_build_ktct_vectorstore,
    load_or_build_triet_vectorstore,
)
from pprint import pprint

if __name__ == "__main__":
    lsd_vs = load_or_build_lsd_vectorstore()
    print(f'[OK] LSD VECTORSTORE LOADED/BUILT')
    # ktct_vs = load_or_build_ktct_vectorstore()
    # print(f'[OK] KTCT VECTORSTORE LOADED/BUILT')
    