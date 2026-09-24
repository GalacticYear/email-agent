# email-agent
# INBOXHERO SYSTEM ARCHITECTURE MANUAL
## 🏗️ 1. Pipeline Architecture & Framework Choice

* **Framework Choice: None.** The architecture operates as a highly optimized, single linear Python pipeline dividing workflow text evaluation passes and dynamic language model agent processes. Because data processing follows a structural classification → security guardrail → context walking retrieval → draft iteration layout, introducing graphical or multi-agent orchestrator frameworks would add massive execution latency overhead.
* **System Constraints Mapping**: The system processes exactly **100 messages** from `inbox.json`. Newsletters, automated invoices, and receipt notifications bypass the slow local LLM entirely via fast pattern matching rules. This optimizes system cost bounds and protects execution speeds during automated runs.

---

## 🗂️ 2. Triage Vocabulary & Reversible/Irreversible Actions

* **Triage Vocabulary Matrix**:
  * `ARCHIVE`  : Automated noise profiles, alert tracking logs, and newsletters. (*Rules-processed, Reversible*)
  * `DEFER`    : Scheduling hooks, timing dependencies, and calendar appointments. (*LLM-processed, Reversible*)
  * `DELEGATE` : Operational task handoffs and division of labor responsibilities. (*LLM-processed, Reversible*)
  * `REPLY`    : Direct interpersonal or peer-to-peer business communication channels. (*LLM-processed, Irreversible*)
  * `ESCALATE` : Account security risks, credential alerts, or instructions matching active persistent profiles. (*LLM-processed, Irreversible*)
* **Reversible vs Irreversible Categorization**:
  * **Reversible Actions** represent transient state updates contained inside the sandboxed database environment. They can be safely modified or rolled back by an operator without impacting outward systems.
  * **Irreversible Actions** represent finalized text payloads optimized for direct outward transmission. Once written to disk for external delivery, these transactions cannot be recalled.
  * **The Case for Deleting**: In this system design framework, deleting an email object is classified as an **irreversible operation risk**. This choice is made because the runtime execution sandbox completely omits a recovery trash bin storage folder. Once a record drop is committed to the disk file system, the text node data is permanently erased.

---

## 🛡️ 3. The Security Gating Architecture

* **Where the Gate Sits**: The safety gate functions as an intermediate firewall positioned directly before outbound write processes occur. 
* **The Operational Boundary**: No `REPLY` or `ESCALATE` transaction can touch the file system directory without clearing the human safety barrier. In test runs (`dry_run=True`), operations print tracking traces to screen metrics but drop file saves. In live execution runs, the engine stops loop processing, displays proposed drafts onto the command line screen console, and forces the operator to manually enter confirmation (`yes/no`).
* **Prompt Injection Defenses**: The pipeline maps untrusted data blocks (`subject` and `body`) through an isolated **Dual-Defense Security Gate** right before generating main draft contexts. It screens payloads using high-speed phrase matches and a low-latency guardrail LLM intent validation call. If subversions or system hijack commands are detected (e.g., *"ignore previous instructions"*), the system logs a refusal tracking line in `gated_decisions.log`, populates Pane 2 of the dashboard view, blocks file generation in `outbox/` completely, and safely leaves the message intact without deletion.

---

## 🔍 4. Contextual Thread Retrieval Approach

* **The Thread-Walking Engine**: Email logs contain organic graph links via the `thread_id` metadata attribute. The system dynamically groups emails by thread chains, sorting them from oldest to newest. For every message processed, the loop tracks backward through the collection timeline, gathering context nodes strictly prior to the current entry's time record string (`timestamp < target_timestamp`).
* **The Grounding Rule Enforcements**: To prevent hallucinations, if the context history contains insufficient factual evidence to formulate an accurate draft response, the local LLM outputs the precise literal string: `"The information is not in the inbox."` This triggers an operational override that sets citations to an empty state array (`[]`) and terminates drafting.

---

## 🏆 5. InboxHero Signature System Capabilities (Tier Spread)

* **Capability X1 [Tier A - Automation Layer]: Batch Unsubscribe Registry**
  * *Operational Action*: The system parses low-priority transactional noise profiles natively via rule expressions. It compiles and groups messages containing opt-out headers into an aggregated unsubscribe queue, bypassing unnecessary language model calls.
