"""
SRF Conference Insights - Security Policy

This document outlines the security policy for the SRF Conference Insights project,
including supported versions, vulnerability reporting procedures, and security best practices.

Author: Ming Liu <mliu@ihep.ac.cn>
Project: SRF Conference Insights
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
"""

# Security Policy

## Supported Versions

We provide security updates for the following versions of SRF Conference Insights:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Current Stable  |
| 0.9.x   | ❌ End of Life     |
| < 0.9   | ❌ End of Life     |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in SRF Conference Insights, please report it responsibly:

### How to Report

1. **Email**: Send details to `mliu@ihep.ac.cn` with subject line "SRF-CI Security Vulnerability"
2. **Private GitHub Security Advisory**: Use GitHub's private vulnerability reporting feature
3. **PGP Encrypted Email**: For sensitive disclosures (PGP key available on request)

### What to Include

Please include the following information in your report:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and affected components
- **Reproduction**: Step-by-step instructions to reproduce the issue
- **Environment**: Affected versions, operating systems, and configurations
- **Proof of Concept**: If available, a minimal proof of concept
- **Suggested Fix**: If you have ideas for remediation

### Response Timeline

We are committed to responding to security reports promptly:

- **Initial Response**: Within 48 hours
- **Triage**: Within 1 week
- **Fix Development**: Within 30 days for critical issues
- **Public Disclosure**: After fix is released (coordinated disclosure)

## Security Best Practices

### For Users

1. **Keep Updated**: Always use the latest stable version
2. **Secure Configuration**: Follow configuration guidelines in documentation
3. **Access Control**: Limit access to sensitive data and configuration files
4. **Network Security**: Use HTTPS when accessing web interfaces
5. **Input Validation**: Be cautious with untrusted PDF files and URLs

### For Developers

1. **Dependency Management**: Regularly update dependencies and check for vulnerabilities
2. **Code Review**: All code changes should be reviewed for security implications
3. **Static Analysis**: Use tools like `bandit` for Python security scanning
4. **Input Sanitization**: Validate and sanitize all user inputs
5. **Authentication**: Implement proper authentication and authorization where needed

## Known Security Considerations

### Web Scraping
- Rate limiting to respect target servers
- User-Agent strings to identify the application
- Respect robots.txt and terms of service

### PDF Processing
- PyMuPDF handles potentially malicious PDFs
- File size limits to prevent resource exhaustion
- Sandboxed processing environment recommended

### Web Interface
- XSS protection through proper output encoding
- CSRF protection for state-changing operations
- Content Security Policy headers

### Data Privacy
- No personal data collection by default
- Conference paper metadata is public information
- Local data processing (no cloud transmission)

## Vulnerability Disclosure Policy

We follow responsible disclosure principles:

1. **Private Reporting**: Initial report should be private
2. **Acknowledgment**: We acknowledge receipt and provide status updates
3. **Coordinated Disclosure**: Public disclosure after fix is available
4. **Credit**: Security researchers receive appropriate credit
5. **CVE Assignment**: For qualifying vulnerabilities, we'll request CVE assignment

## Security Contact

- **Primary Contact**: Ming Liu <mliu@ihep.ac.cn>
- **Institution**: Institute of High Energy Physics, Chinese Academy of Sciences
- **Project**: SRF Conference Insights
- **GitHub**: [@iuming](https://github.com/iuming)

For urgent security matters, please use the direct email contact method.

## Legal

This security policy is provided as guidance and does not create any legal obligations. The project maintainers reserve the right to modify this policy at any time.

---

Thank you for helping keep SRF Conference Insights secure!
