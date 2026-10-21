import json
from pathlib import Path
import tempfile
import unittest
from intention_grounding.profiler import profile_table


class IngestionTests(unittest.TestCase):
    def test_header_only_boolean_and_unknown_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'empty.csv';p.write_text('date,count\n')
            result=profile_table(p)
            self.assertEqual(['date','count'],result['column_names'])
            self.assertFalse(result['source_metadata']['benchmark_eligible'])
            self.assertIsNone(result['source_metadata']['source_url'])
            p=Path(d)/'flags.json';p.write_text('[{"flag":true},{"flag":false}]')
            self.assertEqual('boolean',profile_table(p)['columns'][0]['observed_type'])
            self.assertNotIn('numeric_statistics',profile_table(p)['columns'][0])

    def test_cache_content_config_metadata_and_explicit_missing(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'t.csv';p.write_text('x\n1\nNA\n')
            a=profile_table(p,cache_dir=Path(d)/'cache')
            self.assertEqual('string',a['columns'][0]['observed_type'])
            self.assertTrue(profile_table(p,cache_dir=Path(d)/'cache')['cache_hit'])
            b=profile_table(p,cache_dir=Path(d)/'cache',missing_tokens=('', 'NA'))
            self.assertNotEqual(a['cache_key'],b['cache_key'])
            self.assertEqual(1,b['columns'][0]['null_count'])
            self.assertEqual('number',b['columns'][0]['observed_type'])
            p.write_text('x\n2\n3\n')
            self.assertNotEqual(a['cache_key'],profile_table(p)['cache_key'])
            self.assertTrue(b['scan']['complete'])

    def test_malformed_csv_is_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'t.csv';p.write_text('x,y\n1,2,3\n')
            with self.assertRaisesRegex(ValueError,'TABLE_PARSE_FAILURE'):
                profile_table(p)
