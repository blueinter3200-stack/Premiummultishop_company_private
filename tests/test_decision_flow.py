"""Current regression suite. Superseded GOV-05 assertions are preserved under archive/test-snapshots."""
import copy
import json
from test_work_plans import RP, WP, W, HEAD
import test_work_plans as fixture
import decision_flow as f

class Decisions(fixture.Flow):
    # Reuse fixture helpers without running the inherited tests twice.
    def test_duplicate_decision_event(self):
        e=self.decision(assignment=True);self.save(f.plan(self.root,e))
        self.assertEqual(f.plan(self.root,e)['status'],'already_recorded')
    def test_same_hold_is_not_another_notification(self):
        self.save(f.plan(self.root,self.decision(outcome='보류')))
        e=self.decision(num=101,outcome='보류');e['previous_decision_id']='D-20260907-100'
        self.assertEqual(f.plan(self.root,e)['status'],'unchanged')
    def test_decision_branch_conflict(self):
        d=f.make_decision(self.request,self.decision(outcome='보류'),[])['decision']
        d2=copy.deepcopy(d);d2['decision_id']='D-20260907-101'
        with self.assertRaises(ValueError):f.latest([d,d2],f.chain_key(d))
    def test_nonapproval_cannot_grant_execution(self):
        with self.assertRaises(ValueError):f.plan(self.root,self.decision(outcome='보류',scopes=['research']))
    def test_hold_to_reject_keeps_original(self):
        self.save(f.plan(self.root,self.decision(outcome='보류')))
        before=(self.root/'approvals/D-20260907-100.json').read_bytes()
        e=self.decision(num=101,outcome='반려');e['previous_decision_id']='D-20260907-100';self.save(f.plan(self.root,e))
        self.assertEqual((self.root/'approvals/D-20260907-100.json').read_bytes(),before)
        self.assertEqual(self.read('records/inbox/ACT-002.json')['unread_count'],1)
    def test_approval_revocation_needs_explicit_reason(self):
        self.adopt();e=self.decision(num=101,outcome='보류');e['previous_decision_id']='D-20260907-100'
        with self.assertRaises(ValueError):f.plan(self.root,e)
        e.update(revoke_previous=True,change_reason='업무 중단');self.save(f.plan(self.root,e))
        with self.assertRaises(ValueError):f.plan(self.root,self.update(phase='planning'))
    def test_request_original_is_not_changed_by_decision(self):
        before=(self.root/RP).read_bytes();self.adopt();self.assertEqual((self.root/RP).read_bytes(),before)
    def test_read_only_receipt_never_writes(self):
        self.adopt();e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-003','operation':'mark_notifications',
            'command':'/업무검토','displayed':True,'presentation_ref':'display','delivered_at':'2026-09-07',
            'notification_ids':['N-ASG-20260907-100-ACT-003']}
        self.assertEqual(f.plan(self.root,e)['files'],{})
    def test_human_ack_needs_human_source(self):
        self.adopt();e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-003','operation':'mark_notifications',
            'command':'','displayed':True,'presentation_ref':'display','delivered_at':'2026-09-07',
            'notification_ids':['N-ASG-20260907-100-ACT-003'],'acknowledged':True}
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_no_network_or_file_writes_by_planner(self):
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        f.plan(self.root,self.decision(assignment=True))
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
    def test_plan_cannot_silently_override_held_request(self):
        self.save(f.plan(self.root,self.decision(outcome='보류')))
        # A proxy-own request can be planned, but prior administrator hold remains a gate.
        r=self.read(RP);r['recorded_by_actor_id']='ACT-003';self.write(RP,r)
        e=self.submission();e['submission'].pop('work_id');e['submission'].pop('assignment_ref')
        self.save(f.plan(self.root,e));sp=f"records/submissions/{e['submission']['submission_id']}-r1.json";s=self.read(sp)
        de=self.decision(s,sp,101,scopes=['work_adoption','plan_execution','research'],assignment=True)
        with self.assertRaises(ValueError):f.plan(self.root,de)

for _name in dir(fixture.Flow):
    if _name.startswith("test_") and _name not in Decisions.__dict__:
        setattr(Decisions, _name, None)
