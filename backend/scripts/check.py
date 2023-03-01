# -*- coding:utf-8 -*-
import time

org_csv_file = "/home/xray/Code/cuhk-system/csv/dashboard/[Org]-JobPosting_by2021_withIndustry.csv"
tar_csv_file = "/home/xray/Code/cuhk-system/csv/dashboard/dashboard_data.csv"


def main():
    line_total = 0
    with open(org_csv_file, "r", encoding='utf-8') as f1:
        with open(tar_csv_file, "w", encoding='utf-8') as f2:
            for index, line in enumerate(f1):
                line_total += 1

                _list = line.split(",")
                if index == 0:
                    _list[0] = "id"
                    _list[-1] = "industry\n"
                else:
                    _list[0] = str(int(_list[0]) + 1)

                tar_str = ",".join(_list)
                f2.write(tar_str)
                if not line:
                    break

                print("total_lines: ", line_total)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("start_time: ", start_time)
    print("end_time: ", end_time)
