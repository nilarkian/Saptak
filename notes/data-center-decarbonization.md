---
topic: data-center-decarbonization
is_note: true
layout: note-layout
date: 2026-06-07
title: The Data Center Is Not Decarbonized. It Is Accounted For.
---

# The Data Center Is Not Decarbonized. It Is Accounted For.

### The three architecture decisions that determine real carbon outcomes — and why procurement changes none of them.

---

Your sustainability report says 100% renewable energy. Your data center ran on gas peaker plants at 2am.

This is not hypocrisy. It is a structural measurement problem. Annual renewable energy certificates match consumption on paper across a calendar year. They do not change what the grid delivers to your facility at 3am in December, when renewable generation is low and peaker plants are running at capacity.

The gap between what annual matching reports and what real-time operations require is where the next decade of infrastructure investment will be decided.

You are decarbonizing your data center or you are accounting for it. The difference is not visible in your sustainability report. It is visible in your per-hour grid carbon draw.

---

## Annual RECs satisfy auditors. They do not move the carbon needle.

REC Accounting Theater is the practice of purchasing annual renewable energy certificates that satisfy disclosure frameworks while leaving per-hour grid carbon dependency unchanged.

The mechanics are simple. A company buys certificates representing renewable generation somewhere on the grid — wind in Texas, solar in Arizona — and matches that quantity to annual electricity consumption. The sustainability report reads "100% renewable energy." The regulatory filing is clean. The grid draw at 2am is unchanged: whatever the grid is generating at that hour, that is what the facility is consuming.

This is not fraud. Annual RECs are a financial instrument for supporting renewable generation investment. They are not an operational tool for managing hourly carbon draw. The industry conflated the two, and that conflation is what REC Accounting Theater names precisely.

The scale of the gap shows up in a single comparison. Google's 2023 average Power Usage Effectiveness reached 1.10, against an industry average of 1.58. That delta reflects cooling architecture and workload scheduling, not energy procurement strategy. Google did not buy its way to a PUE of 1.10. It engineered it.

REC Accounting Theater does not change PUE. It does not change where a facility sits on the grid. It does not change when workloads run. Three architecture variables determine real carbon outcomes. Procurement addresses none of them.

There is a structural reason annual REC matching persists: reporting frameworks are built around annual aggregation. RE100 and most disclosure standards accept annual matching as compliance. The problem is resolution, not intent. Dirty-grid dependency hides inside annual figures precisely because the reporting interval is 8,760 times coarser than the grid interval.

That resolution gap is what the next generation of infrastructure decisions must close.

---

## The 24/7 CFE gap is where the dirty hours hide.

The 24/7 CFE Gap is the difference between what annual renewable matching reports and what per-hour carbon-free energy alignment requires — the invisible interval where dirty-grid dependency hides.

Google operationalized the distinction. Its Carbon-Aware Computing methodology tracks grid carbon intensity in real time, by hour and by region. Flexible workloads route toward windows with lower carbon intensity: geographic dispatch during peak renewable hours, temporal deferral during overnight carbon-intensive periods. The result is a facility that draws less carbon not through different procurement, but through different scheduling. I have watched infrastructure teams spend six months negotiating a PPA and three weeks dismissing the scheduling work. The carbon math does not care about the negotiation.

This requires capabilities that procurement cannot deliver: workload observability, grid API integration, and scheduling systems that treat carbon intensity as a dispatch signal alongside cost and priority. It is not a finance function. It is an architecture function.

California solar curtailment makes the gap concrete. California generates surplus solar during midday grid imbalance — energy wasted because the grid cannot absorb it. Data centers with daytime Power Purchase Agreements claim that solar generation. At night, those same facilities draw from gas peaker plants. Annual report: renewable. Hourly reality: carbon-intensive from 7pm to 6am.

The 24/7 CFE Gap cannot be closed with a better procurement contract. It closes when scheduling systems treat the hourly carbon profile of the grid as an operational variable.

