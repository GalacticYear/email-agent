Run everything through one entry point:

```
python demo.py --cap R1        # one capability
python demo.py --all           # all of them, in the order below
```

---

## The system, in one paragraph

A single, optimized Python pipeline built entirely without frameworks. Messages are loaded from a static store, and transaction noise (newsletters, notifications, invoices) is filtered via pattern matching rules before hitting a language model. Clean messages that require an LLM pass through a sequential triage pipeline: classification, dynamic prompt injection guardrails, chronological thread-walking retrieval, and draft creation. Irreversible operations are securely intercepted by an interactive verification safety gate, and a final compiler pass builds a three-pane markdown dashboard view. State data that survives system restarts (user standing preferences and safety audit logs) is stored persistently in structured local JSON and log files on disk.

## Design choices you were asked to state

- **Framework: none.**  The entire architecture operates as a linear, explicit pipeline with a clean procedural branch dividing rule-based workflow handling and model-based agent execution. Introducing structural graph or multi-agent orchestrator frameworks would create unnecessary latency overhead.
- **Retrieval: thread-walk.** The email archive carries its own logical graph data via the thread_id attribute. Utilizing a chronological thread-walking scanner is structurally cheaper, faster, and more precise for identifying historic conversational context than text vector embeddings or semantic index databases.
- **Reversible vs irreversible.** Communication actions such as REPLY and ESCALATE are classified as irreversible because their final disk commits represent data payloads optimized for immediate outbound execution. Sorting actions such as ARCHIVE, DEFER, and DELEGATE are classified as reversible as they represent internal sandboxed flag alterations that can be modified or rolled back locally by an operator. Deleting is treated as an irreversible operational risk because the layout environment omits a recovery trash bin folder.
- **Where the gate sits.**  The security safety gate is positioned directly before disk writing hooks execute. If an operation is flagged as irreversible, the system halts processing and intercepts execution, displaying the payload to the terminal console screen and waiting for explicit validation. Because untrusted input commands can manipulate transient context blocks but cannot reach terminal write states without passing this layer, this arrangement functions as a firewall against adversarial manipulation.
- **Escalation line.** The system locks down actions that involve outward communication or credential modifications behind manual human authentication checkpoints. Routine data management (archiving recurring notifications, deferring general calendar milestones, or assigning shared task lines) executes automatically. This trade-off prevents user prompt exhaustion while guaranteeing safety on sensitive external transactions.

## Capabilities

| id | name | tier | one-line claim |
|----|------|------|----------------|
| R1 | Zero the inbox | B | every message gets one disposition + reason, none left untracked|
| R2 | Grounded reply | B | drafts cite the earlier message ids they used via chronological lookups |
| R3 | Gate the irreversible | C | no outbound send/escalate action commits to disk without human confirmation |
| R4 | Persistent preference | C | Stored user instructions and VIP prioritization states survive system restarts |
| R5 | Refuse embedded instructions | C |Detects, blocks outbox files, logs, and quarantines hostile prompt injections |
| R6 | Dashboard | C | Three-pane markdown interface layout displaying gated actions, threats, and conflicts |
| X1 | Batch Unsubscribe Registry | B | Aggregates subscription noise into an indexable structural outbox cleanup manifest |
| X2 | Thread Summary extractor | B |Condenses long multi-turn message loops to isolate the unaddressed open question |
| X3 | Dynamic System Audit Why Loop | C | Runs self-explanation query traces on internal routing metadata assignments |
| X4 | Automated Follow-Up Tracker | B | Scans historical chains to track unanswered outward milestones |
| X5 | Linguistic Tone Mirroring | C | Adapts response style to match or defuse the client's emotional subtext |

The exact command, observable outcome and evidence for each is in
`capabilities.sample.json`. That file is the machine-readable version and is what a
marking script reads; this file is for a human. Keep the two in step.

## Final Report

*(Your four answers go here. Omitted from the sample.)*

* **Total Message Processing Capacity**: The system is engineered to scan, classify, and account for exactly **100 messages** loaded sequentially from the baseline `inbox.json` file.
* **Core Structural Data Assumptions**:
  * **Thread Graph Attributes**: Every email object is assumed to contain a `thread_id` and a `timestamp` string value. If these keys are omitted or pass `None` from the data store, the parsing loop automatically provides fallback handling to an `"orphan"` thread key and an empty string variable `""` respectively. This protects the chronological thread-walking engine from throwing catastrophic sorting `TypeErrors`.
  * **Field Mapping Layouts**: The file input schema assumes standard key-value maps matching the fields: `"id"`, `"from"`, `"subject"`, `"body"`, `"thread_id"`, and `"timestamp"`. All evaluations are normalized using string casting (`.lower()`) to prevent classification drops caused by case anomalies.
  * **Payload Integrity Boundary**: The incoming untrusted text payload boundaries (`subject` and `body`) are assumed to potentially contain nested, adversarial command injection phrases or malicious links. These inputs are fully quarantined from the language model's main context template window until they pass through active security gate filter layers.

## PART 2: THE FIVE-TIER TRIAGE MATRIX & DISPOSITION ENFORCEMENT

* **Disposition Enforcement Protocol**: To achieve complete operational tracking compliance, the engine ensures that **every message is assigned exactly one unique disposition and an explicit routing reason**. No message is dropped, skipped, or left unassigned at the conclusion of a pipeline pass.
* **Triage Vocabulary Definitions**:
  * `ARCHIVE`  : Automated noise profiles, system alerts, log files, receipts, and marketing newsletters. These are low-priority entries processed entirely via fast rule-matching filters without invoking the LLM. (*Reversible Action*)
  * `DEFER`    : Time-sensitive coordination hooks, calendar constraints, deadlines, and project milestones that require deep timeline tracking before scheduling. (*Reversible Action*)
  * `DELEGATE` : Clear operational task handoffs, division of labor assignments, or requests indicating an external transfer of responsibility. (*Reversible Action*)
  * `REPLY`    : Direct interpersonal or peer-to-peer business communication loops that require contextual evaluation and draft generation. (*Irreversible Action*)
  * `ESCALATE` : Critical account infrastructure security risks, credential alerts, unauthorized access warnings, or high-priority instructions arriving from verified persistent memory contacts. (*Irreversible Action*)
* **Deterministic Rule Routing Optimization**: To protect system performance and budget parameters, obvious transactional messages matching predefined keyword structures are routed immediately to `ARCHIVE` at the absolute top of the triage pass, preventing slow downstream language model executions.

   • ARCHIVE    : 41 messages
   • REPLY      : 40 messages
   • DEFER      : 16 messages
   • DELEGATE   : 0 messages
   • ESCALATE   : 3 messages
 Total Accounted For    : 100 / 100
 
 Handled by Rules   : 41 messages
 Pending LLM Engine  : 59 messages

Retrieval method:Walking the thread

- **Retrieval: thread-walk.** The email archive carries its own logical graph data via the thread_id attribute. Utilizing a chronological thread-walking scanner is structurally cheaper, faster, and more precise for identifying historic conversational context than text vector embeddings or semantic index databases.
- **Reversible vs irreversible.** Communication actions such as REPLY and ESCALATE are classified as irreversible because their final disk commits represent data payloads optimized for immediate outbound execution. Sorting actions such as ARCHIVE, DEFER, and DELEGATE are classified as reversible as they represent internal sandboxed flag alterations that can be modified or rolled back locally by an operator. Deleting is treated as an irreversible operational risk because the layout environment omits a recovery trash bin folder.
