---
skill: log-analysis-patterns
version: 1.0.0
used-by:
  - "@log-analyst"
description: Comprehensive patterns and techniques for analyzing log files, detecting errors, identifying anomalies, and generating actionable reports.
---

# Log Analysis Patterns

This skill provides systematic approaches for analyzing log files across various formats, identifying issues, and generating meaningful reports.

---

## 1. Log Format Identification

### Common Log Formats

**Syslog (RFC 3164)**
```
Mar 15 14:32:01 hostname process[pid]: message
```
Regex pattern:
```regex
^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+?)(?:\[(\d+)\])?:\s+(.*)$
```
Groups: timestamp, hostname, process, pid, message

**Syslog (RFC 5424)**
```
<priority>version timestamp hostname app-name procid msgid structured-data msg
```
Regex pattern:
```regex
^<(\d+)>(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(?:\[([^\]]*)\])?\s*(.*)$
```

**Apache Combined Log Format**
```
127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08"
```
Regex pattern:
```regex
^(\S+)\s+(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+"([^"]+)"\s+(\d+)\s+(\d+|-)\s+"([^"]*)"\s+"([^"]*)"$
```
Groups: ip, identd, user, timestamp, request, status, bytes, referer, user-agent

**Nginx Access Log**
```
192.168.1.1 - - [21/Jan/2026:10:15:30 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "curl/7.68.0" 0.015
```
Regex pattern:
```regex
^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"(\w+)\s+(\S+)\s+\S+"\s+(\d+)\s+(\d+)\s+"([^"]*)"\s+"([^"]*)"\s*(\d+\.?\d*)?$
```

**JSON Structured Logs**
```json
{"timestamp":"2026-01-21T10:15:30.123Z","level":"ERROR","service":"api","message":"Connection failed","trace_id":"abc123"}
```
Parse with jq:
```bash
jq -r 'select(.level == "ERROR") | "\(.timestamp) [\(.service)] \(.message)"'
```

**Common Log Format (CLF)**
```
127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /index.html HTTP/1.0" 200 2326
```

### Format Detection Strategy

1. Check first 10 lines for patterns
2. Look for timestamp formats
3. Identify field delimiters (spaces, tabs, pipes, JSON braces)
4. Detect structured vs unstructured

```bash
# Quick format detection
head -20 logfile.log | grep -E '^\{' && echo "JSON format"
head -20 logfile.log | grep -E '^\w{3}\s+\d{1,2}\s+\d{2}:' && echo "Syslog format"
head -20 logfile.log | grep -E '^\d+\.\d+\.\d+\.\d+' && echo "Web access log"
```

---

## 2. Error Pattern Detection

### Universal Error Indicators

**Critical/Fatal Keywords**
```regex
(?i)(fatal|critical|emergency|panic|crash|abort|segfault|killed|oom|out of memory)
```

**Error Keywords**
```regex
(?i)(error|err|failure|failed|exception|denied|refused|rejected|invalid|corrupt)
```

**Warning Keywords**
```regex
(?i)(warn|warning|deprecated|timeout|retry|slow|degraded|unavailable)
```

### Application-Specific Patterns

**Java/JVM Errors**
```regex
(?i)(java\.lang\.\w*Exception|java\.lang\.\w*Error|OutOfMemoryError|StackOverflowError)
```

**Python Errors**
```regex
(?i)(Traceback \(most recent call last\)|^\w+Error:|^\w+Exception:)
```

**Node.js Errors**
```regex
(?i)(UnhandledPromiseRejection|TypeError:|ReferenceError:|SyntaxError:|ECONNREFUSED|ETIMEDOUT)
```

**Database Errors**
```regex
(?i)(deadlock|lock wait timeout|connection refused|too many connections|disk full|corruption)
```

**HTTP Error Responses**
```regex
HTTP/\d\.\d"\s+(4\d{2}|5\d{2})\s
```

### Grep Commands for Error Detection

```bash
# Find all errors with context
grep -n -i -E "(error|exception|failed|failure)" logfile.log

# Find errors excluding noise
grep -n -i "error" logfile.log | grep -v -i "error_count.*0"

# Count errors by type
grep -o -i -E "(error|exception|failed|timeout)" logfile.log | sort | uniq -c | sort -rn

# Find errors in time range
grep -E "2026-01-21T1[0-2]:" logfile.log | grep -i error
```

