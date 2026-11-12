# Ansible Collection - my_own_namespace.yandex_cloud_elk

My own Ansible collection with a module for creating text files

## Requirements

- Ansible Core
- Python 3

## Included modules

### my_own_module

Creates a text file with the specified content.

Parameters:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| path | str | Yes | Destination file path |
| content | str | Yes | File content |

Example:

```yaml
- name: Create a text file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/own-test.txt
    content: Own test
```
