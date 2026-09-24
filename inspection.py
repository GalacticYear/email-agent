def terminal_inspection_reviews(emails, final_dispositions):
    """
    Renders the data inspection terminal breakdown blocks, grouping
    the top messages for rapid reviewer evaluation.
    """
    print("\nDATA INSPECTION: TOP MESSAGES FOR REVIEW\n")
    
    # Grouping email objects dynamically by assigned disposition category
    grouped_emails = {"escalate": [], "defer": [], "reply": [], "delegate": [], "archive": []}
    
    for email in emails:
        msg_id = email.get("id")
        disp_info = final_dispositions.get(msg_id, {})
        disp_name = disp_info.get("disposition")
        if disp_name in grouped_emails:
            grouped_emails[disp_name].append(email)
            
    # Print the top 5 (or fewer) messages for each category frame layout
    for disp_type, email_list in grouped_emails.items():
        print(f"Category: {disp_type.upper()} ({len(email_list)} messages total)")
        print("-" * 50)
        
        if not email_list:
            print("   (No messages in this category)")
            continue
            
        for index, mail in enumerate(email_list[:5]):
            print(f"   [{index + 1}] ID: {mail.get('id')} | From: {mail.get('from')}")
            print(f"       Subject: {mail.get('subject')}")
