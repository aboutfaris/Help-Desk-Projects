# osTicket: Ticket Lifecycle from Intake to Resolution

Follow one help desk ticket through osTicket from intake to resolution. The agent Layla, created in the post-install lab, logs in, opens a ticket for a reported outage, and works it through to close.

## What you'll use

- Microsoft Azure virtual machine running Windows 10 (21H2)
- Remote Desktop
- Internet Information Services (IIS) hosting osTicket

## Prerequisites

- osTicket installed: see [osTicket prerequisites and installation](https://github.com/aboutfaris/osticket_prereqs)
- Roles, departments, teams, agents, users, SLAs, and help topics configured: see [osTicket post-install configuration](https://github.com/aboutfaris/osTicket-Post-Install-Configuration)

## Steps

The lifecycle has four stages: intake, assignment and communication, working the issue, and resolution. Set the ticket priority from the help topic:

| Help topic | Priority |
|---|---|
| Business Critical Outage | Emergency |
| Personal Computer Issues | High |
| Equipment Request | Normal |
| Password Reset | Low |

### Part 1: Intake

1. Open the osTicket staff login page (`http://localhost/osTicket/scp/login.php` on the VM).
2. Enter the agent username (for example, `<agent-username>` for Layla) and password, then click Log In.

   Expected result: the Agent Panel opens with the Dashboard, Users, Tasks, Tickets, and Knowledgebase tabs, and the header reads "Welcome, Layla."

3. Go to Tickets > New Ticket.
4. Fill in the form for the reported outage (a user cannot reach the company website from their phone or desktop):
   - User: the reporting user (for example, `<user-email> - Dimitri`)
   - Ticket Source: Email
   - Help Topic: Business Critical Outage
   - Department: Maintenance
   - SLA Plan: Sev-A (1 hour)
   - Due Date: a date and time in the future (osTicket rejects a past due date with "Due date must be in the future")
   - Assign To: the agent who will work the ticket (Jamari in this lab)
   - Issue Summary: `Entire website is down.`
   - Details: `Various customers are reporting that they cannot access the main website through their phones and desktop.`
   - Priority Level: Emergency
   - Ticket Status: Open
5. Click Open.

   Expected result: the ticket is created with Emergency priority and the Sev-A SLA. If a required field is missing, osTicket shows "Missing or invalid data" at the top and marks the field in red.

### Part 2: Assignment and communication

6. Open the ticket from Tickets > Open and confirm the assignee, department, and SLA.
7. Post a reply to the user acknowledging the outage and giving an expected update time within the Sev-A window.

### Part 3: Working the issue

8. Add internal notes as you troubleshoot, and post updates to the user as the status changes.

### Part 4: Resolution

9. When the website is back up, post a final reply explaining the fix.
10. Set Ticket Status to Resolved and submit.

## What I learned

- Help topics drive priority and SLA, so an outage ticket starts with an Emergency, 1-hour clock.
- osTicket validates required fields and due dates before it creates a ticket.
- Timely replies and internal notes keep the user informed and leave an audit trail.

## Next steps

- Review the setup: [osTicket prerequisites and installation](https://github.com/aboutfaris/osticket_prereqs)
- Review the configuration: [osTicket post-install configuration](https://github.com/aboutfaris/osTicket-Post-Install-Configuration)
