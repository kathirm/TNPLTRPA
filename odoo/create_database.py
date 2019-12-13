
import erppeek

DATABASE = 'TERAFASTNETWORKS'
SERVER = 'http://10.6.7.85:8069'
ADMIN_PASSWORD = 'abcd123'

client = erppeek.Client(server=SERVER)

if not DATABASE in client.db.list():

    print("The database does not exist yet, creating one!")
    client.create_database(ADMIN_PASSWORD, DATABASE)
 
else:

    print("The database " + DATABASE + " already exists.")
"""

client = erppeek.Client(SERVER, DATABASE, 'admin', 'admin')
proxy = client.model('ir.module.module')
installed_modules = proxy.browse([('state', '=', 'installed')])
for module in installed_modules:
        print('Installed module: ' + module.name)

modules = client.modules('sale', installed=False)
if 'sale' in modules['uninstalled']:
    client.install('sale')
    print('The module sale has been installed!')
"""
