---
layout: note-layout
title: "RCM — Visual Study Map (10 Diagrams)"
topic: "RCM"
sub: "RCM · 8/8"
date: 2026-06-10
series_index: /notes/1234
series_prev: /notes/rcm/rcm-claims-patient-resp
description: "All 10 mermaid diagrams covering the US healthcare RCM chain — the visual study map."
tags:
  - rcm
  - medical-billing
  - healthcare
  - sunknowledge
---

[← Series Overview]({{ '/notes/rcm/rcm-overview' | relative_url }})

> [!tip] How to use this page
> These 10 diagrams give you an 80/20 picture of the entire RCM domain. Study the most important 6 first: 1, 5, 6, 8, 9, 10. Return here any time you need a visual anchor.

---

## 1. The Entire Revenue Cycle

The master chain — every other concept lives somewhere on this flow.

```mermaid
flowchart LR
  M[Member/Patient]
  --> P[Provider]
  P --> A[Authorization]
  A --> S[Service Rendered]
  S --> C[Medical Coding]
  C --> CL[Claim Submission]
  CL --> PY[Payer / Insurance]
  PY --> AP[Approved]
  PY --> DN[Denied]
  DN --> APPEAL[Appeal]
  APPEAL --> PY
  AP --> PAY[Payment]
```

---

## 2. The Healthcare Ecosystem

The 5 participants and how they connect.

```mermaid
graph TD
  HC[US Healthcare]
  HC --> M[Member]
  HC --> P[Provider]
  HC --> PAY[Payer]
  HC --> S[Supplier]
  HC --> R[Researcher]
  M --> P
  P --> PAY
  S --> P
  R --> HC
```

---

## 3. HIPAA & PHI

Who must follow HIPAA, and what PHI protects.

```mermaid
graph TD
  HIPAA
  HIPAA --> HCP[Healthcare Providers]
  HIPAA --> HCPN[Health Plans]
  HIPAA --> HCCH[Clearing House]
  HIPAA --> BA[Business Associates]
  HIPAA --> PHI[Protected Health Information]
```

```mermaid
graph TD
  PHI[Protected Health Information]
  PHI --> Name[Name]
  PHI --> DOB[Date of Birth]
  PHI --> Contact[Phone / Contact Details]
  PHI --> Doa[Date of Admission]
  PHI --> Dos[Date of Discharge]
  PHI --> Dod[Date of Death]
  PHI --> SSN[SSN]
  PHI --> MRN[MRN]
  PHI --> ADDR[Address / Zip / Area Codes]
  PHI --> PHOTO[Photograph]
```

---

## 4. Health Plan Universe

Which plan applies to which patient situation.

```mermaid
graph TD
  PATIENT[Patient Needs Care]
  PATIENT --> AGE[65+ or Disabled?]
  PATIENT --> POV[Low Income?]
  PATIENT --> MIL[Military Family?]
  PATIENT --> VET[Veteran Family?]
  PATIENT --> ACC[Car Accident?]
  PATIENT --> JOB[Work Injury?]
  AGE --> MEDICARE
  POV --> MEDICAID
  MIL --> TRICARE
  VET --> CHAMPVA
  ACC --> NOFAULT[No-Fault Liability]
  JOB --> WORKERSCOMP[Workers Comp]
```

---

## 5. Medicare Parts ★

The four-part structure of Medicare.

```mermaid
graph TD
  MEDICARE
  MEDICARE --> A[Part A]
  MEDICARE --> B[Part B]
  MEDICARE --> C[Part C]
  MEDICARE --> D[Part D]
  A --> INP[Inpatient / Hospital ≥ 24hrs]
  B --> OUTP[Outpatient < 24hrs]
  B --> DME[Durable Medical Equipment]
  C --> ADV[Medicare Advantage]
  D --> RX[Prescription Drugs]
  C --> MAPD[MAPD]
  D --> MAPD
```

---

