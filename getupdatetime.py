import datetime
from sys import platform as PLAT
from os import system
MINOR_VERSION_MAX_LIST = (7, 9)
INTERVAL_DATE_PATCH = ((13, 1, 21), (2, 3, -7))
INTERVAL_DATE_DEFAULT = 42


def get_time_offset(ver):
    # parse version
    major, minor = ver.split('.')[:2]
    minor = int(minor)
    major = int(major)-1
    version_count = minor + sum(MINOR_VERSION_MAX_LIST[:major])
    # calculate days offset
    days = version_count * 42 + 2  # 2 days for first version fix
    # patch special date for some unexpected situations
    if 15 <= version_count <= 16:
        live_offset = 0
    else:
        live_offset = 1

    for before, interval_count, date_patch in INTERVAL_DATE_PATCH:
        version_count -= before
        if version_count <= 0:
            break
        if version_count <= interval_count:
            days += version_count * date_patch
            break
        else:
            days += interval_count * date_patch
            version_count -= interval_count
    return datetime.timedelta(days=days), live_offset


def main():
    base_open_time = datetime.datetime.fromtimestamp(1601262000)
    offset_download_time = datetime.timedelta(days=2)
    indent = ' '
    version = input('please input genshin version(x.x)：')
    time_offset, live_offset = get_time_offset(version)
    offset_live_time = datetime.timedelta(days=10 + live_offset, hours=15)
    open_time = base_open_time + time_offset
    live_time = open_time - offset_live_time
    download_time = open_time - offset_download_time
    print(f'live：{live_time.isoformat(indent)}')
    print(f'pre download：{download_time.isoformat(indent)}')
    print(f'server open：{open_time.isoformat(indent)}')
    if PLAT == 'win32':
        system("pause")


if __name__ == '__main__':
    main()
