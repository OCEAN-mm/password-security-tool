# 🔐 Password Security Tool

**Cybersecurity Portfolio Project #4** | *Python | Cryptography | Brute Force Attack*

## 🎯 Project Overview
A comprehensive password security tool that performs **real brute force MD5 cracking**, entropy-based strength analysis, breach detection, and secure password generation. Unlike simple dictionary attackers, this tool actually tries **every possible combination** to crack hashes.

## 🔧 Features

### 1. REAL Brute Force MD5 Cracker
- Tries **every possible character combination** (a-z, 0-9)
- Configurable maximum password length
- Progress tracking every 100,000 attempts
- Actually cracks unknown passwords (not just dictionary lookup)

### 2. Password Strength Analysis
- Entropy calculation (bits of randomness)
- Length and complexity scoring
- Pattern detection (sequential, repeating)
- Estimated crack time warnings

### 3. Breach Detection
- HaveIBeenPwned API integration
- SHA-1 k-anonymity lookup
- Real-time breach count display

### 4. Secure Password Generation
- Cryptographically random
- Configurable length (8-32 chars)
- High entropy output
