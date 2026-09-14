import unittest

from judge import review_output


class ReviewEvidenceTests(unittest.TestCase):
    def test_skill_read_does_not_hide_a_status_from_the_same_code_mode_call(self):
        original = {'call_id':'mixed-call', 'output':[
            {'type':'input_text','text':'Script completed'},
            {'type':'input_text','text':'Longer waits may not reduce usage; add no cache-only keepalives without measured savings.'},
            {'type':'input_text','text':'{"run_id":"job-7391","status":"running"}'}]}
        reduced = review_output(original)
        self.assertEqual(reduced['output'][2],original['output'][2])
        self.assertEqual(reduced['call_id'],'mixed-call')
        self.assertNotIn('keepalives',str(reduced))
        self.assertIn('keepalives',str(original))


if __name__ == '__main__':
    unittest.main()