| | Annual REC Matching | 24/7 CFE Alignment |
|---|---|---|
| What it reports | Total consumption vs. total renewable certificates | Per-hour carbon intensity vs. per-hour clean generation |
| What it conceals | Hourly grid dependency, regional carbon intensity variance | Nothing — it reports at the same resolution the grid operates |
| Disclosure standard | Satisfies RE100 and most sustainability frameworks | Google's methodology; no universal standard yet |
| Operational requirement | Certificate purchase | Grid API integration, real-time workload scheduling |
| Who can achieve it | Any organization with a procurement budget | Organizations with workload observability and flexible compute |
| 24/7 CFE Gap measurement | Requires per-hour metering against regional grid data | Built into the methodology |

Carbon-Aware Scheduling is the mechanism that closes the 24/7 CFE Gap. It is an infrastructure capability, not a procurement one. Building it requires the right architecture decisions upstream.

---

## Three variables determine real carbon outcomes. Procurement changes none of them.

Annual REC matching is a procurement decision. Siting, cooling architecture, and workload scheduling are architecture decisions. The first changes what you report. The three that follow change what you emit.

Infrastructure architects one step behind the hyperscaler playbook are typically working procurement and efficiency levers — renewable contracts, PUE optimization — while the three architecture variables stay unaddressed in their facilities roadmap. That gap is structural. Closing it requires treating decarbonization as a systems-design problem, not a sourcing problem.

### Siting as Carbon Strategy: location decides your carbon ceiling before a server is racked.

Siting as Carbon Strategy means treating data center geographic location — proximity to renewable generation sources, water availability, grid carbon intensity profiles — as a primary infrastructure decision variable, not a secondary real estate consideration.

Conventional siting prioritizes latency, land cost, and fiber connectivity. Carbon intensity of the local grid enters late, if at all. This order of operations locks in a structural carbon constraint that no subsequent efficiency investment can overcome. A facility built in a high-carbon-intensity grid region will draw dirty power at peak hours regardless of PUE rating, REC purchases, or cooling architecture.

Once the location is chosen, Siting as Carbon Strategy has already been decided, in either direction.

The variables that determine carbon outcomes at the facility level:

- Grid carbon intensity profile by hour — not annual average; the overnight and peak-demand profile is what matters
- Proximity to renewable generation — transmission distance affects curtailment rates and actual carbon attribution
- Water availability — water-scarce regions impose regulatory constraints on evaporative cooling, limiting architecture options
- Curtailment rates in the region — high curtailment signals surplus renewable generation available at low effective carbon cost
- Grid interconnection and storage buildout — forward indicator of clean energy availability over a 5-10 year horizon

Siting as Carbon Strategy reframes the decision from "where is land cheap and fiber available" to "where does the hourly carbon profile of the grid create structural advantage for our workload mix." That siting decision locks in for 15-20 years. It cannot be undone by a procurement contract.

The teams I have seen get this wrong did not make a bad siting decision. They made no siting decision at all — they made a real estate decision and called it done. Those facilities are now locked into grid carbon profiles that no amount of REC purchasing can fix.

### The Cooling Density Ceiling: air cooling cannot serve GPU-dense workloads.

The Cooling Density Ceiling is the point — roughly 50kW per rack — at which air cooling infrastructure can no longer serve modern GPU workload density, requiring architectural replacement rather than incremental optimization.

Air cooling has a physical limit. At rack densities above 50kW, the airflow volumes and temperature differentials required exceed what conventional Computer Room Air Conditioning systems can deliver without facility modification. For enterprise workloads through 2022, this limit was largely theoretical. GPU-dense AI training and inference workloads have made it operational reality, fast.

The numbers leave no room for interpretation. An NVIDIA H100 GPU draws roughly 700 watts. A 1,000-GPU training cluster draws 700kW — 7MW before cooling, storage, and networking overhead. At modern rack densities, this thermal load cannot be handled by air-cooled infrastructure built for CPU-era workloads at 5-10kW per rack.

The Cooling Density Ceiling forces an architecture decision that incremental upgrades cannot defer. I know teams that deferred it. They spent Q3 replacing cooling infrastructure under live workload pressure because the planning cycle had assumed their GPU density wouldn't breach the ceiling for another year. It breached in seven months.

