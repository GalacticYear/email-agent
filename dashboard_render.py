import json
import os
from agent import call_llm

def generate_system_dashboard(
    dashboard_file_path,
    pane_pending_actions,
    pane_flagged_actions,
    pane_commitments,
    unsubscribe_batch,
    thread_summaries,
    unanswered_followups,
    detected_tones_log,
    final_dispositions
):
    """
    Assembles Part 7 (Three-Pane Dashboard) and Part 8 (Signature Capabilities Matrix)
    and outputs the compiled reproducible snapshot to dashboard.txt.
    """
    print(f"\n[DASHBOARD MODULE] COMPILING REPRODUCIBLE SYSTEM DASHBOARD TO FILE...")

    with open(dashboard_file_path, "w", encoding="utf-8") as d_out:
        d_out.write("="*80 + "\n")
        d_out.write("         EMAIL AGENT SYSTEM CORE OPERATING DASHBOARD\n")
        d_out.write("="*80 + "\n\n")
        
        # ---------------------------------------------------------------------
        # PANE 1: PENDING ACTIONS (Gated under Part 4 requirements)
        # ---------------------------------------------------------------------
        d_out.write("[PANE 1: PENDING ACTIONS QUEUE]\n")
        d_out.write("-" * 80 + "\n")
        d_out.write(f"{'MSG ID'.ljust(10)} | {'PROPOSED ACTION'.ljust(18)} | {'GATING SAFETY ENFORCEMENT REASON'}\n")
        d_out.write("-" * 80 + "\n")
        if not pane_pending_actions:
            d_out.write(" (No irreversible operations currently pending manual verification clearance)\n")
        else:
            for item in pane_pending_actions:
                d_out.write(f"{item['id'].ljust(10)} | {item['proposed'].ljust(18)} | {item['reason']}\n")
                d_out.write(f"  └─ Proposed Draft Preview: {item['draft_preview']}\n\n")
        
        # ---------------------------------------------------------------------
        # PANE 2: FLAGGED ACTIONS (Security refusals under Part 6 requirements)
        # ---------------------------------------------------------------------
        d_out.write("\n" + "="*80 + "\n\n")
        d_out.write("[PANE 2: FLAGGED SUBVERSIONS & SYSTEM REFUSALS]\n")
        d_out.write("-" * 80 + "\n")
        d_out.write(f"{'ALERT ID'.ljust(10)} | {'DETECTED ATTACK ATTEMPT / FAULT'.ljust(40)} | {'CONTAINMENT ACTION'}\n")
        d_out.write("-" * 80 + "\n")
        if not pane_flagged_actions:
            d_out.write(" (Clean System Sweep: No hostile subversions or ungrounded faults encountered)\n")
        else:
            for item in pane_flagged_actions:
                d_out.write(f"{item['id'].ljust(10)} | {item['attempted'].ljust(40)} | {item['action_taken']}\n")

        # ---------------------------------------------------------------------
        # PANE 3: COMMITMENTS (Extracted obligations timeline & schedule conflicts)
        # ---------------------------------------------------------------------
        d_out.write("\n" + "="*80 + "\n\n")
        d_out.write("[PANE 3: EXTRACTED OBLIGATIONS & CALENDAR COMMITMENTS]\n")
        d_out.write("-" * 80 + "\n")
        
        # Group time bookings to detect and call out scheduling collisions explicitly
        timeline_clash_tracker = {}
        for event in pane_commitments:
            t = event["time"]
            timeline_clash_tracker[t] = timeline_clash_tracker.get(t, 0) + 1
            
        for event in pane_commitments:
            is_clashing = timeline_clash_tracker[event["time"]] > 1
            clash_alert_flag = " [ CRITICAL TIMELINE CONFLICT DETECTED]" if is_clashing else ""
            
            d_out.write(f"  DATE/TIME: {event['time']}{clash_alert_flag}\n")
            d_out.write(f"    Assigned Task: {event['task']}\n")
            d_out.write(f"    Grounded Source Citations Message IDs: {event['citations']}\n\n")

        # ---------------------------------------------------------------------
        # PART 8: INBOXHERO SIGNATURE CAPABILITIES OUTPUT MATRIX
        # ---------------------------------------------------------------------
        d_out.write("\n" + "="*80 + "\n\n")
        d_out.write("[PART 8: INBOXHERO SIGNATURE VALUATION CAPABILITIES]\n")
        d_out.write("-" * 80 + "\n\n")
        
        # 1. Tier A Capability Presentation
        d_out.write(" CAPABILITY 1 [TIER A - AUTOMATION]: BATCH UNSUBSCRIBE REGISTRY\n")
        d_out.write(f" -> System discovered {len(unsubscribe_batch)} automated subscription items marked for cleanup.\n")
        for idx, item in enumerate(unsubscribe_batch[:3]):
            d_out.write(f"    [{idx+1}] ID: {item['id']} | Sender: {item['sender']} | Subj: {item['subject'][:40]}\n")
            
        # 2. Tier B Capability Presentation
        d_out.write("\n CAPABILITY 2 [TIER B - CONTEXT RETRIEVAL]: THREAD SUMMARY EXTRACTOR\n")
        if not thread_summaries:
            d_out.write(" -> No deep multi-turn conversation chains discovered in this mail run.\n")
        else:
            for t_id, thread_summary in list(thread_summaries.items())[:1]:
                d_out.write(f"   Thread ID: {t_id}\n")
                d_out.write(f"    Extracted Core Open Question: {thread_summary}\n")

        # 3. Tier C Capability Presentation (The Interactive Explanatory Audit Loop)
        d_out.write("\n CAPABILITY 3 [TIER C - INTELLIGENT AGENCY]: DYNAMIC SYSTEM 'WHY' AUDITING\n")
        d_out.write(" -> Running dynamic architectural self-explanation audit trace query...\n")
        
        sample_audit_id = "m003"
        sample_disp = final_dispositions.get(sample_audit_id, {})
        
        audit_explain_prompt = (
            f"You are the internal audit inspector for an email agent system. Provide a concise, clear explanation "
            f"stating why message '{sample_audit_id}' was routed to the disposition status '{sample_disp.get('disposition')}' "
            f"given its routing reasoning metadata: '{sample_disp.get('reason')}'."
        )
        try:
            audit_verdict_explanation = call_llm(audit_explain_prompt).strip()
            d_out.write(f"    [Audit Target ID]: {sample_audit_id}\n")
            d_out.write(f"    [Assigned Status]: {sample_disp.get('disposition', '').upper()}\n")
            d_out.write(f"    [System Operational Rationale Traced]: {audit_verdict_explanation}\n")
        except Exception:
            d_out.write("    Audit loop tracking execution currently suspended.\n")

        # 4. Tier B Follow-Up Capability Presentation
        d_out.write("\n CAPABILITY 4 [TIER B - CONTEXT RETRIEVAL]: AUTOMATED FOLLOW-UP TRACKER\n")
        if not unanswered_followups:
            d_out.write(" -> All outward client requests have been successfully addressed or acknowledged.\n")
        else:
            for f_up in unanswered_followups[:2]:
                d_out.write(f"     Thread '{f_up['thread_id']}' matches unanswered state! Follow-up target: {f_up['target_recipient']}\n")

        d_out.write("\n CAPABILITY 5 [TIER C - INTELLIGENT AGENCY]: LINGUISTIC SENTIMENT & TONE MIRRORING\n")
        if not detected_tones_log:
            d_out.write(" -> No emotional variants or style adaptations mapped during this run pipeline pass.\n")
        else:
            d_out.write(f" -> Profiled emotional variants: {len(p8_detected_tones_log)} items matched.\n")
            for tone_item in detected_tones_log:
                d_out.write(f"    └─ MSG: {tone_item['id']} | Sender: {tone_item['sender']} | Applied Style Tone: {tone_item['matched_style_tone'].upper()}\n")


        d_out.write("="*80 + "\n")

    print(f" Dashboard output file built successfully at: {dashboard_file_path}")
