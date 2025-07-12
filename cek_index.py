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

def load_file_list(filename):
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        print(f"[INFO] Loaded {len(lines)} dari {filename}")
        return lines
    except Exception as e:
        print(f"[ERROR] Gagal baca file {filename}: {e}")
        return []

def is_url_indexed(url, user_agents, proxies):
    max_retries = 3
    for attempt in range(max_retries):
        user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0"
        proxy = random.choice(proxies) if proxies else None

        headers = { "User-Agent": user_agent }
        search_url = f"https://www.google.com/search?q=site:{url}&num=1"
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None

        try:
            response = requests.get(search_url, headers=headers, proxies=proxies_dict, timeout=10)
            if response.status_code == 429:
                raise requests.exceptions.RequestException("429 Too Many Requests")
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
            print(f"[ERROR] ({attempt+1}/3) URL: {url} | Proxy: {proxy} | Error: {e}")
            time.sleep(random.uniform(5, 10))  # Delay sebelum retry

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
        print(f"Delay {delay} detik sebelum cek berikutnya...\n")
        time.sleep(delay)
        q.task_done()

def main():
    parser = argparse.ArgumentParser(description="Backlink Index Checker dengan Proxy Support")
    parser.add_argument("-i", "--input", default="url.txt", help="File input URL")
    parser.add_argument("-o", "--output", default=".", help="Folder output hasil")
    parser.add_argument("-t", "--threads", type=int, default=3, help="Jumlah thread (max 5)")
    args = parser.parse_args()

    max_threads = 5
    if args.threads > max_threads:
        print(f"[WARNING] Thread terlalu banyak. Diatur ke {max_threads}.")
        args.threads = max_threads

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    user_agents = load_file_list(USER_AGENT_FILE)
    proxies = load_file_list(PROXY_FILE)
    urls = load_file_list(args.input)

    indexed_list = []
    non_indexed_list = []
    lock = threading.Lock()
    q = Queue()

    for idx, url in enumerate(urls, 1):
        q.put((url, idx, len(urls)))

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(q, user_agents, proxies, indexed_list, non_indexed_list, lock))
        t.start()
        threads.append(t)

    q.join()
    for _ in threads:
        q.put(None)
    for t in threads:
        t.join()

    with open(os.path.join(args.output, "Indexed.txt"), "w") as f:
        f.writelines([url + "\n" for url in indexed_list])
    with open(os.path.join(args.output, "Non-Indexed.txt"), "w") as f:
        f.writelines([url + "\n" for url in non_indexed_list])

    print(f"[DONE] Cek selesai. Terindex: {len(indexed_list)}, Tidak: {len(non_indexed_list)}")

if __name__ == "__main__":
    main()
