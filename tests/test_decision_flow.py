import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import decision_flow as f

H='a'*40
class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.actors=[dict(actor_id=f'ACT-00{i}',role=r,status='active') for i,r in enumerate(['admin','representative','assistant'],1)]
        self.put('llm-source/ACTOR_REGISTRY.json',{'actors':self.actors})
        self.req=dict(schema_version=3,request_id='R-20260906-010',requester_actor_id='ACT-002',revision=1,content_revision=1,
          title='조사 요청',original_text='상품 조사',submission_status='submitted',primary_scope='work_start',requested_scopes=['work_start','research'],
          current_requirements={'title':'조사 요청','scope':['상품 조사'],'completion_criteria':['근거 보고서']},related_work_ids=[])
        self.rp='records/requests/ACT-002/R-20260906-010.json';self.put(self.rp,self.req)
    def tearDown(self):self.tmp.cleanup()
    def put(self,p,o):
        q=self.root/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(f.dump(o) if not isinstance(o,str) else o,encoding='utf-8')
    def event(self,outcome='승인',num=10,prior=None):
        return dict(operation='decide',write_requested=True,actor_id='ACT-001',command='/업무결정',outcome=outcome,decision_id=f'D-20260906-{num:03d}',
          target_ref=self.rp,target_revision=1,target_hash=f.digest(f.proposal(self.req)),base_commit=H,
          scope_key='work_start',previous_decision_id=prior,reason=None if outcome=='승인' else '예산 확인 필요',
          source={'text':'이 범위로 결정한다. 예산 확인 필요','locator':'test only'},source_event_id=f'test-{num}',decided_at='2026-09-06T23:00:00+09:00',
          granted_scopes=['work_start','research'] if outcome=='승인' else [],conditions=[],work_id='W-20260906-010',assigned_to_actor_id='ACT-003',
          review={'result':'PASS','classification':'work','subject_hash':f.digest(f.proposal(self.req)),'basis_commit':H,'reviewed_by_actor_id':'ACT-001','evidence_refs':[]})
    def apply(self,b):
        for p,t in b['files'].items():self.put(p,t)
        f.verify(self.root,b)
    def test_hold_creates_no_work(self):
        b=f.plan(self.root,self.event('보류'));self.assertFalse(any(p.startswith('work/items/') for p in b['files']))
    def test_approval_creates_one_work(self):
        b=f.plan(self.root,self.event());self.assertEqual(sum(p.startswith('work/items/') for p in b['files']),1)
        w=json.loads(b['files']['work/items/W-20260906-010.json']);self.assertEqual(w['work_status'],'queued')
    def test_notification_to_requester_and_assignee_not_admin(self):
        b=f.plan(self.root,self.event());p=[p for p in b['files'] if p.startswith('records/notifications/')]
        self.assertEqual(len(p),2);self.assertTrue(all('/ACT-001/' not in x for x in p))
    def test_hold_to_approval_keeps_decisions(self):
        a=f.plan(self.root,self.event('보류'));self.apply(a);b=f.plan(self.root,self.event('승인',11,'D-20260906-010'));self.apply(b)
        self.assertEqual(len(list((self.root/'approvals').glob('*.json'))),2)
        inbox=f.load(self.root,'records/inbox/ACT-002.json');self.assertEqual(inbox['unread_count'],1)
        self.assertEqual(inbox['items'][0]['previous_state'],'held');self.assertEqual(inbox['items'][0]['decision'],'approved')
    def test_hold_to_rejection_no_work(self):
        self.apply(f.plan(self.root,self.event('보류')));b=f.plan(self.root,self.event('반려',11,'D-20260906-010'))
        self.assertFalse(any(p.startswith('work/items/') for p in b['files']))
        self.assertEqual(json.loads(b['files']['records/decision-views/ACT-002.json'])['items'][0]['status'],'rejected')
    def test_same_event_is_idempotent(self):
        e=self.event();self.apply(f.plan(self.root,e));b=f.plan(self.root,e);self.assertEqual(b['status'],'already_recorded')
    def test_same_decision_no_new_notification(self):
        self.apply(f.plan(self.root,self.event('보류')));b=f.plan(self.root,self.event('보류',11,'D-20260906-010'));self.assertEqual(b['status'],'unchanged')
    def test_reused_event_key_changed_content_rejected(self):
        e=self.event('보류');self.apply(f.plan(self.root,e));e['reason']='다른 이유'
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_partial_delivery_not_false_success(self):
        e=self.event();b=f.plan(self.root,e);self.apply(b)
        p=next(p for p in b['files'] if p.startswith('records/notifications/'));(self.root/p).unlink()
        with self.assertRaisesRegex(ValueError,'Partial'):f.plan(self.root,e)
    def test_old_commands_rejected(self):
        for cmd in f.RETIRED:
            with self.subTest(cmd=cmd):
                e=self.event();e['command']=cmd
                with self.assertRaisesRegex(ValueError,'RETIRED'):f.plan(self.root,e)
    def test_all_readonly_no_writes(self):
        for cmd in f.READ_ONLY:
            e=self.event();e['command']=cmd;self.assertEqual(f.plan(self.root,e)['files'],{})
    def test_no_save_and_quoted_no_writes(self):
        for field in ['save_prohibited','quoted','read_only']:
            e=self.event();e[field]=True;self.assertEqual(f.plan(self.root,e)['files'],{})
    def test_representative_assistant_cannot_decide(self):
        for aid in ['ACT-002','ACT-003']:
            e=self.event();e['actor_id']=aid
            with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_missing_outcome_not_approval(self):
        e=self.event();e.pop('outcome')
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_missing_nonapproval_reason_rejected(self):
        e=self.event('반려');e['reason']=None
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_nonapproval_never_grants_scopes(self):
        e=self.event('보류');e['granted_scopes']=['work_start']
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_stale_review_and_revision(self):
        for key,value in [('target_revision',2),('target_hash','bad')]:
            e=self.event();e[key]=value
            with self.assertRaises(ValueError):f.plan(self.root,e)
        e=self.event();e['review']['basis_commit']='b'*40
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_conflicting_branch_rejected(self):
        d=f.make_decision(self.req,self.event('보류'),[])['decision'];a=copy.deepcopy(d);a['decision_id']='D-20260906-011'
        with self.assertRaises(ValueError):f.latest([d,a],f.chain_key(d))
    def test_original_not_modified_by_decision(self):
        before=(self.root/self.rp).read_bytes();self.apply(f.plan(self.root,self.event('보류')));self.assertEqual(before,(self.root/self.rp).read_bytes())
    def test_revision_r2_does_not_inherit_r1(self):
        self.apply(f.plan(self.root,self.event('반려')));r=copy.deepcopy(self.req);r['revision']=r['content_revision']=2;r['current_requirements']['scope']=['보완된 조사'];self.put(self.rp,r)
        views=f.render(self.root,{},self.actors);self.assertEqual(json.loads(views['records/decision-views/ACT-002.json'])['items'][0]['status'],'pending')
        self.assertEqual(json.loads(views['records/inbox/ACT-002.json'])['unread_count'],0)
    def test_approved_change_requires_revocation(self):
        self.apply(f.plan(self.root,self.event()));e=self.event('보류',11,'D-20260906-010')
        with self.assertRaises(ValueError):f.plan(self.root,e)
        e.update(revoke_previous=True,change_reason='착수 중단');b=f.plan(self.root,e);self.assertEqual(json.loads(b['files']['work/items/W-20260906-010.json'])['work_status'],'blocked')
    def test_rejected_reopen_requires_reason(self):
        self.apply(f.plan(self.root,self.event('반려')));e=self.event('승인',11,'D-20260906-010')
        with self.assertRaises(ValueError):f.plan(self.root,e)
        e['reopen_reason']='예산 확인 완료';self.assertEqual(f.plan(self.root,e)['status'],'planned')
    def test_submit_requires_review_no_work(self):
        r=copy.deepcopy(self.req);r['revision']=2;e=dict(operation='submit_request',command='/업무요청',actor_id='ACT-002',write_requested=True,base_commit=H,request=r)
        with self.assertRaises(ValueError):f.plan(self.root,e)
        e['review']=self.event()['review'];b=f.plan(self.root,e);self.assertFalse(any(p.startswith('work/items/') for p in b['files']))
    def test_prework_submission_no_w(self):
        sub=dict(submission_id='SUB-R-20260906-010-001',revision=1,request_ref=self.rp,submitted_by_actor_id='ACT-003',work_id=None,primary_scope='work_start',requested_scopes=['work_start','research'],current_requirements=f.proposal(self.req))
        e=dict(operation='submit_submission',command='/품의서작성',actor_id='ACT-003',write_requested=True,base_commit=H,submission=sub,review=self.event()['review'],artifact_text='# 실제 초안\n')
        b=f.plan(self.root,e);self.assertFalse(any(p.startswith('work/items/') for p in b['files']));self.apply(b)
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_only_assigned_actor_updates(self):
        self.apply(f.plan(self.root,self.event()));w=f.load(self.root,'work/items/W-20260906-010.json')
        e=dict(operation='update_work',command='/업무업데이트',actor_id='ACT-002',write_requested=True,base_commit=H,work_ref='work/items/W-20260906-010.json',expected_revision=w['revision'],patch={'work_status':'in_progress'},progress_source='수행 보고',performed_by_actor_id='ACT-003',recorded_at='2026-09-06')
        with self.assertRaises(ValueError):f.plan(self.root,e)
        e['actor_id']='ACT-003';self.assertEqual(f.plan(self.root,e)['status'],'planned')
    def test_fetch_not_delivery_and_readonly_receipt(self):
        self.apply(f.plan(self.root,self.event('보류')));nid='N-D-20260906-010-ACT-002'
        e=dict(operation='mark_notifications',actor_id='ACT-002',write_requested=True,base_commit=H,notification_ids=[nid],delivered_at='2026-09-06')
        with self.assertRaises(ValueError):f.plan(self.root,e)
        e.update(displayed=True,presentation_ref='assistant message',read_only=True);self.assertEqual(f.plan(self.root,e)['files'],{})
        e['read_only']=False;b=f.plan(self.root,e);self.apply(b);self.assertEqual(f.load(self.root,'records/inbox/ACT-002.json')['unread_count'],0)
        self.assertNotIn('acknowledged_at',f.load(self.root,f'records/notification-receipts/ACT-002/{nid}.json'))
    def test_ack_requires_actual_user_source(self):
        self.apply(f.plan(self.root,self.event('보류')))
        e=dict(operation='mark_notifications',actor_id='ACT-002',write_requested=True,base_commit=H,notification_ids=['N-D-20260906-010-ACT-002'],delivered_at='2026-09-06',displayed=True,presentation_ref='display',acknowledged=True)
        with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_submission_approval_updates_request_view_and_not_duplicate_work(self):
        self.apply(f.plan(self.root,self.event('보류')))
        sub=dict(submission_id='SUB-R-20260906-010-001',revision=1,request_ref=self.rp,submitted_by_actor_id='ACT-003',work_id=None,primary_scope='work_start',requested_scopes=['work_start','research'],current_requirements=f.proposal(self.req))
        se=dict(operation='submit_submission',command='/품의서작성',actor_id='ACT-003',write_requested=True,base_commit=H,submission=sub,review=self.event()['review'],artifact_text='# 실제 계획\n')
        self.apply(f.plan(self.root,se));e=self.event('승인',11,'D-20260906-010')
        e.update(command='/품의서결정',target_ref='records/submissions/SUB-R-20260906-010-001-r1.json')
        b=f.plan(self.root,e);self.apply(b)
        view=f.load(self.root,'records/decision-views/ACT-002.json')['items']
        req=next(x for x in view if x['target_type']=='request');self.assertEqual(req['status'],'approved')
        self.assertEqual(len(list((self.root/'work/items').glob('*.json'))),1)
        self.assertEqual(f.load(self.root,'records/inbox/ACT-002.json')['unread_count'],1)
        sv=f.load(self.root,'records/decision-views/ACT-003.json')['items']
        self.assertEqual(next(x for x in sv if x['target_type']=='submission')['status'],'approved')
        sub['revision']=2;se['artifact_text']='# 새 상세 계획\n';self.apply(f.plan(self.root,se))
        sv=f.load(self.root,'records/decision-views/ACT-003.json')['items']
        self.assertEqual(next(x for x in sv if x['target_type']=='submission')['status'],'pending')
    def test_publication_and_expenditure_need_details(self):
        self.req['requested_scopes']+=['publication','expenditure'];self.put(self.rp,self.req)
        for scope in ['publication','expenditure']:
            e=self.event();e['granted_scopes'].append(scope)
            with self.assertRaises(ValueError):f.plan(self.root,e)
    def test_verify_detects_partial_write(self):
        b=f.plan(self.root,self.event('보류'));self.apply(b);(self.root/'records/inbox/ACT-002.json').write_text('{}')
        with self.assertRaises(ValueError):f.verify(self.root,b)
    def test_no_background_or_file_writes_by_plan(self):
        before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()};f.plan(self.root,self.event())
        after={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()};self.assertEqual(before,after)

if __name__=='__main__':unittest.main()
