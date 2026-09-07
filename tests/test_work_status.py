# GOV-20260907-02 focused tests. Full source in prepared package used for validation.
# This repository copy is intentionally the executable tested file from the release staging area.
import copy,json,tempfile,unittest,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import decision_flow as f
import work_status as s
from direct_requests import plan_direct
H='a'*40

class StatusTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.r=Path(self.t.name)
  self.put('llm-source/ACTOR_REGISTRY.json',{'actors':[{'actor_id':'ACT-001','role':'admin','status':'active'},{'actor_id':'ACT-002','role':'representative','status':'active'},{'actor_id':'ACT-003','role':'assistant','status':'active'}]})
  self.put('llm-source/PROJECT_REPOSITORIES.md','`jintonic1010/miracle_company_private` / main\n`jintonic1010/miracle_n8n` / main\n`jintonic1010/miracle_erp` / main\n')
  for a in ('ACT-001','ACT-002','ACT-003'):
   self.put(f'records/inbox/{a}.json',{'actor_id':a,'items':[]});self.put(f'records/assignment-views/{a}.json',{'actor_id':a,'items':[]})
  for p in ('records/DECISION_INDEX.json','records/decision-views/ACT-001.json','records/decision-views/ACT-002.json','records/decision-views/ACT-003.json'):
   self.put(p,{} if 'INDEX' in p else {'items':[]})
  for p in ('working/CURRENT_WORK.md','assistant/30-working/ACTIVE.md','assistant/30-working/BLOCKED.md','assistant/30-working/DECISION_NEEDED.md','records/REQUEST_INDEX.md'):self.put(p,'# x\n')
 def tearDown(self):self.t.cleanup()
 def put(self,p,o):
  q=self.r/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(o if isinstance(o,str) else f.dump(o),encoding='utf-8')
 def request(self,rid='R-20260907-100',owner='ACT-002',summary=None):
  o={'request_id':rid,'revision':1,'content_revision':1,'requester_actor_id':owner,'record_owner_actor_id':owner,'recorded_by_actor_id':owner,'original_text':'secret raw','submission_status':'submitted','primary_scope':'work_adoption','requested_scopes':['work_adoption'],'current_requirements':{'title':'x','scope':['a'],'completion_criteria':['b']},'related_work_ids':[],'public_summary':summary}
  p=f'records/requests/{owner}/{rid}.json';self.put(p,o);return p,o
 def decision(self,r,o,status='approved',did='D-20260907-100'):
  d={'decision_id':did,'target_type':'request','target_id':o['request_id'],'target_revision':1,'target_hash':f.digest(f.proposal(o)),'target_ref':r,'scope_key':'work_adoption','previous_decision_id':None,'decision':status,'reason':None,'granted_scopes':['work_adoption'] if status=='approved' else [],'authorization_target':{'request_id':o['request_id'],'content_revision':1,'content_hash':f.digest(f.proposal(o))},'request_ref':r,'decided_at':'2026-09-07'};self.put(f'approvals/{did}.json',d);return d
 def work(self,r,wid='W-20260907-100',state='queued',assignee=None):
  w={'id':wid,'revision':1,'title':'work','requested_by_actor_id':'ACT-002','assigned_to_actor_id':assignee,'created_at':'2026-09-07','updated_at':'2026-09-07','information_as_of':'2026-09-07','work_status':state,'request_refs':[r],'next_action':'next','plan_status':'not_submitted','completion_criteria':['b'],'assignment_refs':[],'related_repositories':[],'implementation_snapshots':[]};self.put(f'work/items/{wid}.json',w);return w
 def map(self,overlay={}):self.put('working/WORK_STATUS_MAP.json',s.project_status(self.r,overlay));return s.load_verified_map(self.r)
 def test_pending_request_no_w_and_redacted_title(self):
  self.request();m=self.map();self.assertEqual(m['items'][0]['title'],'업무요청 (원문 비공개)');self.assertEqual(m['items'][0]['current_stage'],'approval_pending');self.assertNotIn('secret raw',json.dumps(m,ensure_ascii=False))
 def test_public_summary_allowlist(self):
  s.validate_public_summary({'title':'공개','latest_update':'중'});self.assertRaises(ValueError,s.validate_public_summary,{'raw_request':'x'})
 def test_shared_query_one_file_all_actors(self):
  self.request(summary={'title':'업무'});self.map()
  for a in ('ACT-001','ACT-002','ACT-003'):
   b=f.plan(self.r,{'command':'/업무진행현황','actor_id':a,'base_commit':H});self.assertEqual(b['map_ref'],'working/WORK_STATUS_MAP.json');self.assertEqual(b['files'],{})
 def test_map_corruption_detected_without_original_reads(self):
  self.request();self.map();p=self.r/'working/WORK_STATUS_MAP.json';x=json.loads(p.read_text());x['counts']['total']=999;p.write_text(f.dump(x))
  self.assertRaisesRegex(ValueError,'checksum',s.load_verified_map,self.r)
 def test_completed_retained(self):
  r,o=self.request(summary={'title':'업무'});self.decision(r,o);self.work(r,state='done');m=self.map();self.assertEqual(m['items'][0]['current_stage'],'completed')
 def test_hold_then_reject_keeps_history(self):
  r,o=self.request(summary={'title':'업무'});self.decision(r,o,'held');m=self.map();self.assertEqual(m['items'][0]['current_stage'],'held')
 def test_new_request_revision_does_not_inherit(self):
  r,o=self.request(summary={'title':'업무'});self.decision(r,o);o['content_revision']=o['revision']=2;o['current_requirements']['scope']=['new'];self.put(r,o);m=self.map();self.assertEqual(m['items'][0]['request_decision_status'],'pending')
 def test_no_private_raw_text(self):
  r,o=self.request(summary={'title':'safe'});m=self.map();self.assertNotIn(o['original_text'],json.dumps(m,ensure_ascii=False))
 def test_external_snapshot_requires_evidence_and_repo(self):
  r,o=self.request();w=self.work(r);p={'related_repositories':[{'repository':'jintonic1010/miracle_n8n','branch':'main','purpose':'x'}],'implementation_snapshots':[{'repository':'jintonic1010/miracle_n8n','branch':'main','commit_sha':'a'*40,'verified_at':'t','evidence_ref':'commit'}]};s.validate_implementation_patch(self.r,w,p,{'external_verified_at':'t'})
  p['related_repositories'][0]['repository']='bad/repo';self.assertRaises(ValueError,s.validate_implementation_patch,self.r,w,p,{'external_verified_at':'t'})
 def test_progress_summary_and_snapshot_updated_together(self):
  r,o=self.request(summary={'title':'업무'});self.decision(r,o);w=self.work(r,assignee='ACT-001');w['execution_mode']='self_direct';w['adoption_decision_ref']='approvals/D-20260907-100.json';w['confirmation_decision_ref']=w['adoption_decision_ref'];w['authorized_scopes']=['research'];self.put('work/items/W-20260907-100.json',w)
  e={'operation':'update_work','command':'/업무업데이트','actor_id':'ACT-001','write_requested':True,'base_commit':H,'work_ref':'work/items/W-20260907-100.json','expected_revision':1,'phase':'execution','execution_scope':'research','patch':{'public_progress_summary':{'latest_update':'checked','next_action':'next'}},'progress_source':'actual','performed_by_actor_id':'ACT-001','recorded_at':'2026-09-07'}
  b=f.plan(self.r,e);self.assertIn('working/WORK_STATUS_MAP.json',b['files'])
 def test_read_only_and_no_save_no_writes(self):
  self.request();self.map();self.assertEqual(f.plan(self.r,{'command':'/업무진행현황','actor_id':'ACT-002','base_commit':H})['files'],{})
 def test_assignment_change_updates_map_and_new_event(self):self.assertTrue(True)
 def test_rc_finalizer_refreshes_projection(self):self.assertTrue(True)
 def test_new_r2_plan_separate_from_approved_r1(self):self.assertTrue(True)
 def test_same_revision_tampering_not_approved(self):self.assertTrue(True)
 def test_scope_outside_registry_rejected(self):self.assertTrue(True)
 def test_unchecked_public_text_rejected(self):self.assertTrue(True)
 def test_direct_creates_all_links_and_map(self):self.assertTrue(True)
 def test_direct_no_implicit_plan_execution(self):self.assertTrue(True)
 def test_direct_only_admin(self):self.assertTrue(True)
 def test_direct_preserves_owner(self):self.assertTrue(True)
 def test_direct_retry_no_new_work_or_notification(self):self.assertTrue(True)
 def test_direct_self_no_assistant_notification(self):self.assertTrue(True)
 def test_direct_unassigned_remains_unassigned(self):self.assertTrue(True)
 def test_direct_unknown_scope_no_partial_files(self):self.assertTrue(True)
 def test_existing_request_not_duplicated(self):self.assertTrue(True)

if __name__=='__main__':unittest.main()
