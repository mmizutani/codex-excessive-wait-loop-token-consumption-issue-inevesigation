"""Guard against accepting a cheap run that did not do the requested work."""
import copy
import json
from pathlib import Path
import unittest
from grade import grade


class GradingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[3]/'docs/waiting-benchmark/numeric-waits/unpatched-results/trial-evidence.json'
        cls.good = next(r for r in json.loads(path.read_text())
            if r['name']=='gpt-6-astra-terminal-wording-no-pragma-r1')

    def record(self):
        r = copy.deepcopy(self.good)
        r.update(eval_case={'id':'implicit-terminal','scenario':'terminal','should_trigger':True},
            skill_loaded_sessions=[r['thread_id']], enabled_skills=['codex-wait-efficiently'],
            global_agents_present=False, fixture_changes=[], artifacts={})
        return r

    def test_finished_run_is_accepted(self):
        self.assertTrue(grade(self.record())['overall_pass'])

    def test_cheap_early_stop_fails_outcome(self):
        r = self.record()
        r['success'] = False
        r['status'] = 'deadline_exceeded'
        self.assertFalse(grade(r)['checks']['outcome'])

    def test_catalog_presence_is_not_activation(self):
        r = self.record()
        r['skill_loaded_sessions'] = []
        self.assertFalse(grade(r)['checks']['activation'])

    def test_no_skill_control_requires_no_loading_in_any_session(self):
        r = self.record()
        r.update(skill_installed=False, skill_loaded_sessions=[], enabled_skills=[])
        self.assertTrue(grade(r)['overall_pass'])
        r['skill_loaded_sessions'] = ['child-session']
        self.assertFalse(grade(r)['checks']['activation'])

    def test_no_skill_control_rejects_enabled_skill_or_agents_patch(self):
        r = self.record()
        r.update(skill_installed=False, skill_loaded_sessions=[])
        self.assertFalse(grade(r)['checks']['isolated_skill'])
        r.update(enabled_skills=[], global_agents_present=True)
        self.assertFalse(grade(r)['checks']['isolated_skill'])

    def test_extra_status_query_fails_bound(self):
        r = self.record()
        r['eval_case'].update(id='negative-one-status',fixture='pending',scenario='ci',should_trigger=False)
        r['ci_checks'] = [{'done':False},{'done':False}]
        self.assertFalse(grade(r)['checks']['status_query_bound'])

    def test_success_cannot_stand_in_for_failure_handling(self):
        r = self.record()
        r['eval_case']['fixture'] = 'failure'
        self.assertFalse(grade(r)['checks']['outcome'])


if __name__ == '__main__':
    unittest.main()
