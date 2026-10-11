# InfoTech Set
Hands-on IT infrastructure builds and reference designs: a working osTicket help desk on Azure, plus a secure remote worker network design.

![InfoTech Set architecture](assets/architecture.png)
The osTicket diagram shows the Azure VM and web stack from section 01, the configuration from section 02, and the ticket lifecycle from section 03.

| Section | What you'll build | Folder |
|---|---|---|
| osTicket: Prerequisites and Installation | An Azure Windows 10 VM running IIS, PHP, MySQL, and a fresh osTicket install | [01-osticket-prerequisites-and-installation](01-osticket-prerequisites-and-installation/) |
| osTicket: Post-Installation Configuration | Roles, departments, teams, agents, users, SLAs, and help topics | [02-osticket-post-installation-configuration](02-osticket-post-installation-configuration/) |
| osTicket: Ticket Lifecycle Examples | One outage ticket worked from intake through resolution | [03-osticket-ticket-lifecycle-examples](03-osticket-ticket-lifecycle-examples/) |
| Remote Worker Network | A reference design for a secure work-from-home network: five isolated VLANs, a single NAT edge, and a private mesh VPN | [04-remote-worker-network](04-remote-worker-network/) |

## How to use
Sections 01 through 03 are standalone follow-along guides, each with its own prerequisites, numbered steps, and expected results. Work them in order for the full help desk build, or jump into any one on its own. Delete the Azure resource group when you finish to stop charges.

Section 04 is a reference design rather than a follow-along lab. It documents a segmented home network for a remote worker and includes the script that generates its diagram.

## License
Code and scripts in this repository are licensed under the MIT License (see [LICENSE](LICENSE)). Written guides and diagrams are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Third-party material keeps its original license and is excluded from both.