## 6. HMO vs PPO ★

The managed care plan types comparison.

```mermaid
flowchart TD
  PLAN[Managed Care]
  PLAN --> HMO
  PLAN --> PPO
  HMO --> REF[Referral Required]
  HMO --> INN[In-Network Only]
  HMO --> LOW[Lower Cost]
  PPO --> NOREF[No Referral]
  PPO --> OON[Out-of-Network Allowed]
  PPO --> HIGH[Higher Cost for OON]
```

---

## 7. Provider Hierarchy

Individual vs Facility providers, and the facility types.

```mermaid
graph TD
  PROVIDER
  PROVIDER --> IND[Individual]
  PROVIDER --> FAC[Facility]
  IND --> PCP
  IND --> SPEC[Specialist]
  FAC --> HOSP[Hospital]
  FAC --> SNF
  FAC --> ASC
  FAC --> HH[Home Health]
  FAC --> HOSPICE
```

---

## 8. Authorization Workflow ★

How a member gets from office visit to specialist procedure, with insurance approval at each gate.

```mermaid
sequenceDiagram
  participant M as Member
  participant PCP
  participant S as Specialist
  participant I as Insurance

  M->>PCP: Office Visit
  PCP->>I: Referral Request
  I-->>PCP: Referral Approved
  PCP->>S: Refer Member
  M->>S: Specialist Visit
  S->>I: Prior Authorization Request
  Note over S,I: Surgery / MRI / Expensive Procedure
  I-->>S: Authorization Approved
  S->>M: Perform Service
```

---

## 9. Medical Coding Stack ★

How a visit turns into a claim — the 5 code sets in sequence.

```mermaid
flowchart LR
  V[Patient Visit]
  V --> DX[ICD Diagnosis Code<br/>Why patient came]
  DX --> PROC[CPT Procedure Code<br/>What provider did]
  PROC --> EQ[HCPCS Code<br/>Equipment / Supplies]
  EQ --> MOD[Modifier<br/>Extra Details]
  MOD --> POS[Place of Service<br/>Where]
  POS --> CLAIM[Medical Claim]
  CLAIM --> PAYOR[Insurance Adjudication]
```

---

## 10. Claim Adjudication & Denials ★

The three gates a claim must pass before payment.

```mermaid
flowchart TD
  CLAIM[Claim Submitted]
  CLAIM --> CHECK1{Within TFL?}
  CHECK1 -->|No| DENIAL1[Late Filing Denial]
  CHECK1 -->|Yes| CHECK2{Insurance Active at DOS?}
  CHECK2 -->|No| DENIAL2[Inactive Coverage Denial]
  CHECK2 -->|Yes| CHECK3{Authorization Present?}
  CHECK3 -->|No| DENIAL3[No Auth Denial]
  CHECK3 -->|Yes| APPROVED[Pay Claim]
  DENIAL1 --> APPEAL
  DENIAL2 --> APPEAL
  DENIAL3 --> APPEAL
```

---

> [!success] If you can narrate all 10 diagrams aloud
> You understand the entire Week 1 SunKnowledge training. The ★ ones are the 6 highest-priority.

---

## 📚 RCM Series

[← Overview & Cheat Sheet]({{ '/notes/rcm/rcm-overview' | relative_url }}) ·
[Participants & HIPAA]({{ '/notes/rcm/rcm-participants-hipaa' | relative_url }}) ·
[Plans & Medicare]({{ '/notes/rcm/rcm-plans-medicare' | relative_url }}) ·
[Managed Care]({{ '/notes/rcm/rcm-managed-care' | relative_url }}) ·
[Providers & Auth]({{ '/notes/rcm/rcm-providers-auth' | relative_url }}) ·
[Medical Coding]({{ '/notes/rcm/rcm-coding' | relative_url }}) ·
[Claims & PR]({{ '/notes/rcm/rcm-claims-patient-resp' | relative_url }})
