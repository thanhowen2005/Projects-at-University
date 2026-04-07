import arxiv
import os
import json
import requests
import tarfile
import time
import psutil
from datetime import timezone, timedelta
import threading
from concurrent.futures import ThreadPoolExecutor
import random
from urllib.error import HTTPError, URLError

def safe_results(client, search, max_retries=3):
    """
    Bọc client.results(search) với retry và delay ngẫu nhiên.
    Giữ nguyên cú pháp search gốc, không thay đổi logic chính.
    """
    for attempt in range(max_retries):
        try:
            return list(client.results(search))
        except (arxiv.HTTPError, URLError) as e:
            wait = random.uniform(3, 8)
            print(f"[safe_results] Attempt {attempt+1}/{max_retries} failed ({type(e).__name__}). Retrying in {wait:.1f}s...")
            time.sleep(wait)
        except Exception as e:
            print(f"[safe_results] Unexpected error: {e}")
            time.sleep(3)
    print(f"[safe_results] Failed all {max_retries} retries.")
    return []


def find_paper(paper_id):
    """
    Lấy metadata của một paper trên arXiv dựa vào arXiv ID.
    """
    client = arxiv.Client()
    search = arxiv.Search(id_list=[paper_id])
    results = safe_results(client, search)
    return results[0] if results else None


def find_papers_batch_for_revised_dates(paper_ids):
    """
    Gọi arXiv API để lấy metadata cho nhiều bài báo cùng lúc.
    - Input: list các arXiv ID (dạng '2305.14597')
    - Output: dict {arxiv_id: arxiv.Result}
    """
    client = arxiv.Client()
    search = arxiv.Search(id_list=paper_ids)
    papers = {}
    for paper in safe_results(client, search):
        papers[paper.get_short_id()] = paper
    return papers



def get_source(paper, save_dir="./23127447"):
    """
    Tải TẤT CẢ các phiên bản source chỉ bằng MỘT đối tượng paper,
    bằng cách "vá" (patch) pdf_url bên trong vòng lặp.
    
    LƯU Ý: Đối tượng 'paper' truyền vào PHẢI LÀ phiên bản mới nhất
    để hàm này biết được tổng số phiên bản.
    """
    try:
        # Lấy thông tin ID từ paper mới nhất
        paper_id_full = paper.entry_id.split('/')[-1]
        base_id = paper_id_full.split('v')[0]         
        num_versions = int(paper_id_full.split('v')[1]) 
    except Exception as e:
        print(f"Lỗi khi xử lý paper ID: {e}")
        print("Hãy chắc chắn bạn truyền vào đối tượng paper MỚI NHẤT.")
        return {"success": False, "size_total": 0, "num_versions_found": 0}

    base_dir = os.path.join(save_dir, base_id.replace('.', '-'))
    os.makedirs(base_dir, exist_ok=True)

    print(f"Downloading {num_versions} version(s) for {base_id} (using patch method)...")

    total_size = 0
    success = False

    # Lặp qua từng phiên bản
    for v in range(1, num_versions + 1):
        arxiv_id = f"{base_id}v{v}"
        out_path = os.path.join(base_dir, f"{arxiv_id}.tar.gz")

        # Bỏ qua nếu file đã tồn tại
        if os.path.exists(out_path):
             print(f"   ✓ Skipped {arxiv_id} (already exists)")
             size = os.path.getsize(out_path)
             total_size += size
             success = True
             time.sleep(0.1)
             continue

        try:
            
            # Tự tạo link PDF cho phiên bản 'v'
            pdf_url_v = f"https://arxiv.org/pdf/{arxiv_id}"
            
            # Ghi đè (patch) link này vào ĐỐI TƯỢNG paper
            #    (Dù paper là v7, ta tạm thời gán cho nó link v1, v2...)
            paper.pdf_url = pdf_url_v
            
            # (Bỏ comment để debug)
            # print(f"   [Patched paper.pdf_url to: {paper.pdf_url}]")

            # Gọi download_source().
            paper.download_source(filename=f"{arxiv_id}.tar.gz", dirpath=base_dir)
            
            size = os.path.getsize(out_path)
            total_size += size
            success = True
            print(f"   ✓ Downloaded {arxiv_id} (Size: {size / 1024:.1f} KB)")
        
        except HTTPError as e:
            # Lỗi 404 (Không có source)
            print(f"   ✗ Failed {arxiv_id}: Không có source (HTTP 404).")
        
        except Exception as e:
            # Bắt các lỗi khác
            print(f"   ✗ Failed {arxiv_id}: {type(e).__name__}")

    return {
        "success": success,
        "size_before": total_size,
        "num_versions": num_versions
    }


