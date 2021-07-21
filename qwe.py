import psutil as ps


def get_cpu():
    res = {}
    cpu_time = ps.cpu_times(percpu=True)
    res["time"] = {}
    for index, core in enumerate(cpu_time):
        res["time"][f"core_{index}"] = (core.user, core.system)
    res["load"] = ps.cpu_percent(percpu=True, interval=0.3)
    return res


def get_disk():
    ...


def get_network():
    res = {}
    data = ps.net_io_counters(pernic=True)
    for inter, value in data.items():
        res[inter] = {
            "bytes_sent": value.bytes_sent,
            "bytes_recv": value.bytes_recv,
            "errin": value.errin,
            "errout": value.errout,
        }
    return res


def show(**kwargs):
    cpu_time_template = "User time for {0} {1:>10},\tsystem time for {0} {2:>10}\n"
    cpu_time_str = ""
    cpu = kwargs["cpu"]
    for key, value in cpu["time"].items():
        cpu_time_str += cpu_time_template.format(key, *value)
    print(cpu_time_str)

    net_info_template = (
        "Interface {0:>10} ->\t\t"
        "bytes sent:\t{bytes_sent:>15} | "
        "bytes recv:\t{bytes_recv:>15} | "
        "errin:\t{errin:>15} | "
        "errout:\t{errout:>15} |\n"
    )
    net_info_str = ""
    for name, value in kwargs["net"].items():
        net_info_str += net_info_template.format(name, **value)
    print(net_info_str)


def main():
    cpu_data = get_cpu()
    disk_data = get_disk()
    net_data = get_network()

    show(
        cpu=cpu_data,
        disk=disk_data,
        net=net_data,
    )


if __name__ == "__main__":
    main()
