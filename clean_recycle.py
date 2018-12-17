import sys
import urllib3
from pyral import Rally, rallyWorkset

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
args = [arg for arg in sys.argv[1:] if arg not in options]
server, user, password, apikey, workspace, project = rallyWorkset(options)

rally = Rally(server, user, password, workspace=workspace, project=project, verify_ssl_cert=False)
rally.enableLogging(dest=b'pyral_clear_recycle.log', attrget=True)

recycle_bin_entries = rally.get('RecycleBinEntry', fetch="ObjectID")
print('Found {} RecycleBin Items'.format(recycle_bin_entries.resultCount))

i = 0
for recycle_bin_entry in recycle_bin_entries:
    rally.delete('RecycleBinEntry', recycle_bin_entry.ObjectID)
    my_objects = rally.get('RecycleBinEntry', fetch="ObjectID", query="(ObjectID = {})".format(recycle_bin_entry.ObjectID))
    for my_object in my_objects:
        print("Object ID: {}".format(my_object.ObjectID))
              
    i += 1
    if (i % 100 == 0 or i == recycle_bin_entries.resultCount):
        print("{i} / {result_count}".format(i=i, result_count=recycle_bin_entries.resultCount))

print('Finished cleanup')
