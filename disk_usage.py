from sys import path
import psutil as ps

def get_disk_usage():
    res = {}
    disk_usage = ps.disk_usage("/")
    res["envir"] = {}
    for index, core in enumerate(disk_usage):
        res["envir"][f"core_{index}"] = (core.total, core.used, core.free)
    return res

def get_disk():
    ...


def show(**kwargs):
    disk_usage_template = "Total environ {0} {1:>10},\tUsed environ {0} {2:>10}, \tFree environ {0} {3:>10}\n"
    disk_usage = kwargs["disk_usage"]
    disk_usage_str = ""
    for key, value in disk_usage["envir"].items():
        disk_usage_str += disk_usage_template.format(key, *value)
    print(disk_usage_str)


def main():
    disk_usage_data = get_disk_usage()
    disk_data = get_disk()


    show(
        disk_usage = disk_usage_data,
        disk = disk_data
    )

if __name__ == "__main__":
    main()
