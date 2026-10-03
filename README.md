<p align="center">
<img src="https://i.imgur.com/Clzj7Xs.png" alt="osTicket logo"/>
</p>

# osTicket - Prerequisites and Installation

Hi, I'm Faris, an IT professional. Welcome to my first tutorial on setting up osTicket. This tutorial outlines the prerequisites and installation of the open-source help desk ticketing system osTicket.

## What Is osTicket?

osTicket is a widely used open-source support ticket system. It integrates inquiries created via email, phone, and web-based forms into a simple, easy-to-use multi-user web interface. Manage, organize, and archive all your support requests and responses in one place while giving your customers the accountability and responsiveness they deserve.


## Environments and Technologies Used

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Internet Information Services (IIS)
- HeidiSQL

## Operating Systems Used

- Windows 10 (21H2)

## List of Prerequisites

- Azure Virtual Machine
- osTicket installation files

## Installation Steps

![Create resource group](https://user-images.githubusercontent.com/109401839/212542603-e23e4232-fa2d-461d-9f9e-9da2ca6f5c73.png)

First, create a Resource Group (RG) in Microsoft Azure. Think of the resource group as a folder. Name this resource group "osTickets". I used US East for my RG; take note of which region you use since future resources will be created in the same region.

![Create virtual machine](https://user-images.githubusercontent.com/109401839/212542800-61c916ab-94a8-4e5f-bc6b-8ccdbe768612.png)

Now create a virtual machine under the RG. As before, set the VM region to US East. We'll use Windows 10 with 4 vCPUs, and name this VM "VM-osTicket".

Create a username and password for your VM; you'll log in to it like a regular computer, so take notes to avoid forgetting your login credentials. For this demonstration we use the username `labuser` and a simple lab-only password — in a real deployment, always use a strong, unique password.

Now that our machine is ready, we will connect to it using Remote Desktop Connection. Before that, find the VM's public IP address:

1. Open the VM's overview page in the Azure Portal.
2. Note the public IP address shown there (for example, `<your-vm-public-ip>`).

This is the address you use to connect to the VM with Remote Desktop Connection:

1. Open "Remote Desktop Connection" on your local machine.
2. Enter the VM's public IP address.
3. Click **Connect**.

Now that we're connected, let's enable IIS (Internet Information Services). IIS is a Microsoft web server that runs on Windows and is used to exchange static and dynamic web content with internet users. It can host, deploy, and manage web applications using technologies such as ASP.NET and PHP.

Enable IIS with CGI support:

1. Open the Start menu and search for "Windows Features".
2. Expand **Internet Information Services** > **World Wide Web Services** > **Application Development Features**.
3. Check **CGI** and confirm.

![Enable IIS features](https://user-images.githubusercontent.com/109401839/212543578-18f011ed-b6e4-4d34-9a41-8093904acb3b.png)

Now [download](https://drive.google.com/drive/u/0/folders/1APMfNyfNzcxZC6EzdaNfdZsUwxWYChf6) the installation files needed for osTicket and HeidiSQL.

Head to the installation folders and:

- Download and install PHP Manager for IIS (`PHPManagerForIIS_V1.5.0.msi`)
- Download and install the Rewrite Module (`rewrite_amd64_en-US.msi`)
- Create a directory at `C:\PHP`
- Download PHP 7.3.8 (`php-7.3.8-nts-Win32-VC15-x86.zip`) and unzip its contents into `C:\PHP`
- Download and install `VC_redist.x86.exe`
- Download and install MySQL 5.5.62 (`mysql-5.5.62-win32.msi`)

Next, download osTicket and extract its contents to `C:\inetpub\wwwroot`. Rename the extracted "Upload" folder to "osTicket".

Register and configure PHP in IIS:

1. Open IIS Manager as an administrator.
2. Register PHP using the `C:\PHP` folder you created earlier.
3. In IIS Manager, open PHP Manager and enable the following three extensions: `php_imap.dll`, `php_intl.dll`, and `php_opcache.dll`.
4. Reload IIS Manager and navigate to **Sites > Default > osTicket**.
5. On the right-hand panel, click **Browse *:80** to open the osTicket web interface and confirm it loads.

Finish the osTicket configuration file setup:

1. Navigate to `C:\inetpub\wwwroot\osticket\include\`.
2. Find the file named `ost-sampleconfig.php` and rename it to `ost-config.php`.
3. Right-click the renamed file, open **Properties**, go to the **Security** tab, and click **Disable Inheritance**.
4. Remove the existing permissions and grant access to "Everyone" (lab-only setting; use least-privilege permissions in production).

### HeidiSQL

From the [installation files](https://drive.google.com/drive/u/2/folders/1APMfNyfNzcxZC6EzdaNfdZsUwxWYChf6), download and install [HeidiSQL](https://docs.google.com/document/d/1WovrX2DaS9xkfaSr4LXyB4YnnWpXIgPCMMbbfgHmGVw/edit). Then:

1. Open HeidiSQL.
2. Create a new session using the `root` MySQL account and the password you set during MySQL installation.
3. Connect to the session.
4. Create a database named "osTicket".

### Continue Setup in the Browser

Return to the osTicket web interface and name your helpdesk anything you like. Then continue the install wizard with:

- MySQL Database: `osTicket`
- MySQL Username: `root`
- MySQL Password: *(the password you set during MySQL installation)*
- Click **Install Now!**
