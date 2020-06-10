import erppeek, sys
DATABASE = sys.argv[1] 
SERVER = 'http://18.229.201.107:8069'
ADMIN_PASSWORD = 'master_password'

module_name = ["crm"]
client = erppeek.Client(server=SERVER)
if not DATABASE in client.db.list():
    print("The database does not exist yet, creating one!")
    client.create_database(ADMIN_PASSWORD, DATABASE)#, lang='pt_BR')
else:
    print("The database " + DATABASE + " already exists.")


client = erppeek.Client(SERVER, DATABASE, 'admin', 'admin')
proxy = client.model('ir.module.module')
installed_modules = proxy.browse([('state', '=', 'installed')])
for module in installed_modules:
    print('Installed module: ' + module.name)

for mdle_nme in module_name:
    modules = client.modules(mdle_nme, installed=False)
    if mdle_nme in modules['uninstalled']:
	client.install(mdle_nme)
	print('The module sale has been installed!', mdle_nme)
