import re

with open('inputs/contract.txt', 'r') as f:
    contract = f.read()

# Find all clause-like patterns
clause_pattern = re.findall(r'\b(\d+(?:\.\d+)*)\.?\s', contract)

# Deduplicate and sort by numeric components
def sort_key(s):
    parts = s.split('.')
    return tuple(int(p) for p in parts)

clauses = sorted(set(clause_pattern), key=sort_key)

print("=== CONTRACT CLAUSES ===")
print(f"Total unique clause numbers: {len(clauses)}")
for c in clauses:
    print(c)

# Also find appendix numbers
appendix_pattern = re.findall(r'(Приложение\s+№\s*\d+(?:\.\d+)*)', contract)
print("\n=== APPENDICES ===")
for a in sorted(set(appendix_pattern)):
    print(a)
