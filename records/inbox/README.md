# 결정 알림함 — GOV-20260906-05

actor별 JSON은 다음 회사 업무 행동에서 선택 조회하는 작은 화면이다. 결재 정본은 approvals, 통지 사건은 notifications, 실제 표시/확인은 notification-receipts다. 원문을 상태함으로 이동하지 않는다.
이번 초기화는 기존 결정을 전부 unread로 만들지 않는다. 새 관리자 결정부터 의미 있는 사건을 수신자별로 생성한다. 관리자 자기 릴리스 결정에는 자기 알림을 만들지 않는다. 현재 빈 INBOX가 '미결정 업무나 문제가 없다'는 뜻은 아니다.
상세 규칙: llm-source/workflows/INBOX_WORKFLOW.md. 실제 푸시 서버나 자동 채팅 메시지 설치가 아니다.
