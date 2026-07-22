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
# -*- coding: utf-8 -*-
# =====================================================
# [체크포인트] 3일차 단계 1까지의 완성 코드
# 막혔을 때: 이 파일 내용을 log_analyzer.py에 통째로 붙여넣고
#            다음 단계부터 이어서 진행하세요.
# =====================================================

# ---------- 단계 1. 파싱 ----------
def parse_line(line):
    """로그 한 줄에서 IP, 시각, 메서드, URL, 상태코드를 추출한다.
    형식에 맞지 않는 줄은 None을 반환한다."""
    line = line.strip()                 # 앞뒤 공백 / 줄바꿈 제거
    if line == "":                      # 빈 줄이므로 None 반환
        return None
    parts = line.split()                # 공백 기준으로 나눠서 parts라는 리스트에 저장
    if len(parts) < 9:                  # parts의 길이가 모자라면 깨진 줄 
        return None                     # 잘못된 결과이므로 None 반환
    try:
        status = int(parts[8])          # 상태코드를 정수로 변환
    except ValueError:                  # 숫자가 아니면 깨진 줄
        return None                     # 잘못된 결과이므로 None 반환
    return {
        "ip": parts[0],
        "time": parts[3].lstrip("[") + " " + parts[4].rstrip("]"),
        "method": parts[5].lstrip('"'),
        "url": parts[6],
        "status": status,
    }

entries = []          # 파싱에 성공한 딕셔너리들을 담는 리스트
skipped = 0           # 건너뛴(깨진) 줄 수
total_lines = 0       # 파일의 전체 줄 수

with open("access.log", "r", encoding="utf-8") as f:
    for raw in f:
        total_lines += 1
        entry = parse_line(raw)
        if entry is None:
            skipped += 1
        else:
            entries.append(entry)

print("=== 처음 5줄 파싱 결과 ===")
for e in entries[:5]:
    print(e)
print(f"\n전체 줄 수: {total_lines} / 건너뛴 줄 수: {skipped} / 파싱 성공: {len(entries)}")


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
# ---------- 단계 2. 상태코드별 요청 수 집계 및 정렬 ----------
status_counts = {}  # {상태코드: 개수} 형태로 카운트할 빈 딕셔너리 생성

# 파싱에 성공한 로그들을 하나씩 순회하며 카운팅
for entry in entries:
    status = entry["status"]
    status_counts[status] = status_counts.get(status, 0) + 1

# [출력 1] 상태코드를 오름차순으로 정렬하여 출력
print("\n=== 상태코드별 요청 수 ===")
for status in sorted(status_counts.keys()):
    print(f"{status}: {status_counts[status]}")


# 총합 및 수치 일치 검증
total_status_count = sum(status_counts.values())  # 상태코드별 개수의 총합
expected_count = total_lines - skipped  # 전체 줄 수 - 건너뛴 줄 수

print("\n=== 검증 결과 ===")
print(f"- 상태코드 개수 총합 : {total_status_count}")
print(f"- (전체 - 건너뛴 줄 수): {expected_count}")

if total_status_count == expected_count:
    print("✅ 두 수치가 일치합니다! (집계 성공)")
else:
    print("❌ 수치가 일치하지 않습니다. (확인 필요)")

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
