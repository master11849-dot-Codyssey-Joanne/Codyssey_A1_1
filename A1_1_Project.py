import sys

# 전역 데이터 (프로그램 실행 시 메모리에 유지)
prompts = [
    {"id": 1, "title": "에너지 ETF와 필수소비재", "content": "고유가 시대 자산운용 전략 보고서 개요를 에너지 ETF와 필수소비재 비중 확대를 중심으로 작성해 주세요.", "category": "주식", "favorite": True},
    {"id": 2, "title": "인플레이션 방어주", "content": "인플레이션 시대 자산운용 전략 보고서 개요를 인플레이션 방어주 비중 확대를 중심으로 작성해 주세요.", "category": "주식", "favorite": False},
    {"id": 3, "title": "가상화폐 관련주", "content": "인플레이션 방어를 위한 가상화폐(비트코인) 자산운용 전략보고서를 작성해주세요.", "category": "디지털자산", "favorite": False}
]

# ID 자동 증가를 위한 변수
next_id = 4 

def show_menu():
    print("\n============================================================")
    print("    자산운용관련 보고서 작성 프롬프트 관리 프로그램 v1.0")
    print("============================================================")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록 보기")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 상세 보기 및 즐겨찾기 설정")
    print("0. 프로그램 종료")
    print("========================================")


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