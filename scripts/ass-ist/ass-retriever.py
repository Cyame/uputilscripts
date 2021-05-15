
import os
import sys
import re


if __name__ == "__main__":
    _file_path_ = sys.argv[1]
    with open(_file_path_, 'r', encoding='utf8') as inp, open("TXT.txt", 'w',encoding='utf8') as outp:
        line_num = 0
        for line in inp:
            line_num += 1
            if 'Dialogue' in line:
                # print(line)
                _remove_tags = re.sub(r"\{.*\}","",line)
                _remove_return = re.sub(r"\\N","",_remove_tags)
                _remove_prefix = re.sub(r"Dialogue:.*,","",_remove_return)
                _processed = _remove_prefix.strip()
                print(f"处理第{line_num}行: {_processed}")
                outp.write(_processed+'\n')

