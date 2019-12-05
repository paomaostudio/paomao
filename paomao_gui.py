from gooey import Gooey,GooeyParser
import paomao_pro
#from argparse import ArgumentParser

@Gooey
def main():
    parser = GooeyParser(description="My Cool GUI Program!") 

    parser.add_argument('data',
                            action='store',
                            help="Source directory that contains Excel files")

    parser.add_argument('-d', help='Start date to include')
    args = parser.parse_args()
    print(args.data)
    paomao_pro.main()
if __name__ == '__main__':
    main()