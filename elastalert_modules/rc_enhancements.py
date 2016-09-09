from elastalert.enhancements import BaseEnhancement

class InvCorrEnhancement(BaseEnhancement):

    # The enhancement correlates the IP of the host with the vCenter who manages it
    def process(self, match):
        # Open a file on the disk.
        f = open("/opt/runecast/invsum", "r")
        data=[]
        for l in f.readlines():
            ll = l.split(',')
            data.append(ll)
        f.close();

        v1 = 0
        found = matched = 0
        for i in data:
            v2 = 0
            for k2 in data:
                #if the Inventory summary file has duplicate IPs, use the hostname to correlate
                if i[0] == k2[0]:
                    if v1 != v2:
                        if 'hostname' in match:
                            if match['hostname'] == i[1]:
                                match['vCenter'] = i[3]
                                match['host_moid'] = i[2]
                                match['vCenter_moid'] = i[4]
                                match['host_licensed'] = i[5]
                                found = matched = 1
                v2 += 1
            if found == 0:
                if 'host' in match:
                        if match['host'] == i[0]:
                            match['vCenter'] = i[3]
                            match['host_moid'] = i[2]
                            match['vCenter_moid'] = i[4]
                            match['host_licensed'] = i[5]              
                            found = matched = 1
            v1 += 1
        if matched == 0:
            match['vCenter'] = 'Unknown'
            match['host_moid'] = 'Unknown'
            match['vCenter_moid'] = 'Unknown'
            match['host_licensed'] = 'Unknown'
