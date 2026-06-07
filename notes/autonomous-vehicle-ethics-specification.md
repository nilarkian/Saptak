---
is_note: true
layout: note-layout
date: 2026-06-07
title: The Ethics of a self-driving car Is an Engineering Specification Problem
---

> AV: Autonomous Vehicles

AV ethics has a resource allocation problem. Not a philosophy problem.

Three systematic failures, measurable, traceable, already occurring in deployed systems, get a fraction of the attention collision preference philosophy commands.

You are treating AV ethics as a philosophy problem or an engineering specification problem. The first produces guidelines no deployed system can verify. The second produces accountability that holds.

---

## The industry's ethics budget is going to the wrong problem

AV ethics discourse concentrates most of its energy on collision preference: if the car faces an unavoidable accident, what should it choose? Ethics committees debate it. Conference panels stage it. White papers refine preference hierarchies.

This is Trolley Problem Theater.

Trolley Problem Theater is the allocation of ethics resources to edge-case collision preference philosophy while systematic, measurable failures in deployed systems receive disproportionately less attention. Not an argument that collision ethics is unimportant. A diagnostic: where ethics investment goes versus where it would have the most accountability leverage in deployed systems. I have watched AV ethics panels run for two hours on collision preference philosophy without a single slide on pedestrian detection bias. That is the budget problem made visible.

Trolley Problem Theater absorbs attention that could go elsewhere. AV perception systems detecting darker-skinned pedestrians 5–7% less accurately than lighter-skinned ones, documented across multiple commercial datasets used in production vehicles today. Manufacturers marketing Level 2 driver-assistance systems with Level 4 naming conventions, creating liability voids when drivers stop monitoring the road. Neural decision models making safety-critical choices engineers cannot reconstruct from telemetry after an accident.

Three failures. All measurable. None of them trolley-problem scenarios.

The trolley problem is intractable for three reasons. No cross-cultural consensus exists on collision preference hierarchies. Current neural architectures cannot reliably encode preference rules under real-time inference constraints. The scenario itself is statistically marginal. Genuine unavoidable-collision situations occur at negligible frequency in actual AV operation. None of that makes it unimportant. It makes Trolley Problem Theater the wrong place to concentrate your ethics budget when three measurable failures are accumulating accountability gaps in production systems right now.

---

## The new category: AV Ethics as Engineering Specification

AV Ethics as Engineering Specification is the discipline of translating ethical requirements for autonomous vehicle AI into testable, measurable, enforceable engineering constraints. Not philosophical guidelines that cannot be verified against deployed system behavior.

The distinction is concrete. A philosophical guideline says: the car should not discriminate. An engineering specification says: pedestrian detection accuracy variance by demographic group must remain below 2 percentage points across standard lighting conditions, validated against a dataset with representation within 10% of target operating environment demographics. One is aspirational. The other is auditable. One lands in a white paper. The other lands in a crash investigation.

```
FROM  AV ethics as philosophy: white papers, collision preference hierarchies, ethics boards
TO    AV ethics as engineering specification: bias testing benchmarks, ODD boundary standards, interpretability audit trails
```

It changes three questions.

Not: "What should the car choose in an unavoidable collision?" But: "What systematic failures are already occurring in deployed systems?"

Not: "Is this fair in principle?" But: "How do we measure fairness in production?"

The third question is the most uncomfortable one. Not "who is morally responsible if something goes wrong?" but "how do we build accountability into the system architecture before deployment?" Responsibility is a legal and philosophical frame. Architecture is an engineering one. Only one of those produces a specification you can test against.

The shift matters because Trolley Problem Theater is optimized for the first question in each pair. It generates frameworks for philosophical alignment, and those frameworks cannot be run against a neural decision stack, a training dataset, or an operational design domain. You cannot feed a preference hierarchy into a PyTorch model and verify it. Engineering specification is optimized for the second question in each pair. It generates requirements that can be validated, tested, and enforced before a vehicle operates on public roads.

Three failures define the gap between where ethics attention concentrates and where accountability specification would have the most impact. None of them require philosophical consensus to solve. None of them appeared in a trolley problem scenario. All three are in production systems on public roads right now.

Each one is specifiable. Testable. Enforceable.

---

## Systematic failure 1: Perception Equity Deficit

Before the evidence: think of this as a calibration failure, not an intent failure. No manufacturer designed a biased detector. Every manufacturer trained on available datasets. Available datasets underrepresent certain pedestrian demographics relative to actual urban distributions. The result is a measurable disparity in safety outcomes, traceable to a specific engineering decision with a specific fix.

That is the Perception Equity Deficit.

The Perception Equity Deficit is the systematic under-detection of darker-skinned pedestrians in AV perception systems, traceable to underrepresentation in training datasets and documented at a 5–7% accuracy gap across multiple commercial architectures.

