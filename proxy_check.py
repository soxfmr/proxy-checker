import requests
import logging
import time
import re
import threading

# read the list of proxy IPs in proxyList
proxyList = [] # there are two sample proxy ip

ACCESS_URL = 'http://ip.cn'
ACCESS_TIMEOUT = 5
ACCESS_THREAD = 8

ACCESS_MUTEX = threading.Lock()

def import_proxies(fn):
    proxyList = []
    pattern = re.compile('https:\/\/', re.IGNORECASE)

    with open(fn, 'r') as handle:
        for line in handle:
            try:
                url, port = line.strip().split(' ')
                if (url != '' and port != ''):
                    schema = 'https' if pattern.search(url) != None else 'http'
                    if (not schema.startswith('http')):
                        url = '%s://%s' % (schema, url)

                    proxyList.append({ schema : '%s:%s' % (url, port) })
            except Exception:
                pass

        handle.close()

    return proxyList


def reachable(proxy):
    try:
        time_start = time.time()
        res = requests.get(ACCESS_URL, proxies=proxy, headers={'User-agent' : 'Chrome/51.0'}, timeout = ACCESS_TIMEOUT)
        if res.status_code == 200:
            logging.debug('IP: %s is reachable, timeout: %f' % (proxy, time.time() - time_start))
    except Exception, e:
        return False
    return True

def dispatch(proxyList):
    for item in proxyList:
        result = reachable(item)

        ACCESS_MUTEX.acquire()
        if result:
            print item, "is working"
        else:
            print "Bad Proxy", item
        ACCESS_MUTEX.release()

def main():
    threads = ACCESS_THREAD
    proxyList = import_proxies('ip.txt')

    total = len(proxyList)
    if total == 0:
        return

    missions = total / threads
    remains = total % threads

    if (missions == 0):
        threads = total
        missions = 1
    elif remains > 0:
        threads += 1

    if missions == 0:
        return

    threadPool = []
    for i in range(0, threads):
        offset = i * missions
        dispatcher = threading.Thread(target=dispatch, args=(proxyList[offset:missions + offset],))
        threadPool.append(dispatcher)

    for dispatcher in threadPool:
        #dispatcher.setDaemon(True)
        dispatcher.start()

if __name__ == '__main__':
    main()
