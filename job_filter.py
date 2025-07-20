JOB_KEYWORDS = ["MBA","internal assessment","semester","semesters","exam", "UTI","mutual fund", "index fund"]
    #"job", "career", "vacancy", "opportunity", "opening", "position", "hiring", "recruitment"

JOB_SENDER_EMAILS = [
    "director.dde@pondiuni.ac.in",
    "ddehelpdesk@pondiuni.ac.in",
    "noreply@samarth.edu.in",
    "ddeiaj25@pondiuni.ac.in",
    "utimf@kfintech.com"
   
]
 
def is_job_enquiry(email):
    # Check if email is from any of the specified senders
    if email['from']:
        sender = email['from'].lower()
        if any(job_sender in sender for job_sender in JOB_SENDER_EMAILS):
            return True
    
    # Check for keywords in content
    content = f"{email['subject']} {email['snippet']} {email['body']}".lower()
    return any(keyword in content for keyword in JOB_KEYWORDS)