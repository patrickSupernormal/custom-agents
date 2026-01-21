---
skill: log-analysis
version: "1.0.0"
description: "Techniques for parsing, interpreting, and extracting insights from application logs"
used-by: ["@debugger", "@performance-analyst", "@devops-specialist", "@incident-responder"]
---

# Log Analysis Skill

## Overview
Systematic approach to analyzing application logs for debugging, performance analysis, and incident response.

## Log Format Recognition

### Common Log Formats

#### JSON Logs (Structured)
```json
{"timestamp":"2024-01-15T10:30:45.123Z","level":"error","message":"Database connection failed","service":"api","requestId":"abc-123","error":{"code":"ECONNREFUSED","host":"db.internal"}}
```

#### Apache/Nginx Access Logs
```
192.168.1.1 - - [15/Jan/2024:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```

#### Application Logs (Unstructured)
```
2024-01-15 10:30:45.123 ERROR [main] c.e.UserService - Failed to create user: duplicate email
```

## Step-by-Step Analysis Procedure

### Phase 1: Initial Assessment (2 minutes)
1. **Identify log format**
   ```bash
   head -20 application.log  # View sample entries
   ```

2. **Check time range**
   ```bash
   head -1 application.log   # First entry
   tail -1 application.log   # Last entry
   ```

3. **Assess volume**
   ```bash
   wc -l application.log     # Total lines
   ```

### Phase 2: Error Extraction
1. **Find all errors**
   ```bash
   grep -i "error\|exception\|failed\|fatal" application.log | head -50
   ```

2. **Count error types**
   ```bash
   grep -i "error" application.log | \
     sed 's/.*\(ERROR\|Error\)[^a-zA-Z]*\([a-zA-Z]*\).*/\2/' | \
     sort | uniq -c | sort -rn | head -10
   ```

3. **Find error context** (lines before and after)
   ```bash
   grep -B5 -A5 "CRITICAL_ERROR" application.log
   ```

### Phase 3: Pattern Analysis
1. **Time-based patterns**
   ```bash
   # Errors per hour
   grep -i "error" application.log | \
     cut -d' ' -f1-2 | cut -d':' -f1-2 | \
     sort | uniq -c
   ```

2. **Request ID tracing**
   ```bash
   # Follow a request through logs
   grep "requestId.*abc-123" application.log
   ```

3. **User/IP patterns**
   ```bash
   # Top IPs by request count
   awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
   ```

## Log Parsing Commands

### JSON Log Parsing with jq
```bash
# Extract errors only
cat logs.json | jq -r 'select(.level == "error")'

# Group by error message
cat logs.json | jq -r '.message' | sort | uniq -c | sort -rn

# Filter time range
cat logs.json | jq -r 'select(.timestamp > "2024-01-15T10:00:00")'

# Extract specific fields
cat logs.json | jq -r '[.timestamp, .level, .message] | @tsv'
```

### Performance Analysis
```bash
# Response time extraction (nginx)
awk '{print $NF}' access.log | sort -n | tail -20  # Slowest requests

# P95 response time
awk '{print $NF}' access.log | sort -n | \
  awk '{all[NR]=$1} END {print all[int(NR*0.95)]}'

# Requests per second
awk '{print $4}' access.log | cut -d: -f1-3 | uniq -c
```

### Error Correlation
```bash
# Find what happened before errors
grep -B10 "OutOfMemoryError" application.log | grep -v "OutOfMemory"

# Group related errors by timestamp (within 1 second)
grep "ERROR" application.log | \
  awk '{print $1" "$2}' | cut -d. -f1 | uniq -c | \
  awk '$1 > 5 {print}'  # Clusters of 5+ errors
```

## Decision Criteria

### Prioritization Matrix
| Indicator | Priority | Action |
|-----------|----------|--------|
| FATAL/CRITICAL | P0 | Immediate investigation |
| Repeated errors (>100/min) | P0 | Service degradation |
| 5xx responses spike | P1 | User impact |
| Slow responses (>5s) | P2 | Performance issue |
| Warnings increase | P3 | Monitor trend |

### Root Cause Indicators
| Log Pattern | Likely Cause |
|-------------|--------------|
| Connection refused | Service down or network |
| Timeout | Overload or deadlock |
| OOM | Memory leak or spike |
| 429 Too Many Requests | Rate limiting |
| SSL/TLS errors | Certificate issue |

## Common Log Patterns

### Memory Issues
```
# Java heap
java.lang.OutOfMemoryError: Java heap space

# Node.js
FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed
```

### Database Issues
```
# Connection pool exhausted
HikariPool-1 - Connection is not available, request timed out

# Slow query
Duration: 15234 ms  Execute: SELECT * FROM users WHERE...
```

### Network Issues
```
# DNS failure
getaddrinfo ENOTFOUND api.external.com

# Connection timeout
ETIMEDOUT 10.0.0.5:5432
```

## Analysis Scripts

### Quick Health Check
```bash
#!/bin/bash
LOG_FILE="${1:-application.log}"

echo "=== Log Analysis Summary ==="
echo "Time range: $(head -1 "$LOG_FILE" | cut -d' ' -f1-2) to $(tail -1 "$LOG_FILE" | cut -d' ' -f1-2)"
echo "Total lines: $(wc -l < "$LOG_FILE")"
echo ""
echo "=== Error Counts ==="
grep -c "ERROR\|FATAL" "$LOG_FILE" | xargs echo "Errors:"
grep -c "WARN" "$LOG_FILE" | xargs echo "Warnings:"
echo ""
echo "=== Top Errors ==="
grep "ERROR" "$LOG_FILE" | \
  sed 's/.*ERROR[^a-zA-Z]*//' | cut -c1-80 | \
  sort | uniq -c | sort -rn | head -5
```

### Real-time Monitoring
```bash
# Watch for errors in real-time
tail -f application.log | grep --line-buffered -i "error\|exception"

# With highlighting
tail -f application.log | grep --line-buffered --color=always -E "ERROR|WARN|$"
```

## Common Pitfalls to Avoid

1. **Ignoring timestamps** - Always correlate with time of incident
2. **Missing context** - Look at lines before errors
3. **Single log source** - Cross-reference multiple services
4. **Ignoring warnings** - Often precede errors
5. **Not checking volume** - Error rate matters, not just presence
6. **Timezone confusion** - Normalize to UTC for comparison
7. **Grep without context** - Use `-B` and `-A` flags

## Output Format

When reporting log analysis:
```markdown
## Log Analysis Report

### Summary
- Time range analyzed: [start] to [end]
- Total entries: [count]
- Error rate: [X errors/minute]

### Critical Findings
1. [Error type]: [count] occurrences
   - First seen: [timestamp]
   - Sample: `[error message]`
   - Likely cause: [assessment]

### Timeline
| Time | Event |
|------|-------|
| 10:30:45 | First error observed |
| 10:31:00 | Error rate spike (50/sec) |
| 10:35:00 | Errors stopped |

### Recommended Actions
1. [Action] - [Reason]
2. [Action] - [Reason]
```
