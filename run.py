import json
import os


def process_inbox():

    #Dynamically finding folder where .py script is saved and anchoring that path to inbox.json
    script_directory = os.path.dirname(os.path.abspath(__file__))
    inbox_file_path = os.path.join(script_directory, "inbox.json")
    
    # Anchoring outbox directory structure
    outbox_directory = os.path.join(script_directory, "outbox")
    os.makedirs(outbox_directory, exist_ok=True)

    with open(inbox_file_path, 'r', encoding='utf-8') as file:
        emails=json.load(file)

    print(f"Loaded {len(emails)} emails from inbox")

    #PART 3: Building Chronological thread maps (Thread Walking Prep)
    thread_map = {}
    for email in emails:
        t_id = email.get("thread_id", "orphan")
        if t_id not in thread_map:
            thread_map[t_id] = []
        thread_map[t_id].append(email)
        
    # Sort every thread's emails from oldest to newest based on timestamp
    for t_id in thread_map:
        thread_map[t_id].sort(key=lambda x: x.get("timestamp", ""))

    final_dispositions={}

    count={"archive":0, "reply":0,"defer":0,"delegate":0,"escalate":0}

    rule_processed_count=0
    llm_required_count=0

    #Looping through emails to separate Workflow content and Agent content
    for email in emails:
        msg_id=email.get("id")
        sender=email.get("from","").lower()
        subject=email.get("subject","").lower()
        body=email.get("body","").lower()

        #ESCALATE-detection (Security risks)
        if "security" in subject or "unauthorized" in body or"password" in subject:
            final_dispositions[msg_id]={
                "disposition":"escalate",
                "reason":"Potential security risk or administrative account alert flagged for review",
                "requires_llm": True
            }
            count["escalate"]+=1
            llm_required_count+=1

        #ARCHIVE-detection (automated noise)
        elif ("no-reply" in sender or "noreply" in sender or "notifications" in sender or
              any(k in subject or k in body[:100] for k in ["storage full", "unread messages", "usage", "receipt",
                                                             "invoice", "digest", "newsletter", "shipped", "package",
                                                               "membership","bill","weekly summary","monthly summary",
                                                               "top 5"])):
            final_dispositions[msg_id]={
                "disposition":"archive",
                "reason":"Automated alerts",
                "requires_llm": False
            }
            count["archive"]+=1
            rule_processed_count+=1

        #DEFER-detection (time commitments, constraints, scheduling)
        elif any(k in subject or k in body for k in ["meeting", "deadline", "schedule", "calendar", "tomorrow", "staging"]):
            final_dispositions[msg_id] = {
                "disposition": "defer",
                "reason": "Time-sensitive operational dependency or coordination request held for context compilation.",
                "requires_llm": True
            }
            count["defer"] += 1
            llm_required_count += 1


        # DELEGATE-detection (external task handoff)
        elif any(k in body for k in ["forward to", "assign to", "cc'd", "handle this"]):
            final_dispositions[msg_id] = {
                "disposition": "delegate",
                "reason": "Operational request indicating handoff or division of labor constraints.",
                "requires_llm": True
            }
            count["delegate"] += 1
            llm_required_count += 1

        #REPLY-detection(direct interpersonal communication)
        else:
            final_dispositions[msg_id] = {
                "disposition": "reply",
                "reason": "Direct peer communication queued for standard context generation.",
                "requires_llm": True
            }
            count["reply"] += 1
            llm_required_count += 1


    print(" FIVE-TIER DISPOSITION METRICS:")
    for disp_type, ct in count.items():
        print(f"   • {disp_type.upper().ljust(10)} : {ct} messages")
    print(f" Total Accounted For    : {len(final_dispositions)} / {len(emails)}")
    print(f" Handled by Rules   : {rule_processed_count} messages")
    print(f" Pending LLM Engine  : {llm_required_count} messages")

    if len(final_dispositions) == len(emails):
        print(" Verification Check PASSED: 100% of messages have a unique disposition assigned")
    else:
        print(" Verification Check FAILED: Operational drop detected")

        #INSPECT TOP MESSAGES BY DISPOSITION
    print("\nDATA INSPECTION: TOP MESSAGES FOR REVIEW\n")
    
    # Grouping the actual email objects by their assigned disposition
    grouped_emails = {"escalate": [], "defer": [], "reply": [], "delegate": [], "archive": []}
    
    for email in emails:
        msg_id = email.get("id")
        disp_info = final_dispositions.get(msg_id, {})
        disp_name = disp_info.get("disposition")
        if disp_name in grouped_emails:
            grouped_emails[disp_name].append(email)
            
    # Print the top 5 (or fewer) messages for each category
    for disp_type, email_list in grouped_emails.items():
        print(f"Category: {disp_type.upper()} ({len(email_list)} messages total)")
        print("-" * 50)
        
        if not email_list:
            print("   (No messages in this category)")
            continue
            
        # Slice to show up to the first 5 emails
        for index, email in enumerate(email_list[:5]):
            print(f"   [{index + 1}] ID: {email.get('id')} | From: {email.get('from')}")
            print(f"       Subject: {email.get('subject')}")


 #PART 3 ADDITION:CONTEXTUAL THREAD-WALKING DEMO

    print("\n\nEVALUATING HISTORICAL CONTEXT VIA THREAD WALKING\n")

    
    # We choose the specific 'm003' email from Sam responding about staging credentials
    target_msg_id = "m003"
    target_email = next((e for e in emails if e.get("id") == target_msg_id), None)
    
    if target_email:
        t_id = target_email.get("thread_id")
        full_thread = thread_map.get(t_id, [])
        
        # Walk thread: gather all messages in this thread that happened BEFORE the target email
        historical_context = []
        context_ids = []
        
        for msg in full_thread:
            if msg.get("timestamp") < target_email.get("timestamp"):
                historical_context.append(msg)
                context_ids.append(msg.get("id"))
                
        print(f"  Target Message Identified: {target_msg_id}")
        print(f"   From:    {target_email.get('from')}")
        print(f"   Subject: {target_email.get('subject')}")
        print(f"   Body:    {target_email.get('body')}")
        print(f"\n Thread-Walking Retrieval Results:")
        print(f"   • Cited Context Message IDs (Checked Against Mail Store): {context_ids}")
        
        for idx, ctx_msg in enumerate(historical_context):
            print(f"     [{idx+1}] ID: {ctx_msg.get('id')} | Snippet: {ctx_msg.get('body')[:70]}...")
            
        # Create a grounded reply object matching Part 3 requirements
        grounded_reply = {
            "reply_to_id": target_msg_id,
            "citations": context_ids,
            "draft_body": "Thanks Sam. I checked the earlier report about staging throwing 500s. I am pointing the worker to the new AMQP URL and restarting it now."
        }
        
        # Write to the required outbox file structure
        output_file_path = os.path.join(outbox_directory, f"reply_{target_msg_id}.json")
        with open(output_file_path, 'w', encoding='utf-8') as out_f:
            json.dump(grounded_reply, out_f, indent=2)
            
        print(f"\nGrounded output schema successfully written to: outbox/reply_{target_msg_id}.json")
    else:
        print(f"Target message {target_msg_id} not found in inbox mapping.")


if __name__ == "__main__":

    process_inbox()

