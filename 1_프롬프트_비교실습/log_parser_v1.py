# =====================================================
# 프롬프트 비교 실습 - 미션 1. 대충 요청해 보기 (1차 시도) 
# =====================================================
# 1) "로그 파싱하는 파이썬 코드 줘" 를 AI에게 그대로 보내세요.
# 2) AI가 준 코드를 아래에 붙여넣고 실행해 보세요.
#
# 실행 후 기록해 보기:
# - AI가 어떤 로그 형식을 가정했나? IP 시각 URL 상태코드
# - 외부 라이브러리를 쓰라고 하지는 않았나? 정규표현식, Pandas를 사용하라고 함
# - 내가 원하는 값(IP, 시각, URL, 상태코드)이 나오나? 외부 라이브러리 사용으로 인해 실행이 되지 않는 코드

# TODO: AI가 준 코드를 여기에 붙여넣으세요.
import re
import pandas as pd

# 예시 로그 데이터 (IP - [날짜] "요청" 상태코드 응답크기)
log_data = """
192.168.1.1 - - [21/Jul/2026:14:32:10 +0900] "GET /index.html HTTP/1.1" 200 2326
192.168.1.2 - - [21/Jul/2026:14:32:11 +0900] "POST /login HTTP/1.1" 401 512
10.0.0.5 - - [21/Jul/2026:14:32:15 +0900] "GET /dashboard HTTP/1.1" 500 1024
"""

# 정규표현식 패턴 정의
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>\A?\w+)\s+(?P<path>[^\s]+)\s+HTTP/[0-9.]+"\s+(?P<status>\d+)\s+(?P<bytes>\d+)'
)

parsed_logs = []

for line in log_data.strip().splitlines():
    match = log_pattern.match(line)
    if match:
        parsed_logs.append(match.groupdict())

# 판다스(Pandas) DataFrame으로 변환하면 분석하기 편리합니다.
df = pd.DataFrame(parsed_logs)
print(df)