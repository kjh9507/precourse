# =====================================================
# 로그 분석 만들기 실습 - 확장 미션 (선택)
# =====================================================
# 기본 4단계 + json 저장을 끝냈다면 도전!

# --- 확장 1. 의심 IP 탐지 ---
# IP별 요청 수를 집계해 상위 5개 IP를 출력하세요.
# 특정 IP의 비정상적으로 많은 요청 → 크롤러/공격 트래픽 탐지의 기본 원리

# TODO: 여기에 작성해 보세요.
ip_counts = {}
for entry in entries:
    ip = entry["ip"]
    ip_counts[ip] = ip_counts.get(ip, 0) + 1

top5_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]

print("\n=== 의심 IP 탐지 (최다 요청 TOP 5) ===")
for rank, (ip, cnt) in enumerate(top5_ips, start=1):
    print(f"{rank}위: {ip} ({cnt}회)")

# --- 확장 2. 에러율 계산 ---
# 전체 요청 중 에러(400 이상)의 비율을 퍼센트로 계산해 출력하세요.
# 기대 출력 예: 전체 요청: 2000건 / 에러: 99건 / 에러율: 4.95%

# TODO: 여기에 작성해 보세요.
total_requests = len(entries)
error_requests = sum(1 for entry in entries if entry["status"] >= 400)

if total_requests > 0:
    error_rate = (error_requests / total_requests) * 100
else:
    error_rate = 0.0

print("\n=== 에러율 분석 ===")
print(
    f"전체 요청: {total_requests}건 / 에러: {error_requests}건 / 에러율:"
    f" {error_rate:.2f}%"
)

# --- 확장 3. 메서드별 집계 ---
# GET, POST 등 HTTP 메서드별 요청 수를 추가로 집계해 보세요.

# TODO: 여기에 작성해 보세요.
method_counts = {}
for entry in entries:
    method = entry["method"]
    method_counts[method] = method_counts.get(method, 0) + 1

print("\n=== HTTP 메서드별 요청 수 ===")
for method, count in sorted(
    method_counts.items(), key=lambda x: x[1], reverse=True
):
    print(f"{method}: {count}건")

# --- 확장 4. 리팩토링 요청 연습 ---
# log_analyzer.py 전체를 AI에게 주고, 기능별 함수로 분리 + main 함수 호출 구조로
# 리팩토링을 요청해 보세요.
# ⚠️ 리팩토링 후에도 출력 결과가 이전과 완전히 동일한지 반드시 비교!



