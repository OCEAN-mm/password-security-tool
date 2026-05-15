#!/usr/bin/env python3
"""
Password Security Tool - Cybersecurity Project #4
Author: OCEAN-mm
Description: Password strength analyzer, REAL brute force cracker, and breach checker
"""

import hashlib
import re
import requests
import string
import random
from datetime import datetime
import csv
import time
import itertools

class PasswordSecurityTool:
    def __init__(self):
        self.common_passwords = self.load_common_passwords()
        self.results = []
        
    def load_common_passwords(self):
        """Load common passwords for dictionary attack"""
        try:
            with open('/usr/share/wordlists/rockyou.txt', 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()][:50000]
            print(f"[+] Loaded {len(passwords)} common passwords")
            return passwords
        except:
            return ['password', '123456', 'admin', 'password123', 'qwerty']
    
    def brute_force_md5(self, target_hash, max_length=6):
        """
        REAL brute force cracker - tries EVERY possible combination
        Warning: Only use with short max_length (4-6 characters)
        """
        print(f"\n{'='*60}")
        print(f"🔓 REAL BRUTE FORCE CRACKER")
        print(f"{'='*60}")
        print(f"Target Hash: {target_hash}")
        print(f"Max Length: {max_length} characters")
        
        # Character set (can be reduced for faster cracking)
        chars = string.ascii_lowercase + string.digits  # a-z, 0-9 (36 chars)
        print(f"Character set: {len(chars)} chars (a-z, 0-9)")
        
        total_combinations = sum(len(chars)**i for i in range(1, max_length + 1))
        print(f"Total combinations to try: {total_combinations:,}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        attempts = 0
        
        # Try all lengths from 1 to max_length
        for length in range(1, max_length + 1):
            print(f"[*] Trying length: {length} ({len(chars)**length:,} combinations)")
            
            for combo in itertools.product(chars, repeat=length):
                password = ''.join(combo)
                attempts += 1
                
                # Hash the candidate
                hashed = hashlib.md5(password.encode()).hexdigest()
                
                if hashed == target_hash:
                    elapsed = time.time() - start_time
                    print(f"\n{'='*60}")
                    print(f"✅✅✅ CRACKED! ✅✅✅")
                    print(f"{'='*60}")
                    print(f"Password: {password}")
                    print(f"Length: {length}")
                    print(f"Attempts: {attempts:,}")
                    print(f"Time: {elapsed:.2f} seconds")
                    return password
                
                # Show progress every 100,000 attempts
                if attempts % 100000 == 0:
                    elapsed = time.time() - start_time
                    print(f"   ... {attempts:,} attempts ({elapsed:.1f}s) ...")
        
        print(f"\n❌ Not found after {attempts:,} attempts")
        print("   Try increasing max_length (will take longer)")
        return None
    
    def smart_brute_force(self, target_hash, max_length=5):
        """
        Smarter brute force with common patterns first
        Tries numbers, then letters, then combinations
        """
        print(f"\n[*] Smart brute force on: {target_hash}")
        
        patterns_to_try = [
            # Numbers only
            [str(i).zfill(length) for length in range(1, max_length + 1) for i in range(10**length)],
            # Common words
            ['password', 'admin', 'letmein', 'welcome', 'master'],
            # Numbers with letters
            ['abc123', 'qwerty', '123abc', 'admin123', 'password123'],
        ]
        
        start_time = time.time()
        attempts = 0
        
        for pattern_list in patterns_to_try:
            for password in pattern_list:
                if isinstance(password, str) and len(password) <= max_length:
                    attempts += 1
                    hashed = hashlib.md5(password.encode()).hexdigest()
                    
                    if hashed == target_hash:
                        elapsed = time.time() - start_time
                        print(f"\n✅ CRACKED! Password: {password}")
                        print(f"   Attempts: {attempts}, Time: {elapsed:.2f}s")
                        return password
        
        # Fallback to real brute force
        print("[*] Smart search failed, starting full brute force...")
        return self.brute_force_md5(target_hash, max_length)
    
    def calculate_entropy(self, password):
        """Calculate password entropy"""
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)
        
        if charset_size == 0:
            return 0
        return len(password) * (charset_size.bit_length() - 1)
    
    def check_strength(self, password):
        """Analyze password strength"""
        print(f"\n[*] Analyzing password...")
        
        strength_score = 0
        feedback = []
        length = len(password)
        
        if length < 8:
            feedback.append("❌ Too short")
        elif length < 12:
            strength_score += 1
            feedback.append("⚠️ Acceptable length")
        else:
            strength_score += 2
            feedback.append("✅ Good length")
        
        if re.search(r'[a-z]', password):
            strength_score += 1
        else:
            feedback.append("❌ Missing lowercase")
            
        if re.search(r'[A-Z]', password):
            strength_score += 1
        else:
            feedback.append("❌ Missing uppercase")
            
        if re.search(r'\d', password):
            strength_score += 1
        else:
            feedback.append("❌ Missing numbers")
            
        if re.search(r'[' + re.escape(string.punctuation) + r']', password):
            strength_score += 1
            feedback.append("✅ Has special chars")
        else:
            feedback.append("⚠️ No special chars")
        
        entropy = self.calculate_entropy(password)
        
        if strength_score >= 6 and length >= 12:
            strength_level = "VERY STRONG 🟢"
        elif strength_score >= 4:
            strength_level = "STRONG 🟢"
        elif strength_score >= 2:
            strength_level = "WEAK 🟡"
        else:
            strength_level = "VERY WEAK 🔴"
        
        print(f"\n{'='*50}")
        print(f"STRENGTH: {strength_level}")
        print(f"Length: {length} | Entropy: {entropy} bits | Score: {strength_score}/8")
        print(f"\nFeedback:")
        for f in feedback:
            print(f"  {f}")
        
        # Show cracking time estimate
        if length <= 6:
            print(f"\n⚠️  This password can be brute forced in minutes!")
        
        return {
            'password': password,
            'strength': strength_level,
            'score': strength_score,
            'entropy': entropy,
            'length': length
        }
    
    def check_hibp_breach(self, password):
        """Check if password was in data breaches"""
        print(f"\n[*] Checking breach database...")
        
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        try:
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                for line in response.text.splitlines():
                    found_suffix, count = line.split(':')
                    if found_suffix == suffix:
                        print(f"⚠️  BREACHED! Found in {count} breaches!")
                        return int(count)
                print("✅ Not found in any breach")
                return 0
        except:
            print("⚠️ Could not check breaches")
        return -1
    
    def generate_secure_password(self, length=16):
        """Generate secure random password"""
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        print(f"\n✅ Generated: {password}")
        print(f"   Entropy: {self.calculate_entropy(password)} bits")
        return password
    
    def export_report(self, filename=None):
        """Export results to CSV"""
        if not self.results:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"password_report_{timestamp}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'strength', 'score', 'entropy', 'length'])
            writer.writeheader()
            for r in self.results:
                writer.writerow({
                    'timestamp': datetime.now().isoformat(),
                    'strength': r['strength'],
                    'score': r['score'],
                    'entropy': r['entropy'],
                    'length': r['length']
                })
        print(f"\n[+] Report saved to {filename}")