def extract_versions_for_paper(base_id, save_dir="./23127447"):
    """
    Giải nén tất cả tar.gz của một paper theo cấu trúc:
        student_id/base_id/tex/base_idv<version>/

    Sau khi giải nén:
        - Xóa file tar.gz
        - Xóa tất cả file KHÔNG phải .tex và .bib

    Trả về thống kê:
        - num_versions (int): số version đã giải nén
        - size_after (int): tổng dung lượng các file .tex/.bib (bytes)
    """

    print("Extracting and organizing .tex, .bib files ...")
    base_dir = os.path.join(save_dir, base_id.replace('.', '-'))
    tex_root = os.path.join(base_dir, "tex")
    os.makedirs(tex_root, exist_ok=True)

    if not os.path.exists(base_dir):
        print(f"!Not found: {base_dir}")
        return {"num_versions": 0, "size_after": 0}

    num_versions = 0
    size_after = 0

    for file in os.listdir(base_dir):
        if file.endswith(".tar.gz") and file.startswith(base_id):
            num_versions += 1
            tar_path = os.path.join(base_dir, file)

            version_name = file.replace(".tar.gz", "").replace('.', '-')
            version_dir = os.path.join(tex_root, version_name)
            os.makedirs(version_dir, exist_ok=True)

            # Giải nén file .tar.gz
            try:
                with tarfile.open(tar_path, "r:gz") as tar:
                    tar.extractall(path=version_dir, filter="data")
            except Exception as e:
                print(f"Extract Error {tar_path}: {e}")

            # Xóa file .tar.gz sau khi giải nén
            try:
                os.remove(tar_path)
            except Exception as e:
                print(f"Delete Error {tar_path}: {e}")

            # Duyệt toàn bộ file và giữ lại chỉ .tex và .bib
            for root, dirs, files in os.walk(version_dir, topdown=False):
                for f in files:
                    filepath = os.path.join(root, f)
                    if not (f.lower().endswith(".tex") or f.lower().endswith(".bib")):
                        os.remove(filepath)
                    else:
                        size_after += os.path.getsize(filepath)

    return {
        "num_versions": num_versions,
        "size_after": size_after
    }

    

def get_revised_dates_from_paper(paper):
    """
    Lấy danh sách ngày revised của tất cả phiên bản của paper trên arXiv.
    Sử dụng batch query để giảm số lần request.
    Giờ arXiv gốc là UTC, nên cần chuyển về US Eastern Time (UTC−5)
    để khớp với ngày hiển thị chính thức trên arxiv.org.
    """
    paper_id_base = paper.entry_id.split('/')[-1].split('v')[0]
    try:
        latest_version = int(paper.entry_id.split("v")[-1])
    except ValueError:
        latest_version = 1

    version_ids = [f"{paper_id_base}v{v}" for v in range(1, latest_version + 1)]
    papers_dict = find_papers_batch_for_revised_dates(version_ids)

    revised_dates = []
    eastern_offset = timedelta(hours=-5)  # US Eastern Time (UTC−5)

    for idx, v_id in enumerate(version_ids):
        version_paper = papers_dict.get(v_id)
        if not version_paper:
            revised_dates.append(None)
            continue

        # v1 dùng ngày published, v2+ dùng ngày updated
        dt = version_paper.published if idx == 0 else version_paper.updated

        # Đặt timezone UTC rồi chuyển về Eastern Time
        local_dt = dt.replace(tzinfo=timezone.utc) + eastern_offset
        revised_dates.append(local_dt.strftime("%Y-%m-%d"))

    return revised_dates


