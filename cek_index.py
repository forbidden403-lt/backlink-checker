import requests
from bs4 import BeautifulSoup
import random
import time
import threading
import argparse
from queue import Queue

USER_AGENT_RAW_URL = "https://raw.githubusercontent.com/forbidden403-lt/backlink-checker/main/user_agents.txt"

def load_user_agents(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        user_agents = [line.strip() for line in res.text.splitlines() if line.strip()]
        print(f"[INFO] Loaded {len(user_agents)} user-agent dari GitHub.")
        return user_agents
    except Exception as e:
        print(f"[ERROR] Gagal load user-agent dari GitHub: {e}")
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

def is_url_indexed(url, user_agents):
    user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    headers = {
        "User-Agent": user_agent
    }
    
    query = f"site:{url}"
    search_url = f"https://www.google.com/search?q={query}&num=1"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
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
        print(f"[ERROR] Request error untuk URL {url}: {e}")
        return False

def worker(q, user_agents, indexed_list, non_indexed_list, lock):
    while True:
        item = q.get()
        if item is None:
            break
        
        url, idx, total = item
        print(f"[{idx}/{total}] Cek index: {url}")
        indexed = is_url_indexed(url, user_agents)
        if indexed:
            print(f"--> TERINDEX")
            with lock:
                indexed_list.append(url)
        else:
            print(f"--> BELUM TERINDEX")
            with lock:
                non_indexed_list.append(url)
        
        delay = random.uniform(3, 7)
        print(f"Delay {delay:.2f} detik sebelum cek URL berikutnya...\n")
        time.sleep(delay)
        q.task_done()

def main():
    MAX_THREADS = 5
    parser = argparse.ArgumentParser(description="Backlink Index Checker dengan Multi-threading")
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

    user_agents = load_user_agents(USER_AGENT_RAW_URL)
    urls = load_urls(args.input)
    
    indexed_list = []
    non_indexed_list = []
    lock = threading.Lock()
    q = Queue()
    
    total = len(urls)
    for idx, url in enumerate(urls, 1):
        q.put((url, idx, total))
    
    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(q, user_agents, indexed_list, non_indexed_list, lock))
        t.start()
        threads.append(t)
    
    q.join()
    
    # Stop workers
    for _ in range(args.threads):
        q.put(None)
    for t in threads:
        t.join()
    
    # Simpan hasil
    indexed_file = f"{args.output}/Indexed.txt"
    non_indexed_file = f"{args.output}/Non-Indexed.txt"
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
