# =====================================================
# 프롬프트 비교 실습 - 미션 3. 에러 수정본 저장하기
# =====================================================
# AI에게 수정 요청을 보내 받은 최종 코드를 여기에 붙여넣으세요.
# 아래 세 가지 입력이 모두 에러 없이 처리되면 Mission Clear! 🏁

# TODO: AI가 준 수정본 코드를 여기에 붙여넣으세요.
import re


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


# --- 테스트 코드 ---
sample_log = (
    '127.0.0.1 - - [07/Jul/2026:10:23:45 +0900] "GET /index.html HTTP/1.1" 200 1043'
)
print(parse_line(sample_log))

# --- 최종 확인용 테스트 (붙여넣은 뒤 주석을 풀고 실행) ---
print(parse_line('127.0.0.1 - - [07/Jul/2026:10:23:45 +0900] "GET /index.html HTTP/1.1" 200 1043'))
print(parse_line(""))                        # 빈 줄 → None
print(parse_line("### broken line ###"))     # 형식이 깨진 줄 → None
