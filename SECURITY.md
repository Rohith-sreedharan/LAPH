# Security Considerations for LAPH

## Overview

LAPH executes AI-generated code automatically. While the system includes multiple safety measures, users should understand the security implications.

## Safety Measures Implemented

### 1. Code Execution Sandboxing

Generated code runs with the following restrictions:

- **CPU Limit**: 5 seconds (configurable in `configs/execution.toml`)
- **Memory Limit**: 256 MB (configurable)
- **Timeout**: 8 seconds total process timeout (configurable)
- **Isolated Temporary Files**: Code runs in temporary files that are cleaned up

### 2. Code Analysis

Before execution, code is analyzed for:

- Dangerous operations (`eval`, `exec`, `os.system`)
- File system operations (write, delete)
- Network operations (sockets, HTTP requests)
- Subprocess execution
- Dynamic imports

Warnings are logged but execution is not blocked by default.

### 3. Error Handling

- HTTP requests have timeouts to prevent hanging
- Temporary files are always cleaned up (even on errors)
- Resource limits prevent runaway processes
- Unicode handling prevents encoding errors

### 4. Input Validation

- Task descriptions are validated
- Iteration limits are capped
- LLM outputs are parsed and validated before execution

## Configuration

Edit `configs/execution.toml` to adjust:

```toml
[resource_limits]
cpu_limit = 5           # CPU time in seconds
memory_limit_mb = 256   # Memory in MB
timeout = 8             # Process timeout in seconds
```

## Best Practices

1. **Review Generated Code**: Always review code before running on important systems
2. **Use in Isolated Environments**: Run LAPH in VMs or containers when possible
3. **Monitor Resource Usage**: Keep an eye on system resources during execution
4. **Limit Iterations**: Don't set max_iterations too high
5. **Check Logs**: Review execution logs for warnings and errors

## Known Limitations

- Sandboxing is process-level only (not containerized)
- Code analysis is heuristic-based, not comprehensive
- Resource limits may not prevent all types of abuse
- Some dangerous operations may not be detected

## Recommendations

For production use:

1. Run in a Docker container
2. Use additional OS-level sandboxing (AppArmor, SELinux)
3. Monitor system resources externally
4. Implement additional code review steps
5. Keep backups of important data

## Reporting Security Issues

If you discover a security vulnerability, please report it by opening an issue on GitHub with the "security" label.
