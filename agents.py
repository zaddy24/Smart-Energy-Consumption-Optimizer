"""Deterministic energy-analysis agents with explicit structured handoffs."""
import csv
import io
import math
from datetime import datetime
from collections import defaultdict

class DataAgent:
    def run(self, source):
        rows=list(csv.DictReader(io.StringIO(source)))
        if not rows or len(rows)>20000: raise ValueError('Provide 1 to 20,000 rows.')
        clean=[];seen=set()
        for i,r in enumerate(rows,2):
            try:
                timestamp=datetime.fromisoformat(r['timestamp'])
                device=r['device'].strip()
                kwh=float(r['kwh']);hours=float(r['duration_hours'])
                if not device or not math.isfinite(kwh) or kwh<0 or not math.isfinite(hours) or hours<=0: raise ValueError()
                key=(device,timestamp.isoformat())
                if key in seen: raise ValueError('Duplicate device and timestamp')
                seen.add(key)
                clean.append({'timestamp':timestamp.isoformat(),'device':device,'kwh':kwh,'duration_hours':hours,'average_kw':kwh/hours})
            except (KeyError,ValueError): raise ValueError(f'Row {i}: supply a valid timestamp, device, nonnegative kwh, and positive duration_hours; duplicates are not allowed.')
        return clean

class ConsumptionAgent:
    def run(self,rows,rate):
        devices=defaultdict(float);daily=defaultdict(float)
        for r in rows: devices[r['device']]+=r['kwh'];daily[r['timestamp'][:10]]+=r['kwh']
        total=sum(devices.values())
        return {'total_kwh':round(total,3),'estimated_cost':round(total*rate,2),'devices':[{'device':k,'kwh':round(v,3),'share_percent':round(v/total*100,1) if total else 0} for k,v in sorted(devices.items(),key=lambda x:x[1],reverse=True)],'daily':[{'date':k,'kwh':round(v,3)} for k,v in sorted(daily.items())]}

class AnomalyAgent:
    def run(self,rows):
        groups=defaultdict(list)
        for r in rows:groups[r['device']].append(r)
        alerts=[]
        for device,records in groups.items():
            for r in records:
                peers=[x['average_kw'] for x in records if x is not r]
                baseline=sum(peers)/len(peers) if peers else None
                if len(peers)>=2 and baseline>0 and r['average_kw']>2*baseline:
                    alerts.append({'device':device,'timestamp':r['timestamp'],'message':f"Average power {r['average_kw']:.2f} kW exceeds twice other readings' mean ({baseline:.2f} kW). Verify the meter and operating conditions."})
        return alerts

class OptimizationAgent:
    def run(self,summary,rate,percent):
        return [{'device':d['device'],'action':'Review operating schedules, idle loads, and efficiency settings. Confirm essential loads before reducing runtime.','scenario_kwh':round(d['kwh']*percent/100,3),'scenario_cost':round(d['kwh']*percent/100*rate,2)} for d in summary['devices'][:3] if d['kwh']>0]

def analyze(source,rate=8,percent=10):
    rate=float(rate);percent=float(percent)
    if not math.isfinite(rate) or rate<0 or not math.isfinite(percent) or not 0<=percent<=50:raise ValueError('Rate must be nonnegative; reduction scenario must be 0–50%.')
    rows=DataAgent().run(source)
    summary=ConsumptionAgent().run(rows,rate)
    alerts=AnomalyAgent().run(rows)
    actions=OptimizationAgent().run(summary,rate,percent)
    return {'summary':summary,'alerts':alerts,'actions':actions,'rate':rate,'scenario_percent':percent,'trace':[f'DataAgent validated {len(rows)} readings','ConsumptionAgent aggregated device and daily usage',f'AnomalyAgent identified {len(alerts)} unusual readings','OptimizationAgent prepared scenarios for the three largest consumers'],'limitations':'Costs use your flat per-kWh rate and exclude fixed charges, taxes, demand charges, and time-of-use tariffs. Scenarios are illustrative reductions for the supplied reporting period, not guaranteed savings or monthly projections. Anomalies compare average kW, not raw kWh; short series and overlapping readings require manual review. No equipment is controlled automatically.'}
