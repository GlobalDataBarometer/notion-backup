# Notion Backup

This repo is a fork of  the backup scripts for OpenOwnership's Notion workspace, updated to run for the Global Data Barometer.. 

The code runs via a Github Action, which is scheduled to run daily, as well as whenever code is pushed to the repository.

It now contains backup routines for:

* Notion
* The survey tool Postgres database
## Running the code locally

The code to run the backup lives in /notion/export_notion.py. To run it:

1. Install requirements

   ```shell
   git clone git@github.com:openownership/backup.git
   cd backup
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   touch .env
   ```

2. Set your credentials in the `.env` file:

   ```shell
   NOTION_SPACE_ID=1234-56789-abcdef
   NOTION_EMAIL=notion@example.com
   NOTION_PASSWORD=password
   GDRIVE_ROOT_FOLDER_ID=<get-the-folder-id-from-gdrive>
   GDRIVE_SERVICE_ACCOUNT=<get-the-service-account-info-from-1password>
   GDRIVE_ROOT_FOLDER_ID_PG=<get-the-folder-id-from-gdrive>
   PG_CONNECTION=<get-the-postgress-connection-string-with-password-in-from-digital-ocean>
   ```

3. Run the python module: `python notion`

4. Run the python module: `python postgres`

You can find the space id by logging into Notion as the tech+notion user and then
inspecting one of the ajax requests that notion's front end makes in the
chrome dev console. It's often found in the body of responses from Notion.

Note that this assumes you have a email/password user account, not one through
Google SSO.

## Github Action config

The Github Action is configured via secrets set up in [the repo settings](https://github.com/openownership/notion-backup/settings/secrets).
These are then set as env vars for the python script to use.

For a public repo, there must be edits every 60 days for the action to keep running. 
