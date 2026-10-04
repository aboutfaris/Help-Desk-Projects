# osTicket: Prerequisites and Installation

Install the open-source help desk ticketing system osTicket on a Windows 10 virtual machine in Azure, using IIS, PHP, MySQL, and HeidiSQL. osTicket collects requests from email, phone, and web forms into one multi-user web interface where agents manage, organize, and archive them.

## What you'll use

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Internet Information Services (IIS)
- HeidiSQL
- Windows 10 (21H2)
- osTicket installation files ([download folder](https://drive.google.com/drive/u/0/folders/1APMfNyfNzcxZC6EzdaNfdZsUwxWYChf6))

## Prerequisites

- An Azure subscription

## Steps

### Part 1: Create the VM

1. In the Azure portal, create a resource group named `osTickets` in East US. Create every later resource in the same region.
2. Create a virtual machine in that resource group:
   - Name: `VM-osTicket`
   - Region: East US
   - Image: Windows 10 Pro, version 21H2
   - Size: 4 vCPUs (Standard D4s v3, 16 GiB memory)
   - Username and password: pick your own and write them down (for example, username `labuser`). Use a strong, unique password in any real deployment.

   Expected result: the resource group lists the VM along with the virtual network, public IP address, network security group, and network interface Azure created for it, all in East US.

3. Open the VM's Overview page and note its public IP address (`<vm-public-ip>`).

   Expected result: Status shows Running and Operating system shows Windows (Windows 10 Pro).

4. On your computer, open Remote Desktop Connection, enter `<vm-public-ip>`, click Connect, and sign in with the VM credentials.

### Part 2: Enable IIS with CGI

5. On the VM, open the Start menu and search for "Turn Windows features on or off".
6. Expand Internet Information Services > World Wide Web Services > Application Development Features.
7. Check CGI and click OK.

   Expected result: Internet Information Services, Web Management Tools, and World Wide Web Services show partially selected boxes, and CGI is checked.

### Part 3: Install PHP, MySQL, and osTicket

8. From the installation files, install these in order:
   - PHP Manager for IIS (`PHPManagerForIIS_V1.5.0.msi`)
   - IIS Rewrite Module (`rewrite_amd64_en-US.msi`)
9. Create the folder `C:\PHP` and unzip PHP 7.3.8 (`php-7.3.8-nts-Win32-VC15-x86.zip`) into it.
10. Install `VC_redist.x86.exe`.
11. Install MySQL 5.5.62 (`mysql-5.5.62-win32.msi`) and set a root password. Write it down.
12. Extract osTicket into `C:\inetpub\wwwroot` and rename the extracted `upload` folder to `osTicket`.

### Part 4: Configure PHP in IIS

13. Open IIS Manager as an administrator.
14. In PHP Manager, register PHP using `C:\PHP\php-cgi.exe`.
15. In PHP Manager, enable these extensions: `php_imap.dll`, `php_intl.dll`, and `php_opcache.dll`.
16. Reload IIS Manager and go to Sites > Default Web Site > osTicket.
17. In the right-hand panel, click Browse *:80.

    Expected result: the osTicket installer opens in the browser.

18. Go to `C:\inetpub\wwwroot\osTicket\include\` and rename `ost-sampleconfig.php` to `ost-config.php`.
19. Right-click `ost-config.php`, open Properties > Security > Advanced, and click Disable inheritance.
20. Remove the existing permissions and grant Everyone access. This is a lab-only setting; use least-privilege permissions in production.

### Part 5: Create the database

21. Install HeidiSQL from the installation files ([setup notes](https://docs.google.com/document/d/1WovrX2DaS9xkfaSr4LXyB4YnnWpXIgPCMMbbfgHmGVw/edit)).
22. Open HeidiSQL and create a new session with user `root` and the MySQL password from step 11.
23. Connect to the session and create a database named `osTicket`.

### Part 6: Finish the installer

24. Return to the osTicket installer in the browser and give your help desk a name.
25. Enter the database settings:
    - MySQL Database: `osTicket`
    - MySQL Username: `root`
    - MySQL Password: the password from step 11
26. Click Install Now.

## What I learned

- osTicket on Windows needs IIS with CGI, PHP registered through PHP Manager, and a MySQL database.
- Keeping all Azure resources in one resource group and region makes the lab easy to manage and clean up.
- Open permissions on `ost-config.php` are only for setup; lock them down afterward.

## Next steps / cleanup

- Configure roles, agents, SLAs, and help topics: see [osTicket post-install configuration](../02-osticket-post-installation-configuration/)
- Work a ticket end to end: see [osTicket ticket lifecycle](../03-osticket-ticket-lifecycle-examples/)
- When you finish the series, delete the `osTickets` resource group to stop charges.
