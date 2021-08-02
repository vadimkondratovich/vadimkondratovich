import psutil


def decorator(function):
    def save_txt():
        with open('full_data.txt', 'a') as info:
            result = function()
            info.write(str(result))

        return result

    return save_txt


@decorator
def get_cpu_info():
    res = ()
    all_time = psutil.cpu_times(percpu=True)
    count, percents = 0, psutil.cpu_percent(interval=1, percpu=True)

    for times in all_time:
        res = ([count + 1, str(times.user)[:6], str(times.system)[:6], str(percents[count]) + " %"])
        count += 1

    return res


@decorator
def get_memory_info():
    info = psutil.virtual_memory()
    res = ()
    res = ([f"{int(info.total / 1000000)} MB",
                        f"{int(info.used / 1000000)} MB - {int(info.percent)} %",
                        f"{int(info.free / 1000000)} MB"])

    return res


@decorator
def get_disk_info():
    temp = psutil.disk_partitions()
    res = ()
    for i in temp:
        if i.fstype:
            disk_size = psutil.disk_usage(i.device)
            res = ([i.device,
                        i.fstype,
                        f"{int(disk_size.total / 1000000000)} GB",
                        f"{int(disk_size.used / 1000000000)} GB - {disk_size.percent} %",
                        f"{int(disk_size.free / 1000000000)} GB",
                        ])

    return res


@decorator
def get_process_info():
    res = ()
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        res = ([proc.info['pid'],
                        proc.info['name'],
                        proc.info['username']
                        ])

    return res


#def get_stats_info():
    #res = ()
    #cpu_stats = psutil.cpu_stats()
    #for stat in cpu_stats:
        #res = ([f"{str(stat.ctx_switches)}", 
                #f"{str(stat.interrupts)}", 
                #f"{str(stat.soft_interrupts)}", 
                #f"{str(stat.syscalls)}",
                #])
    #return res


@decorator
def main():
    print("\tДанные о Процессоре", get_cpu_info(), sep="\n")
    print("\tДанные о Оперативной памяти", get_memory_info(), sep="\n")
    print("\tДанные о HDD", get_disk_info(), sep="\n")
    print("\tДанные о Процессах", get_process_info(), sep="\n")
    #print("\tДанные о Статистике", get_stats_info(), sep="\n")



if __name__ == "__main__":
    main()
