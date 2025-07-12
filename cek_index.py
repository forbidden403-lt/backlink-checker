import requests

from bs4 import BeautifulSoup

import random

import time

import threading

import argparse

from queue import Queue

import os



USER_AGENT_FILE = "User-agent.txt"

PROXY_FILE = "proxy_list.txt"



def load_list_from_file(filename, label):

    try:

        with open(filename, "r") as f:

            items = [line.strip() for line in f if line.strip()]

        print(f"[INFO] Loaded {len(items)} {label}.")

        return items

    except Exception as e:

        print(f"[ERROR] Gagal load {label} dari {filename}: {e}")

        return []



def load_urls(filename):

    try:

        with open(filename, "r") as f:

            urls = [line.strip() for line in f if line.strip()]

        print(f"[INFO] Loaded {len(urls)} URLs dari {filename}.")

        return urls

    except Exception as e:

        print(f"[ERROR] Gagal baca file {filename}: {e}")

        return []



def is_url_indexed(url, user_agents, proxies):

    user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0"

    proxy = random.choice(proxies) if proxies else None



    headers = {

        "User-Agent": user_agent

    }



    proxy_dict = {

        "http": proxy,

        "https": proxy

    } if proxy else None



    query = f"site:{url}"

    search_url = f"https://www.google.com/search?q={query}&num=1"



    try:

        response = requests.get(search_url, headers=headers, proxies=proxy_dict, timeout=10)

        response.raise_for_status()



        soup = BeautifulSoup(response.text, "html.parser")

        result_div = soup.find("div", id="search")

        if result_div:

            links = result_div.find_all("a")

            for link in links:

                href = link.get("href", "")

                if url in href:

                    return True

            return False

        else:

            return False

    except Exception as e:

        print(f"[ERROR] Request error untuk URL {url} | Proxy: {proxy} | Error: {e}")

        return False



def worker(q, user_agents, proxies, indexed_list, non_indexed_list, lock):

    while True:

        item = q.get()

        if item is None:

            break



        url, idx, total = item

        print(f"[{idx}/{total}] Cek index: {url}")

        indexed = is_url_indexed(url, user_agents, proxies)

        with lock:

            if indexed:

                print("--> TERINDEX")

                indexed_list.append(url)

            else:

                print("--> BELUM TERINDEX")

                non_indexed_list.append(url)



        delay = random.choice([30, 60, 90])

        print(f"Delay {delay} detik sebelum cek URL berikutnya...\n")

        time.sleep(delay)

        q.task_done()



def main():

    MAX_THREADS = 5

    parser = argparse.ArgumentParser(description="Backlink Index Checker dengan Multi-threading + Proxy")

    parser.add_argument("-i", "--input", default="url.txt", help="File input URL (default: url.txt)")

    parser.add_argument("-o", "--output", default=".", help="Folder output hasil (default: current folder)")

    parser.add_argument("-t", "--threads", type=int, default=3, help=f"Jumlah thread (default: 3, max {MAX_THREADS})")

    args = parser.parse_args()



    if args.threads > MAX_THREADS:

        print(f"[WARNING] Thread terlalu banyak! Dibatasi ke {MAX_THREADS} thread.")

        args.threads = MAX_THREADS

    elif args.threads < 1:

        print(f"[WARNING] Thread minimal 1. Mengatur ke 1 thread.")

        args.threads = 1



    if not os.path.exists(args.output):

        os.makedirs(args.output)



    user_agents = load_list_from_file(USER_AGENT_FILE, "user-agent")

    proxies = load_list_from_file(PROXY_FILE, "proxy")

    urls = load_urls(args.input)



    if not urls:

        print("[ERROR] Tidak ada URL untuk dicek. Pastikan file input benar.")

        return



    indexed_list = []

    non_indexed_list = []

    lock = threading.Lock()

    q = Queue()



    total = len(urls)

    for idx, url in enumerate(urls, 1):

        q.put((url, idx, total))



    threads = []

    for _ in range(args.threads):

        t = threading.Thread(target=worker, args=(q, user_agents, proxies, indexed_list, non_indexed_list, lock))

        t.start()

        threads.append(t)



    q.join()



    for _ in range(args.threads):

        q.put(None)

    for t in threads:

        t.join()



    indexed_file = os.path.join(args.output, "Indexed.txt")

    non_indexed_file = os.path.join(args.output, "Non-Indexed.txt")

    with open(indexed_file, "w") as f:

        for url in indexed_list:

            f.write(url + "\n")

    with open(non_indexed_file, "w") as f:

        for url in non_indexed_list:

            f.write(url + "\n")



    print(f"[DONE] Selesai cek semua URL.")

    print(f"Indexed.txt = {len(indexed_list)} URL")

    print(f"Non-Indexed.txt = {len(non_indexed_list)} URL")



if __name__ == "__main__":

    main()