In 2019, Georgia Tech researchers published findings showing that object detection systems used in AV applications detected darker-skinned pedestrians with 5–7% lower accuracy than lighter-skinned pedestrians. Consistently, across multiple commercial datasets and multiple architectures. Cause: training datasets underrepresent pedestrians of color relative to actual urban demographic distributions. Consequence: a vehicle operating in a diverse urban environment has a measurably higher probability of failing to detect certain pedestrians than others. That is not a philosophical problem. It is a Perception Equity Deficit with a specified cause and a specifiable fix pathway.

The Perception Equity Deficit is specifiable: the performance gap has a number. The cause has a mechanism. The target environment has a demographic distribution that can be measured and compared against dataset demographics.

Accuracy variance across demographic groups can be benchmarked at standard and adversarial lighting conditions before deployment, and a threshold can be set. That is testability. Not aspiration.

Enforceability is already in place in one major market: the EU AI Act (2024) classifies AV AI as high-risk and requires bias testing on representative datasets as a compliance condition for 2026 EU deployment. Not speculation about future legislation. Current requirement.

**The Perception Equity Deficit Fix Pathway**

| Stage | Action | Output |
|---|---|---|
| Audit | Measure demographic representation in training dataset vs. target operating environment | Gap report: % underrepresentation by demographic group |
| Re-collection | Targeted data collection in underrepresented demographic contexts | Dataset delta: documented coverage improvement |
| Bias testing | Accuracy benchmark by demographic group, standard + adversarial conditions | Performance table: variance ≤ specified threshold |
| Deployment threshold | Regulatory submission with maximum variance ceiling | Signed specification: max allowed Perception Equity Deficit |
| Post-market monitoring | Ongoing accuracy tracking in production by demographic group | Drift alert: triggers re-validation when variance rises |

The Perception Equity Deficit is a solved-architecture problem. Expensive, yes. The re-collection phase alone can take 12 to 18 months in underrepresented environments. But the tooling exists. The regulatory pathway is open. What is missing is not understanding. It is treating the gap as an engineering specification problem rather than a philosophical one. That is a decision, not a constraint.

---

## Systematic failure 2: Level-Confusion Liability Gap

The SAE automation taxonomy is precise. Level 2 systems are driver assistance: the driver monitors the road, the driver bears legal responsibility. Level 3 is conditional automation: the driver must be ready to resume control when requested. Level 4 is high automation within a defined Operational Design Domain. The manufacturer accepts that no driver intervention is expected during normal operation.

Marketing language is not that precise.

Systems branded with names implying full autonomy, products embedding "Autopilot," "Full Self-Driving," or "Super Cruise" in their identity, are Level 2 or Level 3 systems. The language implies Level 4 capability. This mismatch is the Level-Confusion Liability Gap.

Level-Confusion Liability Gap is the accountability void created when Level 2 systems are deployed with Level 4 marketing language, inducing driver complacency while leaving legal liability with the driver rather than the manufacturer. Not a deliberate deception to diagnose. Level-Confusion Liability Gap is a structural incentive problem: product names that drive demand also erode the driver vigilance that Level 2 systems depend on for safe operation.

The behavioral evidence is documented. Automation complacency research shows that safety driver intervention rates approach zero over extended exposure, even under explicit alertness instructions. Tesla Autopilot accident analyses have consistently documented drivers not monitoring the road during system engagement. NHTSA's Standing General Order, effective 2021 and updated in 2022, required crash reporting for AV and ADAS systems within 24 hours. Tesla Autopilot reported 273 crashes in the first 10-month reporting window. Waymo reported 2. Per-mile exposure rates differ substantially; the Level-Confusion Liability Gap makes those absolute numbers difficult to assign accountability against when the driver was operating under the understanding that the system could handle the road.

**SAE Level Accountability Map**

| SAE Level | Who monitors | Legal liability | Manufacturer obligation | Level-Confusion Liability Gap |
|---|---|---|---|---|
| Level 2: Driver Assistance | Driver (always) | Driver | Intervention warnings | Branding often implies higher level; complacency induced |
| Level 3: Conditional Automation | Driver (on request) | Driver until handoff | Clear takeover protocol | ODD limits under-disclosed to consumers |
| Level 4: High Automation (ODD-limited) | System | Manufacturer (within ODD) | ODD documentation + validation | ODD Creep expands liability surface past validation |
| Level 5: Full Automation | System | Manufacturer | No ODD limits | Not commercially deployed |

Mercedes-Benz established the first Level 3 precedent in 2022: regulatory approval in Nevada and California with explicit manufacturer liability acceptance when the Level 3 system is active. That is not an extension of Level 4 liability. It proves that manufacturer liability acceptance at conditional automation is achievable. The absence of equivalent requirements for Level 2 systems marketed with Level 4 language is a gap in the regulatory architecture.

