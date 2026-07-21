# =====================================================
# 프롬프트 비교 실습 - 심화미션. 파일 전체 파싱
# =====================================================
# 지금까지는 로그 한 줄을 처리했지만, 실제 서버 로그는 쌓여서 파일이 됩니다.
# 어제 배운 파일 읽기와 오늘 만든 parse_line을 합쳐 파일 전체를 파싱합니다.
# 직접 작성해도 좋고, AI에게 시켜도 좋습니다.
#
# 요구사항
#   - access_mini.log 파일을 한줄씩 읽어 parse_line으로 파싱한다.
#   - 결과가 none이면 건너뛰고, 전체 줄 수와 파싱 성공한 줄, 건너띈 줄을 센다.
#
# 기대 출력
#   전체 줄 수 : 15
#   파싱 성공 : 12
#   건너뛴 줄 : 3

# --- 1. 완성한 parse_line 함수 붙여넣기 ---
# TODO: log_parser_v3.py에서 완성한 parse_line 함수를 붙여넣으세요
def parse_line(log_line: str) -> dict:
    # 간결한 정규표현식 패턴 (IP, 시간, 메서드, URL, 상태코드 추출)
    pattern = r'(\S+) - - \[(.*?)\] "(\w+) (\S+) HTTP/.*?" (\d+)'
    match = re.search(pattern, log_line)

    if not match:
        return None

    # 매칭된 그룹을 순서대로 가져와 딕셔너리로 반환
    ip, timestamp, method, url, status = match.groups()
    return {
        "ip": ip,
        "timestamp": timestamp,
        "method": method,
        "url": url,
        "status_code": int(status),  # 정수 변환
    }


# --- 2. 파일 전체 파싱하기 ---
# TODO: AI가 준 코드를 여기에 붙여넣으세요. 직접 작성해봐도 좋습니다.
import re

# 기존 parse_line 함수 (수정 금지)
def parse_line(log_line: str) -> dict:
    # 간결한 정규표현식 패턴 (IP, 시간, 메서드, URL, 상태코드 추출)
    pattern = r'(\S+) - - \[(.*?)\] "(\w+) (\S+) HTTP/.*?" (\d+)'
    match = re.search(pattern, log_line)

    if not match:
        return None

    # 매칭된 그룹을 순서대로 가져와 딕셔너리로 반환
    ip, timestamp, method, url, status = match.groups()
    return {
        "ip": ip,
        "timestamp": timestamp,
        "method": method,
        "url": url,
        "status_code": int(status),  # 정수 변환
    }


# ==========================================
# 로그 파일 파싱 및 카운팅 메인 로직
# ==========================================
def parse_log_file(file_path: str) -> list[dict]:
    """로그 파일을 한 줄씩 읽어 파싱하고, 파싱 통계를 출력합니다."""
    total_lines = 0
    parsed_lines = 0
    skipped_lines = 0

    parsed_data = []

    # memory-efficient: 파일 전체를 메모리에 올리지 않고 한 줄씩 읽습니다.
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # 개행 문자 제거
            clean_line = line.strip()

            # 빈 줄도 전체 줄 수에 포함하되 파싱 대상에서는 건너뜁니다.
            if not clean_line:
                total_lines += 1
                skipped_lines += 1
                continue

            total_lines += 1
            result = parse_line(clean_line)

            # 파싱 결과 검증 (None 처리)
            if result is None:
                skipped_lines += 1
            else:
                parsed_lines += 1
                parsed_data.append(result)

    # 요청된 통계 형식으로 출력
    print(f"전체 줄 수: {total_lines}")
    print(f"파싱 성공: {parsed_lines}")
    print(f"건너뛴 줄: {skipped_lines}")

    return parsed_data


# 실행 예시 (access_mini.log 파싱)
if __name__ == "__main__":
    # 실행 환경에 access_mini.log 파일이 있다고 가정합니다.
    from pathlib import Path

    # 파이썬 스크립트 파일(__file__)이 위치한 폴더 경로를 기준으로 절대 경로 생성
    BASE_DIR = Path(__file__).resolve().parent
    LOG_FILE_PATH = BASE_DIR / "access_mini.log"

    # 스크립트 위치 기준으로 생성한 경로 전달
    parsed_results = parse_log_file(LOG_FILE_PATH)

