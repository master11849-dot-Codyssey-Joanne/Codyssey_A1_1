import sys
import unicodedata
import json
import os

# 파일 경로 설정
DATA_FILE = "prompts.json"

# 기본 데이터 (최초 실행 시 파일이 없을 때 사용)
DEFAULT_PROMPTS = [
    {"id": 1, "title": "에너지 ETF와 필수소비재", "content": "기관 ETF 자금 유입 데이터와 고래 움직임을 분석하여 상관관계를 시각화하는 파이썬 3.9.5 환경의 스크립트를 작성해줘.", "category": "주식", "favorite": True},
    {"id": 2, "title": "인플레이션 방어주", "content": "MACD, RSI 지표와 슬라이딩 윈도우(3분, 5분) 로직을 활용해 인플레이션 방어주 매매 시그널을 포착하는 알고리즘을 제안해줘.", "category": "주식", "favorite": False},
    {"id": 3, "title": "가상화폐 관련주", "content": "바이낸스 Coin-M 무기한 선물 거래에서 활용할 수 있는 헤지 모드 청산 로직을 포함한 트레이딩 봇 구조를 짜줘.", "category": "디지털자산", "favorite": False}
]

prompts = []
next_id = 1

def load_data():
    """JSON 파일에서 데이터를 불러옵니다. 파일이 없으면 기본 데이터를 생성합니다."""
    global prompts, next_id
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            if prompts:
                next_id = max(p['id'] for p in prompts) + 1
            else:
                next_id = 1
        except Exception as e:
            print(f"⚠️ 데이터 로드 중 오류 발생 (기본 데이터로 시작합니다): {e}")
            prompts = DEFAULT_PROMPTS.copy()
            next_id = 4
            save_data()
    else:
        # 파일이 처음인 경우 기본 데이터 세팅 후 저장
        prompts = DEFAULT_PROMPTS.copy()
        next_id = 4
        save_data()

