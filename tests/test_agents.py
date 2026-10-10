import unittest
from pathlib import Path
from agents import analyze
class Tests(unittest.TestCase):
    def setUp(self):self.source=(Path(__file__).resolve().parents[1]/'sample.csv').read_text()
    def test_demo(self):
        r=analyze(self.source);self.assertEqual(r['summary']['total_kwh'],51);self.assertEqual(r['summary']['estimated_cost'],408);self.assertEqual(len(r['alerts']),1);self.assertEqual(r['actions'][0]['scenario_kwh'],4.1)
    def test_invalid_data(self):
        for source in ('',self.source.replace(',8,4',',-8,4'),self.source.replace(',8,4',',NaN,4'),self.source.replace(',8,4',',8,0')):
            with self.assertRaises(ValueError):analyze(source)
    def test_invalid_settings(self):
        for rate,percent in ((-1,10),(8,51),('NaN',10)):
            with self.assertRaises(ValueError):analyze(self.source,rate,percent)
    def test_duplicate(self):
        with self.assertRaises(ValueError):analyze(self.source+self.source.splitlines()[1]+'\n')
    def test_durations_normalized(self):
        source='timestamp,device,kwh,duration_hours\n2026-01-01,A,2,1\n2026-01-02,A,4,2\n2026-01-03,A,8,4\n'
        self.assertEqual(analyze(source)['alerts'],[])
    def test_zero(self):
        r=analyze('timestamp,device,kwh,duration_hours\n2026-01-01,A,0,1\n');self.assertEqual(r['summary']['total_kwh'],0);self.assertEqual(r['actions'],[])
if __name__=='__main__':unittest.main()
