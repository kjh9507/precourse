# =====================================================
# 로그 분석 만들기 실습 - log_analyzer.py
# =====================================================
# 오늘의 미션: 아래 4단계를 순서대로 완성하세요.
# access.log를 파싱해 상태코드별/시간대별/에러 URL 통계를 내고
# results.json으로 저장합니다. (내일 대시보드에서 사용)

# ❗단계마다 commit 합니다.
# - 터미널로 commit 한다면
#    git add . 
#    git commit -m "precourse day3: 단계N ... 완료"
# - vscode로 commit 한다면
#    코드 저장(ctrl + s) -> 소스 컨트롤 탭 누르기 -> 파일 stage 올리기 -> 커밋 메세지 작성 -> 커밋 버튼

# --- 단계 1. 파싱 ---
# 요구사항
#   - access.log를 한 줄씩 읽는다
#   - 각 줄에서 IP, 시각 문자열, HTTP 메서드, URL, 상태코드(정수)를 추출한다
#   - 확인용으로 처음 5줄의 추출 결과를 출력한다
#   - 마지막에 전체 줄 수를 출력한다 (단계 2의 검산에 사용)
# ⚠️ 이 로그에는 형식이 깨진 줄이 섞여 있습니다! IndexError/ValueError가 나면
#    2일차처럼 에러 메시지를 AI에게 전달하고, 깨진 줄은 건너뛰고
#    건너뛴 줄 수를 출력하도록 수정을 요청하세요.
# 🏁 처음 5줄의 파싱 결과와 건너뛴 줄 수가 출력되면 성공!

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기
import re

# 1. access.log 표준 포맷을 분석하기 위한 정규표현식 Pattern을 작성합니다.
# [IP] [시각 문자열] [HTTP 메서드] [URL] [상태코드]
log_pattern = re.compile(
    r'^(?P<ip>\S+)\s+'  # IP 주소 (공백이 아닌 문자)
    r'\S+\s+\S+\s+'  # 사용 안 하는 정보 (client identity, userid 등)
    r'\[(?P<time>[^\]]+)\]\s+'  # 시각 문자열 ([ ] 감싸진 부분)
    r'"(?P<method>[A-Z]+)\s+'  # HTTP 메서드 (GET, POST 등)
    r'(?P<url>\S+)\s+'  # URL 주소
    r'HTTP/[0-9.]+"\s+'  # HTTP 버전 정보
    r'(?P<status>\d+)'  # 상태 코드 (숫자)
)

parsed_logs = []  # 파싱된 데이터를 담을 리스트
total_lines = 0  # 전체 줄 수를 세는 카운터

# 2. access.log 파일을 한 줄씩 읽어옵니다.
with open('access.log', 'r', encoding='utf-8') as file:
    for line in file:
        total_lines += 1  # 줄 수 카운트 증가
        line = line.strip()

        # 정규표현식 매칭 시도
        match = log_pattern.match(line)
        if match:
            # 매칭 성공 시 데이터 추출
            data = match.groupdict()

            # 상태코드는 요구사항에 따라 정수(int)형으로 변환합니다.
            parsed_data = {
                'ip': data['ip'],
                'time': data['time'],
                'method': data['method'],
                'url': data['url'],
                'status': int(data['status']),
            }
            parsed_logs.append(parsed_data)

# -------------------------------------------------------------
# [단계 1] 확인을 위해 처음 5줄의 파싱 결과를 출력합니다.
# -------------------------------------------------------------
print("=== 처음 5줄 파싱 결과 ===")
for i, log in enumerate(parsed_logs[:5], start=1):
    print(f"[{i}번째 줄]")
    print(f" - IP        : {log['ip']}")
    print(f" - 시각      : {log['time']}")
    print(f" - 메서드    : {log['method']}")
    print(f" - URL       : {log['url']}")
    print(f" - 상태코드  : {log['status']} (타입: {type(log['status']).__name__})")
    print("-" * 40)

# -------------------------------------------------------------
# [단계 2] 마지막에 전체 읽어들인 줄 수를 출력합니다.
# -------------------------------------------------------------
print(f"\n총 읽은 파일 줄 수: {total_lines}줄")

# --- 단계 2. 상태코드별 집계 ---
# 요구사항: 전체 로그의 상태코드별 요청 수를 집계해 출력한다
# 🤔 힌트: 1일차의 딕셔너리 카운팅 패턴
#   status_counts[code] = status_counts.get(code, 0) + 1
# 기대 출력 형식
#   === 상태코드별 요청 수 ===
#   200: 1523
#   404: 87
# 🏁 개수의 총합이 (전체 줄 수 - 건너뛴 줄 수)와 일치하면 성공!

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기


# # --- 단계 3. 시간대별 집계 ---
# 요구사항: 시각 문자열에서 시(hour)만 추출해 0~23시 요청 수를 집계해 출력한다
# 🤔 힌트: "07/Jul/2026:14:23:45 +0900" 을 콜론(:)으로 자르면 두 번째 파트가 시
#   hour = time_str.split(":")[1]     # "14"
#   정렬 출력: for hour in sorted(hourly_counts.keys()): ...
#   변수 이름은 hourly_counts 로 해주세요. (마무리의 json 저장에서 사용합니다)
#   시(hour)를 int()로 바꾸지 마세요. "00" 같은 두 자리 문자열이어야 내일 대시보드와 연결됩니다.
# 기대 출력 형식
#   === 시간대별 요청 수 ===
#   00시: 12
#   ...
#   23시: 31
# 🏁 0~23시 순서대로 정렬되어 출력되면 성공!

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기


# --- 단계 4. 에러 URL TOP 5 ---
# 요구사항
#   - 상태코드가 400 이상인 요청만 대상으로 URL별 발생 횟수를 집계한다
#   - 발생 횟수가 많은 순서로 상위 5개를 출력한다
# 🤔 힌트: 값 기준 내림차순 정렬 후 상위 5개 자르기
#   top5 = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
#   for rank, (url, cnt) in enumerate(top5, start=1):
#       print(f"{rank}위: {url} ({cnt}회)")
#   lambda가 낯설다면 AI에게 이 두 줄의 동작 설명을 요청해 보세요.
# 기대 출력 형식
#   === 에러 최다 URL TOP 5 ===
#   1위: /api/payment (37회)
# 🏁 에러 URL 상위 5개가 횟수와 함께 출력되면 성공!
# ⚠️ 출력까지 끝났다면, 마무리의 json 저장에서 쓸 수 있도록
#    아래 한 줄을 추가해 top_error_urls 변수를 만들어 두세요.
#   top_error_urls = [list(t) for t in top5]   # [[URL, 횟수], ...] 형태

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기


# --- 마무리. 결과를 results.json으로 저장 ---
# 단계 4까지 완성한 뒤, 아래 주석을 해제하세요.
# ★ 키 이름(status_counts / hourly_counts / top_error_urls)은
#   한 글자도 바꾸지 마세요. 내일 대시보드와 연결되는 이름입니다.

# import json
#
# results = {
#     "status_counts": status_counts,
#     "hourly_counts": hourly_counts,
#     "top_error_urls": top_error_urls
# }
#
# with open("results.json", "w", encoding="utf-8") as f:
#     json.dump(results, f, ensure_ascii=False, indent=2)
#
# print("results.json 저장 완료")