---

## 3. Stack Trace Analysis

### Java Stack Trace Pattern

```regex
^(?:Exception|Error|Caused by:|	at |Caused by: )
```

Full extraction:
```regex
(?:^|\n)((?:Exception|Error|Caused by:|\tat )[^\n]*(?:\n(?:\tat |Caused by: )[^\n]*)*)
```

Example stack trace:
```
java.lang.NullPointerException: Cannot invoke method on null object
    at com.example.service.UserService.getUser(UserService.java:45)
    at com.example.controller.UserController.handleRequest(UserController.java:123)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
Caused by: java.sql.SQLException: Connection timed out
    at com.mysql.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:2181)
```

**Key Information to Extract:**
1. Exception type (NullPointerException)
2. Root cause (Caused by)
3. First application frame (UserService.java:45)
4. Entry point (controller/handler)

### Python Stack Trace Pattern

```regex
Traceback \(most recent call last\):[\s\S]*?^\w+(?:Error|Exception):.*$
```

Example:
```
Traceback (most recent call last):
  File "/app/service.py", line 42, in process_request
    result = self.handler.execute(data)
  File "/app/handler.py", line 18, in execute
    return json.loads(raw_data)
ValueError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

### JavaScript/Node.js Stack Trace

```regex
(?:Error|TypeError|ReferenceError):[^\n]*(?:\n\s+at [^\n]+)+
```

Example:
```
TypeError: Cannot read property 'id' of undefined
    at processUser (/app/src/users.js:42:15)
    at Router.handle (/app/node_modules/express/lib/router/layer.js:95:5)
```

### Stack Trace Analysis Commands

```bash
# Extract Java stack traces
grep -A 50 "Exception\|Error" logfile.log | grep -B 1 -A 50 "^\tat "

# Find most common exception types
grep -o "^\w\+Exception\|^\w\+Error" logfile.log | sort | uniq -c | sort -rn

# Find deepest stack frames (application code)
grep "at com.yourcompany" logfile.log | sort | uniq -c | sort -rn
```

---

## 4. Timeline Reconstruction

### Timestamp Extraction Patterns

**ISO 8601**
```regex
\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z|[+-]\d{2}:?\d{2})?
```

**Common Timestamp Formats**
```regex
# YYYY-MM-DD HH:MM:SS
\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}

# DD/Mon/YYYY:HH:MM:SS (Apache)
\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}

# Mon DD HH:MM:SS (Syslog)
\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}

# Epoch milliseconds
\d{13}

# Epoch seconds
\d{10}
```

### Timeline Reconstruction Steps

1. **Extract timestamps and events**
```bash
grep -E "(error|started|stopped|connected|disconnected)" logfile.log | \
  awk '{print $1, $2, $0}' | sort
```

2. **Find time gaps**
```bash
# Find gaps > 60 seconds between log entries
awk '
  /^[0-9]{4}-[0-9]{2}-[0-9]{2}/ {
    cmd = "date -d \""$1" "$2"\" +%s"
    cmd | getline current
    close(cmd)
    if (prev && current - prev > 60) {
      print "GAP: " (current - prev) "s before line " NR
    }
    prev = current
  }
' logfile.log
```

3. **Create event timeline**
```bash
# Extract key events with timestamps
grep -E "(START|STOP|ERROR|CONNECT|DISCONNECT)" logfile.log | \
  awk '{
    timestamp = $1 " " $2
    event = $0
    gsub(/.*\[(INFO|ERROR|WARN)\]/, "", event)
    print timestamp " | " substr(event, 1, 80)
  }'
