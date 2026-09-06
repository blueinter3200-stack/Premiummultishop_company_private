"""Fixture tests; never create production work, notifications, approvals or network calls."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import decision_flow as f
import work_plans as wp

HEAD = 'a' * 40
R = 'R-20260907-100'
RP = f'records/requests/ACT-002/{R}.json'
W = 'W-20260907-100'
WP = f'work/items/{W}.json'

class Flow(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        self.write('llm-source/ACTOR_REGISTRY.json', {'actors':[
            {'actor_id':f'ACT-00{i}', 'role':r, 'status':'active'}
            for i,r in enumerate(['admin','representative','assistant'],1)]})
        self.request={'schema_version':4, 'request_id':R,'revision':1,'content_revision':1,
            'requester_actor_id':'ACT-002','recorded_by_actor_id':'ACT-002','original_text':'상품 조사 요청',
            'submission_status':'submitted','primary_scope':'work_adoption',
            'requested_scopes':['work_adoption','planning','research','plan_execution'],
            'current_requirements':{'title':'상품 조사','scope':['상품 3개 조사'],'completion_criteria':['비교표 제출']}}
        self.write(RP,self.request)
    def tearDown(self): self.temp.cleanup()
    def write(self,p,o):
        q=self.root/p;q.parent.mkdir(parents=True,exist_ok=True)
        q.write_text(f.dump(o) if not isinstance(o,str) else o,encoding='utf-8')
    def read(self,p):return f.load(self.root,p)
    def save(self,b):
        for p,s in b['files'].items():self.write(p,s)
        f.verify(self.root,b)
    def review(self,obj):return {'result':'PASS','classification':'work','subject_hash':f.digest(f.proposal(obj)),
        'basis_commit':HEAD,'reviewed_by_actor_id':'ACT-001','evidence_refs':['source']}
    def decision(self,obj=None,ref=RP,num=100,outcome='승인',scopes=None,assignment=False):
        obj=obj or self.request;kind,_,rev=f.subject(obj)
        source='승인. 부사수에게 맡겨. 계획안을 제출해. 범위 보완 필요'
        e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-001','operation':'decide',
           'command':'/업무결정' if kind=='request' else '/업무계획안결의','target_ref':ref,
           'target_revision':rev,'target_hash':f.digest(f.proposal(obj)), 'scope_key':obj['primary_scope'],
           'outcome':outcome,'granted_scopes':scopes if scopes is not None else (['work_adoption','planning'] if outcome=='승인' else []),
           'review':self.review(obj),'reason':None if outcome=='승인' else '범위 보완 필요',
           'source':{'text':source,'locator':'current test message'},'source_event_id':f'd-event-{num}',
           'decision_id':f'D-20260907-{num}','decided_at':'2026-09-07','work_id':W}
        if assignment:e['assignment']=self.assignment_spec(num)
        return e
    def assignment_spec(self,num=100,to='ACT-003',previous=None):
        return {'assignment_id':f'ASG-20260907-{num}','assigned_to_actor_id':to,'previous_assignment_id':previous,
            'instruction_text':'계획안을 제출해.','approved_brief':{'title':'상품 조사','scope':['상품 3개 조사']},
            'source':{'text':'부사수에게 맡겨. 계획안을 제출해.','locator':'test actual admin message'},
            'assigned_at':'2026-09-07','source_event_id':f'asg-event-{num}'}
    def adopt(self):
        b=f.plan(self.root,self.decision(assignment=True));self.save(b);return b
    def submission(self,oral=False,rev=1):
        obj={'submission_id':f'SUB-{R}-001','revision':rev,'request_ref':RP,'requester_actor_id':'ACT-002',
             'submitted_by_actor_id':'ACT-003','primary_scope':'plan_execution','requested_scopes':['work_adoption','plan_execution','research'],
             'current_requirements':{'title':'상품 조사 계획','scope':['상품 3개 비교'],'completion_criteria':['비교표 제출']}}
        e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-003','operation':'submit_submission',
           'command':'/업무계획안제출','submission':obj,'artifact_text':'# 실제 계획\n상품 3개를 비교합니다.\n'}
        if oral:
            rp=f'records/requests/ACT-003/R-20260907-101.json';obj['request_ref']=rp
            obj['submission_id']='SUB-R-20260907-101-001'
            r=copy.deepcopy(self.request);r.update(request_id='R-20260907-101',recorded_by_actor_id='ACT-003',
              source_type='reported_oral_request',source_verification='reported_not_independently_verified',
              source_locator='부사수의 구두 전달 설명',captured_at='2026-09-07',related_work_ids=[],related_decision_ids=[])
            e['reported_request']=r
        else:
            obj['work_id']=W;obj['assignment_ref']=f'work/assignments/ASG-20260907-100.json'
        e['review']=self.review(obj);return e
    def update(self,**kw):
        w=self.read(WP)
        e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-003','operation':'update_work',
           'command':'/업무업데이트','work_ref':WP,'expected_revision':w['revision'],'patch':{'next_action':'다음 상품 조사'},
           'progress_source':'실제 확인 내역','performed_by_actor_id':'ACT-003','recorded_at':'2026-09-07','execution_scope':'research'}
        e.update(kw);return e
    def test_oral_plan_direct_before_adoption(self):
        b=f.plan(self.root,self.submission(oral=True));self.save(b)
        self.assertFalse(any(p.startswith('work/items/') for p in b['files']))
        r=self.read('records/requests/ACT-003/R-20260907-101.json')
        self.assertEqual(r['requester_actor_id'],'ACT-002');self.assertEqual(r['recorded_by_actor_id'],'ACT-003')
        self.assertEqual(r['submission_status'],'captured')
        self.assertEqual(r['source_verification'],'reported_not_independently_verified')
    def test_proxy_request_submission_is_not_impersonation(self):
        e=self.submission(oral=True);r=e['reported_request']
        p={'base_commit':HEAD,'actor_id':'ACT-003','operation':'submit_request','command':'/업무요청',
           'write_requested':True,'request':r,'review':self.review(r)}
        b=f.plan(self.root,p);self.save(b)
        self.assertEqual(self.read('records/requests/ACT-003/R-20260907-101.json')['requester_actor_id'],'ACT-002')
    def test_oral_claim_cannot_be_verified_direct(self):
        e=self.submission(oral=True);e['reported_request']['source_verification']='verified'
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_no_access_to_unassigned_rep_request(self):
        e=self.submission();e['submission'].pop('work_id');e['submission'].pop('assignment_ref')
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_read_only_and_no_save_do_not_capture(self):
        for flag in ['read_only','save_prohibited','quoted']:
            e=self.submission(oral=True);e[flag]=True
            self.assertEqual(f.plan(self.root,e)['files'],{})
    def test_representative_cannot_submit_plan(self):
        e=self.submission(oral=True);e['actor_id']='ACT-002'
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_all_retired_names_fail(self):
        for cmd in ['/품의서작성','/품의서결정','/품의서결의','/업무확정','/품의서승인']:
            e=self.submission(oral=True);e['command']=cmd
            with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_request_approval_not_execution_approval(self):
        self.adopt();w=self.read(WP)
        self.assertEqual(w['plan_status'],'not_submitted')
        self.assertEqual(w['assigned_to_actor_id'],'ACT-003')
        with self.assertRaises(ValueError):f.plan(self.root,self.update())
    def test_request_cannot_grant_production(self):
        e=self.decision(scopes=['work_adoption','research'])
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_planning_updates_are_allowed(self):
        self.adopt();b=f.plan(self.root,self.update(phase='planning'));self.assertIn(WP,b['files'])
    def test_planning_cannot_claim_execution(self):
        self.adopt()
        with self.assertRaises(ValueError):f.plan(self.root,self.update(phase='planning',patch={'work_status':'in_progress'}))
    def test_assignment_notifies_only_relevant_people(self):
        b=self.adopt();notes=[json.loads(v) for p,v in b['files'].items() if p.startswith('records/notifications/')]
        staff=[n for n in notes if n['recipient_actor_id']=='ACT-003']
        self.assertEqual(len(staff),1);self.assertEqual(staff[0]['event_type'],'assignment')
        self.assertNotIn('raw_request',staff[0]);self.assertNotIn('request_ref',staff[0])
    def test_self_execution_does_not_assign_assistant(self):
        e=self.decision(scopes=['work_adoption','research']);e.update(execution_mode='self_direct',self_execution_authorized=True,assigned_to_actor_id='ACT-001')
        b=f.plan(self.root,e);self.save(b)
        self.assertEqual(self.read(WP)['assigned_to_actor_id'],'ACT-001')
        self.assertEqual(self.read('records/inbox/ACT-003.json')['unread_count'],0)
        u=self.update(actor_id='ACT-001',performed_by_actor_id='ACT-001');f.plan(self.root,u)
    def test_unassigned_does_not_notify_or_allow_execution(self):
        self.save(f.plan(self.root,self.decision()))
        self.assertIsNone(self.read(WP)['assigned_to_actor_id'])
        self.assertEqual(self.read('records/inbox/ACT-003.json')['unread_count'],0)
        with self.assertRaises(ValueError):f.plan(self.root,self.update(actor_id='ACT-001'))
    def test_later_assignment_creates_one_new_notification(self):
        self.save(f.plan(self.root,self.decision()))
        e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-001','operation':'assign_work','command':'',
            'work_ref':WP,'expected_revision':1,'assignment':self.assignment_spec(101)}
        self.save(f.plan(self.root,e));self.assertEqual(self.read('records/inbox/ACT-003.json')['unread_count'],1)
        e['expected_revision']=self.read(WP)['revision'];self.assertEqual(f.plan(self.root,e)['status'],'already_recorded')
    def test_assignment_changed_event_payload_is_rejected(self):
        self.adopt();e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-001','operation':'assign_work','command':'',
            'work_ref':WP,'expected_revision':self.read(WP)['revision'],'assignment':self.assignment_spec()}
        e['assignment']['approved_brief']['scope']=['다른 업무']
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_assignment_remains_visible_after_notification_delivery(self):
        self.adopt();nid='N-ASG-20260907-100-ACT-003'
        e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-003','operation':'mark_notifications','command':'',
           'displayed':True,'presentation_ref':'actually shown test message','delivered_at':'2026-09-07', 'notification_ids':[nid]}
        self.save(f.plan(self.root,e));self.assertEqual(self.read('records/inbox/ACT-003.json')['unread_count'],0)
        self.assertEqual(len(self.read('records/assignment-views/ACT-003.json')['items']),1)
        self.assertNotIn('acknowledged_at',self.read(f'records/notification-receipts/ACT-003/{nid}.json'))
    def test_fetch_is_not_delivery(self):
        self.adopt();e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-003','operation':'mark_notifications','command':'',
           'displayed':False,'notification_ids':['N-ASG-20260907-100-ACT-003']}
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_plan_approval_allows_scoped_execution(self):
        self.adopt();se=self.submission();self.save(f.plan(self.root,se))
        sp=f"records/submissions/{se['submission']['submission_id']}-r1.json";s=self.read(sp)
        self.save(f.plan(self.root,self.decision(s,sp,101,scopes=['plan_execution','research'])))
        b=f.plan(self.root,self.update());self.assertIn(WP,b['files'])
        with self.assertRaises(ValueError):f.plan(self.root,self.update(execution_scope='production'))
    def test_plan_body_tamper_blocks_execution(self):
        self.adopt();se=self.submission();self.save(f.plan(self.root,se));sp=f"records/submissions/{se['submission']['submission_id']}-r1.json";s=self.read(sp)
        self.save(f.plan(self.root,self.decision(s,sp,101,scopes=['plan_execution','research'])))
        self.write(s['artifact_path'],'CHANGED')
        with self.assertRaises(ValueError):f.plan(self.root,self.update())
    def test_new_plan_version_does_not_inherit_approval(self):
        self.adopt();se=self.submission();self.save(f.plan(self.root,se));sp=f"records/submissions/{se['submission']['submission_id']}-r1.json";s=self.read(sp)
        self.save(f.plan(self.root,self.decision(s,sp,101,scopes=['plan_execution','research'])))
        se2=self.submission(rev=2);se2['artifact_text']='new proposed plan';self.save(f.plan(self.root,se2))
        self.assertEqual(self.read(WP)['execution_plan_ref'],sp)
    def test_reassignment_invalidates_previous_execution_plan(self):
        self.adopt();se=self.submission();self.save(f.plan(self.root,se));sp=f"records/submissions/{se['submission']['submission_id']}-r1.json";s=self.read(sp)
        self.save(f.plan(self.root,self.decision(s,sp,101,scopes=['plan_execution','research'])))
        e={'base_commit':HEAD,'write_requested':True,'actor_id':'ACT-001','operation':'assign_work','command':'',
            'work_ref':WP,'expected_revision':self.read(WP)['revision'],'assignment':self.assignment_spec(102,'ACT-001','ASG-20260907-100')}
        self.save(f.plan(self.root,e));self.assertIsNone(self.read(WP)['execution_plan_ref'])
        self.assertEqual(self.read('records/assignment-views/ACT-003.json')['items'],[])
        self.assertEqual(self.read('records/inbox/ACT-003.json')['items'][0]['event_type'],'assignment_released')
    def test_oral_plan_combined_adoption_and_execution(self):
        e=self.submission(oral=True);self.save(f.plan(self.root,e));sp='records/submissions/SUB-R-20260907-101-001-r1.json';s=self.read(sp)
        de=self.decision(s,sp,101,scopes=['work_adoption','plan_execution','research'],assignment=True)
        self.save(f.plan(self.root,de));self.assertEqual(self.read(WP)['plan_status'],'approved')
        f.plan(self.root,self.update())
    def test_hold_then_approve_without_overwriting(self):
        e=self.decision(outcome='보류');self.save(f.plan(self.root,e));before=(self.root/'approvals/D-20260907-100.json').read_bytes()
        e2=self.decision(num=101,assignment=True);e2['previous_decision_id']='D-20260907-100';self.save(f.plan(self.root,e2))
        self.assertEqual((self.root/'approvals/D-20260907-100.json').read_bytes(),before)
    def test_nonapproval_never_assigns_or_creates_work(self):
        for outcome in ['반려','보류','수정요청']:
            b=f.plan(self.root,self.decision(outcome=outcome,assignment=True))
            self.assertFalse(any(p.startswith(('work/items/','work/assignments/')) for p in b['files']))
    def test_unknown_outcome_has_no_default(self):
        e=self.decision();e.pop('outcome')
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_missing_reason_blocks_nonapproval(self):
        e=self.decision(outcome='반려');e['reason']=None
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_assistant_cannot_decide_or_assign(self):
        e=self.decision();e['actor_id']='ACT-003'
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_stale_review_rejected(self):
        e=self.decision();e['review']['subject_hash']='bad'
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_request_change_invalidates_approval(self):
        self.adopt();r=self.read(RP);r['current_requirements']['scope']=['변경'];self.write(RP,r)
        with self.assertRaises(ValueError):f.plan(self.root,self.update(phase='planning'))
    def test_partial_readback_fails(self):
        b=self.adopt();p=next(iter(b['files']));self.write(p,'{}')
        with self.assertRaises(ValueError):f.verify(self.root,b)

if __name__=='__main__': unittest.main()
