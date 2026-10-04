# osTicket: Post-Install Configuration

Configure a fresh osTicket install so it is ready for real tickets: roles, departments, teams, user registration, agents, users, SLAs, and help topics.

## What you'll use

- Microsoft Azure virtual machine running Windows 10 (21H2)
- Remote Desktop
- Internet Information Services (IIS) hosting osTicket

## Prerequisites

- osTicket installed and reachable at `http://localhost/osTicket/scp/` on the VM: see [osTicket prerequisites and installation](https://github.com/aboutfaris/osticket_prereqs)
- Logged in to osTicket as the admin account created during install

Most settings live in the Admin Panel. If the header link reads "Admin Panel", click it to switch from the Agent Panel. Names below are examples; use any names you like.

## Steps

### Part 1: Roles

1. Go to Admin Panel > Agents > Roles.

   Expected result: four default roles are listed: All Access, Expanded Access, Limited Access, and View only.

2. Click Add New Role and name it `Supreme Admin`.
3. Open the Permissions tab and check every permission on the Tickets, Tasks, and Knowledgebase sub-tabs (Assign, Close, Create, Delete, Edit, Edit Thread, Link, Mark as Answered, Merge, Post Reply, Refer, Release, Transfer, and so on).
4. Click Add Role.

### Part 2: Departments

5. Go to Admin Panel > Agents > Departments and click Add New Department.
6. On the Settings tab, set Parent to Top-Level Department, Name to `System Administrators`, Status to Active, and Type to Public. Leave the other fields at their defaults.
7. Click Create Dept.

### Part 3: Teams

8. Go to Admin Panel > Agents > Teams and click Add New Team.
9. Create a team named `Level II Support`.

   Expected result: the Teams list shows Level I Support (a default team) and Level II Support, both Active.

### Part 4: User registration

10. Go to Admin Panel > Settings > Users and open the Settings tab.
11. Under Authentication Settings, check Registration Required ("Require registration and login to create tickets") and set Registration Method to Public (anyone can register).
12. Click Save Changes.

### Part 5: Agents

13. Go to Admin Panel > Agents > Agents and click Add New Agent.
14. On the Account tab, enter the name `Layla Mahmoud`, an email (for example, `<agent-email>`), and a username.
15. Click Set Password. Clear "Send the agent a password reset email", enter a password, and clear "Require password reset at next login".
16. On the Access tab, set Primary Department to `System Administrators` and the role to `Supreme Admin`.
17. Click Create.

    Expected result: the agent is created. If Primary Department or its role is empty, osTicket shows "Unable to add this agent" with "Department is required" and "Role for primary department is required".

18. Repeat steps 13 to 17 for a second agent, `Jamari`, with the Maintenance department.

### Part 6: Users

19. Switch to the Agent Panel and go to Users > User Directory.
20. Click Add User. In the "Lookup or create a user" dialog, enter an email address and full name (both required), then click Add User.
21. Repeat for a second user.

    Expected result: the User Directory lists Byleth and Dimitri alongside the default osTicket Support user.

### Part 7: SLAs

22. In the Admin Panel, go to Manage > SLA and click Add New SLA Plan.
23. Set Name to `Sev-A`, Status to Active, Grace Period to `1` hour, and Schedule to 24/7. Click Add Plan.
24. Repeat for the other two plans:

    | Name | Grace period (hours) | Schedule |
    |---|---|---|
    | Sev-A | 1 | 24/7 |
    | Sev-B | 4 | 24/7 |
    | Sev-C | 8 | Business hours |

    Expected result: "Successfully added a SLA plan", and the list shows Default SLA (18 hours), Sev-A (1), Sev-B (4), and Sev-C (8), all Active.

### Part 8: Help topics

25. Go to Admin Panel > Manage > Help Topics.

    Expected result: four default topics are listed: Feedback, General Inquiry, Report a Problem, and Report a Problem / Access Issue.

26. Click Add New Help Topic and create each of these:
    - Business Critical Outage
    - Personal Computer Issues
    - Equipment Request
    - Password Reset
27. Open Business Critical Outage and go to the New ticket options tab. Set Department to `System Administrators`, Status to Open, Priority to Emergency, SLA Plan to `Sev-A`, and Auto-assign To to `Level II Support`. Click Save Changes.

    Expected result: the Help Topics list shows all eight topics, Active and Public.

## What I learned

- Roles, departments, and teams control who sees and works each ticket.
- SLAs set response deadlines; tying a help topic to an SLA and priority automates triage.
- osTicket validates required agent fields (department and role) before it saves.

## Next steps

- Work a ticket from intake to resolution: see [osTicket ticket lifecycle](https://github.com/aboutfaris/osTicket)
- Review the install: see [osTicket prerequisites and installation](https://github.com/aboutfaris/osticket_prereqs)
