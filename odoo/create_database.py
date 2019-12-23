
import erppeek, sys

DATABASE = 'TERAFASTWORKS'
SERVER = 'http://10.6.7.85:8069'
ADMIN_PASSWORD = 'abcd123'

#module_name = ["hr_attendance", "website_slides", "website", "hr_holidays", "survey", "lunch", "hr_recruitment", "hr_expense"] 

module_name = ["hr_attendance", "website_slides", "website", "hr_holidays", "survey", "lunch", "hr_recruitment", "hr_expense", "hr_skills"] 

client = erppeek.Client(server=SERVER)

if not DATABASE in client.db.list():

    print("The database does not exist yet, creating one!")
    client.create_database(ADMIN_PASSWORD, DATABASE)
 
else:

    print("The database " + DATABASE + " already exists.")


client = erppeek.Client(SERVER, DATABASE, 'admin', 'abcd123')
proxy = client.model('ir.module.module')
installed_modules = proxy.browse([('state', '=', 'installed')])
for module in installed_modules:
        print('Installed module: ' + module.name)


for mdle_nme in module_name:
    modules = client.modules(mdle_nme, installed=False)
    if mdle_nme in modules['uninstalled']:
        client.install(mdle_nme)
        print('The module sale has been installed!', mdle_nme)
        continue
"""
modules = client.modules(module_name, installed=False)
if module_name in modules['uninstalled']:
    client.install(module_name)
    print('The module sale has been installed!')
"""