| Cooling Architecture | PUE Range | Rack Density Limit | WUE | Infrastructure Lock-in | Retrofit Feasibility |
|---|---|---|---|---|---|
| Air cooling | 1.2-1.5 | ~50kW/rack | ~1.5-2.0 L/kWh | Medium | High |
| Direct liquid cooling | 1.1-1.3 | ~100kW/rack | ~0.5-1.0 L/kWh | High | Medium |
| Immersion cooling | 1.03-1.05 | ~250kW/rack | ~0.1-0.3 L/kWh | Very high | Low |

Immersion cooling achieves PUE of 1.03-1.05 — near the theoretical minimum. Air-cooled facilities in standard configurations run 1.2-1.5. The efficiency difference is real, but the more significant constraint is density: immersion-cooled facilities can serve GPU workload density that air-cooled infrastructure physically cannot.

Water Usage Effectiveness adds a second dimension. Google's 2022 average WUE was 1.1 L/kWh against an industry average near 1.8 L/kWh. In water-scarce regions, WUE is becoming a regulatory constraint independent of energy efficiency. The Cooling Density Ceiling and water constraints interact: the cooling architectures that clear the density ceiling also require different water consumption profiles that Siting as Carbon Strategy must account for upstream.

### Carbon-Aware Scheduling: batch workloads are deferrable. Most organizations do not treat deferability as a carbon lever.

Carbon-Aware Scheduling means deferring non-urgent workloads to grid windows with lower carbon intensity — shifting compute temporally or geographically toward clean energy rather than running on a fixed schedule regardless of grid conditions.

Most enterprise workloads have latency tolerance. Batch analytics, model training, data pipeline runs, backup operations — none require a sub-second response. Yet scheduling systems in most organizations dispatch on compute availability and business priority, not grid carbon intensity. Carbon intensity is not a variable in the dispatch logic. It was never added. Nobody asked for it.

Google's Carbon-Aware Computing initiative requires three infrastructure capabilities that procurement cannot substitute: workload observability (which jobs are deferrable and by how long), grid carbon intensity data (real-time API from regional grid operators), and scheduling integration (carbon intensity as a dispatch signal alongside cost and priority). These reduce effective carbon draw without changing annual REC reporting figures.

The 24/7 CFE Gap closes through Carbon-Aware Scheduling. Not through certificates.

Deferability assessment — 4 questions:

1. Latency tolerance — Can this workload run 2-6 hours later without violating a business SLA? Batch analytics: yes. Interactive queries: no.
2. Geographic mobility — Can this workload run in a different region without violating data residency requirements? Multi-region deployments: often yes. Single-jurisdiction data: no.
3. Batch vs. interactive ratio — What percentage of compute hours are batch workloads? Organizations above 40% batch have substantial deferability headroom.
4. Grid API integration — Does your scheduling infrastructure receive real-time regional carbon intensity data? Without it, scheduling cannot respond to grid conditions regardless of workload deferability.

Organizations with more than 40% batch workloads, multi-region deployments, and grid API integration can capture 15-30% reduction in effective carbon draw through Carbon-Aware Scheduling alone — without changing a single procurement contract.

---

## PUE measures the right thing in the wrong context.

Power Usage Effectiveness measures total facility power divided by IT equipment power. It is a useful operational metric. Its blind spot: it measures how efficiently power is used, not how carbon-intensive that power is.

A facility at PUE 1.58 on hydro-powered Pacific Northwest grid draws less carbon than a best-in-class facility at PUE 1.10 on a coal-heavy Midwest grid. PUE measures efficiency within the facility boundary. Carbon outcomes are determined outside it.

REC Accounting Theater exploits this blind spot. Annual certificates make a facility's sustainability report look clean while the PUE score improves independently. Neither captures per-hour carbon intensity. The two metrics can move in opposite directions for years before anyone notices the divergence.

| What PUE measures | What PUE misses |
|---|---|
| Total facility power / IT equipment power | Carbon intensity of the power consumed |
| Cooling and power distribution efficiency | Absolute growth in total facility power draw |
| Operational improvement over time | Scope 3 embodied carbon in hardware manufacturing |
| Performance vs. industry benchmark | Hourly variation in grid carbon intensity |

Microsoft's carbon-negative commitment illustrates the tension. Microsoft pledged carbon-negative operations by 2030. Its data center footprint grew roughly 30% year-over-year from 2020 to 2023. PUE improvements cannot offset absolute consumption growth at that rate. The pledge requires both efficiency gains and structural carbon measures — a combination that Siting as Carbon Strategy and Carbon-Aware Scheduling address, but procurement alone does not.

