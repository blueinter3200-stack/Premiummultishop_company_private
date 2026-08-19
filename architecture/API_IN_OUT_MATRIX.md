# API IN / OUT Matrix

Status: target-direction baseline; exact API capability research pending.

| System | ERP IN | ERP OUT | Need to confirm |
|---|---|---|---|
| Cafe24 | yes | yes | auth, products, variants/SKU, stock, orders, customers, shipping, cancel/return, webhook, limits |
| Naver SmartStore | yes | yes | auth, products, stock, orders, customer/recipient fields, dispatch, cancel/return, inquiry, limits |
| Google | yes | yes where supported | Merchant vs Ads vs other API responsibilities, products, inventory, performance, order-related limits |
| Foreign supplier APIs | yes | future/when needed | catalog, SKU, price, stock, supplier availability, order/purchase capability |
| ERPNext or InvenTree API | yes | yes | chosen ERP, auth, entities, webhooks/events, extension model |

## 구현 전에 반드시 확정할 공통 항목

- authentication method
- read operations
- write operations
- webhook/event availability
- rate limits / quotas
- pagination
- retry/idempotency
- external product ID ↔ internal product ID
- external SKU/variant ID ↔ internal SKU
- external order ID ↔ internal order ID
- customer ID and privacy boundary
- shipment/cancel/return status mapping
- error handling and reconciliation

이 문서는 실제 API 조사 후 구체 endpoint와 권한으로 갱신한다.
