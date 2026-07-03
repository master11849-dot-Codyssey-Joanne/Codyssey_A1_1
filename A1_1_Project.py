import sys
import unicodedata

# 전역 데이터 (프로그램 실행 시 메모리에 유지)
# 기본 데이터에 온체인 데이터, 퀀트 지표(MACD, RSI), 슬라이딩 윈도우 등 활용 사례 반영
prompts = [
    {"id": 1, "title": "에너지 ETF와 필수소비재", "content": "고유가 시대 자산운용 전략 보고서 개요를 에너지 ETF와 필수소비재 비중 확대를 중심으로 작성해 주세요.", "category": "주식", "favorite": True},
    {"id": 2, "title": "인플레이션 방어주", "content": "인플레이션 시대 자산운용 전략 보고서 개요를 인플레이션 방어주 비중 확대를 중심으로 작성해 주세요.", "category": "주식", "favorite": False},
    {"id": 3, "title": "가상화폐 관련주", "content": "인플레이션 방어를 위한 가상화폐(비트코인) 자산운용 전략보고서를 작성해주세요.", "category": "디지털자산", "favorite": False}
]

next_id = 4 

def get_display_width(text):
    """한글 등 동아시아 문자의 시각적 너비를 2로, 나머지를 1로 계산합니다."""
    width = 0
    for char in str(text):
        # 'F'(Fullwidth), 'W'(Wide) 속성을 가진 문자는 2칸 차지
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
    print("\n======================================================")
    print("       자산운용관련 보고서 작성 프롬프트 관리 프로그램 v1.0")
    print("======================================================")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록 보기")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 상세 보기 및 즐겨찾기 설정")
    print("0. 프로그램 종료")
    print("========================================")

def add_prompt():
    global next_id
    print("\n[ 프롬프트 추가 ]")
    title = input("제목을 입력하세요: ")
    content = input("내용을 입력하세요: ")
    category = input("카테고리를 입력하세요: ")
    
    new_prompt = {
        "id": next_id,
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    }
    prompts.append(new_prompt)
    print(f"\n✅ 성공: '{title}' 프롬프트가 추가되었습니다. (ID: {next_id})")
    next_id += 1

def print_prompt_list(target_prompts):
    # 컬럼별 시각적 너비 설정
    col_id = 4
    col_cat = 12
    col_title = 30
    
    print("-" * 65)
    # 헤더 출력
    header = f"{pad_string('ID', col_id)} | {pad_string('카테고리', col_cat)} | {pad_string('제목', col_title)} | 즐겨찾기"
    print(header)
    print("-" * 65)
    
    # 데이터 출력
    for p in target_prompts:
        fav_icon = "★" if p['favorite'] else " "
        row = f"{pad_string(p['id'], col_id)} | {pad_string(p['category'], col_cat)} | {pad_string(p['title'], col_title)} |  {fav_icon}"
        print(row)
    print("-" * 65)

def view_list():
    print("\n[ 전체 프롬프트 목록 ]")
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

        
def main():
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
        elif choice == '0':
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다.")
            sys.exit()
        else:
            print("\n❌ 오류: 잘못된 입력입니다. 0~5 사이의 번호를 선택해주세요.")
            
if __name__ == "__main__":
    main()