The specification here is direct: explicit SAE level designation required in all consumer-facing product naming, with regulatory prohibition on any name that implies higher automation than the system has been certified for. Driver behavior studies can measure complacency rates against naming conventions. That data exists. Enforcing it is a regulatory market-entry decision, not a research gap.

**ODD Creep: where the liability surface grows**

Alongside Level-Confusion Liability Gap sits a related but distinct failure: ODD Creep.

ODD Creep is the gradual expansion of a vehicle's Operational Design Domain beyond proven capability. Each expansion creates a new uncharted liability surface and increases the gap between demonstrated and claimed system competence. A system validated for freeway operation at standard weather conditions expands to surface streets. Then adverse weather. Then complex intersections. Each expansion is incremental. Each is also a new engineering specification problem: what is the system's failure mode in this domain? At what conditions does performance degrade?

ODD Creep is what happens when commercial pressure to expand system utility outpaces validation evidence. The car was certified for the freeway. Someone approved the surface street. Nobody re-ran the test suite. The questions ODD Creep generates are answerable: specifiable, testable, and enforceable. But only when ODD expansion requires mandatory re-validation evidence rather than a form submission.

---

## Systematic failure 3: Interpretability Accountability Gap

In October 2023, a Cruise robotaxi in San Francisco struck a pedestrian already injured by another vehicle. The Cruise vehicle's post-collision behavior compounded the incident: it failed to detect that it had struck a person and dragged the pedestrian 20 feet before stopping. Twenty feet. The California DMV revoked Cruise's operating permit. GM suspended San Francisco robotaxi operations.

Investigators asked a specific question: how had the vehicle's perception system interpreted the scene between the initial collision and the drag event? Speed was recorded. Steering was captured. Braking data existed. What engineers could not reconstruct, from telemetry alone, was the reasoning chain of the neural decision model.

That is the Interpretability Accountability Gap.

The Interpretability Accountability Gap is the inability to reconstruct post-hoc reasoning from non-interpretable neural decision models after an accident, preventing definitive liability assignment and forcing blame diffusion across manufacturer, supplier, and operator. This is not a theoretical future problem. It is present in every neural-stack AV system operating on public roads.

Worth sitting with that for a second. Not "may affect future deployments." Present. Now.

AV perception and decision systems rely on deep neural networks processing sensor data (camera, LiDAR, radar) through learned representations. These representations cannot be traced to explicit decision rules. An attention map shows where the network focused. It does not show why the network classified what it saw the way it did. After an accident, forensic reconstruction relies on telemetry: speed, steering angle, throttle, braking actuation. What telemetry cannot recover is the intermediate reasoning chain.

ODD Creep compounds the Interpretability Accountability Gap directly: each expansion of the operational envelope introduces new scenarios where the network's learned representations may not generalize. Post-accident, the absence of an interpretability trail leaves the same accountability void. ODD Creep and the Interpretability Accountability Gap compound each other. Each ODD expansion without re-validation increases the probability of operating in conditions where the network's behavior is unvalidated and, post-accident, unrecoverable. Two gaps. One investigation. No answers.

**What post-accident telemetry captures vs. cannot reconstruct**

| Data type | Available | What it answers |
|---|---|---|
| Vehicle speed | ✓ | How fast the vehicle was moving |
| Steering angle | ✓ | What path correction was applied |
| Braking actuation | ✓ | When and how hard brakes engaged |
| Sensor data (LiDAR, camera frames) | ✓ partial | What the environment looked like |
| Neural network decision chain | ✗ | Why classification decisions were made |
| Intermediate feature activations | ✗ | What concepts triggered each decision |
| Confidence scores at decision time | ✗ | How certain the system was |

No reconstruction. No liability assignment. When blame diffuses across manufacturer, Tier-1 perception stack supplier, dataset provider, and operator, no single accountability vector holds. Settlements happen. Liability is negotiated. The root cause, the specific system decision that contributed to the outcome, remains uncertified.

The specification is an audit trail requirement: AV systems must retain reconstructible decision records beyond telemetry for a defined post-accident window. Simulation environments can evaluate decision transparency under controlled conditions before deployment approval. That is how you test it before a vehicle hits a public road. The EU AI Act's 2024 explainability requirements for high-risk AI systems, with compliance deadline 2026, establish exactly this accountability standard. One major market already requires it. The gap is everywhere else.

The Interpretability Accountability Gap is not closed by building more interpretable systems alone. It is closed by specifying what interpretability evidence is required for deployment approval, and holding that specification as non-negotiable before a vehicle operates on public roads.

---

## What engineering specification actually requires

Three failures. All specifiable. All testable. The regulatory pathway for each one is already open in at least one major market.

What separates AV Ethics as Engineering Specification from Trolley Problem Theater as a discipline:

