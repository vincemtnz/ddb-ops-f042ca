# DDB Operations tests
Testing DDB performance when performing multiple operations

## Instructions

Install dependencies
```bash
uv sync
```

It should read your aws credentials automatically (botocore).
Make sure you're using the right account and role.

Update .env with the table name.

To run a script, use the following command:
```bash
uv run path/to/script.py

# Example
uv run tasks/read-items.py batch-get --total 500 --prefix XXA --execute
```

To enable debug logging, set the `LOG_LEVEL` ENV variable to `DEBUG`. This will
log all the requests and responses from the AWS SDK, including consumed capacity units
```bash
LOG_LEVEL=DEBUG uv run tasks/read-items.py batch-get --total 500 --prefix XXA --execute

```

NOTE: Pre-existing mock numbers:
- 441134960001
- 441134960002
