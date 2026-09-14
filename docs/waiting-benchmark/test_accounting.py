import unittest
from accounting import price_response

class AccountingTests(unittest.TestCase):
    def test_disjoint_categories_and_included_reasoning(self):
        value = price_response('gpt-6-astra', {'input_tokens':1000,'cached_input_tokens':600,
            'cache_write_input_tokens':300,'output_tokens':100,'reasoning_output_tokens':80})
        self.assertEqual(value['counts']['uncached'], 100)
        self.assertAlmostEqual(value['total_usd'], .01035)

    def test_long_context_is_per_request(self):
        small = price_response('gpt-5.6-sol', {'input_tokens':272000,'output_tokens':100})
        large = price_response('gpt-5.6-sol', {'input_tokens':272001,'output_tokens':100})
        self.assertFalse(small['long_context'])
        self.assertAlmostEqual(large['total_usd'],272001*8/1000000+100*30/1000000)

    def test_invalid_category_overlap_is_rejected(self):
        with self.assertRaises(AssertionError):
            price_response('gpt-6-astra', {'input_tokens':10,'cached_input_tokens':8,
                'cache_write_input_tokens':5,'output_tokens':1})

if __name__=='__main__':
    unittest.main()
