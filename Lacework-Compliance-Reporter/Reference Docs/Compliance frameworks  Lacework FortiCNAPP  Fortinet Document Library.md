The tables on this page list all available compliance frameworks that can be used within Lacework FortiCNAPP's cloud security posture management (CSPM) platform.

<table><colgroup><col> <col></colgroup><tbody><tr><td><img src="https://fortinetweb.s3.amazonaws.com/docs.fortinet.com/v2/resources/d7ba04c4-7ae3-11ef-899d-368457bb1542/images/3ccdce253596f81fffa3a974a15d3df1_Icon-Light-Bulb.png" alt="Note" title="Note"></td><td><h5>Automated vs Manual Policies</h5><p>For some Framework recommendations, it is not possible to automate the policy checks. These policies are <i>manual</i>, and you must verify such policies manually. <span>Lacework FortiCNAPP</span> provides the manual remediation steps for these policies (when available).</p></td></tr></tbody></table>

## AWS frameworks

  
| Framework Name | API Format | Notes |
| --- | --- | --- |
| 
[CIS AWS Benchmark v4.0.1](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/549246/cis-aws-benchmark-v4-0-1)

 | 

```
AWS_CIS_401
```

 |  |
| [AWS CIS 1.4.0 Benchmark](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/687211/cis-aws-1-4-0-benchmark) | `AWS_CIS_14` |  |
| AWS Cloud Security Alliance Cloud Control Matrix (CSA CCM) v4.0.5 | `AWS_CSA_CCM_4_0_5` | Comprised of CIS 1.4.0 policies |
| AWS Cyber Essentials 2.2 Report | `AWS_Cyber_Essentials_2_2` | Comprised of CIS 1.4.0 policies |
| AWS ISO/IEC 27002:2022 | `AWS_CIS_1_4_ISO_IEC_27002_2022` | Comprised of CIS 1.4.0 policies |
| AWS Cybersecurity Maturity Model Certification (CMMC) v1.02 | `AWS_CMMC_1.02` | Comprised of CIS 1.4.0 policies |
| AWS HIPAA Report | `AWS_HIPAA` | Comprised of CIS 1.4.0 policies |
| AWS ISO 27001:2013 Report | `AWS_ISO_27001:2013` | Comprised of CIS 1.4.0 policies |
| AWS NIST 800-171 rev2 Report | `AWS_NIST_800-171_rev2` | Comprised of CIS 1.4.0 policies |
| AWS NIST 800-53 rev5 Report | `AWS_NIST_800-53_rev5` | Comprised of CIS 1.4.0 policies |
| AWS NIST CSF | `AWS_NIST_CSF` | Comprised of CIS 1.4.0 policies |
| AWS PCI DSS 3.2.1 Report | `AWS_PCI_DSS_3.2.1` | Comprised of CIS 1.4.0 policies |
| AWS SOC 2 Report | `AWS_SOC_2` | Comprised of CIS 1.4.0 policies |
| AWS PCI DSS 4.0.0 Report | `AWS_PCI_DSS_4.0.0` | Comprised of CIS 1.4.0 policies |
| [Lacework FortiCNAPP AWS Security Addendum 1.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/622314/lacework-forticnapp-aws-security-addendum-1-0) | `LW_AWS_SEC_ADD_1_0` |  |
| [AWS FSBP Standard](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/173943/aws-foundational-security-best-practices-fsbp-standard) | `FSBP` | This framework uses Lacework FortiCNAPP AWS Security Addendum and AWS CIS 1.4.0 benchmark policies when there is an overlap with the AWS FSBP Standard. |

## Google Cloud frameworks

