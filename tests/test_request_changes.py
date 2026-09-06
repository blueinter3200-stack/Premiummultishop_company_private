"""Synthetic RC acceptance scenarios. No real request, account or GitHub write."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("request_changes", ROOT/"scripts/request_changes.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


def request(actor="ACT-001"):
    return {"schema_version":1,"object_type":"request","request_id":"R-20990101-001",
            "revision":1,"requester_actor_id":actor,"original_text":"구매이력 기반으로 상품 추천",
            "scope":["구매이력"],"request_status":"captured","supersedes":None}


def event(before=None, **overrides):
    before = before or request()
    e = {"base_commit":"a"*40,"current_actor_id":"ACT-001","request_id":before["request_id"],
         "request_change_id":"RC-20990101-001","source_event_id":"synthetic-message-1",
         "before_revision":before["revision"],"before_sha256":rc.digest(before),
         "material_change":True,"materiality_basis":"사용하는 데이터 범위 추가",
         "write_requested":True,"read_only":False,"save_prohibited":False,"is_quoted":False,
         "command":"/업무접수","change_type":"add_scope","changes":{"scope":["구매이력","고객 취향"]},
         "changed_at":"2099-01-01","captured_at":"2099-01-01","change_summary":"고객 취향 추가",
         "change_reason":None,"reason_source":"unknown","source_type":"synthetic_test",
         "source_locator":"tests/test_request_changes.py","source_excerpt":"고객 취향도 같이 사용해",
         "affected_work_ids":[],"affected_decision_ids":[]}
    e.update(overrides)
    return e


class RequestChangeTests(unittest.TestCase):
    def test_A_material_admin_change_creates_rc_and_preserves_original(self):
        before=request(); saved=copy.deepcopy(before)
        result=rc.build_change(before,event(before))
        self.assertEqual(result["status"],"planned")
        self.assertEqual(result["request"]["original_text"],before["original_text"])
        self.assertEqual(result["request"]["revision"],2)
        self.assertEqual(result["request"]["schema_version"],1)
        self.assertEqual(before,saved)
        self.assertIn(result["rc_path"],result["request"]["request_change_refs"])

    def test_B_typo_or_format_only_does_not_create_rc(self):
        self.assertEqual(rc.build_change(request(),event(material_change=False,changes={"scope":["구매 이력"]}))["status"],"nonmaterial_no_rc")
        self.assertEqual(rc.build_change(request(),event(changes={"scope":["구매이력"]}))["status"],"unchanged_no_rc")

    def test_C_explicit_reason_has_exact_evidence(self):
        e=event(source_excerpt="추천 정확도를 높이려고 고객 취향도 같이 사용해",change_reason="추천 정확도 개선",
                reason_source="explicit_user_statement",reason_excerpt="추천 정확도를 높이려고")
        change=rc.build_change(request(),e)["request_change"]
        self.assertEqual(change["reason_excerpt"],e["reason_excerpt"])
        rc.validate_change(change)

    def test_D_unknown_reason_is_not_invented(self):
        change=rc.build_change(request(),event())["request_change"]
        self.assertIsNone(change["change_reason"])
        self.assertIn("변경 이유 미확인",change["unknowns"])
        with self.assertRaises(ValueError):
            rc.build_change(request(),event(change_reason="아마 매출 때문"))

    def test_E_rc_does_not_approve_complete_or_change_status(self):
        before=request();before.update({"approval_status":"pending","execution_status":"not_requested"})
        after=rc.build_change(before,event(before))["request"]
        for key in ("request_status","approval_status","execution_status","supersedes"):
            self.assertEqual(after[key],before[key])
        with self.assertRaises(ValueError):
            rc.build_change(before,event(before,changes={"request_status":"approved"}))

    def test_F_read_only_no_save_questions_and_quotes_do_not_write(self):
        for command in rc.READ_ONLY:
            with self.subTest(command=command):
                self.assertEqual(rc.build_change(request(),event(command=command))["status"],"no_write")
        for flags in ({"read_only":True},{"save_prohibited":True},{"is_quoted":True},{"write_requested":False}):
            self.assertEqual(rc.build_change(request(),event(**flags))["status"],"no_write")

    def test_G_other_requesters_have_no_admin_rc_obligation(self):
        for actor in ("ACT-002","ACT-003"):
            before=request(actor)
            self.assertEqual(rc.build_change(before,event(before,current_actor_id=actor))["status"],"rc_not_required_for_actor")
        with self.assertRaises(ValueError):
            rc.build_change(request(),event(current_actor_id="ACT-003"))

    def test_H_chain_reconstructs_original_before_after_reason_and_impact(self):
        first=rc.build_change(request(),event(affected_work_ids=["W-20990101-001"],affected_decision_ids=["D-20990101-001"]))
        e2=event(first["request"],request_change_id="RC-20990101-002",source_event_id="synthetic-message-2",
                 changes={"scope":["고객 취향"]},change_type="remove_scope")
        second=rc.build_change(first["request"],e2,[first["request_change"]])
        self.assertEqual(second["request_change"]["request_snapshot_before"],first["request_change"]["request_snapshot_after"])
        self.assertEqual(second["request"]["original_text"],request()["original_text"])
        self.assertEqual(second["request_change"]["previous_request_change_ref"],first["rc_path"])
        self.assertEqual(first["request_change"]["affected_work_ids"],["W-20990101-001"])
        self.assertTrue(first["request_change"]["approval_recheck_required"])

    def test_idempotent_retry_and_collision(self):
        e=event(); first=rc.build_change(request(),e)
        self.assertEqual(rc.build_change(first["request"],e,[first["request_change"]])["status"],"already_recorded")
        with self.assertRaises(ValueError):
            rc.build_change(request(),event(source_excerpt="다른 지시"),[first["request_change"]])
        with self.assertRaises(ValueError):
            rc.build_change(request(),event(source_event_id="different-occurrence"),[first["request_change"]])

    def test_stale_revision_and_content_blocked(self):
        for overrides in ({"before_revision":99},{"before_sha256":"0"*64}):
            with self.assertRaises(ValueError):rc.build_change(request(),event(**overrides))

    def test_missing_and_null_are_distinct(self):
        change=rc.build_change(request(),event(changes={"priority":None}))["request_change"]
        self.assertFalse(change["changed_fields"][0]["before_present"])
        self.assertTrue(change["changed_fields"][0]["after_present"])

    def test_original_identity_and_supersedes_cannot_be_patched(self):
        for key in ("original_text","request_id","requester_actor_id","supersedes","revision","schema_version"):
            with self.assertRaises(ValueError):rc.build_change(request(),event(changes={key:"changed"}))

    def test_cancel_and_replace_record_intent_without_automatic_execution(self):
        for typ in ("cancel","replace"):
            result=rc.build_change(request(),event(change_type=typ,changes={"current_requirements":{"intent":typ}}))
            self.assertEqual(result["request"]["request_status"],"captured")
            self.assertEqual(result["request_change"]["change_type"],typ)

    def test_source_evidence_reason_and_unknown_timestamp(self):
        e=event(changed_at=None,reason_source="source_evidence",change_reason="확인된 자료의 제약",
                reason_evidence_refs=[{"path":"example.md","locator":"제약 절"}])
        change=rc.build_change(request(),e)["request_change"]
        self.assertIsNone(change["changed_at"])
        self.assertIn("변경 발언 시각 미확인",change["unknowns"])
        with self.assertRaises(ValueError):
            rc.build_change(request(),event(reason_source="source_evidence",change_reason="근거 없음"))

    def test_tampering_is_detected(self):
        change=rc.build_change(request(),event())["request_change"]
        change["request_snapshot_after"]["original_text"]="overwritten"
        change["after_sha256"]=rc.digest(change["request_snapshot_after"])
        with self.assertRaises(ValueError):rc.validate_change(change)

    def test_atomic_plan_work_links_decision_unchanged_and_partial_readback(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            def put(p,value):
                f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(rc.text(value) if isinstance(value,dict) else value,encoding="utf-8")
            put("llm-source/ACTOR_REGISTRY.json",{"actors":[{"actor_id":"ACT-001","role":"admin","status":"active"}]})
            put("records/requests/ACT-001/R-20990101-001.json",request())
            put("records/REQUEST_INDEX.md","# Existing index\n")
            put("work/items/W-20990101-001.json",{"id":"W-20990101-001","revision":3,"work_status":"in_progress","approval_status":"approved"})
            put("approvals/D-20990101-001.json",{"decision_id":"D-20990101-001","decision":"approved"})
            decision=(root/"approvals/D-20990101-001.json").read_bytes()
            bundle=rc.plan(root,event(affected_work_ids=["W-20990101-001"],affected_decision_ids=["D-20990101-001"]))
            self.assertEqual(rc.load(root,"records/requests/ACT-001/R-20990101-001.json")["revision"],1)
            self.assertNotIn("approvals/D-20990101-001.json",bundle["files"])
            # Test fixture application simulates complete read-back, not a live Git transaction.
            for p,v in bundle["files"].items():put(p,v)
            self.assertEqual(rc.verify_readback(root,bundle),[])
            self.assertEqual(rc.validate_repository(root),1)
            self.assertEqual((root/"approvals/D-20990101-001.json").read_bytes(),decision)
            w=rc.load(root,"work/items/W-20990101-001.json")
            self.assertEqual(w["work_status"],"in_progress")
            self.assertEqual(w["approval_status"],"approved")
            self.assertEqual(len(w["request_change_refs"]),1)
            (root/"records/REQUEST_CHANGE_INDEX.md").unlink()
            self.assertIn("records/REQUEST_CHANGE_INDEX.md",rc.verify_readback(root,bundle))
            with self.assertRaises(OSError):rc.validate_repository(root)
            with self.assertRaises(OSError):
                rc.plan(root,event(affected_work_ids=["W-20990101-001"],affected_decision_ids=["D-20990101-001"]))


if __name__ == "__main__":unittest.main(verbosity=2)
