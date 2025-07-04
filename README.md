# Lacework Public Repository

A collection of Lacework-related tools, scripts, and resources for security testing, compliance reporting, and educational purposes.

## 📁 Repository Structure

### 🔧 [Lacework-Compliance-Reporter](./Lacework-Compliance-Reporter/)
**Multi-platform desktop application for Lacework compliance reporting**

- **Purpose**: Generate and analyze Lacework compliance reports
- **Technology**: Electron + Python + Streamlit
- **Platforms**: Windows, macOS, Linux
- **Features**:
  - Desktop application with web interface
  - Multi-platform installers (.exe, .dmg, .AppImage)
  - Automated builds and releases via GitHub Actions
  - Dynamic release notes generation
  - CHANGELOG.md integration

**Quick Start**: Download the latest release for your platform from the [Releases page](https://github.com/J-C-B/lwpublic/releases)

---

### ☁️ [azure_evil](./azure_evil/)
**Azure security testing and monitoring demonstration script**

- **Purpose**: Generate "suspicious" Azure API activity for security monitoring testing
- **Technology**: Bash script + Azure CLI
- **What it does**:
  - Creates temporary Azure resources (users, apps, storage accounts)
  - Performs reconnaissance activities
  - Uploads test files to storage
  - Cleans up all resources
  - Generates detailed activity logs

**Use Cases**:
- Testing Lacework Azure monitoring capabilities
- Security team training and demonstrations
- Azure activity log analysis practice
- Compliance testing scenarios

**Quick Start**:
```bash
cd azure_evil/
chmod +x baduser_azure_activity.sh
# Edit script with your Azure subscription details
./baduser_azure_azure_activity.sh
```

---

### 🚨 [bad](./bad/)
**Security anti-patterns and examples**

- **Purpose**: Demonstrate security misconfigurations and anti-patterns
- **Contents**:
  - Terraform examples of insecure configurations
  - Security group examples with overly permissive rules
  - Educational resources for security testing

**Note**: These are intentionally insecure configurations for educational purposes only. Do not use in production environments.

---

## 🚀 Getting Started

### For Compliance Reporting
1. Visit the [Lacework-Compliance-Reporter releases](https://github.com/J-C-B/lwpublic/releases)
2. Download the installer for your platform
3. Run the installer and follow the setup wizard
4. Configure your Lacework API credentials
5. Generate compliance reports

### For Azure Security Testing
1. Clone this repository
2. Navigate to the `azure_evil/` directory
3. Configure your Azure subscription details in the script
4. Run the script to generate test activity
5. Monitor the activity in Lacework and Azure

### For Development
1. Clone this repository
2. Navigate to the specific project directory
3. Follow the individual README files for setup instructions
4. Contribute improvements via pull requests

---

## 📋 Prerequisites

### For Lacework-Compliance-Reporter
- Lacework account with API access
- Valid API credentials (API key and secret)
- Internet connection for API communication

### For Azure Evil Script
- Azure subscription
- Azure CLI installed and configured
- Appropriate permissions to create/destroy resources
- Bash shell environment

### For Development
- Git
- Node.js (for Electron development)
- Python 3.11+ (for Python components)
- Platform-specific development tools

---

## 🔒 Security Notice

- **Educational Purpose**: These tools are designed for educational and testing purposes
- **No Production Use**: Do not use the "bad" examples in production environments
- **Responsible Testing**: Always test in isolated environments with proper permissions
- **Compliance**: Ensure all testing activities comply with your organization's policies

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with detailed description

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and community support
- **Security**: Report security issues privately to maintainers

---

## 🔗 Related Resources

- [Lacework Documentation](https://docs.lacework.com/)
- [Azure Security Center](https://azure.microsoft.com/en-us/services/security-center/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

*Last updated: July 2025*