| Framework Name | API Format | Notes |
| --- | --- | --- |
| [CIS Google Cloud Benchmark 1.3.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/744514/cis-google-cloud-1-3-0-benchmark) | `GCP_CIS13` |  |
| [CIS Google Cloud Benchmark 2.0.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/856999/cis-google-cloud-2-0-0-benchmark) | `GCP_CIS_2_0_0` |  |
| GCP Cybersecurity Maturity Model Certification (CMMC) v1.02 | `GCP_CMMC_1_02` | Comprised of CIS 1.3.0 policies |
| GCP HIPAA (2013) Report | `GCP_HIPAA_2013` | Comprised of CIS 1.3.0 policies |
| GCP ISO 27001:2013 Report | `GCP_ISO_27001_2013` | Comprised of CIS 1.3.0 policies |
| GCP NIST 800-171 rev2 Report | `GCP_CIS_1_3_0_NIST_800_171_rev2` | Comprised of CIS 1.3.0 policies |
| GCP NIST 800-53 rev5 Report | `GCP_CIS_1_3_0_NIST_800_53_rev5` | Comprised of CIS 1.3.0 policies |
| GCP NIST CSF Report | `GCP_CIS_1_3_0_NIST_CSF` | Comprised of CIS 1.3.0 policies |
| GCP PCI DSS 3.2.1 Report | `GCP_PCI_DSS_3_2_1` | Comprised of CIS 1.3.0 policies |
| GCP SOC 2 Report | `GCP_SOC_2` | Comprised of CIS 1.3.0 policies |
| GCP PCI DSS 4.0.0 Report | `GCP_PCI_DSS_4_0_0` | Comprised of CIS 1.3.0 policies |
| GCP Cloud Security Alliance Cloud Control Matrix (CSA CCM) v4.0.5 | `GCP_CSA_CCM_4_0_5` | Comprised of CIS 1.3.0 policies |

## Azure frameworks

| Framework Name | API Format | Notes |
| --- | --- | --- |
| [CIS Azure Benchmark 1.5.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/585142/cis-azure-1-5-0-benchmark) | `AZURE_CIS_1_5` |  |
| Azure HIPAA Report | `AZURE_HIPAA_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure ISO 27001:2013 Report | `AZURE_ISO_27001:2013_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure NIST 800-171 rev2 Report | `AZURE_NIST_800-171_rev2_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure NIST 800-53 rev5 Report | `AZURE_NIST_800-53_rev5_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure NIST CSF Report | `AZURE_NIST_CSF_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure PCI DSS 3.2.1 Report | `AZURE_PCI_DSS_3_2_1_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure SOC 2 Report | `AZURE_SOC_2_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure PCI DSS 4.0.0 Report | `AZURE_PCI_DSS_4_0_0_CIS_1_5` | Comprised of CIS 1.5.0 policies |
| Azure Cloud Security Alliance Cloud Control Matrix (CSA CCM) v4.0.5 | `AZURE_CSA_CCM_4_0_5` | Comprised of CIS 1.5.0 policies |

## Oracle Cloud Infrastructure frameworks

| Framework Name | API Format | Notes |
| --- | --- | --- |
| [CIS Oracle Cloud Infrastructure Foundations Benchmark v1.2.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/079229/cis-oracle-cloud-infrastructure-oci-1-2-0-benchmark) | `CIS_OCI_1_2_0` |  |
| [Oracle Cloud Infrastructure Configuration (OCI CFG) Detector Rules](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/711414/oracle-cloud-infrastructure-configuration-detector-rules) | `OCI_CFG_DETECTOR` | This framework uses CIS 1.2.0 policies when there is an overlap with the OCI CFG Detector Rules. |

## Kubernetes frameworks

| Framework Name | API Format | Notes |
| --- | --- | --- |
| [CIS Amazon Elastic Kubernetes Service (EKS) 1.1.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/776180/cis-amazon-elastic-kubernetes-service-eks-1-1-0-benchmark) | _Unavailable_ |  |
| [CIS Google Kubernetes Engine (GKE) Benchmark v1.4.0](https://docs.fortinet.com/document/lacework-forticnapp/latest/lacework-forticnapp-policies/128331/cis-google-kubernetes-engine-gke-1-4-0-benchmark) | `K8S_CIS_GKE_1_4_0` |  |