# Security Anti-Patterns and Examples

This directory contains intentionally insecure configurations and security anti-patterns for **educational purposes only**.

## ⚠️ **IMPORTANT DISCLAIMER**

**DO NOT USE THESE EXAMPLES IN PRODUCTION ENVIRONMENTS**

These configurations are intentionally insecure and are designed solely for:
- Security testing and validation
- Educational demonstrations
- Compliance testing scenarios
- Security team training

## 📁 Contents

### [tf/](./tf/)
**Terraform examples of insecure configurations**

- **bad_example_sg.tf**: Security group with overly permissive rules
  - Allows all inbound traffic (0.0.0.0/0)
  - Allows all outbound traffic (0.0.0.0/0)
  - Demonstrates what NOT to do in production

## 🎯 **Educational Use Cases**

### Security Testing
- Validate security monitoring tools
- Test compliance scanning capabilities
- Verify alert generation

### Training Scenarios
- Security team education
- Compliance training
- Risk assessment exercises

### Research and Development
- Security tool development
- Vulnerability research
- Security architecture analysis

## 🔒 **Security Best Practices**

When working with these examples:

1. **Isolated Environment**: Use only in isolated, controlled environments
2. **No Production**: Never deploy to production systems
3. **Cleanup**: Always clean up test resources after use
4. **Documentation**: Document your testing activities
5. **Compliance**: Ensure testing complies with organizational policies

## 🚨 **What These Examples Demonstrate**

### Security Group Anti-Patterns
- Overly permissive ingress rules
- Unrestricted egress traffic
- Missing security controls
- Poor network segmentation

### General Security Misconfigurations
- Default credentials
- Weak access controls
- Missing encryption
- Inadequate logging

## 📚 **Related Resources**

- [AWS Security Best Practices](https://aws.amazon.com/security/security-learning/)
- [Terraform Security](https://www.terraform.io/docs/cloud/guides/security.html)
- [Cloud Security Alliance](https://cloudsecurityalliance.org/)

---

**Remember**: These are intentionally bad examples. Use them responsibly for educational purposes only. 