def save_metadata(paper_id, paper, save_dir="./23127447"):
    """
    Lưu metadata của paper vào metadata.json, bao gồm:
        - title, authors, submission_date
        - tất cả các revised_dates bằng cách truy xuất từng version
        - publication venue từ arXiv hoặc Semantic Scholar

    Trả về thống kê:
        - metadata_size (int): dung lượng file metadata.json (bytes)
    """
    base_folder = os.path.join(save_dir, paper_id.replace(".", "-"))
    os.makedirs(base_folder, exist_ok=True)

    revised_dates = get_revised_dates_from_paper(paper)

    metadata = {
        "title": paper.title,
        "authors": [a.name for a in paper.authors],
        "publication_venue": paper.journal_ref if paper.journal_ref else None,
        "submission_date": paper.published.strftime("%Y-%m-%d"),
        "revised_dates": revised_dates
    }


    metadata_path = os.path.join(base_folder, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    metadata_size = os.path.getsize(metadata_path)

    print(f"Saved metadata to {metadata_path}")
    return {
        "metadata_size": metadata_size
    }



def find_papers_batch_for_ref(paper_ids):
    """
    Gọi arXiv API để lấy metadata cho nhiều bài báo cùng lúc.
    - Input: list các arXiv ID (dạng '2305.14597')
    - Output: dict {arxiv_id: arxiv.Result}
    """
    client = arxiv.Client()
    search = arxiv.Search(id_list=paper_ids)
    papers = {}
    for paper in safe_results(client, search):
        papers[normalize_id(paper.get_short_id())] = paper
    return papers



def normalize_id(x):
    """Chuẩn hoá arXiv ID (bỏ tiền tố 'arXiv:' và version như v1, v2...)"""
    return x.replace('arXiv:', '').split('v')[0].strip()


def save_references_json(base_id, save_dir="./23127447"):
    """
    Lấy danh sách các bài tham khảo (references) của một paper trên Semantic Scholar,
    lọc ra những bài có ArXiv ID, rồi gom tất cả ID đó để truy vấn arXiv 1 lần
    nhằm lấy metadata chi tiết (title, authors, submission date).

    Quy trình:
        1. Gọi Semantic Scholar API để lấy danh sách reference của paper chính.
        2. Lọc danh sách để chỉ giữ những reference có ArXiv ID.
        3. Gom toàn bộ ArXiv ID lại → query arXiv 1 lần bằng hàm find_papers_batch().
        4. Gộp metadata (title, authors, submission_date) vào dict.
        5. Lưu toàn bộ metadata vào file JSON: <save_dir>/<base_id>/references.json

    Tham số:
        base_id (str): ID của paper gốc (ví dụ: "2305.14597")
        save_dir (str): Thư mục gốc để lưu file JSON kết quả.

    Kết quả:
        - Tạo file JSON chứa metadata các bài tham khảo có trên arXiv.
    """
    print(f"Retrieving References for {base_id} ...")

    paper_dir = os.path.join(save_dir, base_id.replace(".", "-"))
    os.makedirs(paper_dir, exist_ok=True)

    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{base_id}"
    params = {"fields": "references,references.externalIds,references.title"}
    api_key = "Wl9Jy5hTU16ysGg96SXXK5KXhsziU2SE9JXPSnPG"
    headers = {"x-api-key": api_key}
    max_retries = 3
    for attempt in range(max_retries):
        resp = requests.get(url, params=params, headers=headers)

        if resp.status_code == 200:
            time.sleep(1.5)
            break
        elif resp.status_code in (429, 504):  # Quá giới hạn hoặc timeout
            print(f"[!] Got {resp.status_code} for {base_id} — waiting 60s before retry ({attempt+1}/{max_retries})...")
            time.sleep(60)
        else:
            print(f"[!] Error {resp.status_code} for {base_id}")
            return None
    else:
        print("[!] Failed after retries — skipping.")
        return None
    


    data = resp.json()
    refs = data.get("references", [])
    print(f"Found {len(refs)} total references.")

    arxiv_ids = []
    ref_meta = {}
    for ref in refs:
        ext = ref.get("externalIds") or {}
        if "ArXiv" not in ext:
            continue
        ref_id = ext["ArXiv"]
        arxiv_ids.append(ref_id)
        ref_meta[ref_id] = {"SemanticScholar ID": ref.get("paperId")}

    if not arxiv_ids:
        print("No arXiv references found.")
        out_path = os.path.join(paper_dir, "references.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)
        refs_file_size = os.path.getsize(out_path)
        print(f"Saved 0 arXiv references → {out_path}")
        return 0, refs_file_size


    print(f"Querying {len(arxiv_ids)} arXiv papers...")
    papers = find_papers_batch_for_ref(arxiv_ids)
    if len(arxiv_ids) != 0 and len(papers) == 0:
        return None

    arxiv_refs = {}
    for ref_id, base_data in ref_meta.items():
        paper = papers.get(ref_id)
        if not paper:
            continue
        ref_data = {
            **base_data,
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "submission_date": paper.published.strftime("%Y-%m-%d"),
        }
        arxiv_refs[ref_id.replace(".", "-")] = ref_data

    out_path = os.path.join(paper_dir, "references.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(arxiv_refs, f, indent=2, ensure_ascii=False)

    
    refs_file_size = os.path.getsize(out_path)
    print(f"Saved {len(arxiv_refs)} arXiv references → {out_path}")
    
    return len(arxiv_refs), refs_file_size


def format_arxiv_id(prefix: str, number: int):
    """
    Trả về ID arXiv chuẩn từ prefix (YYMM) và số thứ tự.
    Luôn đảm bảo phần số có 5 chữ số (ví dụ: 2305.00001).
    
    Args:
        prefix (str): Tiền tố tháng, ví dụ "2305", "2306"
        number (int): Số bài, ví dụ 1, 97, 14597
        
    Returns:
        str: ID đầy đủ dạng '2305.00001'
    """
    return f"{prefix}.{number:05d}"


def process_paper(base_id, save_dir):
    """
    Xử lý download/extract/metadata cho 1 paper.
    Không xử lý reference ở đây.
    """
    global total_versions, total_source_size
    global total_size_after_extract, total_metadata_size
    global paper_count, total_mem, max_mem

    paper = find_paper(base_id)
    if paper is None:
        return None  # Không tìm thấy paper

    print(f"Processing paper: {base_id}")

    # get_source
    source_stats = get_source(paper, save_dir)

    # extract
    extract_stats = extract_versions_for_paper(base_id, save_dir)

    # metadata
    meta_stats = save_metadata(base_id, paper, save_dir)

    # Cập nhật thống kê thread-safe
    with stats_lock:
        total_versions += source_stats["num_versions"]
        total_source_size += source_stats["size_before"]
        total_size_after_extract += extract_stats["size_after"]
        total_metadata_size += meta_stats["metadata_size"]
        paper_count += 1
        current_mem = process.memory_info().rss / (1024*1024)
        max_mem = max(max_mem, current_mem)
        total_mem += current_mem

    # Trả về base_id để xử lý reference
    return base_id



# Tìm tất cả base id trong range được cho 
def yyyymm_to_yymm(yyyymm: str) -> str:
    """Chuyển 'YYYY-MM' sang 'YYMM' dùng cho arXiv ID."""
    year, month = yyyymm.split("-")
    return year[2:] + month

def next_month_yyyymm(yyyymm: str) -> str:
    """Trả về tháng tiếp theo theo định dạng 'YYYY-MM'."""
    year, month = map(int, yyyymm.split("-"))
    month += 1
    if month > 12:
        month = 1
        year += 1
    return f"{year:04d}-{month:02d}"



def find_last_existing_id(yymm: str, start_id: int = 1, max_possible: int = 30000):
    """Dùng binary search để tìm ID cuối cùng tồn tại trong tháng yymm."""
    low = start_id
    high = max_possible
    last_found = None
    while low <= high:
        mid = (low + high) // 2
        paper_id = format_arxiv_id(yymm, mid)
        paper = find_paper(paper_id)
        if paper:
            last_found = mid
            low = mid + 1
        else:
            high = mid - 1
    return last_found

def find_last_ids_range(start_time: str, start_id: int, end_time: str, end_id: int):
    """Tìm ID cuối cùng tồn tại cho từng tháng từ start_time/start_id đến end_time/end_id."""
    current_time = start_time
    last_ids = {}
    first_month = True
    while True:
        yymm_prefix = yyyymm_to_yymm(current_time)
        s_id = start_id if first_month else 1
        e_id = end_id if current_time == end_time else 30000
        last_id = find_last_existing_id(yymm_prefix, s_id, e_id)
        if last_id:
            last_ids[current_time] = last_id
            print(f"[INFO] Last existing ID for {current_time}: {last_id}")
        else:
            print(f"[INFO] No papers found for {current_time}")
        if current_time == end_time:
            break
        current_time = next_month_yyyymm(current_time)
        first_month = False
    return last_ids

def generate_base_ids(start_time: str, start_id: int, end_time: str, end_id: int):
    """Tạo danh sách tất cả base IDs từ start_time/start_id đến end_time/end_id."""
    last_ids_per_month = find_last_ids_range(start_time, start_id, end_time, end_id)
    base_ids = []
    current_time = start_time
    first_month = True
    while True:
        yymm_prefix = yyyymm_to_yymm(current_time)
        s_id = start_id if first_month else 1
        e_id = last_ids_per_month.get(current_time)
        if e_id:
            for i in range(s_id, e_id + 1):
                base_ids.append(format_arxiv_id(yymm_prefix, i))
        if current_time == end_time:
            break
        current_time = next_month_yyyymm(current_time)
        first_month = False
    return base_ids


# Lock để cập nhật thống kê thread-safe
stats_lock = threading.Lock()

# --- Biến thống kê ---
total_time = 0
total_versions = 0
total_source_size = 0
total_size_after_extract = 0
total_metadata_size = 0
total_ref_size = 0
total_references = 0
total_ref_success = 0
paper_count = 0
total_mem = 0
max_mem = 0

process = psutil.Process()

# --- MAIN ---
if __name__ == "__main__":
    save_dir = "./23127447"
    start = time.time()

    """
    arxiv_id = yymm.xxxxx

    start_time = 2023-05
    start_id = 14597
    => start arxiv = 2305.14597

    end_time = 2023-06
    end_id = 9504
    => end arxiv_id = 2306.09504
    """

    start_time = "2023-05"
    start_id = 14597
    end_time = "2023-06"
    end_id = 9504

    print(f"Fetching all base IDs from {start_id} ({start_time}) to {end_id} ({end_time})...")

    all_base_ids = generate_base_ids(start_time, start_id, end_time, end_id)

    # --- Đa luồng xử lý download/extract/metadata ---
    with ThreadPoolExecutor(max_workers=4) as executor:
        processed_base_ids = list(executor.map(lambda bid: process_paper(bid, save_dir), all_base_ids))

    # --- Xử lý reference tuần tự và tính thời gian vào total_time ---
    for base_id in processed_base_ids:
        if base_id is None:
            continue

        ref_stats = save_references_json(base_id, save_dir)

        with stats_lock:
            if ref_stats is None:
                num_refs = 0
                ref_success = False
            else:
                total_ref_size += ref_stats[1]
                num_refs = ref_stats[0]
                ref_success = True
            total_references += num_refs
            total_ref_success += 1 if ref_success else 0

    total_time += time.time() - start

    # --- Thống kê ---
    success_rate_papers = paper_count / len(all_base_ids) * 100 if paper_count else 0
    avg_versions = total_versions / paper_count if paper_count else 0
    avg_source_size = total_source_size / paper_count if paper_count else 0
    avg_size_after_extract = total_size_after_extract / paper_count if paper_count else 0
    avg_metadata_size = total_metadata_size / paper_count if paper_count else 0
    avg_references = total_references / paper_count if paper_count else 0
    success_rate_refs = (total_ref_success / paper_count) * 100 if paper_count else 0
    total_disk_usage = total_size_after_extract + total_metadata_size + total_ref_size
    avg_disk_usage = total_disk_usage / paper_count if paper_count else 0
    avg_mem = total_mem / paper_count if paper_count else 0

    # --- In thống kê ---
    print(">>> General Info <<<")
    print(f"Papers processed: {len(all_base_ids)}")
    print(f"Total papers processed successfully: {paper_count:.2f}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per paper: {total_time/paper_count:.2f}s")
    print(f"Maximum memory usage: {max_mem:.2f} MB")
    print(f"Average memory usage: {avg_mem:.2f} MB\n")
    print(f"Paper scraping success rate: {success_rate_papers:.2f}%\n")

    print(">>> Source & Extraction <<<")
    print(f"Total versions downloaded: {total_versions}, avg per paper: {avg_versions:.2f}")
    print(f"Total source size (bytes): {total_source_size}, avg per paper: {avg_source_size:.2f}")
    print(f"Total size after extraction (bytes): {total_size_after_extract}, avg per paper: {avg_size_after_extract:.2f}\n")

    print(">>> Metadata <<<")
    print(f"Total metadata collected: {paper_count}")
    print(f"Total metadata size (bytes): {total_metadata_size}, avg per paper: {avg_metadata_size:.2f}\n")

    print(">>> References <<<")
    print(f"Total references collected: {total_references}, avg per paper: {avg_references:.2f}")
    print(f"Total references file size (bytes): {total_ref_size}")
    print(f"Reference scraping success rate: {success_rate_refs:.2f}%\n")

    print(">>> Disk Usage (Extract + Metadata + References) <<<")
    print(f"Total disk usage (bytes): {total_disk_usage}")
    print(f"Average disk usage per paper (bytes): {avg_disk_usage:.2f}\n")

    # --- Ghi thống kê ra file ---
    stat_path = os.path.join("statistic.txt")
    with open(stat_path, "w", encoding="utf-8") as f:
        f.write(">>> General Info <<<\n")
        f.write(f"Papers processed: {len(all_base_ids)}\n")
        f.write(f"Total papers processed successfully: {paper_count}\n")
        f.write(f"Total time: {total_time:.2f}s\n")
        f.write(f"Average time per paper: {(total_time / len(all_base_ids)):.2f}s\n")
        f.write(f"Maximum memory usage: {max_mem:.2f} MB\n")
        f.write(f"Average memory usage: {avg_mem:.2f} MB\n")
        f.write(f"Paper scraping success rate: {success_rate_papers:.2f}%\n\n")

        f.write(">>> Source & Extraction <<<\n")
        f.write(f"Total versions downloaded: {total_versions}, avg per paper: {avg_versions:.2f}\n")
        f.write(f"Total source size (bytes): {total_source_size}, avg per paper: {avg_source_size:.2f}\n")
        f.write(f"Total size after extraction (bytes): {total_size_after_extract}, avg per paper: {avg_size_after_extract:.2f}\n\n")

        f.write(">>> Metadata <<<\n")
        f.write(f"Total metadata collected: {paper_count}\n")
        f.write(f"Total metadata size (bytes): {total_metadata_size}, avg per paper: {avg_metadata_size:.2f}\n\n")

        f.write(">>> References <<<\n")
        f.write(f"Total references collected: {total_references}, avg per paper: {avg_references:.2f}\n")
        f.write(f"Total references file size (bytes): {total_ref_size}\n")
        f.write(f"Reference scraping success rate: {success_rate_refs:.2f}%\n\n")

        f.write(">>> Disk Usage (Extract + Metadata + References) <<\n")
        f.write(f"Total disk usage (bytes): {total_disk_usage}\n")
        f.write(f"Average disk usage per paper (bytes): {avg_disk_usage:.2f}\n")

    print(f"\n✓ Statistics saved to: {stat_path}")