def save_data():
    """현재 메모리의 데이터를 JSON 파일로 저장합니다."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ 데이터 저장 중 오류 발생: {e}")

def get_display_width(text):
    """한글 등 동아시아 문자의 시각적 너비를 2로, 나머지를 1로 계산합니다."""
    width = 0
    for char in str(text):
        if unicodedata.east_asian_width(char) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width

def pad_string(text, total_width):
    """지정된 총 너비에 맞춰 시각적 너비를 계산한 후 공백을 패딩합니다."""
    text = str(text)
    display_width = get_display_width(text)
    padding = total_width - display_width
    return text + " " * padding if padding > 0 else text

def show_menu():
    print("\n========================================")
    print("       프롬프트 관리 프로그램 v1.2")
    print("========================================")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록 보기")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 상세 보기 및 즐겨찾기 설정")
    print("6. 카테고리별 Markdown 내보내기")
    print("0. 프로그램 종료")
    print("========================================")

def add_prompt():
    global next_id
    print("\n[ 프롬프트 추가 ]")
    title = input("제목을 입력하세요: ")
    content = input("내용을 입력하세요: ")
    category = input("카테고리를 입력하세요: ")
    
    if not title or not content or not category:
        print("❌ 오류: 모든 필드를 입력해야 합니다.")
        return

    new_prompt = {
        "id": next_id,
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    }
    prompts.append(new_prompt)
    save_data()  # 변경사항 저장
    print(f"\n✅ 성공: '{title}' 프롬프트가 추가 및 저장되었습니다. (ID: {next_id})")
    next_id += 1

def print_prompt_list(target_prompts):
    col_id = 4
    col_cat = 14
    col_title = 32
    
    print("-" * 70)
    header = f"{pad_string('ID', col_id)} | {pad_string('카테고리', col_cat)} | {pad_string('제목', col_title)} | 즐겨찾기"
    print(header)
    print("-" * 70)
    
    for p in target_prompts:
        fav_icon = "★" if p['favorite'] else "☆"
        row = f"{pad_string(p['id'], col_id)} | {pad_string(p['category'], col_cat)} | {pad_string(p['title'], col_title)} |  {fav_icon}"
        print(row)
    print("-" * 70)

def view_list():
    print("\n[ 전체 프롬프트 목록 ]")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    print_prompt_list(prompts)
    print(f"총 {len(prompts)}개의 프롬프트가 있습니다.")

def view_by_category():
    print("\n[ 카테고리별 조회 ]")
    category = input("조회할 카테고리를 입력하세요: ")
    filtered = [p for p in prompts if p['category'] == category]
    
    if not filtered:
        print("해당 카테고리의 프롬프트가 없습니다.")
    else:
        print_prompt_list(filtered)

def search_prompt():
    print("\n[ 프롬프트 검색 ]")
    keyword = input("검색어를 입력하세요: ").lower()
    filtered = [p for p in prompts if keyword in p['title'].lower() or keyword in p['content'].lower()]
    
    if not filtered:
        print("검색 결과가 없습니다.")
    else:
        print("\n[ 검색 결과 ]")
        print_prompt_list(filtered)

def view_details():
    print("\n[ 상세 보기 ]")
    try:
        pid = int(input("조회할 프롬프트 ID를 입력하세요: "))
    except ValueError:
        print("❌ 오류: 숫자 형태의 ID를 입력해야 합니다.")
        return

    target = next((p for p in prompts if p['id'] == pid), None)
    
    if not target:
        print("❌ 오류: 해당 ID의 프롬프트를 찾을 수 없습니다.")
        return
    
    fav_icon = "★" if target['favorite'] else "☆"
    print("\n========================================")
    print(f"[ID: {target['id']}] {target['title']} (카테고리: {target['category']})")
    print(f"즐겨찾기: {fav_icon}")
    print("-" * 40)
    print("[내용]")
    print(target['content'])
    print("========================================")
    
    toggle = input("\n이 프롬프트를 즐겨찾기에 추가/해제 하시겠습니까? (y/n): ").lower()
    if toggle == 'y':
        target['favorite'] = not target['favorite']
        save_data()  # 즐겨찾기 상태 실시간 저장
        new_icon = "★" if target['favorite'] else "☆"
        print(f"✅ 성공: 즐겨찾기 상태가 변경 및 저장되었습니다. ({fav_icon} -> {new_icon})")

def export_to_markdown():
    """전체 프롬프트를 카테고리별 Markdown 파일로 내보냅니다."""
    print("\n[ 카테고리별 Markdown 내보내기 ]")
    if not prompts:
        print("❌ 오류: 내보낼 프롬프트 데이터가 없습니다.")
        return

    # 카테고리별로 데이터 그룹화
    category_map = {}
    for p in prompts:
        cat = p['category']
        if cat not in category_map:
            category_map[cat] = []
        category_map[cat].append(p)

    # 각 카테고리별로 파일 생성
    try:
        for cat, p_list in category_map.items():
            # 파일명에 공백이나 특수문자가 들어갈 수 있으므로 안전하게 처리
            safe_cat_name = "".join([c for c in cat if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).strip()
            filename = f"prompts_{safe_cat_name}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# 📂 {cat} 카테고리 프롬프트 목록\n\n")
                f.write(f"본 파일은 프로그램에서 내보낸 {cat} 관련 프롬프트 목록입니다. (총 {len(p_list)}개)\n\n")
                f.write("---\n\n")
                
                for idx, p in enumerate(p_list, 1):
                    fav_status = "★ 즐겨찾기" if p['favorite'] else "☆ 일반"
                    f.write(f"## {idx}. {p['title']}\n")
                    f.write(f"- **ID**: {p['id']}\n")
                    f.write(f"- **상태**: {fav_status}\n\n")
                    f.write(f"### 📝 내용\n")
                    f.write(f"```text\n{p['content']}\n```\n\n")
                    f.write("---\n\n")
            print(f"💾 파일 생성 완료: {filename}")
        print("\n✅ 성공: 모든 카테고리가 각각의 Markdown 파일로 성공적으로 내보내졌습니다.")
    except Exception as e:
        print(f"❌ 오류: 파일 내보내기 중 문제가 발생했습니다 ({e})")

def main():
    load_data()  # 프로그램 시작 시 데이터 불러오기
    while True:
        show_menu()
        choice = input("선택 메뉴 번호: ")
        
        if choice == '1':
            add_prompt()
        elif choice == '2':
            view_list()
        elif choice == '3':
            view_by_category()
        elif choice == '4':
            search_prompt()
        elif choice == '5':
            view_details()
        elif choice == '6':
            export_to_markdown()
        elif choice == '0':
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다.")
            sys.exit()
        else:
            print("\n❌ 오류: 잘못된 입력입니다. 0~6 사이의 번호를 선택해주세요.")

if __name__ == "__main__":
    main()