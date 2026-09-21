import json
import os


def process_inbox():

    #Dynamically finding folder where .py script is saved and anchoring that path to inbox.json
    script_directory = os.path.dirname(os.path.abspath(__file__))
    inbox_file_path = os.path.join(script_directory, "inbox.json")

    with open(inbox_file_path, 'r', encoding='utf-8') as file:
        emails=json.load(file)

    print(f"Loaded {len(emails)} emails from inbox")

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

        #ESCALATE-detection
        if "security" in subject or "unauthorized" in body or"password" in subject:
            final_dispositions[msg_id]={
                "disposition":"escalate",
                "reason":"Potential security risk or administrative account alert flagged for review",
                "requires_llm": True
            }
            count["escalate"]+=1
            llm_required_count+=1

        #ARCHIVE-detection
        elif ("no-reply" in sender or "noreply" in sender or "notifications" in sender or
              any(k in subject or k in body[:100] for k in ["storage full", "unread messages", "usage", "receipt", "invoice", "digest", "newsletter", "shipped"])):
            final_dispositions[msg_id]={
                "disposition":"archive",
                "reason":"Automated alerts",
                "requires_llm": False
            }
            count["archive"]+=1
            rule_processed_count+=1

        #DEFER-detection
        elif any(k in subject or k in body for k in ["meeting", "deadline", "schedule", "calendar", "tomorrow", "staging"]):
            final_dispositions[msg_id] = {
                "disposition": "defer",
                "reason": "Time-sensitive operational dependency or coordination request held for context compilation.",
                "requires_llm": True
            }
            count["defer"] += 1
            llm_required_count += 1


        # DELEGATE-detection
        elif any(k in body for k in ["forward to", "assign to", "cc'd", "handle this"]):
            final_dispositions[msg_id] = {
                "disposition": "delegate",
                "reason": "Operational request indicating handoff or division of labor constraints.",
                "requires_llm": True
            }
            count["delegate"] += 1
            llm_required_count += 1

        #REPLY-detection
        else:
            final_dispositions[msg_id] = {
                "disposition": "reply",
                "reason": "Direct peer communication queued for standard context generation.",
                "requires_llm": True
            }
            count["reply"] += 1
            llm_required_count += 1


    print("FIVE-TIER DISPOSITION METRICS:")
    for disp_type, ct in count.items():
        print(f"   • {disp_type.upper().ljust(10)} : {ct} messages")
    print("-" * 60)
    print(f"Total Accounted For    : {len(final_dispositions)} / {len(emails)}")
    print(f"Handled by Rules   : {rule_processed_count} messages")
    print(f"Pending LLM Engine  : {llm_required_count} messages")
    print("-" * 60)

    if len(final_dispositions) == len(emails):
        print("Verification Check PASSED: 100% of messages have a unique disposition assigned!")
    else:
        print("Verification Check FAILED: Operational drop detected.")

if __name__ == "__main__":

    process_inbox()