def main():
    print("""
    ╔══════════════════════════════════════════╗
    ║     Password Security Tool v3.0          ║
    ╚══════════════════════════════════════════╝
    """)
    
    tool = PasswordSecurityTool()
    
    while True:
        print("\n" + "="*40)
        print("MENU")
        print("="*40)
        print("1. Check password strength")
        print("2. CRACK MD5 hash (REAL brute force)")
        print("3. Generate secure password")
        print("4. Check breach database")
        print("5. Full audit")
        print("0. Exit")
        
        choice = input("\nSelect: ")
        
        if choice == '1':
            pwd = input("Enter password: ")
            result = tool.check_strength(pwd)
            tool.results.append(result)
            
        elif choice == '2':
            print("\n💡 Test with these short passwords (length 4-5):")
            print("   Hash for 'abc' → 900150983cd24fb0d6963f7d28e17f72")
            print("   Hash for '1234' → 81dc9bdb52d04dc20036dbd8313ed055")
            print("   Hash for 'hello' → 5d41402abc4b2a76b9719d911017c592")
            
            target = input("\nEnter MD5 hash: ")
            max_len = int(input("Max password length to try (4-6 recommended): ") or 5)
            
            print("\n⚠️  Starting REAL brute force...")
            print("   This tries EVERY possible combination!")
            tool.brute_force_md5(target, max_len)
            
        elif choice == '3':
            length = int(input("Length (default 16): ") or 16)
            tool.generate_secure_password(length)
            
        elif choice == '4':
            pwd = input("Enter password: ")
            tool.check_hibp_breach(pwd)
            
        elif choice == '5':
            pwd = input("Enter password to audit: ")
            tool.check_strength(pwd)
            tool.check_hibp_breach(pwd)
            result = tool.check_strength(pwd)
            tool.results.append(result)
            
        elif choice == '0':
            if tool.results:
                tool.export_report()
            print("\n[✓] Goodbye!")
            break

if __name__ == "__main__":
    main()
