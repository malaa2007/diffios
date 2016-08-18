import os
import argparse
import datetime
import difflib
import pprint


def filelines(fp):
    with open(fp, 'r') as f:
        fl = [line.rstrip() for line in f.readlines()]
    return fl


def hostname(f):
    fl = filelines(f)
    hn_lines = list(ln for ln in fl if 'hostname' in ln.lower())
    return hn_lines[0].split()[1]


def compare(cases=None, candidate=None):
    if not cases:
        cases = "./cases"
    if not candidate:
        candidate = "./candidate.txt"
    res = "\n{0:=<69} [ Start ]\n".format("")
    # d = {}
    for f in os.listdir(cases):
        case = os.path.join("./cases", f)
        hn = hostname(case)
        # d[hn] = {}
        diff = list(difflib.context_diff(filelines(candidate), filelines(case)))
        missing = '\n'.join(x[2:] for x in diff if x.startswith('- '))
        additional = '\n'.join(x[2:] for x in diff if x.startswith('+ '))
        # d[hn]["-"] = missing
        # d[hn]["+"] = additional
        title = "\n[ Host: {0} ] {1:=<{2}}".format(hn, "", (79 - (len(hn) + 11)))
        minus = "\n\n-\n\n{0}".format(missing)
        plus = "\n\n+\n\n{0}".format(additional)
        res += "{0}{1}{2}\n".format(title, minus, plus)
    res += "{0:=<68} [ Finish ]\n".format("")
    # pprint.pprint(d)
    return res

def diff_to_file(diff):
    timestamp = datetime.datetime.now().isoformat().split(
            '.')[0].replace(':', '').replace('T', '-')
    fout = 'diff-{0}.txt'.format(timestamp)
    with open(fout, 'a') as output:
        output.write(diff)
    return diff

compare()
# print(diff_to_file(compare()))


# def main():

#     parser = argparse.ArgumentParser(
#     prog="cscodiff",
#     description="""
#         list differences between multiple Cisco configuration files
#         and a base Cisco configuration file.
#         """,
#     formatter_class=argparse.RawDescriptionHelpFormatter,
#     epilog="""
#         TODO: add epic description
#   	""")
#     parser.add_argument("base_file",
#                         help="Specify the base configuration file you are comparing against")
#     parser.add_argument("comparison_files",
#                         help="Specify the directory containing the Cisco configuration files you want to compare against the base file")
#     #  group = parser.add_mutually_exclusive_group()
#     #  group.add_argument("--csv", help="Output results as CSV file", action="store_true")
#     args = parser.parse_args()


#     base = filelines(args.base_file)
#     for f in os.listdir(args.comparison_files):
#         case = filelines(os.path.join(args.comparison_files, f))
#         diff = compare(base, case)
#         append_to_file('[{0}] {1}\n\n{2}\n'.format(hostname(case), '*' * 50, diff))


# if __name__ == '__main__':
#     main()
