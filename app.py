from os import getloadavg
import psutil 
from functools import wraps


def to_file(func):
    @wraps(func)
    def _exe():
        res = func()
        with open("app.txt", "w") as file:
            file.write(str(res))
        return res
    return _exe


@to_file    
def get_cpu():
    res = {}
    cpu_time = psutil.cpu_times(percpu=True)
    res["time"] = {}
    for index, core in enumerate(cpu_time):
        res["time"][f"core_{index}"] = (core.user, core.system)
    res["load"] = psutil.cpu_percent(percpu=True, interval=0.3)
    return res


def get_disk():
    ...


@to_file
#def get_freq():
    #res = {}
    #freq_time = psutil.cpu_freq(percpu=True)
    #res["time"] = {}
    #for index, core in enumerate(freq_time):
        #res["time"][f"core_{index}"] = (core.max, core.min)
    #res["load"] = psutil.cpu_freq(percpu=True)
    #return res



def show(**kwargs):
    cpu_time_template = "User time for {0} {1:>10},\tsystem time for {0} {2:>10}\n"
    cpu_time_str = ""
    cpu = kwargs["cpu"]
    #cpu_freq_template = "user freq for {0} {1:>10}, \tsystem freq for {0} {2:>10}\n"
    #cpu_freq_str = ""
    #freq = kwargs["freq"]
    for key, value in cpu["time"].items():
        cpu_time_str += cpu_time_template.format(key, *value)
    #for key, value in freq["freq"].items():
        #cpu_freq_str += cpu_freq_template.format(key, *value)
    print(cpu_time_str)
    #print(cpu_freq_str)


def main():
    cpu_data = get_cpu()
    disk_data = get_disk()
    #freq_data = get_freq()


    show(
        cpu=cpu_data,
        disk=disk_data,
        #freq=freq_data
    )

if __name__ == "__main__":
    main()