**AV Ethics Priority Matrix**

| Failure mode | Measurability | Current regulatory treatment | Engineering specification exists? | Accountability impact |
|---|---|---|---|---|
| Trolley Problem Theater | Unmeasurable (scenario-dependent) | Ethics review only | No enforceable spec | None: philosophical edge case |
| Perception Equity Deficit | Measured: % accuracy variance by demographic | EU AI Act 2026 compliance req. | Yes: bias testing benchmark | High: applies to every deployment |
| Level-Confusion Liability Gap | Measurable: complacency data, crash reporting | Partial: NHTSA SGO; Mercedes L3 precedent | Partial: SAE taxonomy exists; branding requirements absent | High: applies to Level 2/3 deployments globally |
| Interpretability Accountability Gap | Partially measurable: telemetry coverage vs. gap | EU AI Act explainability req. 2026 | Partial: audit trail standards not yet universal | Critical: every post-accident investigation |
| ODD Creep | Measurable: expansion triggers vs. validation evidence | Inconsistent (notification-based) | No mandatory re-validation standard | High: each ODD expansion = new uncharted liability surface |

The table shows what Trolley Problem Theater costs. Not that collision preference philosophy is wrong. It is unmeasurable, unenforceable, and concentrated at exactly the wrong problem while four measurable failures accumulate accountability gaps in production systems.

**Engineering specification checklist for AV ethics compliance**

What an ethics specification requires, as opposed to a philosophy paper or a marketing ethics statement:

- [ ] **Perception bias testing:** Accuracy variance by demographic group ≤ specified threshold, validated against a dataset with documented representation vs. target ODD demographics
- [ ] **ODD boundary documentation:** Defined operating conditions with supporting validation evidence; each ODD expansion triggers mandatory re-validation, not administrative notification
- [ ] **SAE level labeling compliance:** Consumer-facing product names, UI, and marketing materials state certified SAE level explicitly; naming conventions that imply higher automation than certified are prohibited
- [ ] **Interpretability audit trail:** Post-accident decision record retention beyond telemetry for a defined window; reconstruction capability certified in pre-deployment simulation testing
- [ ] **Liability assignment by SAE level:** Documented in product terms, insurance filings, and regulatory submissions, specifying who bears liability at each level boundary
- [ ] **Post-market monitoring protocol:** Ongoing accuracy and performance tracking by demographic group and ODD boundary; drift alerts trigger re-validation before continued operation
- [ ] **Incident reporting standard:** NHTSA SGO-equivalent minimum; per-mile rate reporting alongside absolute numbers; public annual safety report as baseline expectation

Ethics compliance is not a philosophy paper reviewed by a board. It is an auditable specification reviewed by an engineering team.

---

## The binary that matters

Waymo has driven over 20 million autonomous miles on public roads in Phoenix, San Francisco, and Los Angeles. Zero at-fault fatal accidents in autonomous mode are on public record. Waymo publishes an annual safety report: incident rates, miles driven, at-fault classification, defined methodology. No other major AV operator matches that transparency standard.

**AV Operator Transparency Benchmark**

| Reporting dimension | Waymo standard | Industry norm |
|---|---|---|
| Annual safety report | Published, publicly available | Absent for most operators |
| Per-mile incident rate | Reported | Rarely disclosed; absolute numbers only |
| At-fault classification | Reported | Not standard practice |
| Miles driven | Disclosed | Inconsistently disclosed |
| Incident methodology | Defined and public | Not standard |
| NHTSA SGO compliance | Full compliance | Variable |

That gap is not regulatory luck. It is what AV Ethics as Engineering Specification looks like in production: named metrics, defined methodology, public accountability. I have read through several major operators' public safety disclosures. Most are three paragraphs with no methodology. That is not a transparency report. Other operators don't match Waymo's standard because it isn't required. It should be.

The trolley problem is a thought experiment. It generates excellent conference panels. It has not produced a single accountability framework that constrained deployed system behavior. Trolley Problem Theater absorbs ethics energy that could build Perception Equity Deficit thresholds, Level-Confusion Liability Gap labeling requirements, and Interpretability Accountability Gap audit standards.

You are designing AV ethics as a philosophy problem or an engineering specification problem. Philosophy produces guidelines. Engineering specifications produce systems that can be tested, measured, and held to account.

The difference shows up in crash reports. In detection accuracy gaps by pedestrian demographic. In 20 feet of road drag in October 2023. In the absence of an audit trail that could answer the question no engineer in San Francisco could answer: exactly what did the system decide, and why?

Build the specification. Enforce it.


> The industry spends 90% of its ethics budget on the trolley problem while three systematic failures — Perception Equity Deficit, Level-Confusion Liability Gap, and Interpretability Accountability Gap — accumulate accountability gaps in deployed systems.