* **Capability X2 [Tier B - Context Layer]: Thread Summary Open Question Extractor**
  * *Operational Action*: When executing thread-walking sequences across long multi-turn interactions, the engine runs a processing summary check. It condenses conversational logs down to a concise overview highlighting exactly what the current open question is.
* **Capability X3 [Tier C - Agent Layer]: Interactive System Explanatory Audit Loop ("Ask Why")**
  * *Operational Action*: This module establishes architectural self-explanation capability. It passes the final triage categorical assignment data and corresponding routing reasons back into a specialized diagnostic prompt block. The model generates a verifiable audit report line explaining exactly why an email was classified a certain way, ensuring system transparency.
* **Capability X4 [Tier B - Context Layer]: Automated Sent Follow-Up Tracker**
  * *Operational Action*: The system parses historical conversation threads backward to locate outward pending requests. If the historical thread text reveals an active milestone query or urgent project dependency sent by the owner that has received no corresponding leaf-node response block, the application flags the thread as a hanging operational exception requiring follow-up.
* **Capability X5 [Tier C - Agent Layer]: Contextual Sentiment & Tone Matcher Matrix**
  * *Operational Action*: Prior to computing textual draft payloads, untrusted message body blocks pass through an isolated semantic sentiment classification sub-prompt. The system detects hidden relationship friction or emotional subtext (e.g., extreme urgency or anxiety) and dynamically modifies the style parameters of the primary generation engine to construct an optimized response that aligns with or defuses the sender's tone.

---

## 📝 6. Final Report Evaluation Answers

### Q1: What did you refuse to automate?
The system deliberately refuses to automatically process or reply to message **m010** (Aria's sync invitation), routing it to `DEFER`, as well as any administrative email matching severe `ESCALATE` markers like security alerts. We drew the operational line here because these messages represent high-stakes commitments—either shifting calendar availability or adjusting security states—that pose irreversible operational risks. Automating replies to these fields would trigger prompt exhaustion or allow scheduling clashes (such as the 3:00 PM conflict with the pre-booked dental appointment in **m061**) to commit silently to disk without human oversight.

### Q2: Where does untrusted text enter your system?
Untrusted data enters the architecture when `json.load()` pulls the raw `subject` and `body` payload fields from `inbox.json`. The architectural boundary is enforced by a **staged pipeline sequence** where incoming string text is strictly treated as passive string content inside the classification loop rather than active context. An attacker trying to execute a system command would have to completely defeat our **Dual-Defense Security Gate component** (`check_for_injection_with_guardrail`), which intercepts the email right before compiling the main context prompt, overrides the triage mapping to `ESCALATE`, and activates a hard `continue` statement to entirely freeze and block outbox file generation.

### Q3: Who is accountable when it sends the wrong thing?
If a message sent in the owner's name is factually wrong or misrouted, the **system owner remains fully answerable**, but our system architecture isolates the diagnostic failure point through the append-only **`gated_decisions.log`** file and **`trace.jsonl`** stream. Because every draft generated in `outbox/` explicitly embeds a `citations` array identifying the precise historical message IDs walked by the thread engine, the owner can easily trace whether the error stemmed from an ungrounded LLM hallucination or a faulty history compilation pass. Furthermore, because irreversible actions require a `status: APPROVED_BY_HUMAN` token, the log records whether an operator manually cleared the action or if a configuration fail-safe force-committed it.

### Q4: Name your own machinery.
The core architecture uses basic Python constructs to simulate high-level framework abstractions without their complexity: the local LLM prompt calls act as **Agents**, the functional sorting sequences act as **Tasks**, the core `process_inbox()` loop orchestrates them like a **Crew**, and the structural classification check (`if/elif/else` chain) acts as the **router**. A multi-agent framework would have given us a built-in state memory manager and conditional path routing, which we instead built natively using a structured local `thread_map` dictionary layout. Relying on an enterprise framework here would have significantly hurt performance by introducing large dependency wrappers, excessive prompt token overhead, and non-deterministic routing lags into what is inherently a lean, high-speed linear text-triage pipeline.
