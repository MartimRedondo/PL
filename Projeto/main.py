import sys
import parser_1 as parser

for linha in sys.stdin:
    parser.rec_parser(linha)
    