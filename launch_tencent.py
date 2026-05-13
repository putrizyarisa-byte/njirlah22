import os
import json
import uuid
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models

SECRET_ID = "YOUR_TENCENT_SECRET_ID"
SECRET_KEY = "YOUR_TENCENT_SECRET_KEY"
REGION = "ap-singapore"

def get_client(service, version):
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    httpProfile = HttpProfile()
    httpProfile.endpoint = f"{service}.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    if service == "cvm":
        return cvm_client.CvmClient(cred, REGION, clientProfile)
    elif service == "vpc":
        return vpc_client.VpcClient(cred, REGION, clientProfile)

def setup_network():
    print("Mengecek jaringan (VPC & Subnet)...")
    client = get_client("vpc", "20170312")
    
    # Check for Default VPC
    req = vpc_models.DescribeVpcsRequest()
    req.Filters = [{"Name": "is-default", "Values": ["true"]}]
    resp = client.DescribeVpcs(req)
    
    vpc_id = None
    if len(resp.VpcSet) > 0:
        vpc_id = resp.VpcSet[0].VpcId
        print(f" Default VPC ditemukan: {vpc_id}")
    else:
        print(" Tidak ada Default VPC. Membuat baru...")
        req = vpc_models.CreateVpcRequest()
        req.VpcName = "NJIRLAH_VPC"
        req.CidrBlock = "10.0.0.0/16"
        resp = client.CreateVpc(req)
        vpc_id = resp.Vpc.VpcId
        print(f" VPC dibuat: {vpc_id}")
        
    # Check Subnet
    req = vpc_models.DescribeSubnetsRequest()
    req.Filters = [{"Name": "vpc-id", "Values": [vpc_id]}]
    resp = client.DescribeSubnets(req)
    
    subnet_id = None
    zone = "ap-singapore-3"
    if len(resp.SubnetSet) > 0:
        # Cari subnet di ap-singapore-3
        for sub in resp.SubnetSet:
            if sub.Zone == "ap-singapore-3":
                subnet_id = sub.SubnetId
                break
                
    if subnet_id is None:
        print(" Tidak ada Subnet di ap-singapore-3. Membuat baru...")
        req = vpc_models.CreateSubnetRequest()
        req.VpcId = vpc_id
        req.SubnetName = "NJIRLAH_SUBNET_SG3"
        req.CidrBlock = "10.0.2.0/24"
        req.Zone = "ap-singapore-3"
        resp = client.CreateSubnet(req)
        subnet_id = resp.Subnet.SubnetId
        print(f" Subnet dibuat: {subnet_id}")
    else:
        print(f" Subnet ditemukan: {subnet_id} ({zone})")
        
    return vpc_id, subnet_id, zone

def launch_instance(vpc_id, subnet_id, zone):
    print("\nMeluncurkan GPU Spot Instance...")
    client = get_client("cvm", "20170312")
    
    req = cvm_models.RunInstancesRequest()
    
    # Pengaturan dasar
    req.InstanceChargeType = "SPOTPAID"  # Spot instance untuk harga murah 70%
    req.Placement = cvm_models.Placement()
    req.Placement.Zone = zone
    
    # Gunakan instance GN7 (T4 GPU) yang tersedia
    req.InstanceType = "GN7.2XLARGE32" 
    
    # Image Ubuntu 22.04
    req.ImageId = "img-pi0ii46r"  # Standard Ubuntu 22.04
    
    req.VirtualPrivateCloud = cvm_models.VirtualPrivateCloud()
    req.VirtualPrivateCloud.VpcId = vpc_id
    req.VirtualPrivateCloud.SubnetId = subnet_id
    
    req.InternetAccessible = cvm_models.InternetAccessible()
    req.InternetAccessible.InternetChargeType = "TRAFFIC_POSTPAID_BY_HOUR"
    req.InternetAccessible.InternetMaxBandwidthOut = 100
    req.InternetAccessible.PublicIpAssigned = True
    
    # Password Random yang kuat
    pwd = f"NjirlahSS!{uuid.uuid4().hex[:8]}"
    req.LoginSettings = cvm_models.LoginSettings()
    req.LoginSettings.Password = pwd
    
    req.InstanceName = "Njirlah-GPU-Node"
    req.InstanceCount = 1
    
    try:
        resp = client.RunInstances(req)
        print("\n✅ SERVER GPU BERHASIL DILUNCURKAN!")
        print(f"Instance ID : {resp.InstanceIdSet[0]}")
        print(f"Password SSH: {pwd}")
        print("\nTunggu sekitar 2 menit lalu jalankan perintah ini:")
        print(f"ssh ubuntu@<IP_PUBLIK_TENCENT>")
    except Exception as e:
        print("\nGAGAL MELUNCURKAN SERVER!")
        print(repr(e))

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        v_id, s_id, z = setup_network()
        launch_instance(v_id, s_id, z)
    except Exception as e:
        print(f"Error: {repr(e)}")
