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


def get_stats():
    res = {}
    cpu_stats = ps.cpu_stats()
    res["stats"] = {}
    for index, stat in enumerate(cpu_stats):
        res["stats"][f"stat_{index}"] = (stat.ctx_switches, stat.interrupts, stat.soft_interrupts, stat.syscalls)
    return res


def get_freq():
    res = {}
    cpu_freq = ps.cpu_freq(percpu=True)
    res["time"] = {}
    for index, freq in enumerate (cpu_freq):
        res["time"][f"freq_{index}"] = (freq.current, freq.min, freq.max)   
    return res


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


def get_addresses():
    res = {}
    addr = ps.net_if_addrs()
    for ass, value in addr.items():
        res[ass] = {
            "family": value.family,
            "address": value.address,
            "netmask": value.netmask,
            "broadcast": value.broadcast,
            "ptp": value.ptp,
        }
    return res


def get_disks():
    res ={}
    disks = ps.disk_io_counters(perdisk=True)
    for number, value in disks.items():
        res[number] = {
            "read_count": value.read_count, 
            "write_count": value.write_count,
            "read_bytes": value.read_bytes, 
            "write_bytes": value.write_bytes,
            "read_time": value.read_time,
            "write_time": value.write_time
        }
    return res


def show(**kwargs):
    cpu_time_template = "User time for {0} {1:>10},\tsystem time for {0} {2:>10}\n"
    cpu_time_str = ""
    cpu = kwargs["cpu"]
    for key, value in cpu["time"].items():
        cpu_time_str += cpu_time_template.format(key, *value)
    print(cpu_time_str)

    addresses_data_template = (
        "family:\t{family:>5},\t"
        "address:\t{address:>10},\t"
        "netmask:\t{netmask:>10},\t"
        "broadcast:\t{broadcast:>10},\t"
        "ptp:\t{ptp:>10}\n"
    )
    addresses_data_str = ""
    for name, value in kwargs["add"].items():
        addresses_data_str += addresses_data_template.format(name, **value)
    print(addresses_data_str)


    cpu_stats_template = (
        "ctx_switches:\t{write_count:>5},\t"
        "interrupts:\t{read_bytes:>10},\t"
        "soft_interrupts:\t{write_bytes:>10},\t"
        "syscalls:\t{read_time:>10},\n"
    )
    cpu_stats_str = ""
    stats = kwargs["cpu"]
    for key, value in stats["stats"].items():
        cpu_stats_str += cpu_stats_template.format(key, *value)
    print(cpu_stats_str)


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


    disks_info_template = (
        "write_count:\t{write_count:>5},\t"
        "read_bytes:\t{read_bytes:>10},\t"
        "write_bytes:\t{write_bytes:>10},\t"
        "read_time:\t{read_time:>10},\t"
        "write_time:\t{write_time:>10}\n"
    )
    disks_info_str = ""
    for name, value in kwargs["disks"].items():
        disks_info_str += disks_info_template.format(name, **value)
    print(disks_info_str)


    cpu_freq_template = "Current:\t{current:>10}", "min:\t{min:>10}", "max:\t{max:>10}\n"
    cpu_freq_str = ""
    cpu = kwargs["cpu"]
    for name, value in cpu["time"].items():
        cpu_freq_str += cpu_freq_template.format(name, **value)
    print(cpu_freq_str)



def main():
    cpu_data = get_cpu()
    disk_data = get_disk()
    net_data = get_network()
    freq_data = get_freq()
    disks_data = get_disks()
    stats_data = get_stats()
    addresses_data = get_addresses()


    show(
        cpu=cpu_data,
        disk=disk_data,
        net=net_data,
        freq=freq_data,
        disks=disks_data,
        stats=stats_data,
        addresses=addresses_data,
    )


if __name__ == "__main__":
    main()