Apple's Scope 3 accounting clarifies the priority ordering for device manufacturers: roughly 95% of Apple's total emissions are supply chain, not data centers. Carbon-intensive manufacturing across Scope 3 dwarfs data center operational carbon for device companies. For hyperscalers and infrastructure-heavy enterprises, data center carbon is the dominant operational variable — and the 24/7 CFE Gap is the dominant measurement failure.

PUE is not the villain. It captures a real signal about cooling and power distribution efficiency. The blind spot is precise: it does not capture the carbon intensity of the power it measures. A facility optimizing PUE while ignoring grid carbon intensity is improving the denominator of the wrong equation.

---

## The carbon lever decision matrix

Not all carbon decisions carry equal weight. More importantly: not all are reversible.

| Carbon Lever | What It Changes | What It Doesn't Change | Reversibility |
|---|---|---|---|
| Siting as Carbon Strategy | Grid carbon intensity profile for the facility's 15-20 year life | Existing facilities; real-time grid conditions | Locked at construction |
| Cooling Density Ceiling | Maximum workload density serviceable; PUE floor achievable | Siting decision; grid carbon profile | Locked at infrastructure build; expensive to retrofit |
| Carbon-Aware Scheduling | Per-hour carbon draw through workload timing; effective carbon rate | Facility siting; cooling architecture; grid carbon profile | Reversible — scheduling is software, but infrastructure capability must be built first |
| REC/PPA Procurement | Annual renewable matching; disclosure compliance | Per-hour grid carbon dependency; siting, cooling, or scheduling | Fully reversible; annual contract |

The procurement decision is the only fully reversible one. The architecture decisions lock in.

Siting locks for 15-20 years. Cooling infrastructure locks for 10-15 years. Carbon-Aware Scheduling is software — reversible in principle, but only available if the infrastructure capability has been built. The absence of workload observability and grid API integration is itself a locked-in constraint until an investment cycle addresses it.

The decision hierarchy is clear. Siting decisions made now determine the carbon ceiling for facilities that will operate through 2040. Cooling decisions made for GPU-era workloads cannot be incrementally retrofitted from air-cooled infrastructure built for CPU densities. REC Accounting Theater satisfies the annual report in the meantime.

---

## The infrastructure roadmap question has already shifted.

The next decade of data center investment will be decided by infrastructure architects who treat decarbonization as an architecture problem, not a procurement function.

The playbook is observable. Google's 24/7 CFE methodology, Microsoft's structural tension between pledge and growth rate, Apple's Scope 3 accounting that locates carbon precisely — these are not aspirational examples. They are evidence that the correct variables are siting, cooling architecture, and workload scheduling. None of those variables respond to procurement.

Three questions for a facilities roadmap:

1. What is the hourly carbon intensity profile of your current grid, and what does it look like in 5 years? If you lack this data, your siting calculus is incomplete regardless of your annual renewable percentage.
2. What is your rack density trajectory over the next 3 years, and at what point does it breach the Cooling Density Ceiling for air cooling? If GPU workloads are in your roadmap, the ceiling is already approaching. It does not recede.
3. What percentage of your compute hours are batch workloads, and does your scheduling infrastructure have access to real-time grid carbon data? If you are above 40% batch with no grid API integration, Carbon-Aware Scheduling is an unbuilt infrastructure capability, not a procurement gap.

The carbon problem is not solved by what you buy. It is solved by where you build, how you cool, and when you run workloads.

---

Annual REC matching will not disappear overnight. Disclosure frameworks are built around it, and organizations that have invested in renewable procurement are supporting real generation capacity investment. That matters.

What REC Accounting Theater cannot do is close the 24/7 CFE Gap. It cannot change the Cooling Density Ceiling. It cannot substitute for Siting as Carbon Strategy decisions already locked into facilities that will operate for 20 more years.

The decisions are being made now. The question is whether your facilities roadmap treats them as architecture problems or procurement problems.

That difference will not appear in this year's sustainability report. It will appear in your per-hour grid carbon draw in 2035.


> The three architecture decisions that determine real carbon outcomes — and why procurement changes none of them.