```

### Correlating Events by Time Window

```bash
# Find all events within 5 seconds of an error
error_time=$(grep -m1 "CRITICAL ERROR" logfile.log | grep -oE "^\S+ \S+")
grep -E "^${error_time%:*}" logfile.log
```

---

## 5. Correlation Across Log Sources

### Request Tracing with Trace IDs

**Pattern for trace/correlation IDs**
```regex
(?:trace[_-]?id|correlation[_-]?id|request[_-]?id|x-request-id)[=:]["']?([a-f0-9-]{8,36})
```

**Cross-log correlation**
```bash
# Extract trace ID from error
trace_id=$(grep "ERROR" app.log | grep -oE "trace_id=[a-f0-9-]+" | head -1 | cut -d= -f2)

# Find related entries across all logs
grep -r "$trace_id" /var/log/myapp/
```

### Session-Based Correlation

```bash
# Find all activity for a session
session_id="abc123"
grep -h "$session_id" *.log | sort -t' ' -k1,2
```

### User Journey Reconstruction

```bash
# Track user through system
user_id="user@example.com"

# Combine and sort entries from multiple sources
cat auth.log api.log web.log | \
  grep "$user_id" | \
  sort -t' ' -k1,2 | \
  awk '{print NR": "$0}'
```

### Multi-Service Correlation Pattern

```bash
# For microservices with shared trace IDs
for log in service-a.log service-b.log service-c.log; do
  echo "=== $log ==="
  grep "$trace_id" "$log" | head -5
done
```

---

## 6. Anomaly Detection Patterns

### Volume Anomalies

**Spike detection**
```bash
# Count entries per minute
awk -F'[: ]' '{print $1":"$2":"$3}' logfile.log | \
  uniq -c | \
  awk '$1 > 1000 {print "SPIKE: "$0}'
```

**Sudden silence detection**
```bash
# Detect periods with no logs (>5 min gap)
awk '
  /^[0-9]{4}-[0-9]{2}-[0-9]{2}T/ {
    gsub(/[TZ]/, " ", $1)
    "date -d \""$1"\" +%s" | getline ts
    if (last_ts && ts - last_ts > 300) {
      print "SILENCE: " (ts - last_ts) "s gap ending at " $1
    }
    last_ts = ts
  }
' logfile.log
```

### Pattern Anomalies

**Unusual error frequency**
```bash
# Compare error rate to baseline
error_count=$(grep -c -i error logfile.log)
total_count=$(wc -l < logfile.log)
error_rate=$(echo "scale=4; $error_count / $total_count" | bc)
echo "Error rate: $error_rate"
# Alert if > 0.01 (1%)
```

**New error types**
```bash
# Find error patterns not seen in baseline
grep -i error current.log | \
  grep -o -E "\w+Error|\w+Exception" | \
  sort -u > current_errors.txt

grep -i error baseline.log | \
  grep -o -E "\w+Error|\w+Exception" | \
  sort -u > baseline_errors.txt

comm -23 current_errors.txt baseline_errors.txt
```

### Timing Anomalies

**Slow response detection**
```bash
# Find requests taking > 5 seconds
grep -E "response_time[=:]([5-9]\d{3}|[1-9]\d{4,})" logfile.log

# Alternative for duration in seconds
grep -E "duration[=:]\s*[5-9]\.|duration[=:]\s*[1-9][0-9]+\." logfile.log
```

**Request timeout patterns**
```regex
(?i)(timeout|timed?\s*out|deadline exceeded|context deadline|read timeout|write timeout|connect timeout)
```

---

## 7. Performance Issue Indicators

### Latency Patterns

**High latency indicators**
```regex
(?i)(slow|latency|response.time|duration|elapsed)[=:>\s]+([5-9]\d{3}|[1-9]\d{4,})\s*(ms|milliseconds)
```

**Database slow queries**
```regex
(?i)(slow query|query time[=:]\s*[1-9]\d*\.\d+|lock wait|deadlock)
```

### Resource Exhaustion

**Memory issues**
```regex
(?i)(out of memory|oom|heap|memory.*(limit|exhausted|pressure)|gc overhead|cannot allocate)
```

**Connection pool exhaustion**
```regex
(?i)(pool exhausted|no available connections|connection limit|max connections|too many connections)
```

**Disk issues**
```regex
(?i)(disk full|no space left|quota exceeded|inode|write failed.*disk)
```

**CPU/Thread issues**
```regex
(?i)(thread pool|queue full|backpressure|rate limit|throttl|cpu.*100%)
```

### Performance Analysis Commands

```bash
# Extract response times and calculate percentiles
grep -oE "response_time=\d+" logfile.log | \
  cut -d= -f2 | \
  sort -n | \
  awk '
    {a[NR]=$1; sum+=$1}
    END {
      print "Count:", NR
      print "Mean:", sum/NR
      print "P50:", a[int(NR*0.5)]
      print "P95:", a[int(NR*0.95)]
      print "P99:", a[int(NR*0.99)]
      print "Max:", a[NR]
    }
  '

# Find slowest endpoints
grep -E "GET|POST|PUT|DELETE" access.log | \
  awk '{print $NF, $(NF-3), $7}' | \
  sort -rn | head -20
```

---

## 8. Security Event Identification

### Authentication Events

**Failed login attempts**
```regex
(?i)(authentication failed|login failed|invalid password|access denied|unauthorized|401|403)
```

**Brute force indicators**
```bash
# Find IPs with many failed logins
grep -i "authentication failed\|login failed" auth.log | \
  grep -oE "\d+\.\d+\.\d+\.\d+" | \
  sort | uniq -c | sort -rn | \
  awk '$1 > 10 {print "ALERT: "$1" failures from "$2}'
```

### Suspicious Activity Patterns

**SQL injection attempts**
```regex
(?i)(union\s+select|;\s*drop|'\s*or\s*'|1=1|--\s*$|/\*.*\*/)
```

**Path traversal**
```regex
(?i)(\.\.\/|\.\.\\|%2e%2e|%252e)
```

**Command injection**
```regex
(?i)(\|\s*\w+|;\s*\w+|`[^`]+`|\$\([^)]+\))
```

### Security Log Analysis Commands

```bash
# Find failed SSH attempts
grep "Failed password" /var/log/auth.log | \
  awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# Detect potential port scanning
grep "refused connect" logfile.log | \
  awk '{print $NF}' | sort | uniq -c | sort -rn

# Find privilege escalation attempts
grep -i "sudo\|su\|privilege\|permission denied" auth.log

# Unusual access times
grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}T(0[0-5]|2[2-3]):" access.log
```

### Sensitive Data Exposure Detection

```regex
(?i)(password|secret|token|api[_-]?key|private[_-]?key|credential)[=:]["']?\S+
```

**Note:** Report findings but never include actual sensitive values in reports.

---

## 9. Grep/Regex Patterns for Common Issues

### Quick Reference Pattern Library

| Issue Type | Grep Pattern |
|------------|--------------|
| Any error | `grep -i -E "(error\|exception\|failed\|failure)"` |
| HTTP 5xx | `grep -E 'HTTP/[0-9.]+"\s+5[0-9]{2}'` |
| HTTP 4xx | `grep -E 'HTTP/[0-9.]+"\s+4[0-9]{2}'` |
| Timeout | `grep -i -E "(timeout\|timed.?out)"` |
| Connection issues | `grep -i -E "(connection refused\|ECONNREFUSED\|connect failed)"` |
| Memory issues | `grep -i -E "(out of memory\|oom\|heap)"` |
| Disk issues | `grep -i -E "(disk full\|no space\|quota)"` |
| Null/undefined | `grep -i -E "(null pointer\|undefined\|nil)"` |
| Stack trace start | `grep -E "(^Exception\|^Error\|Traceback)"` |
| Slow queries | `grep -i -E "slow.?query\|query time[=:]\s*[1-9]"` |

### Multi-Pattern Searches

```bash
# Comprehensive error search
grep -n -i -E \
  "(error|exception|failed|failure|fatal|critical|panic|crash|abort)" \
  logfile.log

# Network issues
grep -n -i -E \
  "(ECONNREFUSED|ETIMEDOUT|connection reset|broken pipe|network unreachable)" \
  logfile.log

# Resource exhaustion
grep -n -i -E \
  "(out of memory|heap|no space left|too many open files|connection limit)" \
  logfile.log
```

### Context-Aware Searches

```bash
# Error with 5 lines before and after
grep -B 5 -A 5 -i "error" logfile.log

# First occurrence of each unique error
grep -i "error" logfile.log | sort -u

# Errors with line numbers for reference
grep -n -i "error" logfile.log
```

### Advanced Pattern Combinations

```bash
# Errors excluding known/expected ones
grep -i "error" logfile.log | \
  grep -v -E "(error_count=0|errors: 0|no errors)"

# Find error clusters (multiple errors within 10 lines)
grep -n -i "error" logfile.log | \
  awk -F: '
    prev && $1 - prev < 10 {
      print "Cluster at lines " prev " - " $1
    }
    {prev = $1}
  '
```

---

## 10. Reporting Findings Templates

### Summary Report Template

```markdown
# Log Analysis Report

**Analysis Period:** [START_TIME] to [END_TIME]
**Log Sources:** [LIST OF FILES]
**Generated:** [CURRENT_TIMESTAMP]

## Executive Summary

- **Total Entries Analyzed:** [COUNT]
- **Error Rate:** [PERCENTAGE]%
- **Critical Issues Found:** [COUNT]
- **Warnings:** [COUNT]

## Key Findings

### 1. [ISSUE TITLE]
- **Severity:** Critical/High/Medium/Low
- **First Occurrence:** [TIMESTAMP]
- **Frequency:** [COUNT] occurrences
- **Impact:** [DESCRIPTION]
- **Example:**
  ```
  [LOG_LINE_EXAMPLE]
  ```
- **Recommendation:** [ACTION]

### 2. [NEXT ISSUE]
...

## Error Distribution

| Error Type | Count | Percentage | First Seen | Last Seen |
|------------|-------|------------|------------|-----------|
| [TYPE]     | [N]   | [%]        | [TIME]     | [TIME]    |

## Timeline of Events

| Time | Event | Severity |
|------|-------|----------|
| [T1] | [E1]  | [S1]     |

## Recommendations

1. **Immediate Actions:**
   - [ACTION 1]
   - [ACTION 2]

2. **Short-term Improvements:**
   - [IMPROVEMENT 1]

3. **Long-term Considerations:**
   - [CONSIDERATION 1]

## Appendix

### A. Search Commands Used
```bash
[COMMANDS]
```

### B. Raw Error Counts
```
[DATA]
```
```

### Quick Analysis Report (for urgent issues)

```markdown
# Urgent Issue Report

**Issue:** [BRIEF DESCRIPTION]
**Severity:** Critical
**Time Detected:** [TIMESTAMP]

## Symptoms
- [SYMPTOM 1]
- [SYMPTOM 2]

## Evidence
```
[RELEVANT LOG LINES]
```

## Root Cause (Suspected)
[ANALYSIS]

## Immediate Actions Required
1. [ACTION 1]
2. [ACTION 2]
```

### Automated Report Generation Script

```bash
#!/bin/bash
# Generate quick log analysis report

LOG_FILE="$1"
OUTPUT="analysis_report_$(date +%Y%m%d_%H%M%S).md"

echo "# Log Analysis Report" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "**File:** $LOG_FILE" >> "$OUTPUT"
echo "**Generated:** $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

echo "## Statistics" >> "$OUTPUT"
echo "- Total lines: $(wc -l < "$LOG_FILE")" >> "$OUTPUT"
echo "- Errors: $(grep -c -i error "$LOG_FILE")" >> "$OUTPUT"
echo "- Warnings: $(grep -c -i warn "$LOG_FILE")" >> "$OUTPUT"
echo "" >> "$OUTPUT"

echo "## Top Errors" >> "$OUTPUT"
echo '```' >> "$OUTPUT"
grep -i error "$LOG_FILE" | \
  grep -oE "\w+Error|\w+Exception|error:[^,]+" | \
  sort | uniq -c | sort -rn | head -10 >> "$OUTPUT"
echo '```' >> "$OUTPUT"
echo "" >> "$OUTPUT"

echo "## Recent Errors (Last 10)" >> "$OUTPUT"
echo '```' >> "$OUTPUT"
grep -i error "$LOG_FILE" | tail -10 >> "$OUTPUT"
echo '```' >> "$OUTPUT"

echo "Report saved to: $OUTPUT"
```

### Findings Severity Classification

| Severity | Criteria | Response Time |
|----------|----------|---------------|
| Critical | Service down, data loss, security breach | Immediate |
| High | Functionality impaired, significant errors | Within 1 hour |
| Medium | Performance degraded, elevated error rates | Within 24 hours |
| Low | Minor issues, warnings, deprecations | Next sprint |

---

## Best Practices

1. **Always establish baseline** - Know normal error rates before diagnosing issues
2. **Check time correlation** - Relate errors to deployments, traffic changes
3. **Follow the chain** - Trace errors through connected services
4. **Quantify impact** - Count affected users/requests, not just error counts
5. **Preserve evidence** - Save relevant log sections before rotation
6. **Document patterns** - Build a library of known issues and their signatures
7. **Automate detection** - Convert manual analysis into monitoring alerts
